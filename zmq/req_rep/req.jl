using ZMQ

s2=Socket(REQ)

connect(s2, "tcp://127.0.0.1:5555")

send(s2, "test request")
close(s2)
