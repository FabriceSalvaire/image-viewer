####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from invoke import task
 # import sys

####################################################################################################

from .clean import clean_flycheck as clean_flycheck

####################################################################################################

@task
def clean_api(ctx):
    ctx.run('rm -rf doc/sphinx/source/api')

####################################################################################################

@task(clean_flycheck, clean_api)
def make_api(ctx):
    print('\nGenerate RST API files')
    ctx.run('pyterate-rst-api {0.Package}'.format(ctx))
    print('\nRun Sphinx')
    with ctx.cd('doc/sphinx/'):
        ctx.run('./make-html') #--clean

####################################################################################################

@task()
def make_readme(ctx):
    from setup_data import long_description
    with open('README.rst', 'w') as fh:
        fh.write(long_description)
    # import subprocess
    # subprocess.call(('rst2html', 'README.rst', 'README.html'))
    ctx.run('rst2html README.rst README.html')

####################################################################################################

@task
def update_authors(ctx):
    # Keep authors in the order of appearance and use awk to filter out dupes
    ctx.run("git log --format='- %aN <%aE>' --reverse | awk '!x[$0]++' > AUTHORS")
