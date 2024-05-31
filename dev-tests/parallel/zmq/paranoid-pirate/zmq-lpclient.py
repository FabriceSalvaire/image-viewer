####################################################################################################
#
#  Lazy Pirate client
#  Use zmq_poll to do a safe request-reply
#  To run, start lpserver and then randomly kill/restart it
#
#   Author: Daniel Lundin <dln(at)eintr(dot)org>
#
####################################################################################################

import itertools
import zmq

####################################################################################################

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

####################################################################################################

def connect(context):
    client = context.socket(zmq.REQ)
    client.connect(SERVER_ENDPOINT)

def client() -> None:
    context = zmq.Context()

    print("Connecting to server...")
    client = connect(context)

    # Sequential: send and poll for response
    for sequence in itertools.count():
        request = str(sequence).encode()
        print(f"Sending ({request})")
        client.send(request)

        retries_left = REQUEST_RETRIES
        while True:
            print("Poll server")
            if client.poll(REQUEST_TIMEOUT) & zmq.POLLIN:
                reply = client.recv()
                if int(reply) == sequence:
                    print(f"Server replied OK {reply}")
                    break
                else:
                    print("Error: Malformed reply from server: {reply}")
                    # ok ???
                    continue

            print("Warning: No response from server")
            retries_left -= 1

            # Socket is confused. Close and remove it.
            #   Set linger period for socket shutdown: discard all pending messages
            client.setsockopt(zmq.LINGER, 0)
            client.close()

            if retries_left == 0:
                print("Error: Server seems to be offline, abandoning")
                # sys.exit()
                return

            print("Reconnecting to server...")
            # Create new connection
            client = connect(context)
            print(f"Resending {request}")
            client.send(request)


client()
