
using HTTP, JSON

# Server
@async HTTP.WebSockets.listen("127.0.0.1", UInt16(8081)) do ws
    println("Conexion stablished")
    while !eof(ws)
        recieved_message = readavailable(ws)
        println("received message")
        println(recieved_message)
        isempty(recieved_message) ? break : nothing
        data = JSON.parse(String(recieved_message))
        println(data)
        say = rand() < 0.1 ? "bye" : "hello"
        send_message = Dict(:x => rand(), :y => say)
        jmessage = JSON.json(send_message)
        write(ws, jmessage)
    end
end

# Client
HTTP.WebSockets.open("ws://127.0.0.1:8081") do ws
    running = true
    while running
        send_message = Dict(:x => 0.34, :y => "hello")
        data = JSON.json(send_message)
        write(ws, data)
        recieved_message = readavailable(ws)
        message = JSON.parse(String(recieved_message))
        println(message)
        running = message["y"] == "bye" ? false : true
    end
    println("Exiting...")
    println()
end
