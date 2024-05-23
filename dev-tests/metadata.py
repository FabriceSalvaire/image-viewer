####################################################################################################

from pprint import pprint

from ImageBrowser.library.timer import TimerNs, Timer

import numpy as np

####################################################################################################

image_path = '20240426_142347.jpg'

timer_ns = Timer('', start=False)
timer = TimerNs('', start=False)

####################################################################################################

def run(func, n: int) -> None:
    for i in range(n):
        func()

def rule(title):
    print()
    print('\u2500'*100)
    print()
    print(title)

####################################################################################################

rule('Pillow')

import PIL.Image
import PIL.ExifTags

timer.start()
img = PIL.Image.open(image_path)
timer.stop()
print(f"time: {timer.delta_ms} ms")   # 50 ms
timer.start()
print(f"size: {img.size}")
data = np.asarray(img)
timer.stop()
print(f"time: {timer.delta_ms} ms")   # 95 ms

if False:
    exif_data = img._getexif()
    # pprint(exif_data)
    exif_data_str = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in exif_data.items()
        if k in PIL.ExifTags.TAGS
    }
    pprint(exif_data_str)

####################################################################################################

rule('Qt')

from PySide6.QtGui import QImage

timer.start()
img = QImage(image_path)
timer.stop()
print(f"time: {timer.delta_ms} ms")   # 100 ms
print(f"size: {img.size()}")

print(f"format: {img.format()}")   # Format.Format_RGB32
# img = img.convertToFormat(QImage.Format.Format_RGB32)
timer.start()
width = img.width()
height = img.height()
ptr = img.constBits()
data = np.array(ptr).reshape(height, width, 4)
timer.stop()
print(f"time: {timer.delta_ms} ms")   # 9 ms

####################################################################################################

rule('OpenCV')

import cv2 as cv

timer.start()
img = cv.imread(image_path)
timer.stop()
print(f"time: {timer.delta_ms} ms")   # 135 ms
print(type(img))   # <class 'numpy.ndarray'>
print(f"size: {img.shape}")
