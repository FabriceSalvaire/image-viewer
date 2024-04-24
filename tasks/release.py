####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from invoke import task

####################################################################################################

STANDARD_PACKAGES = (
    'argparse',
    'atexit',
    'datetime',
    'hashlib',
    'importlib',
    'json',
    'logging',
    'operator',
    'os',
    'pathlib',
    'shutil',
    'signal',
    'stat',
    'subprocess',
    'sys',
    'time',
    'traceback',
)

@task()
def show_import(ctx):
    package = ctx.Package
    with ctx.cd(package):
        result = ctx.run("grep -r -h -E  '^(import|from) [a-zA-Z]' . | sort | uniq", hide='out')
    imports = set()
    for line in result.stdout.split('\n'):
        if line.startswith('from'):
            position = line.find('import')
            line = line[5:position]
        elif line.startswith('import'):
            line = line[7:]
        # print('|{}|'.format(line))
        position = line.find('.')
        if position != -1:
            line = line[:position]
        line = line.strip()
        if line:
            imports.add(line)
    imports -= set(STANDARD_PACKAGES)
    imports -= set((package,))
    for item in sorted(imports):
        print(item)

@task
def find_package(ctx, name):
    ctx.run('pip freeze | grep -i {}'.format(name))

####################################################################################################

@task()
def update_git_sha(ctx):
    result = ctx.run('git describe --tags --abbrev=0 --always', hide='out')
    sha = result.stdout.strip()
    filename = Path(ctx.Package, '__init__.py')
    with open(str(filename) + '.in', 'r') as fh:
        lines = fh.readlines()
    with open(filename, 'w') as fh:
        for line in lines:
            if '@' in line:
                line = line.replace('@GIT_SHA@', sha)
            fh.write(line)

####################################################################################################

def show_python_site(ctx):
    ctx.run('python3 -m site')

@task(update_git_sha)
def build(ctx):
    ctx.run('python3 setup.py build')

@task(build)
def install(ctx):
    ctx.run('python3 setup.py install')
