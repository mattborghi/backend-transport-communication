# encoding: utf-8
#
#   Custom routing Router to Dealer
#

import time
import random
import string
from random import randint
from multiprocessing import Process, Pool

import zmq
import numpy as np

NBR_WORKERS = 5

# We have two workers, here we copy the code, normally these would
# run on different boxes...
#


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def worker_bytes(name):
    if isinstance(name, bytes):
        return name
    return name.encode()


def worker_thread(name, context=None):
    print("Init worker -> %s" % name)
    context = context or zmq.Context.instance()
    worker = context.socket(zmq.DEALER)
    worker.setsockopt(zmq.IDENTITY, worker_bytes(name))
    worker.connect("ipc://routing.ipc")

    total = 0
    while True:
        # We receive one part, with the workload
        request = worker.recv()
        finished = request == b"END"
        if finished:
            print("%s received: %s messages" % (name, total))
            break
        total += 1


context = zmq.Context.instance()
client = context.socket(zmq.ROUTER)
client.bind("ipc://routing.ipc")

# We can set worker names as bytes type of string
# WORKER_NAMES = [np.random.bytes(12) for _ in range(NBR_WORKERS)]
WORKER_NAMES = [get_random_string(4) for _ in range(NBR_WORKERS)]

# with Pool(5) as p:
#     p.map(worker_thread, WORKER_NAMES)
for worker_name in WORKER_NAMES:
    Process(target=worker_thread, args=(worker_name,)).start()

# Wait for threads to stabilize
time.sleep(1)

# Send 10 tasks scattered to A twice as often as B
for _ in range(100):
    # Send two message parts, first the address...
    ident = random.choice(WORKER_NAMES)
    # And then the workload
    work = b"This is the workload"
    client.send_multipart([worker_bytes(ident), work])

for worker in WORKER_NAMES:
    client.send_multipart([worker_bytes(worker), b'END'])
