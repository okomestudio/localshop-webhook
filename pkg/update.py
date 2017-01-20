# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import os
import shutil
import subprocess
from subprocess import call

from .config import index_server
from .config import matchers
from .config import repo_root
from .exceptions import SkipUpdate


log = logging.getLogger(__name__)


def _update_package(repo, ssh_url, branch, matcher):
    os.chdir(repo_root)
    repo_dir = os.path.join(repo_root, repo)

    if not os.path.exists(repo_dir):
        log.info('Repo %s does not exist; cloning...', repo)
        call(['git', 'clone', ssh_url, repo])

    os.chdir(repo_dir)

    call(['git', 'fetch', 'origin'])
    call(['git', 'checkout', branch])
    call(['git', 'reset', '--hard', 'origin/' + branch])

    p = subprocess.Popen(['python', 'setup.py', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    version = out.strip()
    if not matcher.version.match(version):
        raise SkipUpdate(
            ('Version "{}" for branch "{}" does not '
             'trigger package update').format(
                 version, branch))

    p = subprocess.Popen(
        ['python', 'setup.py', 'sdist', 'upload', '-r', index_server],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        raise Exception('Error uploading: \n{}'.format(out + '\n' + err))


def update_package(commit):
    branch = commit['ref'][11:]

    for matcher in matchers:
        if matcher.branch.match(branch):
            break
    else:
        raise SkipUpdate('Branch "{}" not watched'.format(branch))

    ssh_url = commit['repository']['ssh_url']
    repo = commit['repository']['name']

    try:
        _update_package(repo, ssh_url, branch, matcher)
    except Exception:
        log.exception('Error updating git repo; cloning again...')
        os.chdir(repo_root)
        shutil.rmtree(repo)
        try:
            _update_package(repo, ssh_url, branch, matcher)
        except Exception:
            log.exception(
                'Error updating git repo; retry after cloning failed')
            raise
