# Simple example of pub/client using python
# in order to connect to julia
import zmq
import time

port = 3000
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = "kitty cats"
    messagedata = "Hello cats from Python!"
    socket.send_string("%s %s" % (topic, messagedata))
    time.sleep(3)
    topic = "doggy dogs"
    messagedata = "Hello dogs from Python!"
    socket.send_string("%s %s" % (topic, messagedata))
    time.sleep(3)
