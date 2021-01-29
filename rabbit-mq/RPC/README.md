# Remote procedure call (RPC)

Previously, we used Work Queues to distribute time-consuming tasks among multiple workers.

But what if we need to run a function on a remote computer and wait for the result? Well, that's a different story. This pattern is commonly known as `Remote Procedure Call` or `RPC`.

![rpc](https://www.rabbitmq.com/img/tutorials/python-six.png)

Our RPC will work like this:

- When the Client starts up, it creates an anonymous exclusive callback queue.
For an RPC request, the Client sends a message with two properties: `reply_to`, which is set to the callback queue and `correlation_id`, which is set to a unique value for every request.

- The request is sent to an `rpc_queue` queue.

- The RPC worker (aka: server) is waiting for requests on that queue. When a request appears, it does the job and sends a message with the result back to the Client, using the queue from the `reply_to` field.

- The client waits for data on the callback queue. When a message appears, it checks the `correlation_id` property. If it matches the value from the request it returns the response to the application.


If the RPC server is too slow, you can scale up by just running another one. Try running a second `rpc_server.py` in a new console.

On the client side, the RPC requires sending and receiving only one message. No synchronous calls like `queue_declare` are required. As a result the RPC client needs only one network round trip for a single RPC request.

Our code is still pretty simplistic and doesn't try to solve more complex (but important) problems, like:

- How should the client react if there are no servers running?
- Should a client have some kind of timeout for the RPC?
- If the server malfunctions and raises an exception, should it be forwarded to the client?
- Protecting against invalid incoming messages (eg checking bounds) before processing.