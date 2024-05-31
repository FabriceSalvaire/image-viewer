#!/usr/bin/env python

"""
Farm out processing to multiple processes via zmq.
"""

####################################################################################################

import pickle
import threading
import multiprocessing as mp
import zmq

# deprecated
# https://www.tornadoweb.org/en/stable/ioloop.html#module-tornado.ioloop
from zmq.eventloop.ioloop import IOLoop
# A utility class for event-based messaging on a zmq socket using tornado.
from zmq.eventloop.zmqstream import ZMQStream

import numpy as np

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
        self.f = f

    ##############################################

    def run(self):
        ctx = zmq.Context()
        sock_data = ctx.socket(zmq.REP)
        sock_data.connect('ipc://mp_pool_zmq_demo_data')

        sock_ctrl = ctx.socket(zmq.SUB)
        sock_ctrl.setsockopt(zmq.SUBSCRIBE, b'')
        sock_ctrl.connect('ipc://mp_pool_zmq_demo_ctrl')

        # Note that the control socket stream isn't flushed when a quit signal
        # is received because doing so causes errors:
        ioloop = IOLoop.instance()
        stream_data = ZMQStream(sock_data, ioloop)
        stream_ctrl = ZMQStream(sock_ctrl, ioloop)

        def ctrl_handler(msg):
            if msg[0] == b'quit':
                print('quitting', self)
                stream_data.flush()
                ioloop.stop()
        stream_ctrl.on_recv(ctrl_handler)

        def data_handler(msg):
            data = pickle.loads(msg[0])
            print(self, data)
            result = self.f(data)
            msg = pickle.dumps([data, result])
            sock_data.send(msg)
        stream_data.on_recv(data_handler)

        ioloop.start()

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
        self.callback = callback

        ctx = zmq.Context()
        self.sock_data = ctx.socket(zmq.DEALER)
        self.sock_data.bind('ipc://mp_pool_zmq_demo_data')

        self.sock_ctrl = ctx.socket(zmq.PUB)
        self.sock_ctrl.bind('ipc://mp_pool_zmq_demo_ctrl')

        self.proc_list = [Worker(target) for i in range(N)]

    ##############################################

    def start(self):
        """
        Start all worker processes and result handler.
        """

        # Start workers:
        for p in self.proc_list:
            p.start()

        # Startup results handler:
        self.ioloop = IOLoop.instance()
        stream = ZMQStream(self.sock_data, self.ioloop)
        stream.on_recv(self.callback)
        threading.Thread(target=self.ioloop.start).start()

    ##############################################

    def put(self, data):
        """
        Process a datum.
        """
        self.sock_data.send_multipart((b'', pickle.dumps(data)))

    ##############################################

    def join(self):
        """
        Wait until all workers are stopped.
        """

        self.ioloop.stop()

        # Send quit signals until all workers stop running:
        while self.proc_list:
            self.sock_ctrl.send(b'quit')
            for p in self.proc_list:
                if not p.is_alive():
                    self.proc_list.remove(p)
        self.sock_ctrl.close()
        self.sock_data.close()

####################################################################################################

if __name__ == '__main__':

    # Data to process:
    data_list = [np.random.rand(2, 2) for i in range(10)]

    # Function to apply to each datum:
    def f(data):
        return np.linalg.inv(data)

    # Function for handling processed data:
    results = []
    def callback(msg):
        data, result = pickle.loads(msg[1])
        results.append((data, result))

    # Start process pool:
    pool = WorkerPool(5, f, callback)
    pool.start()

    # Send data to workers for processing:
    for data in data_list:
        pool.put(data)

    # Wait for all results to arrive before telling all workers to terminate:
    while len(results) < len(data_list):
        continue
    pool.join()

    # Display results:
    print(results)
