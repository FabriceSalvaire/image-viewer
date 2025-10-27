#!/usr/bin/env python

"""
Farm out processing to multiple processes via zmq asyncio.

This implementation is not safe if a worker fails.

- heartbeat
- signal worker is ready

- if the main process crashes => childs are always killed
  True ???
- if the main process becomes unresponsive ???
- if a child crashes ???
- if a child becomes unresponsive (infinite loop etc.) ???

We don't know where are dispatched data !!!
Thus we must track the replies.

see also https://github.com/zeromq/libzmq/issues/3387
IPC listener fails to clean up temporary socket files/directories
"""

####################################################################################################

import asyncio
import multiprocessing as mp
import pickle
import random
import tempfile
import time

# https://psutil.readthedocs.io/en/latest/
import psutil

import zmq
from zmq.asyncio import Context, Poller

####################################################################################################

N = 100
NUMBER_OF_WORKERS = 5
# N = 1000
# NUMBER_OF_WORKERS = 4
# N = 11_000
# NUMBER_OF_WORKERS = 10

TMP_DIR = tempfile.TemporaryDirectory()
print(f"Temporary directory {TMP_DIR.name}")
IPC_DATA = f'ipc://{TMP_DIR.name}/pool_zmq_data'
IPC_CTRL = f'ipc://{TMP_DIR.name}/pool_zmq_ctrl'
print(f"IPC {IPC_CTRL} {IPC_DATA}")

SLEEP_INF = 100   # ms
SLEEP_SUP = 200

####################################################################################################

class Worker(mp.Process):
    """
    Process stream of data until a quit signal is received.

    Parameters
    ----------
    f : callable
        Function of one argument to apply to each input datum.
    """

    ##############################################

    def __init__(self, f):
        super(Worker, self).__init__()
        self._f = f

    ##############################################

    def run(self):
        ctx = Context()
        self._socket_ctrl = ctx.socket(zmq.SUB)   # -> PUB
        self._socket_ctrl.setsockopt(zmq.SUBSCRIBE, b'')   # subscribe to all messages
        self._socket_ctrl.connect(IPC_CTRL)

        self._socket_data = ctx.socket(zmq.REP)   # -> DEALER
        self._socket_data.connect(IPC_DATA)

        self.poller = Poller()
        self.poller.register(self._socket_data, zmq.POLLIN)
        self.poller.register(self._socket_ctrl, zmq.POLLIN)

        self._dont_exit = True
        self._counter = 0
        self._job_time_accumulator = 0

        asyncio.run(self.main())

        self._socket_data.close()
        self._socket_ctrl.close()

    ##############################################

    async def ctrl_handler(self):
        msg = await self._socket_ctrl.recv()
        print(f"> {self.name}: Receive msg {msg}")
        if msg == b'quit':
            print(f"> {self.name}: done {self._counter} Quit")
            self._dont_exit = False

    ##############################################

    async def data_handler(self):
        msg = await self._socket_data.recv()
        job_start = time.monotonic()
        data = pickle.loads(msg)
        print(f"> {self.name}: Receive msg {msg} data {data}")
        # simulate workload
        _ = random.randint(SLEEP_INF, SLEEP_SUP) / 1000
        await asyncio.sleep(_)
        result = self._f(data)
        msg = [self.name, data, result]
        msg = pickle.dumps(msg)
        self._socket_data.send(msg)
        self._counter += 1
        job_time = time.monotonic() - job_start
        self._job_time_accumulator += job_time
        print(f"> {self.name}: job time {job_time:.3f} s")
        if self.name == 'Worker-1' and self._counter > 10:
            1/0
        elif self.name == 'Worker-2' and self._counter > 10:
            await asyncio.sleep(1000)

    ##############################################

    async def main(self):
        while self._dont_exit:
            events = dict(await self.poller.poll())
            if self._socket_ctrl in events:
                await self.ctrl_handler()
            if self._dont_exit and self._socket_data in events:
                await self.data_handler()

####################################################################################################

