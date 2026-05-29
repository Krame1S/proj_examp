import asyncio
import logging

from shared.log.setup import setup_logging
from tag_service.broker.consumer import rpc_consumer
from shared.broker.queues import ConsumerQueue
from shared.broker.exchanges import ResponseExchange
from tag_service.core.config import settings
from tag_service.core.database import close_db_pool
from tag_service.broker.consumer_processor import ConsumerProcessor


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    logger = logging.getLogger(__name__)
    logger.info("Starting tag_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TAG_CREATE.value,
                callback=ConsumerProcessor.create_tag,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TAG_LIST.value,
                callback=ConsumerProcessor.list_tags,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TAG_GET_BY_ID.value,
                callback=ConsumerProcessor.get_tag_by_id,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TAG_PATCH.value,
                callback=ConsumerProcessor.patch_tag,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TAG_DELETE.value,
                callback=ConsumerProcessor.delete_tag,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())