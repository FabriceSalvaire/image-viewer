# Generate thumbnails on disk cache

See [freedesktop.org — Thumbnails Specification](https://www.freedesktop.org/wiki/Specifications/thumbnails/)

- format is PNG (8-bit non-interlaced with full alpha transparency)
- sizes are the two power series 128 to 1024
- respect metadata affecting the interpretation of the image (Exif)
- name mangling is a MD5 hash of `file:///home/jens/photos/me.png` which gives `/home/jens/.cache/thumbnails/normal/c6ee772d9e49320e97ec29a7eb5b1697.png`
- permission are 700 and 600
- see "Concurrent Thumbnail Creation"
  Rename a temporary file to the thumbnail filename.
  Since this is an atomic operation the new thumbnail is either completely written or not.
- see "Detect Modifications"

## ImageMagick

See [ImageMagick – Command-line Options](https://imagemagick.org/script/command-line-options.php#thumbnail)

```
convert input.jpg -thumbnail 128x output.png
identify -verbose output.png
```
