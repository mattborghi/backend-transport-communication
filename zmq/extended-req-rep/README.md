# Extended REQ-REP

Given that this setup is not that good for scaling

![setup](https://zguide.zeromq.org/images/fig15.png)

We’ll write a little message queuing broker that gives us this flexibility. The broker binds to two endpoints, a frontend for clients and a backend for services.

> When you use REQ to talk to REP, you get a strictly synchronous request-reply dialog. The client sends a request. The service reads the request and sends a reply. The client then reads the reply. If either the client or the service try to do anything else (e.g., sending two requests in a row without waiting for a response), they will get an error.

There are two sockets called DEALER and ROUTER that let you do nonblocking request-response.

![imag](https://zguide.zeromq.org/images/fig16.png)