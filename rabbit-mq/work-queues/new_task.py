#!/usr/bin/env python
import pika
import sys
import json



def main(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
            # content_type='application/json',
        ))
    print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    from random import randrange
    NUM_TASKS = 10
    # MAX_NUMBER_SECONDS = 10
    for i in range(1,NUM_TASKS):
        # TASKS_TIME = randrange(1, MAX_NUMBER_SECONDS)
        TASKS_TIME = i
        message = ''.join(['.' for i in range(1, TASKS_TIME)])
        message = json.dumps({'payload': message})
        main(message)
