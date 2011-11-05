#!/usr/bin/python
# encoding: utf-8
import os
import yaml


class yConfig():

    def __init__(self):
        self.basedir = os.path.dirname(__file__)
        self.config = os.path.join(self.basedir, 'config.yaml')
        self.content = {}

    def save(self):
        "Save content"
        openfile = open(self.config, 'w')
        yaml.dump(self.content, openfile, default_flow_style=False)
        openfile.close()

    def clean(self):
        "Clean content"
        self.config.close()
        self.config = open(self.config, 'w')

    def set(self, **kwargs):
        "Set kwargs in config.yaml"
        try:
            self.content.update(kwargs)
            return self.content
        except Exception, error:
            print error
            return False

    def load(self):
        "Load config file"
        openfile = open(self.config)
        content = yaml.load(openfile)
        openfile.close()
        return content

    def get(self):
        "Get content in config.yaml"
        if not self.content:
            return self.load()

        return self.content
