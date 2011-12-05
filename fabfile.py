#!/usr/bin/python
# encoding: utf-8

import os
from fabric.api import *
from fabric.colors import red, green, yellow
from fabric.contrib.console import confirm
from fabric.contrib.project import upload_project, rsync_project
from fabric.operations import put
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
    output = run('easy_install -Zmaxd %s %s' %
            (env.python_path, egg), pty=False)


def requeriments(textfile):
    "Install multiples eggs"

    fileopen = open(textfile)
    for line in fileopen.readlines():
        pip(line)
    fileopen.close()


def _get_listdir():
    "Get path from eggs"

    dirs = []
    with cd(env.python_path):
        run('ls > ~/tmp/listdir.txt')
        get("~/tmp/listdir.txt", local_path='.')
        dirList = open('./listdir.txt', 'r')
    for di in dirList.readlines():
        dirs.append(str(env.python_path) + str(di).replace('\n', ''))
    dirs.append(env.path)
    os.remove('./listdir.txt')
    return dirs


def create_htaccess():
    "Create .htaccess"
    dirList = _get_listdir()
    project = os.path.basename(os.path.realpath("../"))

    htaccess = """SetHandler python-program
PythonHandler django.core.handlers.modpython
SetEnv DJANGO_SETTINGS_MODULE {0}.settings
PythonInterpreter {0}
PythonOption django.root /{0}
PythonPath "{1}" + sys.path
""".format(project, dirList)

    name = '.htaccess'
    file_open = open(name, 'w')
    file_open.write(htaccess)
    file_open.close()
    run('mkdir -p %s' % env.path)
    put(os.path.realpath(name), env.path)
    print "Created .htaccess file"


def upload():
    project = os.path.realpath('..')
    remote = env.path
    run('mkdir -p %s' % remote)

    upload_project(project, remote)


def build():
    "Build packages in server"

    print(yellow('Install eggs'))
    requeriments('requeriments.txt')

    print(yellow('Create config'))
    create_htaccess()

    print(yellow('Send files'))
    upload()

