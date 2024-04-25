####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from pathlib import Path
import shutil

from invoke import task

from .clean import flycheck as _clean_flycheck
from .release import update_git_sha as _update_git_sha

####################################################################################################

SOURCE_PATH = Path(__file__).resolve().parents[1]

SPHINX_PATH = SOURCE_PATH.joinpath('doc', 'sphinx')
BUILD_PATH = SPHINX_PATH.joinpath('build')
RST_SOURCE_PATH = SPHINX_PATH.joinpath('source')
RST_API_PATH = RST_SOURCE_PATH.joinpath('api')
RST_EXAMPLES_PATH = RST_SOURCE_PATH.joinpath('examples')

####################################################################################################

@task
def clean_build(ctx):
    # ctx.run('rm -rf {}'.format(BUILD_PATH))
    if BUILD_PATH.exists():
        shutil.rmtree(BUILD_PATH)

####################################################################################################

@task
def clean_api(ctx):
    # ctx.run('rm -rf {}'.format(RST_API_PATH))
    if RST_API_PATH.exists():
        shutil.rmtree(RST_API_PATH)

@task(_update_git_sha, _clean_flycheck, clean_api)
def make_api(ctx):
    print()
    print('Generate RST API files')
    ctx.run('pyterate-rst-api {0.Package}'.format(ctx))
    run_sphinx(ctx)
    print('')
    print('<<< Check API contains undocumented >>>')

####################################################################################################

@task
def run_sphinx(ctx):
    print()
    print('Run Sphinx')
    working_path = SPHINX_PATH
    # subprocess.run(('make-html'), cwd=working_path)
    # --clean
    with ctx.cd(str(working_path)):
        ctx.run('make-html')

####################################################################################################

@task
def xdg_open(ctx):
    ctx.run('xdg-open doc/sphinx/build/html/index.html')
