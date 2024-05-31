# ZMQ

- [ZeroMQ](https://zeromq.org)
- [Introduction | ØMQ - The Guide](https://zguide.zeromq.org)
- [ZeroMQ | Get started](https://zeromq.org/get-started)

- [ZeroMQ pattern for load balancing work across workers based on idleness - Stack Overflow](https://stackoverflow.com/questions/30824819/zeromq-pattern-for-load-balancing-work-across-workers-based-on-idleness)

# Socket

- [zmq_socket(3) - 0MQ Api](http://api.zeromq.org/2-2:zmq-socket)
- [ZeroMQ | Socket API](https://zeromq.org/socket-api)


0MQ provides the the following transports:
- **tcp** unicast transport using TCP
- **udp** unreliable unicast and multicast using UDP
- **ipc** local inter-process communication transport
  aka AF_UNIX
  [unix(7) - Linux manual page](https://man7.org/linux/man-pages/man7/unix.7.html)
  [zmq_ipc(7) - 0MQ Api](http://api.zeromq.org/4-2:zmq-ipc)
  Windows 10 support Unix sockets (Build 17063)
- **inproc** local in-process (inter-thread) communication transport
  [zmq_inproc(7) - 0MQ Api](http://api.zeromq.org/4-2:zmq-inproc)
- **pgm**, **epgm** reliable multicast transport using PGM
  [Pragmatic General Multicast - Wikipedia](https://en.wikipedia.org/wiki/Pragmatic_General_Multicast)
- **vmci** virtual machine communications interface (VMCI)
  for VMware virtual machines

## Request-reply pattern

The request-reply pattern is used for sending requests from a client to one or more instances of a service, and receiving subsequent replies to each request sent.

These are the legal combinations:
- REQ    -> REP
- REQ    -> ROUTER
- DEALER -> REP
- DEALER -> ROUTER
- DEALER -> DEALER
- ROUTER -> ROUTER

And these combinations are invalid:
- REQ -> REQ
- REQ -> DEALER
- REP -> REP
- REP -> ROUTER

### REQ

A socket of type `ZMQ_REQ` is used by a client to send requests to and receive replies from a service.
This socket type allows only an **alternating sequence** of `zmq_send(request)` and subsequent `zmq_recv(reply)` calls.
Each request sent is **round-robined among all services**, and each reply received is matched with the last issued request.

### REP

A socket of type `ZMQ_REP` is used by a service to receive requests from and send replies to a client.
This socket type allows only an alternating sequence of `zmq_recv(request)` and subsequent `zmq_send(reply)` calls.
Each request received is **fair-queued from among all clients**, and each reply sent is routed to the client that issued the last request.
If the original requester doesn't exist any more the reply is silently discarded.

### DEALER (was XREQ) 

A socket of type `ZMQ_DEALER` is an advanced pattern used for extending request/reply sockets.
Each message sent is **round-robined among all connected peers**, and each message received is **fair-queued from all connected peers**.

### ROUTER (was XREP)

A socket of type `ZMQ_ROUTER` is an advanced pattern used for extending request/reply sockets.
When receiving messages a `ZMQ_ROUTER` socket shall prepend a message part containing the identity of the originating peer to the message before passing it to the application.
Messages received are **fair-queued from among all connected peers**.
When sending messages a `ZMQ_ROUTER` socket shall remove the first part of the message and use it to determine the identity of the peer the message shall be routed to.
If the peer does not exist anymore the message shall be silently discarded.

## Publish-subscribe pattern

The publish-subscribe pattern is used for one-to-many distribution of data from a single publisher to multiple subscribers in a fan out fashion.

## PUB

A socket of type `ZMQ_PUB`` is used by a publisher to distribute data.
Messages sent are distributed in a fan out fashion to all connected peers.
The `zmq_recv` function is not implemented for this socket type.

## SUB

A socket of type `ZMQ_SUB` is used by a subscriber to subscribe to data distributed by a publisher.
Initially a `ZMQ_SUB` socket is not subscribed to any messages, use the `ZMQ_SUBSCRIBE` option of `zmq_setsockopt` to specify which messages to subscribe to.
The `zmq_send` function is not implemented for this socket type.

We can filter the first bytes of a message using `socket.setsockopt(zmq.SUBSCRIBE, b'FIRST BYTES')`

## XPUB

Same as `ZMQ_PUB` except that you can receive subscriptions from the peers in form of incoming messages.
Subscription message is a byte 1 (for subscriptions) or byte 0 (for unsubscriptions) followed by the subscription body.
Messages without a sub/unsub prefix are also received, but have no effect on subscription status.

## XSUB

Same as `ZMQ_SUB` except that you subscribe by sending subscription messages to the socket.
Subscription message is a byte 1 (for subscriptions) or byte 0 (for unsubscriptions) followed by the subscription body.
Messages without a sub/unsub prefix may also be sent, but have no effect on subscription status.

## Pipeline pattern

The pipeline pattern is used for distributing data to nodes arranged in a pipeline.
Data always flows down the pipeline, and each stage of the pipeline is connected to at least one node.
When a pipeline stage is connected to multiple nodes data is round-robined among all connected nodes.

### PUSH

A socket of type `ZMQ_PUSH` is used by a pipeline node to send messages to downstream pipeline nodes.
Messages are **round-robined to all connected downstream nodes**.
The `zmq_recv()` function is not implemented for this socket type.

### PULL

A socket of type `ZMQ_PULL` is used by a pipeline node to receive messages from upstream pipeline nodes.
Messages are **fair-queued from among all connected upstream nodes**.
The `zmq_send()` function is not implemented for this socket type.

## Exclusive pair pattern

The exclusive pair pattern is used to connect a peer to precisely one other peer.
This pattern is used for inter-thread communication across the inproc transport.

### PAIR

A socket of type `ZMQ_PAIR` can only be connected to a single peer at any one time.
No message routing or filtering is performed on messages sent over a `ZMQ_PAIR` socket.

## Native Pattern

The native pattern is used for communicating with TCP peers and allows asynchronous requests and replies in either direction.

### STREAM

A socket of type `ZMQ_STREAM` is used to send and receive TCP data from a non-0MQ peer, when using the `tcp://` transport.
A `ZMQ_STREAM` socket can act as client and/or server, sending and/or receiving TCP data asynchronously.

# Device

[Devices in PyZMQ — PyZMQ documentation](https://pyzmq.readthedocs.io/en/latest/howto/devices.html)

[zmq_device(3) - 0MQ Api](http://api.zeromq.org/2-2:zmq-device)
Deprecated since version libzmq-3.2: Use zmq.proxy

The device connects a frontend socket to a backend socket. Conceptually, data flows from frontend to backend.
Depending on the socket types, replies may flow in the opposite direction.

**Queue device**
ZMQ_QUEUE creates a shared queue that collects requests from a set of clients, and distributes these fairly among a set of services.
Requests are fair-queued from frontend connections and load-balanced between backend connections.
Replies automatically return to the client that made the original request.

This device is part of the request-reply pattern.
The frontend speaks to clients and the backend speaks to services.
You should use ZMQ_QUEUE with a ZMQ_XREP socket for the frontend and a ZMQ_XREQ socket for the backend. 

**Forwarder device**
ZMQ_FORWARDER collects messages from a set of publishers and forwards these to a set of subscribers.
You will generally use this to bridge networks, e.g. read on TCP unicast and forward on multicast.

This device is part of the publish-subscribe pattern.
The frontend speaks to publishers and the backend speaks to subscribers.
You should use ZMQ_FORWARDER with a ZMQ_SUB socket for the frontend and a ZMQ_PUB socket for the backend.
Other combinations are not documented.

**Streamer device**
ZMQ_STREAMER collects tasks from a set of pushers and forwards these to a set of pullers.
You will generally use this to bridge networks.
Messages are fair-queued from pushers and load-balanced to pullers.

This device is part of the pipeline pattern.
The frontend speaks to pushers and the backend speaks to pullers.
You should use ZMQ_STREAMER with a ZMQ_PULL socket for the frontend and a ZMQ_PUSH socket for the backend.
Other combinations are not documented.

# Patterns

## Load Balancing Pattern

- [3. Advanced Request-Reply Patterns | ØMQ - The Guide](https://zguide.zeromq.org/docs/chapter3/#The-Load-Balancing-Pattern)

The broker has to know when the worker is ready, and keep a list of workers so that it can take the least recently used worker each time.
Workers send a “ready” message when they start, and after they finish each task.
The broker reads these messages one-by-one.
Each time it reads a message, it is from the last used worker.
And because we’re using a ROUTER socket, we get an identity that we can then use to send a task back to the worker.

Examples for 4 workers:
-       [w1, w2, w3, w4]
- <- w1
- <- w2
- <- w3
- <- w4
- -> w2 
- -> w4
- -> w1
- -> w3 [w2, w4, w1, w3]

- ROUTER Broker and REQ Workers
- ROUTER Broker and DEALER Workers
  There are two specific differences:
  - The REQ socket always sends an empty delimiter frame before any data frames; the DEALER does not.
  - The REQ socket will send only one message before it receives a reply; the DEALER is fully asynchronous.

# Examples

- [Connection Diagrams of The IPython ZMQ Cluster — IPython 2.4.2 documentation](https://ipython.org/ipython-doc/2/development/parallel_connections.html)
- [Connection Diagrams of The IPython ZMQ Cluster — IPython 1.2.1: An Afternoon Hack documentation](https://ipython.readthedocs.io/en/1.x/development/parallel_connections.html)

See `site-packages/ipykernel/heartbeat.py`
