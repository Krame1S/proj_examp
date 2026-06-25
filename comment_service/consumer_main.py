import asyncio
import logging

from shared.log.setup import setup_logging
from comment_service.broker.consumer import rpc_consumer
from shared.broker.queues import ConsumerQueue
from shared.broker.exchanges import ResponseExchange
from comment_service.core.config import settings
from comment_service.core.database import close_db_pool
from comment_service.broker.consumer_processor import ConsumerProcessor
from shared.metrics.setup import setup_tracing
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    setup_tracing(service_name="comment_service")
    AsyncPGInstrumentor().instrument()
    logger = logging.getLogger(__name__)
    logger.info("Starting comment_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.COMMENT_CREATE.value,
                callback=ConsumerProcessor.create_comment,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.COMMENT_LIST.value,
                callback=ConsumerProcessor.list_comments,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.COMMENT_DELETE.value,
                callback=ConsumerProcessor.delete_comment,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())