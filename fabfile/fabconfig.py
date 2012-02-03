#!/usr/bin/python
# # encoding: utf-8
from fabric.api import env

# globals
env.hosts = ['valdergallo.com.br']
env.user = 'valdergall'
env.path = '~/public_html/teste/'
env.python_path = '~/eggs/'
env.colors = True
env.format = True
env.config_file = 'fabconfig.yaml'