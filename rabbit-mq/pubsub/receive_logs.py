#!/usr/bin/env python
import pika
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    # Each consumer declares its own queue to listen to.
    # exclusive = True makes it two close the queue when the consumer closes.
    result = channel.queue_declare(queue='', exclusive=True)
    # In this case a random name is assigned.
    queue_name = result.method.queue
    # Connect the queue to the exchange
    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

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
