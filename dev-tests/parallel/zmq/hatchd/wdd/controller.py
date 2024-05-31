####################################################################################################

from __future__ import print_function
from multiprocessing import Process, Event
from six.moves import xrange
import json
import logging
import time
import uuid

import zmq

from wdd.worker import Worker

####################################################################################################

class Job(object):
    def __init__(self, work):
        self.id = uuid.uuid4().hex
        self.work = work

####################################################################################################

class Controller(object):
    """
    Manage distribution of jobs to workers and collation of results.
    """

    CONTROL_PORT = 5755

    def __init__(self, stop_event, port=CONTROL_PORT):
        self.logger = logging.getLogger(__name__)
        self.stop_event = stop_event
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind('tcp://*:{0}'.format(port))
        self.workers = {}
        # We won't assign more than 50 jobs to a worker at a time; this ensures
        # reasonable memory usage, and less shuffling when a worker dies.
        self.max_jobs_per_worker = 50
        # When/if a client disconnects we'll put any unfinished work in here,
        # work_iterator() will return work from here as well.
        self._work_to_requeue = []

    def work_iterator(self):
        """Return an iterator that yields work to be done.
        """
        iterator = iter(xrange(0, 10000))
        while True:
            if self._work_to_requeue:
                yield self._work_to_requeue.pop()
            else:
                num = next(iterator)
                yield Job({'number': num})

    def run(self):
        for job in self.work_iterator():
            next_worker_id = None
            while next_worker_id is None:
                # First check if there are any worker messages to process. We
                # do this while checking for the next available worker so that
                # if it takes a while to find one we're still processing
                # incoming messages.
                while self.socket.poll(0):
                    # Note that we're using recv_multipart() here, this is a
                    # special method on the ROUTER socket that includes the
                    # id of the sender. It doesn't handle the json decoding
                    # automatically though so we have to do that ourselves.
                    worker_id, message = self.socket.recv_multipart()
                    message = json.loads(message.decode('utf8'))
                    self._handle_worker_message(worker_id, message)
                # If there are no available workers (they all have 50 or
                # more jobs already) sleep for half a second.
                next_worker_id = self._get_next_worker_id()
                if next_worker_id is None:
                    time.sleep(0.5)
            # We've got a Job and an available worker_id, all we need to do
            # is send it. Note that we're now using send_multipart(), the
            # counterpart to recv_multipart(), to tell the ROUTER where our
            # message goes.
            self.logger.info('sending job %s to worker %s', job.id,
                             next_worker_id)
            self.workers[next_worker_id][job.id] = job
            self.socket.send_multipart(
                [next_worker_id, json.dumps((job.id, job.work)).encode('utf8')])
            if self.stop_event.is_set():
                break
        self.stop_event.set()

    def _get_next_worker_id(self):
        """Return the id of the next worker available to process work. Note
        that this will return None if no clients are available.
        """
        # It isn't strictly necessary since we're limiting the amount of work
        # we assign, but just to demonstrate that we're doing our own load
        # balancing we'll find the worker with the least work
        if self.workers:
            worker_id, work = sorted(self.workers.items(),
                                     key=lambda x: len(x[1]))[0]
            if len(work) < self.max_jobs_per_worker:
                return worker_id
        # No worker is available. Our caller will have to handle this.
        return None

    def _handle_worker_message(self, worker_id, message):
        """Handle a message from the worker identified by worker_id.

        {'message': 'connect'}
        {'message': 'disconnect'}
        {'message': 'job_done', 'job_id': 'xxx', 'result': 'yyy'}
        """
        if message['message'] == 'connect':
            assert worker_id not in self.workers
            self.workers[worker_id] = {}
            self.logger.info('[%s]: connect', worker_id)
        elif message['message'] == 'disconnect':
            # Remove the worker so no more work gets added, and put any
            # remaining work into _work_to_requeue
            remaining_work = self.workers.pop(worker_id)
            self._work_to_requeue.extend(remaining_work.values())
            self.logger.info('[%s]: disconnect, %s jobs requeued', worker_id,
                             len(remaining_work))
        elif message['message'] == 'job_done':
            result = message['result']
            job = self.workers[worker_id].pop(message['job_id'])
            self._process_results(worker_id, job, result)
        else:
            raise Exception('unknown message: %s' % message['message'])

    def _process_results(self, worker_id, job, result):
        self.logger.info('[%s]: finished %s, result: %s',
                         worker_id, job.id, result)

####################################################################################################

def run_worker(event):
    logging.basicConfig(level=logging.INFO)
    worker = Worker(event)
    worker.run()


def run_controller(event):
    logging.basicConfig(level=logging.INFO)
    Controller(event).run()


def run():
    stop_event = Event()
    processes = []
    processes.append(Process(target=run_controller, args=(stop_event,)))
    # Start a few worker processes
    for i in range(10):
        processes.append(Process(target=run_worker, args=(stop_event,)))
    # To test out our disconnect messaging we'll also start one more worker
    # process with a different event that we'll stop shortly after starting.
    another_stop_event = Event()
    processes.append(Process(target=run_worker, args=(another_stop_event,)))
    for p in processes:
        p.start()
    try:
        time.sleep(5)
        another_stop_event.set()
        # The controller will set the stop event when it's finished, just
        # idle until then
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        another_stop_event.set()
    print('waiting for processes to die...')
    for p in processes:
        p.join()
    print('all done')

####################################################################################################

if __name__ == '__main__':
    run()
