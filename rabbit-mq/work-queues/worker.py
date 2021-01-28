#!/usr/bin/env python
import pika
import time
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # durable = True sets message durability
    # auto_ack=False, this will ensure message acknoledgement is setup -> no messages missed when worker is shutdown
    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        task_time = body.count(b'.')
        time.sleep(task_time)
        print(" [x] Done %d seconds" % task_time)
        # It's time to remove the auto_ack flag and send a proper acknowledgment from the worker, once we're done with a task.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # fair queue prefetch_count = 1
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
