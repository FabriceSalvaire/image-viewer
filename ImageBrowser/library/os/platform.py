####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to query the platform for features.

"""

# Fixme: Look alternative Python package
# Fixme: rework...
# Fixme: move QtPlatform ???
# Fixme: lazy import OpenGL -> Qt ???

####################################################################################################

__ALL__ = ['Platform', 'QtPlatform']

####################################################################################################

from enum import IntEnum, auto
import os
import platform
import sys

####################################################################################################

class PlatformType(IntEnum):
    Linux = auto()
    Windows = auto()
    OSX = auto()

####################################################################################################

class Platform:

    """Class to store platform properties"""

    ##############################################

    def __init__(self):
        self.python_version = platform.python_version()

        self.os = self._get_os()
        self.node = platform.node()
        # deprecated in 3.8 see distro package
        # self.distribution = ' '.join(platform.dist())
        self.machine = platform.machine()
        self.architecture = platform.architecture()[0]

        # CPU
        self.cpu = self._get_cpu()
        self.number_of_cores = self._get_number_of_cores()
        self.cpu_khz = self._get_cpu_khz()
        self.cpu_mhz = int(self._get_cpu_khz()/float(1000)) # rint

        # RAM
        self.memory_size_kb = self._get_memory_size_kb()
        self.memory_size_mb = int(self.memory_size_kb/float(1024)) # rint

    ##############################################

    def _get_os(self):
        if os.name in ('nt',):
            return PlatformType.Windows
        elif sys.platform in ('linux',):
            return PlatformType.Linux
        # Fixme:
        # elif sys.platform in 'osx':
        #     return PlatformType.OSX
        else:
            raise RuntimeError('unknown platform: {} / {}'.format(os.name, sys.platform))

    ##############################################

    def _get_cpu(self):
        if self.os == PlatformType.Linux:
            with open('/proc/cpuinfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'model name' in line:
                        s = line.split(':')[1]
                        return s.strip().rstrip()
        elif self.os == PlatformType.Windows:
            raise NotImplementedError

    ##############################################

    def _get_number_of_cores(self):
        if self.os == PlatformType.Linux:
            number_of_cores = 0
            with open('/proc/cpuinfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'processor' in line:
                        number_of_cores += 1
            return number_of_cores
        elif self.os == PlatformType.Windows:
            return int(os.getenv('NUMBER_OF_PROCESSORS'))

    ##############################################

    def _get_cpu_khz(self):
        if self.os == PlatformType.Linux:
            with open('/proc/cpuinfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'cpu MHz' in line:
                        s = line.split(':')[1]
                        return int(1000 * float(s))
        if self.os == PlatformType.Windows:
            raise NotImplementedError

    ##############################################

    def _get_memory_size_kb(self):
        if self.os == PlatformType.Linux:
            with open('/proc/meminfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'MemTotal' in line:
                        s = line.split(':')[1][:-3]
                        return int(s)

        if self.os == PlatformType.Windows:
            raise NotImplementedError

    ##############################################

    def __str__(self):
        str_template = '''
Platform {0.node}
  Hardware:
    Machine: {0.machine}
    Architecture: {0.architecture}
    CPU: {0.cpu}
      Number of Cores: {0.number_of_cores}
      CPU Frequence: {0.cpu_mhz} MHz
    Memory: {0.memory_size_mb} MB

  Python: {0.python_version}
'''
        return str_template.format(self)

####################################################################################################

class QtPlatform(Platform):

    """Class to store Qt platform properties"""

    ##############################################

    def __init__(self):
        super().__init__()

        # Fixme: QT_VERSION_STR ...
        from qtpy import QtCore, QtWidgets
 
        # AttributeError: module 'qtpy.QtCore' has no attribute 'QT_VERSION'
        self.qt_version = '...'   # QtCore.QT_VERSION _STR
        self.pyqt_version = '...'   # QtCore.PYQT_VERSION_STR

        # Screen

        # try:
        #     application = QtWidgets.QApplication.instance()
        #     self.desktop = application.desktop()
        #     self.number_of_screens = self.desktop.screenCount()
        # except:
        #     self.desktop = None
        #     self.number_of_screens = 0
        # for i in range(self.number_of_screens):
        #     self.screens.append(Screen(self, i))
        try:
            application = QtWidgets.QApplication.instance()
            self.screens = [Screen(screen) for screen in application.screens()]
        except:
            self.screens = []

        # OpenGL
        self.gl_renderer = None
        self.gl_version = None
        self.gl_vendor = None
        self.gl_extensions = None

    ##############################################

    @property
    def number_of_screens(self):
        return len(self.screens)

    ##############################################

    def query_opengl(self):
        # Fixme: require OpenGL
        import OpenGL.GL as GL
        self.gl_renderer = GL.glGetString(GL.GL_RENDERER)
        self.gl_version = GL.glGetString(GL.GL_VERSION)
        self.gl_vendor = GL.glGetString(GL.GL_VENDOR)
        self.gl_extensions = GL.glGetString(GL.GL_EXTENSIONS)

    ##############################################

    def __str__(self):
#         str_template = '''
#    OpenGL
#      Render: {0.gl_renderer}
#      Version: {0.gl_version}
#      Vendor: {0.gl_vendor}
#    Number of Screens: {0.number_of_screens}
# '''
#        message += str_template.format(self)

        message = super().__str__()

        for screen in self.screens:
            message += str(screen)

        str_template = '''
  Software Versions:
    Qt: {0.qt_version}
    PyQt: {0.pyqt_version}
'''
        message += str_template.format(self)

        return message

####################################################################################################

class Screen:

    """Class to store screen properties"""

    ##############################################

    # def __init__(self, platform_obj, screen_id):
    def __init__(self, qt_screen):
        self.name = qt_screen.name()
        size = qt_screen.size()
        self.screen_width, self.screen_height = size.width(), size.height()
        self.dpi = qt_screen.physicalDotsPerInch()
        self.dpi_x = qt_screen.physicalDotsPerInchX()
        self.dpi_y = qt_screen.physicalDotsPerInchY()

        # self.screen_id = screen_id

        # qt_screen_geometry = platform_obj.desktop.screenGeometry(screen_id)
        # self.screen_width, self.screen_height = qt_screen_geometry.width(), qt_screen_geometry.height()

        # widget = platform_obj.desktop.screen(screen_id)
        # self.dpi = widget.physicalDpiX(), widget.physicalDpiY()

        # qt_available_geometry = self.desktop.availableGeometry(screen_id)

    ##############################################

    def __str__(self):
        str_template = """
  Screen {0.name}
    geometry   {0.screen_width}x{0.screen_height} px
    resolution {0.dpi:.2f} dpi
"""
        return str_template.format(self)
