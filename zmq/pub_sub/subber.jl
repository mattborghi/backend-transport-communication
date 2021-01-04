using ZMQ

context = Context()
socket = Socket(context, SUB)
ZMQ.connect(socket, "tcp://127.0.0.1:3000")
ZMQ.subscribe(socket, "kitty cats")
# if we don't use a 2nd argument we receive all messages
# ZMQ.subscribe(socket) 
println("Subscriber connected to port 3000")

while true
    message = unsafe_string(ZMQ.recv(socket))
    println("received: " * message)
end

ZMQ.close(socket)
ZMQ.close(context)
