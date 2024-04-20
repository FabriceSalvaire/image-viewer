# Qt/QML Image

Qt supports these image formats (some require a 3rd party codec):
- GIF
- JP2 (codec not bundled)
- JPG
- MNG (codec not bundled)
- PNG
- SVG
- TIFF (codec bundled)
- WBMP (codec **not** bundled)
- WEBP (codec bundled)
and also
- BMP
- PBM
- PGM
- PPM
- TGA (read)
- XBM
- XPM

- QML can load asynchronously local or remote images (network transparency for HTTP)
  QML can also load asynchronously image from an image provider as a `QPixmaps`
  `Image { source: "image://myimageprovider/image.png" }`
  It means `source` is just a string for theses three cases.
  See `asynchronous : bool`
- QML can cache image, see `cache : bool`
- QML handles an image as a GPU texture
- QML can apply transformation metadata such as EXIF orientation, see `autoTransform : bool`

**References**
- [Resource Loading and Network Transparency](https://doc.qt.io/qt-6/qtqml-documents-networktransparency.html)
- [Qt Image Formats](https://doc.qt.io/qt-6/qtimageformats-index.html)
- [QImageReader Class](https://doc.qt.io/qt-6/qimagereader.html)
- [QImageReader Class:_Supported Image Formats](https://doc.qt.io/qt-6/qimagereader.html#supportedImageFormats)
- [QQuickImageProvider Class](https://doc.qt.io/qt-6/qquickimageprovider.html)
- [Image QML Type](https://doc.qt.io/qt-6/qml-qtquick-image.html)
- [QImageIOPlugin Class](https://doc.qt.io/qt-6/qimageioplugin.html)

# Uncommon Image Format

- implement a `QImageIOPlugin`
- implement a Python loader an a `QQuickImageProvider`

# Python Image Library

- [Pillow Image file formats](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)

# Metadata

- [QMediaMetaData Class | Qt Multimedia 6.7.1](https://doc.qt.io/qt-6/qmediametadata.html)

## PNG

- [Pillow PngImagePlugin.PngInfo](https://pillow.readthedocs.io/en/stable/PIL.html#pngimageplugin-pnginfo-class)

## Exif

- [Pillow ExifTags Module](https://pillow.readthedocs.io/en/stable/reference/ExifTags.html)
- [exif — Python module](https://exif.readthedocs.io/en/latest/usage.html)
- [philvl/ZExifTool: Qt5 and Qt6 interface for ExifTool by Phil Harvey](https://github.com/philvl/ZExifTool)

**Orientation**
- 1 = Horizontal (normal)
- 2 = Mirror horizontal
- 3 = Rotate 180
- 4 = Mirror vertical
- 5 = Mirror horizontal and rotate 270 CW
- 6 = Rotate 90 CW
- 7 = Mirror horizontal and rotate 90 CW
- 8 = Rotate 270 CW

See [Exif Orientation](http://sylvana.net/jpegcrop/exif_orientation.html)

## Tiff

- [Pillow TiffTags Module](https://pillow.readthedocs.io/en/stable/reference/TiffTags.html)

# Interesting Libraries

# Super-resolution

- [super-resolution GitHub Topics GitHub](https://github.com/topics/super-resolution)

- [alexjc/neural-enhance: Super Resolution for images using deep learning](https://github.com/alexjc/neural-enhance)
  archived 8 years ago
- [Deep Neural Network-based Enhancement for Image and Video Streaming Systems: A Survey and Future Directions](https://arxiv.org/pdf/2106.03727.pdf)
- [idealo/image-super-resolution: Super-scale your images and run experiments with Residual Dense and Adversarial Networks](https://github.com/idealo/image-super-resolution)
  3 years ago
- [TencentARC/GFPGAN: GFPGAN aims at developing Practical Algorithms for Real-world Face Restoration](https://github.com/TencentARC/GFPGAN)
- [xinntao/Real-ESRGAN: Real-ESRGAN aims at developing Practical Algorithms for General Image/Video Restoration](https://github.com/xinntao/Real-ESRGAN)
