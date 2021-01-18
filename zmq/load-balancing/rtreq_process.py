# encoding: utf-8
#
#   Custom routing Router to Mama (ROUTER to REQ)
#

import time
import random
from multiprocessing import Process

import zmq
from random import randint

NBR_WORKERS = 10


def set_id(zsocket):
    """Set simple random printable identity on socket"""
    identity = u"%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))
    zsocket.setsockopt_string(zmq.IDENTITY, identity)


def worker_thread(context=None):
    context = context or zmq.Context.instance()
    worker = context.socket(zmq.REQ)

    # We use a string identity for ease here
    set_id(worker)
    worker.connect("tcp://localhost:5671")

    total = 0
    while True:
        # Tell the router we're ready for work
        worker.send(b"ready")

        # Get workload from router, until finished
        workload = worker.recv()
        finished = workload == b"END"
        if finished:
            print("Processed: %d tasks" % total)
            break
        total += 1

        # Do some random work
        time.sleep(0.1 * random.random())


context = zmq.Context.instance()
client = context.socket(zmq.ROUTER)
client.bind("tcp://*:5671")

for _ in range(NBR_WORKERS):
    Process(target=worker_thread).start()

for _ in range(NBR_WORKERS * 100):
    # LRU worker is next waiting in the queue
    address, empty, ready = client.recv_multipart()

    client.send_multipart([
        address,
        b'',
        b'This is the workload',
    ])

# Now ask mama to shut down and report their results
for _ in range(NBR_WORKERS):
    address, empty, ready = client.recv_multipart()
    client.send_multipart([
        address,
        b'',
        b'END',
    ])
