#!/usr/bin/env python

import os
import sys

from setuptools import setup, Command
from setuptools.command.test import test as TestCommand
import pkg_resources


def read(readme_file):
    return open(os.path.join(os.path.dirname(__file__), readme_file)).read()


setup(
    name='pokr',
    version='0.0.0',
    author='Ross Fenning',
    author_email='pypi@rossfenning.co.uk',
    packages=['pokr'],
    description='Framework for building product and personal 2scorecards.',
    url='https://github.com/avengerpenguin/pokr',
    install_requires=[
        'quart', 'invoke', 'beautifulsoup4', 'PyGithub', 'todoist-python', 'sh', 'cachetools', 'livereload',
        'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'feedparser', 'pybraries',
    ],
    tests_require=[],
    setup_requires=[],
)
