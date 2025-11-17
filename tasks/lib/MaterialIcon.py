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
import subprocess
import tempfile
import urllib3

####################################################################################################

urllib3.disable_warnings()

####################################################################################################

class MaterialIconFetcher:

    BASE_URL = 'https://fonts.gstatic.com/s/i'

    SCALE = (1, 2)
    PNG_DP = (18, 24, 36, 48)
    SVG_DP = (20, 24, 40, 48)

    ##############################################

    def __init__(self, icons_path: str, theme: str) -> None:
        self._icons_path = Path(str(icons_path)).resolve()
        self._theme = str(theme)
        self._theme_path = self._icons_path.joinpath(self._theme)
        self._svg_path = self._icons_path.joinpath('svg')
        print(f"Theme path: {self._theme_path}")
        print(f"SVG path: {self._svg_path}")

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
        url = f'{self.BASE_URL}/materialicons/{name}/v{version}/{filename}'
        data = self._fetch_ressource(url)
        return filename, data

    ##############################################

    def _fetch_svg_icon(
        self,
        name: str,
        dp: int = 24,
        style: str = 'outlined',   # sharp outlined rounded
        fill: bool = False,
        weight: int = None,
        grade: int = 0,
    ) -> list[str, bytes]:
        # https://fonts.gstatic.com/s/i/materialiconsoutlined/home/v16/24px.svg
        # https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/check/default/24px.svg
        # https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/chevron_right/default/24px.svg
        # https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/backspace/fill1/24px.svg
        # https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/home/wght500/24px.svg
        style0 = 'materialsymbols'
        style2 = 'default'
        if fill:
            style2 = 'fill1'
        filename = f'{dp}px.svg'
        url = f'{self.BASE_URL}/short-term/release/{style0}{style}/{name}/{style2}/{filename}'
        data = self._fetch_ressource(url).decode('utf8')
        # print(data)
        if data.startswith('<!DOCTYPE html>'):
            raise NameError('Wrong icon url')
        return data

    ##############################################

    def _extract_png_archive(self, name: str, color: str, dp: int, version: int) -> None:
        filename, data = self._fetch_png_icon(name=name, color=color, dp=dp, version=version)
        zip_path = self._tmp_directory_path.joinpath(filename)
        with open(zip_path, 'wb') as fh:
            fh.write(data)
        with ZipFile(zip_path, 'r') as zip_archive:
            zip_archive.extractall(self._tmp_directory_path)

    ##############################################

    def fetch_png_icon(self, src_name: str, dst_name: str, style: str, color: str, version: int) -> None:
        for dp in self.PNG_DP:
            self._extract_png_archive(name=src_name, dp=dp, color=color, version=version)
        print()
        for dp in self.PNG_DP:
            for scale in self.SCALE:
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

                # RCC
                rcc_line = f'<file>icons/{self._theme}/{size_directory}/{filename}</file>'
                if dp != 36:
                    rcc_line = f'<!-- {rcc_line} -->'
                rcc_line = ' '*8 + rcc_line
                print(rcc_line)

    ##############################################

    def fetch_svg_icon(
        self,
        src_name: str,
        dst_name: str,
        dp: int = 24,
        style: str = 'outlined',   # sharp outlined rounded
        fill: bool = False,
        weight: int = None,
        grade: int = 0,
    ) -> None:
        rcc = ''
        for dp in self.SVG_DP:
            data = self._fetch_svg_icon(name=src_name, dp=dp, style=style, fill=fill, weight=weight, grade=grade)
            color = 'black' if fill else 'white'
            svg_path = self._svg_path.joinpath(f'{dst_name}-{color}-{dp}px.svg')
            if svg_path.exists():
                print(f"{svg_path} exists")
            else:
                print(f"Write {svg_path}")
                svg_path.write_text(data)
            for scale in self.SCALE:
                filename = self.run_inkscape(svg_path, dp, scale)

                # RCC
                if scale > 1:
                    size_directory = f'{dp}x{dp}@{scale}'
                else:
                    size_directory = f'{dp}x{dp}'
                rcc_line = f'<file>icons/{self._theme}/{size_directory}/{filename}</file>'
                if dp != 40:
                    rcc_line = f'<!-- {rcc_line} -->'
                rcc += ' '*8 + rcc_line + os.linesep
        print()
        print(rcc)

    ##############################################

    def run_inkscape(self, svg_path: Path, dp: int, scale: int) -> str:
        inkscape_options = [
            '--export-area-page',
            '--export-background=white',
            '--export-background-opacity=0',
        ]

        filename = svg_path.stem[:-5] + '.png'
        if scale > 1:
            size_directory = f'{dp}x{dp}@{scale}'
        else:
            size_directory = f'{dp}x{dp}'
        size_path = self._theme_path.joinpath(size_directory)
        size_path.mkdir(exist_ok=True)
        png_path = size_path.joinpath(filename)
        command = (
            'inkscape',
            *inkscape_options,
            '--export-filename={}'.format(png_path),
            # --export-width=
            '--export-height={}'.format(dp*scale),
            str(svg_path),
        )
        # print('>', ' '.join(command))
        subprocess.check_call(command)
        return filename
