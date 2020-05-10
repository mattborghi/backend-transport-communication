using ZMQ

context = Context()
socket = Socket(context, PUB)
ZMQ.bind(socket, "tcp://*:3000")

# using Printf
while true
    ZMQ.send(socket, "kitty cats", more = true)
    ZMQ.send(socket, "Hello cats from Julia!")
    # zipcode = Printf.@sprintf("%05d",rand(1:99999))
    # temperature = rand(-80:135)
    # relhumidity = rand(10:60)
    # ZMQ.send(socket, "$zipcode $temperature") # $relhumidity
    # yield()
    ZMQ.send(socket, "puppy dogs", more = true)
    ZMQ.send(socket, "Hello dogs from Julia!")
    sleep(2)
end


ZMQ.close(socket)
ZMQ.close(context)
