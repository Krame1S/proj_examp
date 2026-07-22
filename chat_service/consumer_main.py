import asyncio
import logging

from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from shared.broker.consumer import RpcConsumer
from shared.broker.queues import ConsumerQueue
from shared.log.setup import setup_logging
from shared.metrics.setup import setup_tracing

from chat_service.broker.consumer_processor import ConsumerProcessor
from chat_service.core.config import settings
from chat_service.core.database import close_db_pool

rpc_consumer = RpcConsumer(amqp_url=settings.RABBIT_AMQP)


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    setup_tracing(service_name="chat_service")
    AsyncPGInstrumentor().instrument()
    logger = logging.getLogger(__name__)
    logger.info("Starting chat_service RPC consumer")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_REQUEST_CREATE.value,
                    callback=ConsumerProcessor.create_request,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_REQUEST_LIST.value,
                    callback=ConsumerProcessor.list_requests,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_REQUEST_ACCEPT.value,
                    callback=ConsumerProcessor.accept_request,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_REQUEST_DECLINE.value,
                    callback=ConsumerProcessor.decline_request,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_REQUEST_CANCEL.value,
                    callback=ConsumerProcessor.cancel_request,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_ROOM_LIST.value,
                    callback=ConsumerProcessor.list_rooms,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_ROOM_GET.value,
                    callback=ConsumerProcessor.get_room,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_MESSAGE_CREATE.value,
                    callback=ConsumerProcessor.create_message,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.CHAT_MESSAGE_LIST.value,
                    callback=ConsumerProcessor.list_messages,
                )
            )
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
