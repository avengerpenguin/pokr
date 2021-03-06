#!/usr/bin/env python

import os

from setuptools import find_packages, setup


def read(readme_file):
    return open(os.path.join(os.path.dirname(__file__), readme_file)).read()


setup(
    name="pokr",
    version="0.0.0",
    author="Ross Fenning",
    author_email="pypi@rossfenning.co.uk",
    packages=find_packages(),
    description="Framework for building product and personal scorecards.",
    url="https://github.com/avengerpenguin/pokr",
    install_requires=[
        "aiohttp",
        "quart",
        "invoke",
        "beautifulsoup4",
        "PyGithub",
        "todoist-python",
        "sh",
        "cachetools",
        "livereload",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "feedparser",
        "pybraries",
    ],
)
