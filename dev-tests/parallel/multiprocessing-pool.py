####################################################################################################

import multiprocessing
from multiprocessing import Pool

####################################################################################################

print(multiprocessing.cpu_count())

def f(x):
    _ = 0
    for i in range(1_00_000_000):
        _ += i*x
    return _

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, list(range(1, 10))))
