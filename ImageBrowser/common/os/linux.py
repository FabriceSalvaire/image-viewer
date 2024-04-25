####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Linux tools

see also https://psutil.readthedocs.io/en/latest/#psutil.disk_partitions

* /usr/bin/mount
* lsblk
* blkid

* /proc/partitions
* /proc/mounts -> /proc/self/mounts   see PROC(5) use fstab format
* /proc/self/mountinfo
* /proc/self/mountstats
* /proc/partitions
* /dev/disk/by-uuid

"""

####################################################################################################

__ALL__ = ['MountPoints', 'Device']

####################################################################################################

# from os import PathLike
from pathlib import Path
from pprint import pprint
from typing import Iterator, Union
import json
import logging
import subprocess

from ImageBrowser.common.singleton import SingletonMetaClass

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathStr = Union[Path, str]

####################################################################################################

class Device():

    ##############################################

    def __init__(
        self,
        name: str,   # device name e.g. /dev/sda1
        uuid: str,
        label: str,
        major: int,
        minor: int,
        fs_type: str,
        mount_points: list[str],
    ) -> None:
        self._name = str(name)
        self._uuid = str(uuid)
        self._label = str(label) if label is not None else None
        self._major = int(self._major)
        self._minor = int(self._minor)
        self._fs_type = str(fs_type)
        self._mount_points = [str(_) for _ in mount_points]

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def label(self) -> str:
        return self._label

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def major_minor(self) -> str:
        return f'{self._major}:{self._minor}'

    @property
    def fs_type(self) -> str:
        return self._fs_type

    @property
    def mount_points(self) -> Iterator[str]:
        return iter(self._mount_points)

    def __str__(self) -> str:
        return f"Device '{self._name}'  {self.major_minor}  uuid={self._uuid}  label='{self._label}'  fstype={self._fs_type}  mounts={self._mount_points}"
        # f"{self._mount_point} ->"

####################################################################################################

class MountPoints(metaclass=SingletonMetaClass):

    _logger = _module_logger.getChild('MountPoints')

    # MOUNT_COMMAND = ('/usr/bin/mount')
    LSBLK = '/usr/bin/lsblk'

    # PROC_MOUNTS = '/proc/self/mounts'

    FILE_SYSTEM_TYPES = (
        'btrfs',
        'ext2',
        'ext3',
        'ext4',
        'ntfs',
        'vfat',
        'xfs',
    )

    SPECIAL_TYPES = (
        # 'fuseblk',
        'LVM2_member',
        'autofs',
        'binfmt_misc',
        'bpf',
        'cgroup2',
        'configfs',
        'debugfs',
        'devpts',
        'devtmpfs',
        'efivarfs',
        'fuse.gvfsd-fuse',
        'fuse.portal',
        'fusectl',
        'hugetlbfs',
        'mqueue',
        'proc',
        'pstore',
        'rpc_pipefs',
        'securityfs',
        'selinuxfs',
        'squashfs',
        'swap',
        'sysfs',
        'tmpfs',
        'tracefs',
    )

    ##############################################

    def __init__(self) -> None:
        self._devices = list(self._get_devices())
        self._map = {
            m: d
            for d in self._devices
            for m in d.mount_points
        }

    ##############################################

    def _get_devices(self) -> Iterator[Device]:
        self._logger.info(f"Scan mount points...")
        command = (self.LSBLK, '--json', '--fs')
        process = subprocess.run(command, capture_output=True)
        data = process.stdout.decode('utf8')
        data = json.loads(data)

        def process_node(node):
            # print('-'*50)
            pprint(node)
            fs_type = node['fstype']
            mount_points = node['mountpoints']
            name = node['name']
            label = node['label']
            uuid = node['uuid']
            if fs_type is not None and fs_type not in self.FILE_SYSTEM_TYPES and fs_type not in self.SPECIAL_TYPES:
                self._logger.warning(f"Unknown filesytem type {fs_type}")
            if mount_points != [None] and fs_type in self.FILE_SYSTEM_TYPES:
                # if 'maj:min' in node:
                #     major, minor = [int(_) for _ in node['maj:min'].split(':')]
                # else:
                #     raise NameError(f"no major:minor for {name}")
                major, minor = None
                yield Device(name, uuid, label, major, minor, fs_type, mount_points)
            if 'children' in node:
                for _ in node['children']:
                    yield from process_node(_)

        for node in data['blockdevices']:
            yield from process_node(node)

        # process = subprocess.run(self.MOUNT_COMMAND, capture_output=True)
        # for line in process.stdout.decode('utf-8').splitlines():
        #     device, _, mount_point, _, type_, mount_options = line.split(' ')
        #     if type_ not in self.SYSTEM_TYPES:

        # with open(self.PROC_MOUNTS, encoding='utf8') as fh:
        #     for line in fh:
        #         device, mount_point, type_, mount_options, _, _ = line.split(' ')
        #         if type_ not in self.SYSTEM_TYPES:

    ##############################################

    def __len__(self) -> int:
        return len(self._devices)

    def __iter__(self) -> Iterator[Device]:
        return iter(self._devices)

    def __getitem__(self, mount_point: str) -> Device:
        return self._map[mount_point]

    ##############################################

    # def is_mount(self, path: Union[AnyStr, PathLike[AnyStr]]) -> bool:
    def is_mount(self, path: PathStr) -> bool:
        return str(path) in self._map

    ##############################################

    def device_for(self, path: PathStr) -> Device:
        path = Path(path)
        stat = path.stat(follow_symlinks=True)
        inode = stat.st_ino
        device_id = stat.st_dev
        major = os.major(device_id)
        minor = os.minor(device_id)
        print(f"{path} {device_id} {inode}")
