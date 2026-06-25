import asyncio
import logging

from attachment_service.broker.consumer import rpc_consumer
from attachment_service.broker.consumer_processor import ConsumerProcessor
from attachment_service.core.config import settings
from attachment_service.core.database import close_db_pool
from shared.broker.exchanges import ResponseExchange
from shared.broker.queues import ConsumerQueue
from shared.log.setup import setup_logging
from shared.metrics.setup import setup_tracing
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    setup_tracing(service_name="attachment_service")
    AsyncPGInstrumentor().instrument()
    logger = logging.getLogger(__name__)
    logger.info("Starting attachment_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.ATTACHMENT_CREATE.value,
                    callback=ConsumerProcessor.create_attachment,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.ATTACHMENT_LIST.value,
                    callback=ConsumerProcessor.list_attachments,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.ATTACHMENT_DELETE.value,
                    callback=ConsumerProcessor.delete_attachment,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())