from broker.consumer import UserConsumer
import pika
from os import environ

params = pika.URLParameters(environ.get('RABBITMQ_URI'))
connection = pika.BlockingConnection(params)
channel = connection.channel()

user_queue = UserConsumer(channel)

print(f'Started user_queue: {type(user_queue)}')

channel.start_consuming()
channel.close()