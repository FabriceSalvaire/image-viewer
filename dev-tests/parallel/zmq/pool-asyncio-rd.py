#!/usr/bin/env python

# Fixme: process are not killed when raise !!!

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
import json
import multiprocessing as mp
import pickle
import random
import tempfile
import time
import threading
from typing import Callable

# https://psutil.readthedocs.io/en/latest/
import psutil

import zmq
from zmq.asyncio import Context, Poller

from colorama import Fore
import colorama

####################################################################################################

# FG_COLOR = Fore.BLACK
FG_COLOR = Fore.WHITE

colorama.init(autoreset=False)

def cprint(*args) -> None:
    print(*args, FG_COLOR)

#################################################################################################### 

N = 100
NUMBER_OF_WORKERS = 5
# N = 1000
# NUMBER_OF_WORKERS = 4
# N = 11_000
# NUMBER_OF_WORKERS = 10

TMP_DIR = tempfile.TemporaryDirectory()
cprint(f"{Fore.RED}Temporary directory{FG_COLOR} {TMP_DIR.name}")
IPC_DATA = f'ipc://{TMP_DIR.name}/pool_zmq_data'
IPC_CTRL = f'ipc://{TMP_DIR.name}/pool_zmq_ctrl'
cprint(f"{Fore.RED}IPC{FG_COLOR} {IPC_CTRL} {IPC_DATA}")

SLEEP_INF = 100   # ms
SLEEP_SUP = 200

####################################################################################################

