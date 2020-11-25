using ZMQ

port = "5556"
socket = Socket(PAIR)
println("Subscriber connected to port $port")
bind(socket, "tcp://*:$port")

while true
    message = unsafe_string(ZMQ.recv(socket))
    println("received: " * message)
    sleep(10)
    ZMQ.send(socket, "send result to python")
end

ZMQ.close(socket)
# ZMQ.close(context)