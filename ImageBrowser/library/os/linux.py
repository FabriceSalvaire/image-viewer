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
import collections
import json
import logging
import os
import subprocess

from ImageBrowser.common.singleton import SingletonMetaClass

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathStr = Union[Path, str]

####################################################################################################

class LsblkInterface():

    _logger = _module_logger.getChild('LsblkInterface')

    LSBLK = '/usr/bin/lsblk'

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

    DeviceInfo = collections.namedtuple(
        'DeviceInfo',
        (
            'name',
            'uuid',
            'label',
            'major',
            'minor',
            'fs_type',
            'mount_points'
        ))

    ##############################################

    def __init__(self) -> None:
        self._logger.info(f"Scan mount points...")
        # lsblk is unable to return all the informations with one call...
        # thus we have to merge
        devices = {_.name: _ for _ in self.process(self.run())}
        self._devices = []
        for d in self.process(self.run('--fs')):
            if d.fs_type in self.FILE_SYSTEM_TYPES:
                _ = devices[d.name]
                device = d._replace(
                    major=_.major,
                    minor=_.minor,
                )
                self._devices.append(device)

    ##############################################

    @property
    def devices(self) -> Iterator[DeviceInfo]:
        return iter(self._devices)

    ##############################################

    def run(self, *args) -> dict:
        command = (self.LSBLK, '--json', *args)
        process = subprocess.run(command, capture_output=True)
        data = process.stdout.decode('utf8')
        return json.loads(data)

    ##############################################

    def process_node(self, node: dict) -> Iterator[DeviceInfo]:
        # print('-'*50)
        # pprint(node)
        name = node['name']
        mount_points = node['mountpoints']
        major = None
        minor = None
        label = None
        uuid = None
        fs_type = None
        if mount_points != [None]:
            if 'maj:min' in node:
                major, minor = [int(_) for _ in node['maj:min'].split(':')]
            else:
                label = node['label']
                uuid = node['uuid']
                fs_type = node['fstype']
                if fs_type is not None and fs_type not in self.FILE_SYSTEM_TYPES and fs_type not in self.SPECIAL_TYPES:
                    self._logger.warning(f"Unknown filesytem type {fs_type}")
            yield self.DeviceInfo(
                name=name,
                uuid=uuid,
                label=label,
                major=major,
                minor=minor,
                fs_type=fs_type,
                mount_points=mount_points,
            )
        if 'children' in node:
            for _ in node['children']:
                yield from self.process_node(_)

    ##############################################

    def process(self, data: dict) -> Iterator[DeviceInfo]:
        for node in data['blockdevices']:
            yield from self.process_node(node)

####################################################################################################

class Device():

    ##############################################

    @classmethod
    def to_major_minor_int(cls, major: int, minor: int) -> int:
        return major << 16 + minor

    ##############################################

    def __init__(
        self,
        name: str,   # device name e.g. /dev/sda1
        uuid: str,   # partition uuid
        label: str,  # partition label
        major: int,  # identifies the driver associated with the device
        minor: int,
        fs_type: str,
        mount_points: list[str],
    ) -> None:
        self._name = str(name)
        self._uuid = str(uuid)
        self._label = str(label) if label is not None else None
        self._major = int(major)
        self._minor = int(minor)
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
    def major_minor_str(self) -> str:
        return f'{self._major}:{self._minor}'

    @property
    def major_minor_int(self) -> int:
        return self.to_major_minor_int(self._major, self._minor)

    @property
    def fs_type(self) -> str:
        return self._fs_type

    @property
    def mount_points(self) -> Iterator[str]:
        return iter(self._mount_points)

    def __str__(self) -> str:
        return f"Device '{self._name}'  major:minor={self.major_minor_str}  uuid={self._uuid}  label='{self._label}'  fstype={self._fs_type}  mounts={self._mount_points}"
        # f"{self._mount_point} ->"

####################################################################################################

class MountPoints(metaclass=SingletonMetaClass):

    _logger = _module_logger.getChild('MountPoints')

    ##############################################

    def __init__(self) -> None:
        self._devices = list(self._get_devices())
        self._mount_map = {
            m: d
            for d in self._devices
            for m in d.mount_points
        }
        self._majmin_map = {
            d.major_minor_int: d
            for d in self._devices
        }

    ##############################################

    def _get_devices(self) -> Iterator[Device]:
        for _ in LsblkInterface().devices:
            yield Device(**_._asdict())

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
        # inode = stat.st_ino
        _ = stat.st_dev
        _ = Device.to_major_minor_int(os.major(_), os.minor(_))
        return self._majmin_map[_]
