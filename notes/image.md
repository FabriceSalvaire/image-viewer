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
- We can use the network transparency to connect to a local process
  QML supports HTTP
  Does Qt have a plugin mechanism for an alternative scheme like ZMQ ???
  See also [REST API | The Qt 6 Book](https://www.qt.io/product/qt6/qml-book/ch13-networking-rest-api)
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
