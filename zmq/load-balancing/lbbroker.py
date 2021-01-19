# Load-balancing broker
#
# Clients and workers are shown here in-process.
#

# from __future__ import print_function

from multiprocessing import Process

import zmq


NBR_CLIENTS = 10
NBR_WORKERS = 3


def client_task(ident):
    """Basic request-reply client using REQ socket."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Client-{}".format(ident).encode("ascii")
    socket.connect("ipc://frontend.ipc")

    # Send request, get reply
    socket.send(b"HELLO")  # Figure 1: one-part messages
    reply = socket.recv()
    print("{}: {}".format(socket.identity.decode("ascii"),
                          reply.decode("ascii")))


def worker_task(ident):
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Worker-{}".format(ident).encode("ascii")
    socket.connect("ipc://backend.ipc")

    # Tell broker we're ready for work
    socket.send(b"READY")

    while True:
        address, _, request = socket.recv_multipart()  # Figure 4: three-parts messages
        print("{}: {}".format(socket.identity.decode("ascii"),
                              request.decode("ascii")))
        socket.send_multipart([address, b"", b"OK"])


def main():
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("ipc://frontend.ipc")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")

    # Start background tasks
    def start(task, *args):
        process = Process(target=task, args=args)
        process.daemon = True
        process.start()
    for i in range(NBR_CLIENTS):
        start(client_task, i)
    for i in range(NBR_WORKERS):
        start(worker_task, i)

    # Initialize main loop state
    count = NBR_CLIENTS
    workers = []
    poller = zmq.Poller()
    # Only poll for requests from backend until workers are available
    poller.register(backend, zmq.POLLIN)

    while True:
        # If there are currently events ready to be processed,
        # this function will return immediately.
        # Returns dict of the form socket : event_mask
        # where in this case socket is frontend or backend
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()  # Figure 3: Five-part messages
            worker, _, client = request[:3]  # first 3 elems
            if not workers:
                # Poll for clients now that a worker is available
                print("no workers available backends")
                poller.register(frontend, zmq.POLLIN)
            workers.append(worker)
            if client != b"READY" and len(request) > 3:
                # If client reply, send rest back to frontend
                _, reply = request[3:]
                frontend.send_multipart([client, b"", reply])
                count -= 1
                if not count:  # enters when count = 0
                    break

        if frontend in sockets:
            # Get next client request, route to last-used worker
            client, _, request = frontend.recv_multipart()  # Figure 2
            worker = workers.pop(0)
            backend.send_multipart(
                [worker, b"", client, b"", request])  # Figure 3
            if not workers:
                # Don't poll clients if no workers are available
                print("no workers available frontend")
                poller.unregister(frontend)

    # Clean up
    backend.close()
    frontend.close()
    context.term()


if __name__ == "__main__":
    main()
