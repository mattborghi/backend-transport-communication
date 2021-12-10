import zmq
import time
import os

port = "5556"
host = "*"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://%s:%s" % (host, port))
# socket.bind(os.environ['CLIENT_CONNECT_URI'])
print("client connected to tcp://%s:%s" % (host, port))

# while True:
for i in range(5):
    socket.send_string("Sending message %d to julia" % i)
    msg = socket.recv()
    print("Result: ", msg)
    time.sleep(3)
