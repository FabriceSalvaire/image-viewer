####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from pathlib import Path
import os

from invoke import task

from .lib.MaterialIcon import MaterialIconFetcher

####################################################################################################

SOURCE_PATH = Path(__file__).resolve().parents[1]
ICONS_PATH = SOURCE_PATH.joinpath('ImageBrowser', 'frontend', 'rcc', 'icons')

####################################################################################################

def _rcc_message():
    print('Run inv qt.rcc')


@task
def fetch_png_icon(ctx, src_name, dst_name=None, style='baseline', color='black', version=18):
     # style: [baseline], outline, round, twotone, sharp
     # color: [black], white
    theme = 'material'
    print('Icons path:', ICONS_PATH, theme)
    if dst_name is None:
        dst_name = src_name.replace('_', '-')
    print(f'{src_name} -> {dst_name}   style={style} color={color} version={version}')
    fetcher = MaterialIconFetcher(ICONS_PATH, theme)
    fetcher.fetch_png_icon(
        src_name,
        dst_name or src_name.replace('_', '-'),
        style,
        color,
        version
    )
    _rcc_message()

####################################################################################################

@task
def fetch_svg_icon(ctx, src_name, dst_name=None, style='outlined', fill=False):
    theme = 'material'
    print('Icons path:', ICONS_PATH, theme)
    if dst_name is None:
        dst_name = src_name.replace('_', '-')
    print(f'{src_name} -> {dst_name}   style={style} fill={fill}')
    fetcher = MaterialIconFetcher(ICONS_PATH, theme)
    fetcher.fetch_svg_icon(
        src_name,
        dst_name or src_name.replace('_', '-'),
        style=style,
        fill=fill,
    )
    _rcc_message()

####################################################################################################

@task
def fix_name(ctx):
    for directory, _, filenames in os.walk(ICONS_PATH):
        directory = Path(directory)
        for filename in filenames:
            path = directory.joinpath(filename)
            if path.suffix == '.png':
                if '_' in filename:
                    new_filename = filename.replace('_', '-')
                    new_path = directory.joinpath(new_filename)
                    print(path, new_path)
                    path.rename(new_path)

####################################################################################################

@task
def search_icon(ctx, name: str, delete: bool = False):
    for (dirpath, dirnames, filenames) in ICONS_PATH.walk():
        for filename in filenames:
            if name in filename:
                filename = dirpath.joinpath(filename)
                if delete:
                    print(f'Remove {filename}')
                    filename.unlink()
                else:
                    print(filename)
