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
    python_path = get_list_dir()
    project = os.path.basename(os.getcwd())
    htaccess = open('./conf/htaccess.conf').read() % \
        { 'project': project, 'python_path': python_path }
  
    name = '.htaccess'
    file_open = open(name, 'w')
    file_open.write(htaccess)
    file_open.close()
    run('mkdir -p %s' % env.path)
    put(os.path.realpath(name), env.path)
    print "Created .htaccess file"
    

def update_bashrc():
    "Update .bashrc"
    get('~/.bashrc', './')
    project = os.path.basename(os.getcwd())
    bashrc = open('./conf/bash.conf').read() % { 'python_path': python_path }
    with open(".bashrc", "a") as f:
        check_content = f.read()
        if bashrc not in check_content:
            f.write(bashrc)
            f.close()
            put(".bashrc", "~/")

@task
def upload():
    "Upload project"
    project = os.path.dirname(__file__)
    remote = env.path
    run('mkdir -p %s' % remote)
    
    with cd(remote):
        upload_project(project, remote)


def create_config():
    "Create htaccess and bashrc"
    create_htaccess()
    update_bashrc()


@task
@with_settings(warn_only=True)
def build():
    "Build packages in server"
    print(yellow('Install eggs'))
    requeriments('requeriments.txt')

    print(yellow('Create config'))
    create_config()

    print(yellow('Send files'))
    upload()