class AtomicCounter:

    ##############################################

    def __init__(self, value=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self._value = value
        self._lock = threading.Lock()

    ##############################################

    def increment(self, offset=1):
        """Atomically increment the counter by offset (default 1) and return the new value."""
        with self._lock:
            self._value += offset
            return self._value

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

    def __init__(self, target: Callable, callback: Callable) -> None:
        super().__init__()
        self._target = target
        self._callback = callback
        self._ready = False

    ##############################################

    # Fixme: bname ?
    @property
    def id(self) -> str:
        return self._name

    @property
    def bid(self) -> bytes:
        return self._name.encode('utf8')

    @property
    def callback(self) -> Callable:
        return self._callback

    ##############################################

    def set_ready(self) -> None:
        cprint(f"{Fore.BLUE}Worker is ready:{FG_COLOR} {self.name}")
        self._ready = True

    @property
    def ready(self) -> bool:
        return self._ready

    ##############################################

    def run(self):
        cprint(f"{Fore.BLUE}Run worker:{FG_COLOR} {self.name} PID {self.pid}")
        ctx = Context()
        self._socket_ctrl = ctx.socket(zmq.SUB)   # -> PUB
        self._socket_ctrl.setsockopt(zmq.SUBSCRIBE, b'')   # subscribe to all messages
        self._socket_ctrl.connect(IPC_CTRL)

        self._socket_data = ctx.socket(zmq.DEALER)   # -> ROUTER
        # identity = self.name.encode('ascii')
        identity = self.name.encode('utf8')
        self._socket_data.identity = identity
        self._socket_data.connect(IPC_DATA)

        self.poller = Poller()
        self.poller.register(self._socket_data, zmq.POLLIN)
        self.poller.register(self._socket_ctrl, zmq.POLLIN)

        self._dont_exit = True
        self._counter = 0
        self._job_time_accumulator = 0

        cprint(f"{Fore.BLUE}Start asyncio loop for worker:{FG_COLOR} {self.name}")
        asyncio.run(self.main())
        cprint(f"{Fore.BLUE}Asyncio loop done for worker:{FG_COLOR} {self.name}")

        self._socket_data.close()
        self._socket_ctrl.close()
        cprint(f"{Fore.BLUE}Worker done:{FG_COLOR} {self.name}")

    ##############################################

    async def main(self):
        # to simulate a startup timeout
        # await asyncio.sleep(10)
        msg = {'message': 'ready'}   # connect ?
        await self._socket_data.send_json(msg)

        while self._dont_exit:
            # block indefinitely until a requested event has occurred on at least one socket
            # timeout is ms
            events = dict(await self.poller.poll(timeout=-1))
            if self._socket_ctrl in events:
                await self.ctrl_handler()
            if self._dont_exit and self._socket_data in events:
                await self.data_handler()

    ##############################################

    async def ctrl_handler(self):
        msg = await self._socket_ctrl.recv()
        cprint(f"{Fore.BLUE}> {self.name}: Receive msg{FG_COLOR} {msg}")
        if msg == b'quit':
            cprint(f"{Fore.BLUE}> {self.name}: done{FG_COLOR} {self._counter} Quit")
            self._dont_exit = False

    ##############################################

    async def data_handler(self):
        msg = await self._socket_data.recv_json()
        job_start = time.monotonic()
        # data = pickle.loads(msg)
        cprint(f"{Fore.BLUE}> {self.name}: Receive msg{FG_COLOR} {msg}")
        # simulate workload
        _ = random.randint(SLEEP_INF, SLEEP_SUP) / 1000
        await asyncio.sleep(_)
        data = msg['data']
        result = self._target(data)
        # msg = [self.name, data, result]
        # msg = pickle.dumps(msg)
        # self._socket_data.send(msg)
        msg = {
            'result': result,
        }
        await self._socket_data.send_json(msg)
        self._counter += 1
        job_time = time.monotonic() - job_start
        self._job_time_accumulator += job_time
        cprint(f"{Fore.BLUE}> {self.name}: job time{FG_COLOR} {job_time:.3f} s")
        if self.name == 'Worker-1' and self._counter > 10:
            1/0
        elif self.name == 'Worker-2' and self._counter > 10:
            await asyncio.sleep(1000)

####################################################################################################

class Job:

    LAST_JOB_ID = AtomicCounter(1)

    ##############################################

    def __init__(self, msg) -> None:
        self.id = self.LAST_JOB_ID.increment()
        self.msg = msg

####################################################################################################

# Fixme: Controller ?
class WorkerPool:
    """Pool of worker processes"""

    ##############################################

    def __init__(self) -> None:
        self._workers = {}
        self._last_worker_reply_time = {}

        self._started = False
        self._counter = 0
        self._sender_done = False
        self._sender_counter = 0
        self._receiver_counter = 0

        self._monitor_task = None
        self._receiver_task = None
        self._sender_task = None

        self._socket_data = None
        self._socket_ctrl = None
        self._create_sockets()

    ##############################################

    def _create_sockets(self) -> None:
        ctx = Context()
        self._socket_data = ctx.socket(zmq.ROUTER)
        self._socket_data.bind(IPC_DATA)
        self._socket_ctrl = ctx.socket(zmq.PUB)
        self._socket_ctrl.bind(IPC_CTRL)

    ##############################################

    def start(self, number_of_workers: int, target: Callable, callback: Callable) -> None:
        """Start all worker processes and result handler."""
        workers = [Worker(target, callback) for i in range(number_of_workers)]
        self._workers = {_.id: _ for _ in workers}
        for _ in workers:
            _.start()
            cprint(f"{Fore.RED}Started worker:{FG_COLOR} {_.name} PID {_.pid}")

        # p.is_alive()
        # p.terminate()
        # p.kill()
        # p.exitcode

    ##############################################

    async def run(self, data_list):
        async with asyncio.TaskGroup() as tg:
            self._monitor_task = tg.create_task(self.monitor())
            self._receiver_task = tg.create_task(self.receiver(data_list))
            # self._sender_task = tg.create_task(self.sender(data_list))

    ##############################################

    async def monitor(self) -> None:
        while not self._started or self._counter:
            await asyncio.sleep(.5)
            cprint(f"{Fore.RED}!!! Monitor...")
            kill = False
            for worker in self._workers.values():
                now = time.monotonic()
                last = self._last_worker_reply_time.get(worker.name, None)
                if last is not None:
                    delay = now - last
                else:
                    delay = -1
                if not worker.is_alive():
                    cprint(f"{Fore.RED}  Worker{FG_COLOR} {worker.name} is dead since {delay:.3f} s")
                    if self._sender_done:
                        kill = True
                else:
                    process_info = psutil.Process(worker.pid)
                    memory_info = process_info.memory_info()
                    # https://github.com/dask/distributed/issues/1409
                    rss = memory_info.rss / 1024**2
                    cprint(f"{Fore.RED}  Worker{FG_COLOR} {worker.name} memory {rss:.1f} MB")
                    if delay > 3:
                        cprint(f"{Fore.RED}  Worker{FG_COLOR} {worker.name} is slow since {delay:.3f} s")
                        # worker could be idle, must check a ping-pong
                        if self._sender_done:
                            kill = True
                            worker.kill()
            if kill:
                cprint(f"{Fore.RED}  Must end")
                self._receiver_task.cancel()
                return

    ##############################################

    async def _data_recv(self) -> list[bytes, dict]:
        worker_id, msg = await self._socket_data.recv_multipart()
        worker_id = worker_id.decode('utf8')
        msg = json.loads(msg)
        msg['worker_id'] = worker_id
        return worker_id, msg

    ##############################################

    # def _job_iterator(self, data_list):

    ##############################################

    def _get_next_worker(self):
        try:
            return self._worker_lru.pop()
        except IndexError:
            raise StopIteration

    ##############################################

    async def receiver(self, data_list) -> None:
        try:
            # poller = Poller()
            # poller.register(self._socket_data, zmq.POLLIN)
            #    events = await poller.poll()
            #    if self._socket_data in dict(events):

            # Wait all workers are ready
            number_of_workers = len(self._workers)
            self._worker_lru = []
            while number_of_workers:
                # timeout in ms
                event = await self._socket_data.poll(timeout=1000, flags=zmq.POLLIN)
                if not event:
                    raise NameError("Worker ready timeout")
                worker_id, msg = await self._data_recv()
                cprint(f"{Fore.RED}Received from{FG_COLOR} {worker_id} {msg}")
                worker = self._workers[worker_id]
                worker.set_ready()
                self._worker_lru.append(worker)
                number_of_workers -= 1
                # cprint(f"{Fore.RED}Worker ready{FG_COLOR} {worker_id}")
            cprint(f"{Fore.RED}All walkers are ready")

            data_it = iter(data_list)

            # Send job to each workers
            #   kind of zip...
            while True:
                try:
                    worker = self._get_next_worker()
                    await self.put(worker, data_it)
                except StopIteration:
                    break

            # Send job
            while True:
                try:
                # timeout in ms
                    job_timemout = 10 * 60 * 1000   # ms
                    event = await self._socket_data.poll(timeout=job_timemout, flags=zmq.POLLIN)
                    if not event:
                        raise NameError("Worker job timeout")
                    worker_id, msg = await self._data_recv()
                    cprint(f"{Fore.RED}Receive msg from:{FG_COLOR} {worker_id} -> {msg}")
                    worker = self._workers[worker_id]
                    # self._worker_lru.append(worker)
                    await self.put(worker, data_it)
                except StopIteration:
                    break

            # while not self._started or self._counter:
            #     cprint(f"{Fore.RED}Counter {self._counter}   {self._receiver_counter} / {self._sender_counter}")
            #     if self._counter != (self._sender_counter - self._receiver_counter):
            #         raise NameError("Counter mismatch")
            #     events = await poller.poll()
            #     if self._socket_data in dict(events):
            #         msg = await self._socket_data.recv_multipart()
            #         worker, data, result = pickle.loads(msg[1])
            #         self._last_worker_reply_time[worker] = time.monotonic()
            #         cprint(f"{Fore.RED}Receive msg {msg} from {worker}: {data} -> {result}")
            #         self._callback(data, result)
            #         self._counter -= 1
            #         self._receiver_counter += 1
        except asyncio.CancelledError:
            cprint('Receiver canceled')
            raise
        # finally:
        #     cprint('')

    ##############################################

    # async def sender(self, data_list):
    #     # Send data to workers for processing
    #     # It fills a queue for each worker
    #     self._counter = 0
    #     self._started = False
    #     self._sender_done = False
    #     for data in data_list:
    #         await self.put(data)
    #         self._counter += 1
    #         self._sender_counter += 1
    #         cprint(f"{Fore.RED}Sended{FG_COLOR} '{data}'   sent = {self._sender_counter}")
    #         self._started = True
    #         # Wait for worker else this coroutine finnish nearly immediadely
    #         delta_counter = self._sender_counter - self._receiver_counter
    #         if delta_counter > 10:
    #             _ = SLEEP_INF / 1000
    #             cprint(f"{Fore.RED}Sleep{FG_COLOR} {_}s    delta = {delta_counter} sent = {self._sender_counter} ...")
    #             await asyncio.sleep(_)
    #     self._sender_done = True

    ##############################################

    async def put(self, worker, data_it):
        # worker = self._get_next_worker()
        data = next(data_it)
        # _ = pickle.dumps(data)
        msg = {'data': data}
        cprint(f"{Fore.RED}Send job{FG_COLOR} {msg} to worker {worker.id}")
        _ = json.dumps(msg).encode('utf8')
        msg = [worker.bid, _]
        await self._socket_data.send_multipart(msg)

        # msg = (b'', pickle.dumps(data))
        # await self._socket_data.send_multipart(msg)

    ##############################################

    async def join(self):
        """ Wait until all workers are stopped.
        """
        # Send quit signals until all workers stop running:
        while self._workers:
            await self._socket_ctrl.send(b'quit')
            for name, worker in self._workers.items():
                if not worker.is_alive():
                    del self._workers[name]
        self._socket_ctrl.close()
        self._socket_data.close()

####################################################################################################

async def main():
    # Fixme: can wait for ever at counter = 1000 for N = 11_000
    #   solved by ???
    #   lost message / queue ???

    pool = WorkerPool()

    def target(data: int) -> int:
        return data**2

    results = []
    def callback(data, result):
        results.append((data, result))

    pool.start(NUMBER_OF_WORKERS, target, callback)

    data_list = [i for i in range(N)]
    await pool.run(data_list)

    # both tasks have finnished
    await pool.join()

    cprint('Results', len(results) == N)

####################################################################################################

if __name__ == '__main__':
    asyncio.run(main())
