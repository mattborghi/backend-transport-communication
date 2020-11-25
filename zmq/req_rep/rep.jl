using ZMQ

s1 = Socket(REP)
println("Running server…")
bind(s1, "tcp://*:5555")
while true
    msg = recv(s1, String)
    send(s1, "test response") 
end
close(s1)
