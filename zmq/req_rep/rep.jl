using ZMQ

s1=Socket(REP)

bind(s1, "tcp://*:5555")

msg = recv(s1, String)
send(s1, "test response")
close(s1)
