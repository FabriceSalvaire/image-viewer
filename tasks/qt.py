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

####################################################################################################

SOURCE_PATH = Path(__file__).absolute().parents[1]
FRONTEND_PATH = SOURCE_PATH.joinpath('ImageBrowser', 'frontend')
QML_PATH = FRONTEND_PATH.joinpath('qml')
RCC_PATH = FRONTEND_PATH.joinpath('rcc')

####################################################################################################

@task
def clean(ctx):   # noqa:
    for _ in (
            'application.rcc',
            'resources.py',
    ):
        RCC_PATH.joinpath(_).unlink()

####################################################################################################

@task
def rcc(ctx):   # noqa:
    with ctx.cd(RCC_PATH):
        ctx.run('pyside6-rcc application.qrc -o resources.py')

####################################################################################################

@task()
def qml(ctx, path):
    """Run qml tool"""
    path = Path(path).absolute()
    if not (path.exists() and path.is_dir()):
        print(f"Directory {path} doesn't exist")
    # aka /usr/bin/qml
    qml = Path(ctx.Qt.bin_path).joinpath(ctx.Qt.qml_command)
    includes = ' '.join([f'-I {_}' for _ in (QML_PATH,)])
    command = f'{qml} {includes} {path}'
    env = {
        'QT_LOGGING_RULES': ';'.join((
            '*.debug=true',
            'qt.*.debug=false',
            '*.info=true',
        )),
    }
    # with ctx.cd('.'):
    print(command)
    ctx.run(command, env=env)

####################################################################################################

@task()
def get_qt_source(ctx):
    # path = Path(path)
    path = Path(ctx.Qt.source_path)
    if not path.exists():
        # https://wiki.qt.io/Building_Qt_6_from_Git
        ctx.run(f'git clone git://code.qt.io/qt/qt5.git {path}')
    with ctx.cd(path):
        # branch = 'dev'
        branch = 'v6.4.0'
        ctx.run(f'git switch {branch}')
        ctx.run(f'perl init-repository --module-subset')

####################################################################################################

@task()
def find_qml_source(ctx, pattern):
    pattern = pattern.lower()
    qt_path = Path(ctx.Qt.source_path).resolve()
    controls_path = qt_path.joinpath('qtquickcontrols2', 'src')
    print(controls_path)
    for root, _, filenames in os.walk(controls_path):
        root = Path(root)
        for filename in filenames:
            filename = Path(filename)
            if filename.suffix == '.qml':
                if pattern in filename.name.lower():
                    file_path = root.joinpath(filename)
                    print(file_path)
