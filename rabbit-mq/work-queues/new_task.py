#!/usr/bin/env python
import pika
import sys


def main(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    # message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    from random import randrange
    NUM_TASKS = 5
    MAX_NUMBER_SECONDS = 10
    for i in range(NUM_TASKS):
        TASKS_TIME = randrange(1, MAX_NUMBER_SECONDS)
        message = ''.join(['.' for i in range(TASKS_TIME)])
        main(message)
