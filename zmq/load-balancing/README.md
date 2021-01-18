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

