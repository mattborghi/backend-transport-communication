#!/usr/bin/env python
import pika
import sys
from time import sleep


def main(routing_key, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare a topic exchange
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    # read the routing key and the message
    # routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    # message = ' '.join(sys.argv[2:]) or 'Hello World!'
    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()


if __name__ == '__main__':
    # Routing keys are of the form <facility.severity>
    # To emit a log with a routing key "kern.critical" type:
    # python emit_log_topic.py "kern.critical" "A critical kernel error"
    main("kern.critical", "A critical kernel error")
    sleep(3)
    main("anonymous.info", "Hello World!")
