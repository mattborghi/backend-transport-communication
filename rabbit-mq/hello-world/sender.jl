using AMQPClient


function main()
    # Establish connection to RabbitMQ Server
    port = AMQPClient.AMQP_DEFAULT_PORT
    login = "guest"  # default is usually "guest"
    password = "guest"  # default is usually "guest"
    auth_params = Dict{String,Any}("MECHANISM"=>"AMQPLAIN", "LOGIN"=>login, "PASSWORD"=>password)

    conn = connection(; virtualhost="/", host="localhost", port=port, auth_params=auth_params, amqps=nothing)

    chan = channel(conn, AMQPClient.UNUSED_CHANNEL, true)

    success, message_count, consumer_count = queue_declare(chan, "hello")
    
    EXCG_DIRECT = ""
    message = "Hello World!"
    M = Message(Vector{UInt8}(message), content_type="text/plain") # , delivery_mode=PERSISTENT
    basic_publish(chan, M; exchange=EXCG_DIRECT, routing_key="hello")
    
    println(" [x] Sent '$message'")

    if isopen(conn)
        close(conn)
        # close is an asynchronous operation. To wait for the negotiation to complete:
        AMQPClient.wait_for_state(conn, AMQPClient.CONN_STATE_CLOSED)
    end
end

main()