import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

# while True:
for i in range(5):
    socket.send_string("Sending message %d to julia" % i)
    msg = socket.recv()
    print("Result: ", msg)
    time.sleep(3)
