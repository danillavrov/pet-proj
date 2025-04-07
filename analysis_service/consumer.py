import asyncio

import aio_pika
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import get_async_session, user_stat

# Настройка логирования для лучшей диагностики
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
QUEUE_NAME = "user_events"

async def main():
    connection = None
    try:
        # 1. Подключение к RabbitMQ
        # connect_robust автоматически обрабатывает переподключения
        logging.info(f"Connecting to RabbitMQ at {RABBITMQ_URL}...")
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        logging.info("Successfully connected to RabbitMQ.")

        # 2. Создание канала
        # Использование 'async with' гарантирует закрытие канала
        async with connection.channel() as channel:
            logging.info("Channel created.")

            # 3. Установка QoS (Quality of Service)
            # prefetch_count=1 означает, что консьюмер будет брать только одно
            # сообщение за раз и не получит следующее, пока не обработает текущее.
            await channel.set_qos(prefetch_count=1)
            logging.info("QoS set (prefetch_count=1).")

            # 4. Объявление очереди (idempotent - безопасно вызывать много раз)
            # durable=True - очередь переживет перезапуск брокера
            queue = await channel.declare_queue(
                QUEUE_NAME,
                durable=True
            )
            logging.info(f"Queue '{QUEUE_NAME}' declared.")

            logging.info(" [*] Waiting for messages. To exit press CTRL+C")

            # 5. Начало потребления сообщений из очереди
            # Использование 'async with queue.iterator()' удобно для цикла
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    # 'async with message.process()' автоматически отправляет ack
                    # при успешном выходе из блока или nack при исключении.
                    async with message.process():
                        body = message.body.decode()
                        logging.info(f" [x] Received message: '{body}'")

                        db: AsyncSession = get_async_session()
                        try:
                            query = await db.execute(select(user_stat).where(user_stat.user == body["user"]))
                        except Exception as e:
                            logging.error(e)



                        logging.info(f" [x] Done processing message: '{body}'")

                        # Если нужно прервать цикл по какому-то условию
                        # if body == 'quit':
                        #     logging.info("Received 'quit' message. Stopping consumer...")
                        #     break

    except aio_pika.exceptions.AMQPConnectionError as e:
        logging.error(f"RabbitMQ Connection Error: {e}. Check if RabbitMQ is running and accessible.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True) # Выводим traceback
    finally:
        if connection and not connection.is_closed:
            await connection.close()
            logging.info("RabbitMQ connection closed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Consumer stopped by user (Ctrl+C).")