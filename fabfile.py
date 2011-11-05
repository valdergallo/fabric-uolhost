#!/usr/bin/python
# encoding: utf-8

import os
import config
from fabric.api import *
from fabric.contrib.console import confirm
from settings import *

yc = config.yConfig()


def test():
    "Test connection with server"
    run('echo $PWD')
    run('uptime')
    run('uname -a')
    run('python -V')


def _save_config(project_path):
    "Private create config.yaml file"

    yc.set(host=env.host)
    yc.set(path=project_path)
    yc.set(python_path=env.python_path)
    yc.save()


def pip(egg):
    "Install eggs"
    config = yc.get()
    python_path = config['python_path']
    local('easy_install -Zmaxd %s %s' % (python_path, egg))


def requeriments(textfile):
    "Install multiples eggs"

    fileopen = open(textfile)
    for line in fileopen.readline():
        pip(line)
    fileopen.close()


def build(project_path=env.path):
    "Build packages in server"

    _save_config(project_path)
    print('ok')
