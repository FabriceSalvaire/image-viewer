####################################################################################################

# https://docs.python.org/3/library/concurrent.futures.html

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import math
import multiprocessing

####################################################################################################

import sysconfig
import sys
Py_GIL_DISABLED = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
is_gil_enabled = sys._is_gil_enabled()
print(f"GIL Disabled: {Py_GIL_DISABLED} {not(is_gil_enabled)}")

####################################################################################################

def job(thread_id, *args, **kwargs):
    print(f"Run thread #{thread_id}...")
    c = 0
    for i in range(50_000_000):
        c += math.sqrt(i)
    print(f"thread #{thread_id} done")
    return c

NUMBER_OF_THREADS = multiprocessing.cpu_count()

def main1():
    threads = []
    print(f"Start {NUMBER_OF_THREADS} threads")
    for i in range(NUMBER_OF_THREADS):
        _ = Thread(target=job, args=[i])
        print(f"Start thread #{i}")
        _.start()
        threads.append(_)

    for i in range(NUMBER_OF_THREADS):
        print(f"Join thread #{i}")
        # blocking
        threads[i].join()

def main2():
    # executor = ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS)
    # threads = []
    # print(f"Start {NUMBER_OF_THREADS} threads")
    # for i in range(NUMBER_OF_THREADS):
    #     print(f"Start thread #{i}")
    #     _ = executor.submit(job, i)
    #     threads.append(_)
    with ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
        for i in range(NUMBER_OF_THREADS):
            print(f"Start thread #{i}")
            _ = executor.submit(job, i)

main2()
print(f"Exit")
