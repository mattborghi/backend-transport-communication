using AMQPClient

Base.exit_on_sigint(false)

abstract type AbstractConnection end

struct Connection <: AbstractConnection
    port 
    login
    password
    conn
    chan
end

function connect()
    # Establish the connection to the RabbitMQ Server
    port = AMQPClient.AMQP_DEFAULT_PORT
    login = "guest"  # default is usually "guest"
    password = "guest"  # default is usually "guest"
    auth_params = Dict{String,Any}("MECHANISM" => "AMQPLAIN", "LOGIN" => login, "PASSWORD" => password)

    conn = connection(; virtualhost="/", host="localhost", port=port, auth_params=auth_params, amqps=nothing)

    chan = channel(conn, AMQPClient.UNUSED_CHANNEL, true)
    
    return Connection(port, login, password, conn, chan)
end


function main(connection::AbstractConnection)
    chan = connection.chan

    success, message_count, consumer_count = queue_declare(chan, "hello") # durable=True
    
    println(" [*] Waiting for messages. To exit press CTRL+C")

    callback = rcvd_msg -> begin
        msg_str = String(rcvd_msg.data)
        println(" [x] Received '$msg_str'")
        # It's time to remove the auto_ack flag and 
        # send a proper acknowledgment from the worker, 
        # once we're done with a task.
        # basic_ack(chan, rcvd_msg.delivery_tag)
    end
    
    success, consumer_tag = basic_consume(chan, "hello", callback)
    
    @assert success
    # println("consumer registered with tag $consumer_tag")

    # go ahead with other stuff...
    # or wait for an indicator for shutdown

    while true
        sleep(1)
    end
end


try
    connection = connect()
    main(connection)
catch e
    if e isa InterruptException
        println("Exited")
        # unsubscribe the consumer from the queue
        # basic_cancel(connection, consumer_tag)
    else
        print("There was an error")
        print(e)
    end
    exit()
end

