import asyncio
import logging

from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from shared.broker.consumer import RpcConsumer
from shared.broker.exchanges import ResponseExchange
from shared.broker.queues import ConsumerQueue
from shared.log.setup import setup_logging
from shared.metrics.setup import setup_tracing

from tag_service.broker.consumer_processor import ConsumerProcessor
from tag_service.core.config import settings
from tag_service.core.database import close_db_pool

rpc_consumer = RpcConsumer(amqp_url=settings.RABBIT_AMQP)


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    setup_tracing(service_name="tag_service")
    AsyncPGInstrumentor().instrument()
    logger = logging.getLogger(__name__)
    logger.info("Starting tag_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.TAG_CREATE.value,
                    callback=ConsumerProcessor.create_tag,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.TAG_LIST.value,
                    callback=ConsumerProcessor.list_tags,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.TAG_GET_BY_ID.value,
                    callback=ConsumerProcessor.get_tag_by_id,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.TAG_PATCH.value,
                    callback=ConsumerProcessor.patch_tag,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.TAG_DELETE.value,
                    callback=ConsumerProcessor.delete_tag,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
