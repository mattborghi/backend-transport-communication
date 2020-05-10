using HTTP, JSON
# Server
# Working with client py! and Julia! and Node!!!
@async HTTP.WebSockets.listen("127.0.0.1", UInt16(8080)) do ws
    while !eof(ws)
        # println("client listening")
        data = readavailable(ws)
        if !isempty(data)
            println("server received ", String(data))
            write(ws, "Hello from Julia server!")
        end
    end
end

# Client
HTTP.WebSockets.open("ws://127.0.0.1:8080") do ws
    #  println("client sending info")
    write(ws, "Hello!")
    # write(ws, "ANother thing!")
    # write(ws, JSON.json(Dict("a" => 1)))
    # x = readavailable(ws)
    # @show x
    # println(String(x))
end;

