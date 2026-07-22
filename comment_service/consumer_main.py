import asyncio
import logging

from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from shared.broker.consumer import RpcConsumer
from shared.broker.exchanges import ResponseExchange
from shared.broker.queues import ConsumerQueue
from shared.log.setup import setup_logging
from shared.metrics.setup import setup_tracing

from comment_service.broker.consumer_processor import ConsumerProcessor
from comment_service.core.config import settings
from comment_service.core.database import close_db_pool

rpc_consumer = RpcConsumer(amqp_url=settings.RABBIT_AMQP)


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    setup_tracing(service_name="comment_service")
    AsyncPGInstrumentor().instrument()
    logger = logging.getLogger(__name__)
    logger.info("Starting comment_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.COMMENT_CREATE.value,
                    callback=ConsumerProcessor.create_comment,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.COMMENT_LIST.value,
                    callback=ConsumerProcessor.list_comments,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.COMMENT_DELETE.value,
                    callback=ConsumerProcessor.delete_comment,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