class WorkerPool:
    """
    Pool of worker processes.

    Parameters
    ----------
    N : int
        Number of processes to start.
    target : callable
        Function of one argument to apply to each input datum.
    callback : callable
        Function of one argument to apply to each result.
    """

    ##############################################

    def __init__(self, N, target, callback):
        self._callback = callback

        ctx = Context()
        #
        self._socket_data = ctx.socket(zmq.DEALER)
        self._socket_data.bind(IPC_DATA)

        self._socket_ctrl = ctx.socket(zmq.PUB)
        self._socket_ctrl.bind(IPC_CTRL)

        self._proc_list = [Worker(target) for i in range(N)]

        self._started = False
        self._counter = 0
        self._sender_done = False
        self._sender_counter = 0
        self._receiver_counter = 0

        self._monitor_task = None
        self._receiver_task = None
        self._sender_task = None

        self._last_worker_reply_time = {}

    ##############################################

    def start(self):
        """Start all worker processes and result handler."""
        for p in self._proc_list:
            p.start()
            print(f"Started worker {p.name} PID {p.pid}")
        # p.is_alive()
        # p.terminate()
        # p.kill()
        # p.exitcode

    ##############################################

    async def run(self, data_list):
        async with asyncio.TaskGroup() as tg:
            self._monitor_task = tg.create_task(self.monitor())
            self._receiver_task = tg.create_task(self.receiver())
            self._sender_task = tg.create_task(self.sender(data_list))

    ##############################################

    async def monitor(self) -> None:
        while not self._started or self._counter:
            await asyncio.sleep(.5)
            print(f"!!! Monitor...")
            kill = False
            for p in self._proc_list:
                now = time.monotonic()
                last = self._last_worker_reply_time[p.name]
                delay = now - last
                if not p.is_alive():
                    print(f"  Worker {p.name} is dead since {delay:.3f} s")
                    if self._sender_done:
                        kill = True
                else:
                    process_info = psutil.Process(p.pid)
                    memory_info = process_info.memory_info()
                    # https://github.com/dask/distributed/issues/1409
                    rss = memory_info.rss / 1024**2
                    print(f"  Worker {p.name} memory {rss:.1f} MB")
                    if delay > 3:
                        print(f"  Worker {p.name} is slow since {delay:.3f} s")
                        # worker could be idle, must check a ping-pong
                        if self._sender_done:
                            kill = True
                            p.kill()
            if kill:
                print(f"  Must end")
                self._receiver_task.cancel()
                return

    ##############################################

    async def receiver(self) -> None:
        try:
            poller = Poller()
            poller.register(self._socket_data, zmq.POLLIN)
            while not self._started or self._counter:
                print(f"Counter {self._counter}   {self._receiver_counter} / {self._sender_counter}")
                if self._counter != (self._sender_counter - self._receiver_counter):
                    raise NameError("Counter mismatch")
                events = await poller.poll()
                if self._socket_data in dict(events):
                    msg = await self._socket_data.recv_multipart()
                    worker, data, result = pickle.loads(msg[1])
                    self._last_worker_reply_time[worker] = time.monotonic()
                    print(f"Receive msg {msg} from {worker}: {data} -> {result}")
                    self._callback(data, result)
                    self._counter -= 1
                    self._receiver_counter += 1
        except asyncio.CancelledError:
            print('Receiver canceled')
            raise
        # finally:
        #     print('')

    ##############################################

    async def sender(self, data_list):
        # Send data to workers for processing
        # It fills a queue for each worker
        self._counter = 0
        self._started = False
        self._sender_done = False
        for data in data_list:
            await self.put(data)
            self._counter += 1
            self._sender_counter += 1
            print(f"Sended '{data}'   sent = {self._sender_counter}")
            self._started = True
            # Wait for worker else this coroutine finnish nearly immediadely
            delta_counter = self._sender_counter - self._receiver_counter
            if delta_counter > 10:
                _ = SLEEP_INF / 1000
                print(f"Sleep {_}s    delta = {delta_counter} sent = {self._sender_counter} ...")
                await asyncio.sleep(_)
            # Fixme: a better strategy is to continuously fill the queue of each worker to a maximum.
            #   so we must track the length of each queue
            #   and wait for a job done event when all the queue are full
            #     empty_queue = asyncio.Event()
            #     receiver do for each msg
            #       empty_queue.set()
            #     sender do when queue is full
            #       empty_queue.clear()
            #       await empty_queue.wait()
        self._sender_done = True

    ##############################################

    async def put(self, data):
        """Process a datum """
        msg = (b'', pickle.dumps(data))
        await self._socket_data.send_multipart(msg)

    ##############################################

    async def join(self):
        """ Wait until all workers are stopped.
        """
        # Send quit signals until all workers stop running:
        while self._proc_list:
            await self._socket_ctrl.send(b'quit')
            for p in self._proc_list:
                if not p.is_alive():
                    self._proc_list.remove(p)
        self._socket_ctrl.close()
        self._socket_data.close()

####################################################################################################

async def main():
    # Fixme: can wait for ever at counter = 1000 for N = 11_000
    #   solved by ???
    #   lost message / queue ???

    data_list = [i for i in range(N)]

    def f(data):
        return data**2

    results = []
    def callback(data, result):
        results.append((data, result))

    pool = WorkerPool(NUMBER_OF_WORKERS, f, callback)
    pool.start()
    await pool.run(data_list)
    # both tasks have finnished
    await pool.join()

    print('Results', len(results) == N)

####################################################################################################

if __name__ == '__main__':
    asyncio.run(main())
