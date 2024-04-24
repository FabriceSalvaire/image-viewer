####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

from invoke import task

####################################################################################################

@task
def clean_flycheck(ctx):
    with ctx.cd(ctx.Package):
        ctx.run(r'find . -name "flycheck*.py" -exec rm {} \;')

@task
def clean_emacs_backup(ctx):
    ctx.run(r'find . -name "*~" -type f -exec rm -f {} \;')

@task(clean_flycheck, clean_emacs_backup)
def clean(ctx):
    pass
