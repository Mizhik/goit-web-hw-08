import pika

from faker import Faker
from models import User

fake = Faker()

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672)
    )
channel = connection.channel()

channel.exchange_declare(exchange="Goit Homework", exchange_type="direct")
channel.queue_declare(queue="Homework queue", durable=True)
channel.queue_bind(exchange="Goit Homework", queue="Homework queue")


def create_task(nums):
    for _ in range(nums):
        contact = User(
            fullname=fake.name(),
            email=fake.email(),
        ).save()
        channel.basic_publish(
            exchange="Goit Homework",
            routing_key="Homework queue",
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()

if __name__ == "__main__":
    create_task(10)
