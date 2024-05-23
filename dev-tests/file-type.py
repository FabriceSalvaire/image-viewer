from pathlib import Path
from ImageBrowser.library.path.file import File

IMAGE_EXAMPLES = Path('../image-examples')

# [Magic number (programming) - Wikipedia](https://en.wikipedia.org/wiki/Magic_number_%28programming%29)
# hexdump -C

_ = File(IMAGE_EXAMPLES, '20240426_142347.png')
print(_)
# [PNG - Wikipedia](https://en.wikipedia.org/wiki/PNG)
# A PNG file starts with an 8-byte signature
#   89
#   50 4E 47 = PNG
#   0D 0A = CRLF
#   1A
#   0A
print(_.first_bytes(8))
# b'\x89PNG\r\n\x1a\n'

_ = File(IMAGE_EXAMPLES, '20240426_142347.no_exif.jpg')
print(_)
# [JPEG File Interchange Format - Wikipedia](https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format)
# JPEG image files begin with FF D8 and end with FF D9.
# JPEG/JFIF files contain the null terminated string "JFIF" (4A 46 49 46 00).
# JPEG/Exif files contain the null terminated string "Exif" (45 78 69 66 00),
#   followed by more metadata about the file.
print(_.first_bytes(2))
# b'\xff\xd8'
print(_.first_bytes(16))
# b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x02\x00;'
print(_.last_bytes(2))
# b'\xff\xd9'

_ = File(IMAGE_EXAMPLES, '20240426_142347.jpg')
print(_)
# [Exif file format](https://www.media.mit.edu/pia/Research/deepview/exif.html)
print(_.first_bytes(2))
print(_.first_bytes(16))
# b'\xff\xd8\xff\xe1BoExif\x00\x00II*\x00'
print(_.last_bytes(2))
# not FF D9 but b'FT'

_ = File(IMAGE_EXAMPLES, '20240426_142347.webp')
print(_)
# [WebP - Wikipedia](https://en.wikipedia.org/wiki/WebP)
print(_.first_bytes(4))
# b'RIFF'
print(_.first_bytes(32))
# b'RIFFn?\x16\x00WEBPVP8X\n\x00\x00\x00\x08\x00\x00\x00\xef\x0f\x00[\x07\x00VP'

_ = File(IMAGE_EXAMPLES, '20240426_142347.tiff')
print(_)
# [TIFF - Wikipedia](https://en.wikipedia.org/wiki/TIFF)
# TIFF files begin with either "II" or "MM" followed by 42 as a
# two-byte integer in little or big endian byte ordering. "II" is for
# Intel, which uses little endian byte ordering, so the magic number
# is 49 49 2A 00. "MM" is for Motorola, which uses big endian byte
# ordering, so the magic number is 4D 4D 00 2A.
print(_.first_bytes(4))
# b'II*\x00'

_ = File(IMAGE_EXAMPLES, '20240426_142347.gif')
print(_)
# [Graphics Interchange Format — Wikipédia](https://fr.wikipedia.org/wiki/Graphics_Interchange_Format)
# GIF image files have the ASCII code for "GIF89a" (47 49 46 38 39 61) or "GIF87a" (47 49 46 38 37 61)
print(_.first_bytes(6))
# b'GIF89a'
