#!/usr/bin/python
# encoding: utf-8

import os
import config
from fabric.api import *
from fabric.colors import red, green, yellow
from fabric.contrib.console import confirm
from settings import *

yc = config.yConfig()


def test():
    "Test connection with server"
    run('echo $PWD')
    run('uptime')
    run('uname -a')
    run('python -V')


def _save_config(project, project_path):
    "Private create config.yaml file"

    yc.set(host=env.host)
    yc.set(project=project)
    yc.set(path=project_path)
    yc.set(python_path=env.python_path)
    yc.save()


def pip(egg):
    "Install eggs"
    config = yc.get()
    python_path = config['python_path']
    run("mkdir -p %s" % python_path)
    run('easy_install -Z -m -a -x -d %s %s' % (python_path, egg))


def requeriments(textfile):
    "Install multiples eggs"

    fileopen = open(textfile)
    for line in fileopen.readlines():
        pip(line)
    fileopen.close()


def _get_list_dir():
    "Get path from eggs"

    dirs = []
    dirList = os.listdir(env.python_path)
    for dir in dirList:
        dirs.append(os.path.join(env.python_path, dir))
    return dirs


def create_htaccess():
    "Create .htaccess"
    dirList = get_list_dir()

    htaccess = """
SetHandler python-program
PythonHandler django.core.handlers.modpython
SetEnv DJANGO_SETTINGS_MODULE {0}.src.settings
PythonInterpreter {0}
PythonOption django.root /{0}
PythonPath "{1} + sys.path"
""".format(env.project, dirList)

    file_open = open('.htaccess','w')
    file_open.write(htaccess)
    file_open.close()

    print "Created .htaccess file"


def build():
    "Build packages in server"

    print(yellow('save config'))
    _save_config(env.project, env.python_path)

    print(yellow('Install eggs'))
    requeriments('requeriments.txt')
