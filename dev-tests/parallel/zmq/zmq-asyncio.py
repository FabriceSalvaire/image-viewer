import asyncio
import zmq
import zmq.asyncio
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

async def send_request(socket, request):
    print(f"Sending request {request}...")
    await socket.send_string("Hello")
    message = await socket.recv()
    print(f"Received reply {request} [{message}]")
    await asyncio.sleep(1)

async def async_client(socket):
    async with asyncio.TaskGroup() as tg:
        for request in range(20):
            tg.create_task(send_request(socket, request))

def client(ports=['5556']):
    context = zmq.asyncio.Context.instance()
    print(f"Connecting to server with ports {ports}")
    socket = context.socket(zmq.REQ)
    for port in ports:
        socket.connect(f"tcp://localhost:{port}")
    asyncio.run(async_client(socket))

####################################################################################################

if __name__ == '__main__':
    # Now we can run a few servers
    server_ports = range(5550, 5558, 2)
    for server_port in server_ports:
        Process(target=server, args=(server_port,)).start()
    # Now we can connect a client to all these servers
    client(server_ports)
