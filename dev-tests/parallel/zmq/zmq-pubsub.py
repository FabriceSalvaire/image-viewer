####################################################################################################

# Request-reply, which connects a set of clients to a set of
# services. This is a remote procedure call and task distribution
# pattern.

# Running server on port: 5550
# Running server on port: 5554
# Running server on port: 5552
# Running server on port: 5556
# Connecting to server with ports range(5550, 5558, 2)
#
# Sending request 0...
# Received request #0: b'Hello'
# Received reply 0 [b'World from 5550']
# Sending request 1...
# Received request #0: b'Hello'
# Received reply 1 [b'World from 5552']
# Sending request 2...
# Received request #0: b'Hello'
# Received reply 2 [b'World from 5554']
# Sending request 3...
# Received request #0: b'Hello'
# Received reply 3 [b'World from 5556']

####################################################################################################

import zmq
import time
from multiprocessing import Process

####################################################################################################

def server(port='5556'):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{port}')
    print(f"Running server on port: {port}")
    # serves only 5 request and dies
    for request_number in range(5):
        # Wait for next request from client
        message = socket.recv()
        print(f"Received request #{request_number}: {message}")
        socket.send_string(f"World from {port}")

####################################################################################################

def client(ports=['5556']):
    context = zmq.Context()
    print(f"Connecting to server with ports {ports}")
    socket = context.socket(zmq.REQ)
    for port in ports:
        socket.connect(f"tcp://localhost:{port}")
    for request in range(20):
        print(f"Sending request {request}...")
        socket.send_string("Hello")
        message = socket.recv()
        print(f"Received reply {request} [{message}]")
        time.sleep(1)

####################################################################################################

if __name__ == '__main__':
    # Now we can run a few servers
    server_ports = range(5550, 5558, 2)
    for server_port in server_ports:
        Process(target=server, args=(server_port,)).start()
    # Now we can connect a client to all these servers
    Process(target=client, args=(server_ports,)).start()
