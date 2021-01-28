#!/usr/bin/env python
import pika
from time import sleep


def main():
    # Establish a connection to the RabbitMQ Server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Check that the recipent queue exists before sending a message
    # If it does not exists the message will be dropped
    channel.queue_declare(queue='hello')

    # Now we want to send a message to the 'hello' queue
    # In RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    message_sent = 'Hello World!'
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message_sent)
    print(" [x] Sent '%s'" % message_sent)

    connection.close()


if __name__ == '__main__':
    NUM_WORKS = 3
    for i in range(NUM_WORKS):
        main()
        sleep(1)
