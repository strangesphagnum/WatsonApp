import aio_pika

from settings import settings


class AMQPQueueConstructor:
    amqp_connection: aio_pika.Connection
    amqp_queue: aio_pika.Queue
    amqp_channel: aio_pika.Channel
    routing_queue: str

    def __init__(self, routing_queue: str):
        self.routing_queue = routing_queue

    async def publish_message(self, message: str):
        self.amqp_connection = await aio_pika.connect_robust(settings.rabbit_dsn)
        async with self.amqp_connection:
            self.amqp_channel = await self.amqp_connection.channel()
            await self.amqp_channel.declare_queue(self.routing_queue)
            await self.amqp_channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=self.routing_queue,
            )


chat_document_amqp = AMQPQueueConstructor(settings.AMQP_TELEGRAM_QUEUE_NAME)
