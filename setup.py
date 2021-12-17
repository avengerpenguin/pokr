#!/usr/bin/env python
from setuptools import setup

NAME = "pokr"
setup(
    name=NAME,
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": f"{NAME}/_version.py",
        "fallback_version": "0.0.0",
    },
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    packages=[NAME, "pokr.metrics"],
    package_data={NAME: ["py.typed", "templates/*.html"]},
    description="Framework for building product and personal scorecards.",
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    install_requires=[
        "aiohttp",
        "quart",
        "invoke",
        "doctrine",
        "beautifulsoup4",
        "PyGithub",
        "todoist-python",
        "cachetools",
        "livereload",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "feedparser",
        "pybraries",
        "pytz",
        "google-analytics-data",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-pikachu",
            "pytest-mypy",
            "pytest-asyncio",
            "types-cachetools",
            "types-requests",
            "types-pytz",
            "types-beautifulsoup4",
        ],
    },
)
