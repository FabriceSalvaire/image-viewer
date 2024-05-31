from __future__ import print_function
from multiprocessing import Process, Event
import time
import uuid
from six.moves import xrange
import zmq


class Controller(object):
    """Generate jobs, send the jobs out to workers and collect the results.
    """
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.context = zmq.Context()
        # Create a push socket to send out jobs to the workers
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind('tcp://127.0.0.1:5755')
        # And a pull socket to accept the results of the work. In a very
        # simple case you could let the workers handle the results directly
        # (for example storing into a database) but this is a little
        # bit neater.
        self.socket_result = self.context.socket(zmq.PULL)
        self.socket_result.bind('tcp://127.0.0.1:5756')

    def work_iterator(self):
        """Return an iterator that yields work to be done.

        This iterator is super boring and yields successive ints using
        xrange().
        """
        return xrange(0, 10000)

    def run(self):
        for i in self.work_iterator():
            # For each job in our list of work send it out to a worker.
            # Messages sent using a push socket are round-robin load balanced
            # all connected workers.
            self.socket.send_json({'number': i})
            # Poll the incoming socket for results. poll() returns a Truthy
            # value if there are messages waiting.
            while self.socket_result.poll(0):
                result = self.socket_result.recv_json()
                print(result['worker_id'], result['result'])
            if self.stop_event.is_set():
                break
        self.stop_event.set()


class Worker(object):
    """Accept work in the form of {'number': xxx}, square the number and
    send it back to the controller in the form
    {'result': xxx, 'worker_id': yyy}. Our "work" in this case is just
    squaring the contents of 'number'.
    """
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://127.0.0.1:5755')
        self.socket_result = self.context.socket(zmq.PUSH)
        self.socket_result.connect('tcp://127.0.0.1:5756')
        # We'll send this id back with our results to make it easier
        # to verify that work is getting distributed among multiple
        # workers.
        self.my_id = uuid.uuid4().hex[:4]

    def run(self):
        while not self.stop_event.is_set():
            # Poll the socket for incoming messages. This will wait up to
            # 0.1 seconds before returning False. The other way to do this is
            # is to use zmq.NOBLOCK when reading from the socket, catching
            # zmq.AGAIN and sleeping for 0.1.
            while self.socket.poll(100):
                work = self.socket.recv_json()
                self.socket_result.send_json(
                    {'result': work['number'] ** 2, 'worker_id': self.my_id})


# We'll use multiprocessing to run multiple workers and one controller, but
# we need module-level functions to do that.

def run_worker(event):
    Worker(event).run()


def run_controller(event):
    Controller(event).run()


def run():
    # We'll set this Event when we want all the processes to exit
    stop_event = Event()
    Process(target=run_controller, args=(stop_event,)).start()
    # Start ten worker processes
    for i in range(10):
        Process(target=run_worker, args=(stop_event,)).start()
    try:
        # The controller will set the stop event when it's finished, just
        # idle until then
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
    print('all done')


if __name__ == '__main__':
    run()
