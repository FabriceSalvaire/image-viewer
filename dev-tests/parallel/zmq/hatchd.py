####################################################################################################

# WARNING: this code has issues !!!

# https://www.hatchd.com.au/blog/zeromq-and-the-art-of-work-distribution

# See Load Balancing Pattern

# for _ in range(NBR_WORKERS * 10):
#     # LRU worker is next waiting in the queue
#     address, empty, ready = client.recv_multipart()
#     client.send_multipart([
#         address,
#         b'',
#         b'This is the workload',
#     ])
# for _ in range(NBR_WORKERS):
#     address, empty, ready = client.recv_multipart()
#     client.send_multipart([
#         address,
#         b'',
#         b'END',
#     ])

####################################################################################################

# https://docs.python.org/3/library/threading.html#event-objects
# https://superfastpython.com/multiprocessing-event-object-in-python
from multiprocessing import Process, Event
import json
import logging
import random
import time
import uuid

import zmq

####################################################################################################

class Job:

    LAST_JOB_ID = 0

    def __init__(self, work):
        # uuid.uuid4().hex
        Job.LAST_JOB_ID += 1
        self.id = Job.LAST_JOB_ID
        self.work = work

####################################################################################################

class Controller:
    """Generate jobs, send the jobs out to workers and collect the results.
    """

    CONTROL_PORT = 5755

    ##############################################

    def __init__(self, stop_event, port=CONTROL_PORT):
        # self.logger = logging.getLogger(__name__)
        self.stop_event = stop_event
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(f'tcp://*:{port}')
        # We'll keep our workers here, this will be keyed on the worker id,
        # and the value will be a dict of Job instances keyed on job id.
        self.workers = {}
        # We won't assign more than 50 jobs to a worker at a time; this ensures
        # reasonable memory usage, and less shuffling when a worker dies.
        self.max_jobs_per_worker = 50
        # When/if a client disconnects we'll put any unfinished work in here,
        # work_iterator() will return work from here as well.
        self._work_to_requeue = []

    ##############################################

    def work_iterator(self):
        """Return an iterator that yields work to be done.
        """
        # iter() makes our xrange object into an iterator so we can use next() on it.
        iterator = iter(range(0, 10_000))
        while True:
            # Return requeued work first. We could simplify this method by
            # returning all new work then all requeued work, but this way we
            # know _work_to_requeue won't grow too large in the case of
            # many disconnects.
            if self._work_to_requeue:
                yield self._work_to_requeue.pop()
            else:
                try:
                    _ = next(iterator)
                    work = {'number': _}
                    yield Job(work)
                except StopIteration:
                    # Fixme:
                    return

    ##############################################

    def run(self):
        # This algo attemps to continuously fill the queue of each worker to its maximum.
        # It routes a job to the worker with lowest queue.

        # Another idea is to send a job to each worker
        # then send a new job to the worker that replied
        # but in this case the worker is idle until it receives a new job

        # Notice for asyncio, we can split this algo in several concurent tasks.

        # Fixme: it exits before to receive all results
        #  so N job must be large enought to demonstrate how it works !!!
        # must implement a counter and a final loop to receive them.
        for job in self.work_iterator():
            next_worker_id = None
            while next_worker_id is None:
                # First check if there are any worker messages to process.
                #   We do this while checking for the next available worker
                #   so that if it takes a while to find one we're still processing incoming messages.
                # Read all pending messages
                #   any message: while block is not executed
                #   one message: while block is executed once but fail the next time
                #   more than one message: while block is executed until message are queued
                while self.socket.poll(0):
                    # Note that we're using recv_multipart() here,
                    #   this is a special method on the ROUTER socket
                    #   that includes the id of the sender.
                    #   It doesn't handle the json decoding automatically
                    #   though so we have to do that ourselves.
                    worker_id, message = self.socket.recv_multipart()
                    worker_id = worker_id.decode('ascii')
                    message = json.loads(message.decode('utf8'))
                    print(f"Controller: received from {worker_id}: {message}")
                    self._handle_worker_message(worker_id, message)
                # If there are no available workers
                #   (they all have 50 or more jobs already)
                # sleep for half a second.
                # Fixme: we could wait for a message
                #   We must receive a job done to get a worker.
                next_worker_id = self._get_next_worker_id()
                if next_worker_id is None:
                    time.sleep(0.5)
            # We've got a Job and an available worker_id, all we need to do is send it.
            #   Note that we're now using send_multipart(),
            #   the counterpart to recv_multipart(),
            #   to tell the ROUTER where our message goes.
            print(f"Controller: sending job {job.id} to worker {next_worker_id}")
            self.workers[next_worker_id][job.id] = job
            data = (job.id, job.work)
            json_data = json.dumps(data).encode('utf8')
            msg = [
                next_worker_id.encode('ascii'),
                json_data,
            ]
            self.socket.send_multipart(msg)
            if self.stop_event.is_set():
                break
        self.stop_event.set()
        #! self.socket.close()
        print("Controller done")

    ##############################################

    def _get_next_worker_id(self):
        """Return the id of the next worker available to process work. Note
        that this will return None if no clients are available.
        """
        # It isn't strictly necessary since we're limiting the amount of work
        # we assign, but just to demonstrate that we could have any
        # algorithm here that we wanted we'll find the worker with the least
        # work and try that.
        if self.workers:
            sorted_workers = sorted(self.workers.items(), key=lambda _: len(_[1]))
            _= {worker: len(jobs) for worker, jobs in sorted_workers}
            print(f"Controller:   workers = {_}")
            worker_id, work = sorted_workers[0]
            if len(work) < self.max_jobs_per_worker:
                return worker_id
        # No worker is available. Our caller will have to handle this.
        return None

    ##############################################

    def _handle_worker_message(self, worker_id, message):
        """Handle a message from the worker identified by worker_id.

        {'message': 'connect'}
        {'message': 'disconnect'}
        {'message': 'job_done', 'job_id': 'xxx', 'result': 'yyy'}
        """
        if message['message'] == 'connect':
            assert worker_id not in self.workers
            self.workers[worker_id] = {}
            print(f"Controller: worker {worker_id} connected")
        elif message['message'] == 'disconnect':
            # Remove the worker so no more work gets added, and put
            # any remaining work into _work_to_requeue
            remaining_work = self.workers.pop(worker_id)
            self._work_to_requeue.extend(remaining_work.values())
            print(f"Controller: worker {worker_id} disconnect, {len(remaining_work)} jobs requeued")
        elif message['message'] == 'job_done':
            result = message['result']
            job_id = message['job_id']
            print(f"Controller: worker {worker_id} job {job_id} done")
            job = self.workers[worker_id].pop(job_id)
            self._process_results(worker_id, job, result)
        else:
            raise Exception(f"unknown message: {message['message']}")

    ##############################################

    def _process_results(self, worker_id, job, result):
        print(f"Controller: {worker_id}: finished {job.id}, result: {result}")

