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
ICONS_PATH = SOURCE_PATH.joinpath('DatasheetExtractor', 'frontend', 'rcc', 'icons')

####################################################################################################

@task
def fetch_icon(ctx, src_name, dst_name=None, style='baseline', color='black', version=12):
     # style: [baseline], outline, round, twotone, sharp
     # color: [black], white
    theme = 'material'
    print('Icons path:', ICONS_PATH, theme)
    if dst_name is None:
        dst_name = src_name.replace('_', '-')
    print(f'{src_name} -> {dst_name}   style={style} color={color} version={version}')
    fetcher = MaterialIconFetcher(ICONS_PATH, theme)
    fetcher.fetch_icon(
        src_name,
        dst_name or src_name.replace('_', '-'),
        style,
        color,
        version
    )

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
