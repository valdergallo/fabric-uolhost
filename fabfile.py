#!/usr/bin/python
# encoding: utf-8

import os
from fabric.api import *
from fabric.colors import red, green, yellow
from fabric.contrib.console import confirm
from settings import *
from fabric.state import output

output['status'] = False
output['running'] = False

def test():
    "Test connection with server"
    run('echo $PWD')
    run('uptime')
    run('uname -a')
    run('python -V')

def pip(egg):
    "Install eggs"
    output = run("mkdir -p %s" % env.python_path, pty=False)
    output = run('easy_install -Zmaxd %s %s' % (env.python_path, egg), pty=False)


def requeriments(textfile):
    "Install multiples eggs"

    fileopen = open(textfile)
    for line in fileopen.readlines():
        pip(line)
    fileopen.close()


def _get_list_dir():
    "Get path from eggs"

    dirs = []
    dirList = run('ls %s' % env.python_path)
    for dir in dirList.split('  '):
        dirs.append(env.python_path+dir)
    dirs.append(env.path)
    return dirs


def create_htaccess():
    "Create .htaccess"
    dirList = _get_list_dir()

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

    print(yellow('Install eggs'))
    requeriments('requeriments.txt')

    print(yellow('Create config'))
    create_htaccess()


