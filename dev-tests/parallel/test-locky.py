####################################################################################################

import os
import multiprocessing as mp
from time import sleep, time
from pprint import pprint

import loky
from loky import get_reusable_executor, set_loky_pickler, wrap_non_picklable_objects

####################################################################################################

# Store the initialization status in a global variable of a module.
loky._INITIALIZER_STATUS = "uninitialized"

@wrap_non_picklable_objects
def initializer(x):
    print(f"[{mp.current_process().name}] init")
    loky._INITIALIZER_STATUS = x

@wrap_non_picklable_objects
def return_initializer_status(delay=0):
    sleep(delay)
    return getattr(loky, '_INITIALIZER_STATUS', 'uninitialized')

####################################################################################################

@wrap_non_picklable_objects
def async_func(k, *args):
    pid = os.getpid()
    print(f"Hello from PID {pid} with arg {k}")
    # sleep(.01)
    sleep(1)
    return pid

####################################################################################################

set_loky_pickler('pickle')

large_list = list(range(1_000_000))

# Create an executor with 4 worker processes,
# that will automatically shutdown after idling for 2s
executor = get_reusable_executor(
    max_workers=2,
    initializer=initializer,
    initargs=('initialized',),
    context='loky',   # ???
    timeout=1000,
)

assert loky._INITIALIZER_STATUS == 'uninitialized'
executor.submit(return_initializer_status).result()
assert executor.submit(return_initializer_status).result() == 'initialized'

# With reuse=True, the executor use the same initializer
executor = get_reusable_executor(max_workers=4, reuse=True)
for x in executor.map(return_initializer_status, [0.5] * 4):
    assert x == 'initialized'

# With reuse='auto', the initializer is not used anymore as a new executor is created.
executor = get_reusable_executor(max_workers=4)
for x in executor.map(return_initializer_status, [0.1] * 4):
    assert x == 'uninitialized'

t_start = time()
res = executor.submit(async_func, 1, large_list)
print("Got results:", res.result())
print(f"time: {time() - t_start:.3f}s")

results = executor.map(async_func, range(10))
# results is a generator
for _ in results:
    pprint(_)
# async_func return the PID
# n_workers = len(set(results))
# print("Number of used processes:", n_workers)
# assert n_workers == 4

