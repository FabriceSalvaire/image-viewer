export ImageBrowser_source_path=${PWD}

# source /opt/python-virtual-env/py312/bin/activate
source /opt/python-virtual-env/qt/bin/activate

export PYTHONPYCACHEPREFIX=${ImageBrowser_source_path}/.pycache
export PYTHONDONTWRITEBYTECODE=${ImageBrowser_source_path}/.pycache

append_to_python_path_if_not ${ImageBrowser_source_path}