####################################################################################################

class Worker:
    """Accept work in the form of {'number': xxx}, square the number
    and send it back to the controller in the form {'result': xxx,
    'worker_id': yyy}. Our "work" in this case is just squaring the
    contents of 'number'.  """

    ##############################################

    def __init__(self, stop_event, id_):
        self.stop_event = stop_event
        self.id = id_
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        # We don't need to store the id anymore, the socket will handle it all for us.
        # identity = uuid.uuid4().hex[:3].encode('ascii')
        identity = str(self.id).encode('ascii')
        self.socket.identity = identity
        self.socket.connect(f'tcp://127.0.0.1:{Controller.CONTROL_PORT}')   # -> Router

    ##############################################

    def run(self):
        try:
            # Send a connect message
            print(f"Worker {self.id}: send connect")
            self.socket.send_json({'message': 'connect'})
            # Poll the socket for incoming messages. This will wait up to
            # 0.1 seconds before returning False. The other way to do this
            # is is to use zmq.NOBLOCK when reading from the socket,
            # catching zmq.AGAIN and sleeping for 0.1.
            while not self.stop_event.is_set():
                if self.socket.poll(100):
                    # Note that we can still use send_json()/recv_json() here,
                    # the DEALER socket ensures we don't have to deal with
                    # client ids at all.
                    job_id, work = self.socket.recv_json()
                    print(f"Worker {self.id}: received job {job_id}: {work}")
                    result = self._do_work(work)
                    msg = {
                        'message': 'job_done',
                        'result': result,
                        'job_id': job_id,
                    }
                    print(f"Worker {self.id}: job {job_id} done: {msg}")
                    self.socket.send_json(msg)
        except KeyboardInterrupt:
            pass
        finally:
            self._disconnect()
        print(f"Worker {self.id}: done")
        #! self.socket.close()

    ##############################################

    def _disconnect(self):
        """Send the Controller a disconnect message and end the run loop.
        """
        self.stop_event.set()
        print(f"Worker {self.id}: send disconnect")
        self.socket.send_json({'message': 'disconnect'})

    ##############################################

    def _do_work(self, work):
        result = work['number'] ** 2
        time.sleep(random.randint(1, 10))
        return result

####################################################################################################

def run_worker(event, id_):
    logging.basicConfig(level=logging.INFO)
    worker = Worker(event, id_)
    worker.run()

####################################################################################################

def run_controller(event):
    logging.basicConfig(level=logging.INFO)
    Controller(event).run()

####################################################################################################

def run():
    stop_event = Event()
    processes = []
    processes.append(Process(target=run_controller, args=(stop_event,)))
    # Start a few worker processes
    for i in range(10):
        processes.append(Process(target=run_worker, args=(stop_event, i)))
    # To test out our disconnect messaging we'll also start one more worker
    # process with a different event that we'll stop shortly after starting.
    # another_stop_event = Event()
    # processes.append(Process(target=run_worker, args=(another_stop_event, i+1)))
    for p in processes:
        p.start()
    # try:
    #     time.sleep(5)
    #     another_stop_event.set()
    #     # The controller will set the stop event when it's finished, just idle until then
    #     while not stop_event.is_set():
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     stop_event.set()
    #     another_stop_event.set()
    while not stop_event.is_set():
        time.sleep(1)
    time.sleep(10)
    print('waiting for processes to die...')
    # Fixme: hang ...
    for p in processes:
        print(f"join process {p.name}")
        p.join()
        print(f"process {p.name} done")
    print("all done")

####################################################################################################

if __name__ == '__main__':
    run()
