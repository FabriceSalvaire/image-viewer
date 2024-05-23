from urllib.parse import urlparse

_ = urlparse("scheme://netloc/path;parameters?query#fragment")
print(_)
print(_.scheme)
print(_.netloc)
print(_.path)
print(_.query)

_ = urlparse("http://docs.python.org:80/3/library/urllib.parse.html?highlight=params#url-parsing")
print(_)

_ = urlparse("file:file.txt")
print(_)

_ = urlparse("file:/home/foo/file.txt")
print(_)

_ = urlparse(r"file:C:\foo\file.txt")
print(_)

from pathlib import Path, PureWindowsPath
# _ = Path('c:/Program Files/PSF')
_ = PureWindowsPath('c:/Program Files/PSF')
print(_.parts)
print(_.drive)
