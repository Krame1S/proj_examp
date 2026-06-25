import asyncio
import logging

from shared.log.setup import setup_logging
from shared.metrics.setup import setup_tracing
from task_service.broker.consumer import rpc_consumer
from shared.broker.queues import ConsumerQueue
from shared.broker.exchanges import ResponseExchange
from task_service.core.config import settings
from task_service.core.database import close_db_pool, close_redis_client
from task_service.broker.consumer_processor import ConsumerProcessor
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    setup_tracing(service_name="task_service")
    AsyncPGInstrumentor().instrument()
    logger = logging.getLogger(__name__)
    logger.info("Starting task_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TASK_CREATE.value,
                callback=ConsumerProcessor.create_task,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TASK_LIST.value,
                callback=ConsumerProcessor.list_tasks,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TASK_GET_BY_ID.value,
                callback=ConsumerProcessor.get_task_by_id,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TASK_PATCH.value,
                callback=ConsumerProcessor.patch_task,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
            tg.create_task(rpc_consumer.start_consuming(
                queue_name=ConsumerQueue.TASK_DELETE.value,
                callback=ConsumerProcessor.delete_task,
                response_exchange_name=ResponseExchange.DEFAULT,
            ))
    finally:
        await close_db_pool()
        await close_redis_client()


if __name__ == "__main__":
    asyncio.run(main())