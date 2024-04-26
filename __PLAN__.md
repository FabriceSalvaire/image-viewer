# TODO

- [X] remove book...
- [X] test
  [X] check new thumbnail code !
- [X] look at common code with datasheet
  [X] login ...
- [X] port to PySide 6.7
  check datasheet
  look at async...
- test
- spdx
- improve thumbnail generator

---

# Bugs

- shorcut null
- [X] prev next hang

---

# References

- [Image viewer - Wikipedia](https://en.wikipedia.org/wiki/Image_viewer)
- [Comparison of image viewers - Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_image_viewers)
- [Gwenview Alternatives: 25+ Image Viewers & Image Editors | AlternativeTo](https://alternativeto.net/software/gwenview/)
- [Free Photo Editing Apps - A Comparison and some Personal Experiences - 35mmc](https://www.35mmc.com/26/07/2023/free-photo-editing-apps-a-comparison-and-some-personal-experiences)


- [Gwenview](https://apps.kde.org/fr/gwenview)
- [Geeqie](https://www.geeqie.org)
  has more features than Gwenview
  started 1998 as GqView
  C/GTK
  [geeqie.git/tree](http://geeqie.org/cgi-bin/gitweb.cgi?p=geeqie.git;a=tree)

**RAW**
- Lightroom Classic
- [darktable](https://www.darktable.org)
- [RawTherapee](https://www.rawtherapee.com)
- [digiKam](https://www.digikam.org)
  crashes...
  collection features (face, similarity)
  gps map
- [UFRaw](https://ufraw.sourceforge.net)

- Eye of GNOME
- gThumb
- KPhotoAlbum
- Shotwell
- F-Spot
- [nomacs](https://nomacs.org)
  C++/Qt

**Non libre**
- IrfanView
- XnView MP
- ImageGlass

# Features

# UI

- fullscreen mode
- recent page
- collection / directory page
- image page
  Gwenview: show selected images
- collapsable sidebar
  - directory tree
  - info
  - action

# Recents

- store recents collection

- directory
- image

# Folder Tree

# Path Navigator

- path
  -> str editable / killable
  -> > ... > ... > ...
- name is a target to drag and drop
- click on > shows a list of directories

# Collection

A collection can be
- a bunch of local or remote images
- a directory

A directory can have sub-collections (sub-directory).

- sort by
  name
  mtime
  size byte
  resolution
  note
  **reverse mode**

# Thumbnail Viewer

- size 48 -> 1024 px
- layout a centered grid
- show name below the image
- actions on imgae
  de/select +/-
  full screen
  rotate left/right
- filter
- no aka dolphin selection mode
- image drag-and-drop
- rectangular selection by intersection
  work if started in the blank area at right / bottom
- directory properties
- new directory

# Image Information

- name
- path
- size resolution
- mtime
- Exif
- note star
- labels
- description

# Image Actions

# Other Gwnenview features

- print
- copy
- delete
- diaporama
- share
- colorometry sRGB

# ...

-[libPGF – Progressive Graphics File](https://libpgf.or/)
 [Progressive Graphics File - Wikipedia](https://en.wikipedia.org/wiki/Progressive_Graphics_File)
- [Exiv2 - Image metadata library and tools](https://exiv2.org)
- [gPhoto](http://www.gphoto.org)
- [Lensfun](https://lensfun.github.io)
- [LibRaw](https://www.libraw.org)

---

# Library

- an image is defined by its byte content
- we can compute a hash for that
  must be unique for a large collection
- an image can be
  overwritten
  renamed in the directory (file name)
  moved inside the device or outside
- the path of an image can be altered
- image inode is unchanged when
  overwritten
  renamed
  moved inside
- the device of an image can be
  mounted elsewhere (mount point)
  renamed (label)
- device uuid should be a constant
- thus we can track a image by the pair (device uuid, inode)
  else we can use a hash -> (device uuid, inode) / hash
  else we must add an uuid in the image metadata
- path alias
  - a path can contains a symbolic link
  - a directory entry can be a hard link

NTFS
- inode is file ID
- [Does Windows have Inode Numbers like Linux? - Stack Overflow](https://stackoverflow.com/questions/7162164/does-windows-have-inode-numbers-like-linux)
- [Device Unique Identifiers (DUIDs) for Storage Devices - Windows drivers | Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/drivers/storage/device-unique-identifiers--duids--for-storage-devices)
