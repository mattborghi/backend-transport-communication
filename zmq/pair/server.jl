using ZMQ

port = "5556"
socket = Socket(PAIR)
connect(socket, "tcp://0.0.0.0:$port")
println("Subscriber connected to port $port")

while true
    message = unsafe_string(ZMQ.recv(socket))
    println("received: " * message)
    sleep(5)
    ZMQ.send(socket, "send result to python")
end

ZMQ.close(socket)
# ZMQ.close(context)