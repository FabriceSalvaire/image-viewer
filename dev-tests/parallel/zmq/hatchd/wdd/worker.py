####################################################################################################

import random
import time
import uuid

import zmq

####################################################################################################

class Worker:
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        # We don't need to store the id anymore, the socket will handle it
        # all for us.
        self.socket.identity = uuid.uuid4().hex[:4].encode('utf8')
        self.socket.connect('tcp://127.0.0.1:5755')

    def run(self):
        try:
            # Send a connect message
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
                    self.socket.send_json(
                        {'message': 'job_done',
                         'result': self._do_work(work),
                         'job_id': job_id})
        except KeyboardInterrupt:
            pass
        finally:
            self._disconnect()

    def _disconnect(self):
        """Send the Controller a disconnect message and end the run loop.
        """
        self.stop_event.set()
        self.socket.send_json({'message': 'disconnect'})

    def _do_work(self, work):
        result = work['number'] ** 2
        time.sleep(random.randint(1, 10))
        return result
