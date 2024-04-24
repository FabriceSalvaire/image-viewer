####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

import os

import ImageBrowser

####################################################################################################

def merge_include(src_lines, doc_path, included_rst_files=None):
    if included_rst_files is None:
        included_rst_files = {}
    text = ''
    for line in src_lines:
        if line.startswith('.. include::'):
            include_file_name = line.split('::')[-1].strip()
            if include_file_name not in included_rst_files:
                # print "include", include_file_name
                with open(os.path.join(doc_path, include_file_name)) as fh:
                    included_rst_files[include_file_name] = True
                    text += merge_include(fh.readlines(), doc_path, included_rst_files)
        else:
            text += line
    return text

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read_readme(file_name):

    source_path = os.path.dirname(os.path.realpath(__file__))
    if os.path.basename(source_path) == 'tools':
        source_path = os.path.dirname(source_path)
    elif 'build/bdist' in source_path:
        source_path = source_path[:source_path.find('build/bdist')]
    absolut_file_name = os.path.join(source_path, file_name)
    doc_path = os.path.join(source_path, 'doc', 'sphinx', 'source')

    # Read and merge includes
    with open(absolut_file_name) as fh:
        lines = fh.readlines()
    text = merge_include(lines, doc_path)

    return text

####################################################################################################

if not __file__.endswith('conf.py'):
    long_description = read_readme('README.txt')
else:
    long_description = ''

####################################################################################################

setup_dict = dict(
    name='ImageBrowser',
    version=ImageBrowser.__version__,
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='Qt Application to scan and read images',
    license='GPLv3',
    keywords= 'scan image image viewer',
    url='https://github.com/FabriceSalvaire/image-browser',
    long_description=long_description,
)
