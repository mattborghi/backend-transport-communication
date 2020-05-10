using Sockets
using JSON

pipe = ""

if Sys.iswindows()
    pipe = "\\\\.\\pipe\\testsocket"
else
    pipe = tempname()
end

@async begin
    server = listen(pipe)
    while true
        sock = accept(server)
        @async while isopen(sock)
            # println(sock)
            input = JSON.parse(sock)
            # write(sock, readline(sock, keep = true))
            # JSON.print(sock, Dict("data" => input["y"]))
            JSON.print(sock, Dict("data" => rand(input["input"])))
        end
    end
end


clientside = connect(pipe)
#
for i in 1:10
    JSON.print(clientside, Dict("input" => i))
    println(JSON.parse(clientside))
end




using Sockets
@async begin
    server = listen(2003)
    while true
        sock = accept(server)
        println("Hello World\n")
    end
end

# listen(ip"127.0.0.1",2002)




# server written in Julia
using Sockets
server = listen(ip"127.0.0.1", 2000)
sock = accept(server)
while true
    write(sock, "echo: " * readline(sock) * "\n")
end

# client written in Julia
# Works with client.py
using Sockets
clientside=connect(2000)
println(clientside,"abc")
println(readline(clientside))
