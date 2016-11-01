#!/usr/bin/env python2.7
import codecs
import os
import re

from setuptools import setup


def find_meta(category, fpath='pkg/__init__.py'):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, fpath), 'r') as f:
        package_root_file = f.read()
    matched = re.search(
        r"^__{}__\s+=\s+['\"]([^'\"]*)['\"]".format(category),
        package_root_file, re.M)
    if matched:
        return matched.group(1)
    raise Exception('Meta info string for {} undefined'.format(category))


setup(
    name='localshop-webhook',
    description='GitHub webhook for Localshop PyPI server',
    author=find_meta('author'),
    author_email=find_meta('author_email'),
    license=find_meta('license'),
    version=find_meta('version'),
    platforms=['Linux'],
    classifiers=[],
    package_dir={'localshop_webhook': 'pkg'},
    packages=['localshop_webhook'],
    scripts=[],
    url='https://github.com/okomestudio/localshop-webhook',
    install_requires=['flask'])
