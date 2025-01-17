####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

# https://material.io/tools/icons/static/icons/baseline-save-24px.svg
# https://material.io/tools/icons/static/icons/baseline-save-black-36.zip

# https://material.io/tools/icons/static/icons/outline-save-black-36.zip
# https://material.io/tools/icons/static/icons/round-save-black-36.zip
# https://material.io/tools/icons/static/icons/sharp-save-black-36.zip
# https://material.io/tools/icons/static/icons/twotone-save-black-36.zip

# https://material.io/tools/icons/static/icons/baseline-save-white-36.zip

# 1x/baseline_save_black_18dp.png: PNG image data, 18 x 18, 8-bit gray+alpha, non-interlaced
# 1x/baseline_save_black_24dp.png: PNG image data, 24 x 24, 8-bit gray+alpha, non-interlaced
# 1x/baseline_save_black_36dp.png: PNG image data, 36 x 36, 8-bit gray+alpha, non-interlaced
# 1x/baseline_save_black_48dp.png: PNG image data, 48 x 48, 8-bit gray+alpha, non-interlaced

# 2x/baseline_save_black_18dp.png: PNG image data, 36 x 36, 8-bit gray+alpha, non-interlaced
# 2x/baseline_save_black_24dp.png: PNG image data, 48 x 48, 8-bit gray+alpha, non-interlaced
# 2x/baseline_save_black_36dp.png: PNG image data, 72 x 72, 8-bit gray+alpha, non-interlaced
# 2x/baseline_save_black_48dp.png: PNG image data, 96 x 96, 8-bit gray+alpha, non-interlaced

####################################################################################################

from pathlib import Path
from zipfile import ZipFile
import os
import shutil
import tempfile
import urllib3

####################################################################################################

urllib3.disable_warnings()

####################################################################################################

class MaterialIconFetcher:

    BASE_URL = 'https://fonts.gstatic.com/s/i/materialicons'

    SCALE = (1, 2)
    DP = (18, 24, 36, 48)

    ##############################################

    def __init__(self, icons_path: str, theme: str) -> None:
        self._icons_path = Path(str(icons_path)).resolve()
        self._theme = str(theme)
        self._theme_path = self._icons_path.joinpath(self._theme)

        if not self._icons_path.exists():
            os.mkdir(self._icons_path)
        if not self._theme_path.exists():
            os.mkdir(self._theme_path)

        self._http = urllib3.PoolManager()

        # with tempfile.TemporaryDirectory() as tmp_directory:
        self._tmp_directory = tempfile.TemporaryDirectory()
        self._tmp_directory_path = Path(self._tmp_directory.name)
        print('tmp_directory', self._tmp_directory_path)

    ##############################################

    def _fetch_ressource(self, url: str) -> bytes:
        print('Fetch', url, '...')
        request = self._http.request('GET', url)
        return request.data

    ##############################################

    def _fetch_png_icon(self, name: str, color: str, dp: int, version: int) -> list[str, bytes]:
        # https://fonts.gstatic.com/s/i/materialicons/picture_as_pdf/v12/24px.svg
        # https://fonts.gstatic.com/s/i/materialicons/picture_as_pdf/v12/black-24dp.zip
        #   2x/baseline_picture_as_pdf_black_24dp.png
        #   1x/baseline_picture_as_pdf_black_24dp.png
        filename = f'{color}-{dp}dp.zip'
        url = f'{self.BASE_URL}/{name}/v{version}/{filename}'
        data = self._fetch_ressource(url)
        return filename, data

    ##############################################

    def _extract_png_archive(self, name: str, color: str, dp: int, version: int) -> None:
        filename, data = self._fetch_png_icon(name=name, color=color, dp=dp, version=version)
        zip_path = self._tmp_directory_path.joinpath(filename)
        with open(zip_path, 'wb') as fh:
            fh.write(data)
        with ZipFile(zip_path, 'r') as zip_archive:
            zip_archive.extractall(self._tmp_directory_path)

    ##############################################

    def fetch_icon(self, src_name: str, dst_name: str, style: str, color: str, version: int) -> None:
        for dp in self.DP:
            self._extract_png_archive(name=src_name, dp=dp, color=color, version=version)

        print()
        for scale in self.SCALE:
            for dp in self.DP:
                # 1x/baseline_save_black_18dp.png
                src_path = self._tmp_directory_path.joinpath(
                    f'{scale}x',
                    f'{style}_{src_name}_{color}_{dp}dp.png'
                )

                if scale > 1:
                    size_directory = f'{dp}x{dp}@{scale}'
                else:
                    size_directory = f'{dp}x{dp}'
                size_path = self._theme_path.joinpath(size_directory)
                if not size_path.exists():
                    os.mkdir(size_path)
                filename = f'{dst_name}-{color}.png'
                dst_path = size_path.joinpath(filename)

                # print('Copy', src_path, dst_path)
                shutil.copyfile(src_path, dst_path)

                rcc_line = f'<file>icons/{self._theme}/{size_directory}/{filename}</file>'
                if dp != 36:
                    rcc_line = f'<!-- {rcc_line} -->'
                rcc_line = ' '*8 + rcc_line
                print(rcc_line)
