####################################################################################################

# https://github.com/zeromq/pyzmq/blob/main/examples/asyncio/coroutines.py

import asyncio
import time

import zmq
from zmq.asyncio import Context, Poller

####################################################################################################

url = 'tcp://127.0.0.1:5555'

ctx = Context.instance()

####################################################################################################

async def ping() -> None:
    """print dots to indicate idleness"""
    while True:
        await asyncio.sleep(0.5)
        print('.')

async def receiver() -> None:
    """receive messages with polling"""
    pull = ctx.socket(zmq.PULL)
    pull.connect(url)
    poller = Poller()
    poller.register(pull, zmq.POLLIN)
    while True:
        events = await poller.poll()
        if pull in dict(events):
            print("recving", events)
            msg = await pull.recv_multipart()
            print('recvd', msg)

async def sender() -> None:
    """send a message every second"""
    tic = time.time()
    push = ctx.socket(zmq.PUSH)
    push.bind(url)
    while True:
        print("sending")
        msg = str(time.time() - tic).encode('ascii')
        await push.send_multipart([msg])
        await asyncio.sleep(1)

async def main() -> None:
    # tasks = [
    #     asyncio.create_task(ping()),
    #     asyncio.create_task(receiver()),
    #     asyncio.create_task(sender()),
    # ]
    # done, pending = await asyncio.wait(tasks)
    async with asyncio.TaskGroup() as tg:
        tg.create_task(ping())
        tg.create_task(receiver())
        tg.create_task(sender())

 # start the asyncio program
asyncio.run(main())
