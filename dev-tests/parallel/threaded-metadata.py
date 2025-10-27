# Don't see any speed improvement
#   45s for 100k images
#   100% CPU load ???
# Don't see any crash

# <frozen importlib._bootstrap>:488: RuntimeWarning:
# The global interpreter lock (GIL) has been enabled to load module
# 'PIL._imaging', which has not declared that it can run safely without the GIL.
# To override this behavior and keep the GIL disabled (at your own risk),
# run with PYTHON_GIL=0 or -Xgil=0.

####################################################################################################

# https://docs.python.org/3/library/concurrent.futures.html

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
# from pprint import pprint
# from threading import Thread
import argparse
import multiprocessing

####################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument(
    'path',
    metavar='PATH',
    help='foo help',
)
args = parser.parse_args()
src = Path(args.path)

NUMBER_OF_THREADS = multiprocessing.cpu_count()
files = list(src.glob('**/*.jpg'))
print(f"Number of files {len(files)}")
dispatch = []
stride = len(files) // NUMBER_OF_THREADS
start = 0
for i in range(NUMBER_OF_THREADS):
    stop = start + stride
    if i == (NUMBER_OF_THREADS - 1):
        stop = len(files)
    view = [str(_) for _ in files[start:stop]]
    dispatch.append(view)
    print(f"Number of files #{i} {start}:{stop} {len(view)}")
    start = stop

####################################################################################################

import numpy # segfault...
import PIL.Image
import PIL.ExifTags

def read_exif(path):
    try:
        img = PIL.Image.open(path)
        exif_data = img._getexif()
        if exif_data:
            exif_data_str = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in exif_data.items()
                if k in PIL.ExifTags.TAGS
            }
        # pprint(exif_data_str)
    # except (FileNotFoundError, PIL.UnidentifiedImageError, IsADirectoryError):
    except Exception as e:
        print(e)

def job(thread_id, files, *args, **kwargs):
    print(f"Run thread #{thread_id}...")
    for _ in files:
        read_exif(_)
        print(f"Thread #{thread_id}: {_}")
    print(f"Thread #{thread_id} done")

####################################################################################################

with ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
    futures = []
    for i in range(NUMBER_OF_THREADS):
        print(f"Start thread #{i}")
        _ = executor.submit(job, i, list(dispatch[i]))
        futures.append(_)
    for _ in as_completed(futures):
        print(_.result())

print(f"Exit")
