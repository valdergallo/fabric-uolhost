#!/usr/bin/python
# # encoding: utf-8
from fabric.api import env
import os

BASEDIR = os.path.dirname(__file__)

env.project = 'teste'
env.hosts = ['valdergallo.com.br']
env.user = 'valdergall'
env.path = '~/public_html/teste/'
env.python_path = '~/eggs/'
