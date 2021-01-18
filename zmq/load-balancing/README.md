# Load Balancing pattern

The load balancing pattern solves the main problem with simple round robin routing (as PUSH and DEALER offer) which is that round robin becomes inefficient if tasks do not all roughly take the same time.

Consider the scenario of a worker (DEALER or REQ) connected to a broker (ROUTER): the broker has to know when the worker is ready, and keep a list of workers so that it can take the least recently used worker each time.

The solution is really simple, in fact: workers send a “ready” message when they start, and after they finish each task. The broker reads these messages one-by-one. Each time it reads a message, it is from the last used worker. And because we’re using a ROUTER socket, we get an identity that we can then use to send a task back to the worker.

It’s a twist on request-reply because the task is sent with the reply, and any response for the task is sent as a new request.

## ROUTER Broker to REQ Workers

There is implemented a multithreaded and multiprocessing versions.

## ROUTER Broker to DEALER Workers

Anywhere you can use REQ, you can use DEALER. There are two specific differences:

- The REQ socket always sends an empty delimiter frame before any data frames; the DEALER does not.
- The REQ socket will send only one message before it receives a reply; the DEALER is fully asynchronous.

The synchronous versus asynchronous behavior has no effect on our example because we’re doing strict request-reply. It is more relevant when we address recovering from failures.

## Load balancing message broker

The previous example is half-complete. It can manage a set of workers with dummy requests and replies, but it has no way to talk to clients. If we add a second frontend ROUTER socket that accepts client requests, and turn our example into a proxy that can switch messages from frontend to backend, we get a useful and reusable tiny load balancing message broker.

![imag](https://zguide.zeromq.org/images/fig32.png)

### Message envelope

Let’s assume the client’s identity is “CLIENT” and the worker’s identity is “WORKER”. The client application sends a single frame containing “Hello”.

![imag](https://zguide.zeromq.org/images/fig33.png)

**Figure 1**: Message that Client sends.

Because the REQ socket adds its empty delimiter frame and the ROUTER socket adds its connection identity, the proxy reads off the frontend ROUTER socket the client address, empty delimiter frame, and the data part.

![imag](https://zguide.zeromq.org/images/fig34.png)

**Figure 2**: Message coming in on Frontend.

The broker sends this to the worker, prefixed by the address of the chosen worker, plus an additional empty part to keep the REQ at the other end happy.

![imag](https://zguide.zeromq.org/images/fig35.png)

**Figure 3**: Message sent to Backend.

This complex envelope stack gets chewed up first by the backend ROUTER socket, which removes the first frame. Then the REQ socket in the worker removes the empty part, and provides the rest to the worker application.

![imag](https://zguide.zeromq.org/images/fig36.png)

**Figure 4**: Message delivered to Worker.

The worker has to save the envelope (which is all the parts up to and including the empty message frame) and then it can do what’s needed with the data part. Note that a REP socket would do this automatically, but we’re using the REQ-ROUTER pattern so that we can get proper load balancing.

On the return path, the messages are the same as when they come in, i.e., the backend socket gives the broker a message in five parts, and the broker sends the frontend socket a message in three parts, and the client gets a message in one part.
