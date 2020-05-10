using ZMQ

context = Context()
socket = Socket(context, SUB)
ZMQ.connect(socket, "tcp://127.0.0.1:3000")
ZMQ.subscribe(socket, "kitty cats")
println("Subscriber connected to port 3000")

while true
    message = unsafe_string(ZMQ.recv(socket))
    println("received: " * message)
end

ZMQ.close(socket)
ZMQ.close(context)
