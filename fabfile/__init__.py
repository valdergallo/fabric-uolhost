#!/usr/bin/python
# encoding: utf-8
from __future__ import with_statement
import os
import time
import fabconfig

from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm
from fabric.contrib.project import upload_project

#globals
env.release = time.strftime('%Y%m%d%H%M%S')
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))


@task
def test():
    "Test connection with server"
    run('echo $PWD')
    run('uptime')
    run('uname -a')
    run('python -V')


@task
def pip(egg):
    "Install eggs"
    output = run("mkdir -p %s" % env.python_path, pty=False)
    output = run('easy_install -Zmaxd %s %s' %
            (env.python_path, egg), pty=False)

@task
def requeriments(textfile):
    "Install multiples eggs"

    fileopen = open(textfile)
    for line in fileopen.readlines():
        pip(line)
    fileopen.close()

@task
@with_settings(warn_only=True)
def get_list_dir():
    "Get path from eggs"
    dirs = []
    run('mkdir -p %s' % env.python_path)
    run('ls %s > ~/.fab_listdir' % env.python_path)
    get('~/.fab_listdir', '/tmp/')
    run('rm -y ~/.fab_listdir')
    dirList = open('/tmp/.fab_listdir')
    for directory in dirList.readlines():
        dirs.append(os.path.join(env.python_path, directory.replace('\n','/')))
    dirs.append(env.path)
    print dirs
    return dirs


def create_htaccess():
    "Create .htaccess"
    dirList = get_list_dir()
    project = os.path.basename(os.getcwd())

    htaccess = """SetHandler python-program
PythonHandler django.core.handlers.modpython
SetEnv DJANGO_SETTINGS_MODULE {0}.src.settings
PythonInterpreter {0}
PythonOption django.root /{0}
PythonPath "{1} + sys.path"
""".format(project, dirList)

    name = '.htaccess'
    file_open = open(name, 'w')
    file_open.write(htaccess)
    file_open.close()
    run('mkdir -p %s' % env.path)
    put(os.path.realpath(name), env.path)
    print "Created .htaccess file"


@task
def upload():
    "Upload project"
    project = os.path.dirname(__file__)
    remote = env.path
    run('mkdir -p %s' % remote)

    upload_project(project, remote)


@task
def build():
    "Build packages in server"

    print(yellow('Install eggs'))
    requeriments('requeriments.txt')

    print(yellow('Create config'))
    create_htaccess()

    print(yellow('Send files'))
    upload()

