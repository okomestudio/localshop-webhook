# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re
from collections import namedtuple


env = os.environ

#: The secret used for encoding GitHub commit message.
webhook_secret = env.get('WEBHOOK_SECRET')

#: The path to the top-level directory where git repos are cloned.
repo_root = env.get('WEBHOOK_REPO_ROOT', '/home/localshop/repos')

#: The identifier in `.pypirc` pointing to the localshop repository.
index_server = env.get('WEBHOOK_INDEX_SERVER', 'localshop')

#: The file containing matcher specs. Each line contains a
#: tab-delimited branch name/version name regex pair to be matched
#: against incoming commit message. If matched, package update gets
#: triggered; if not matched, the commit message is ignored.
matcher_specs_file = env.get('WEBHOOK_MATCHER_SPECS_FILE')


#: Matching conditions (using branch name/package version) for
#: triggering package index update.
matchers = []

Watched = namedtuple('Watched', 'branch version')

if matcher_specs_file:
    with open(matcher_specs_file) as f:
        for line in f:
            branch, version = line.split()
            matchers.append(Watched(re.compile(branch.strip()),
                                    re.compile(version.strip())))
else:
    matchers.append(Watched(re.compile('.*'), re.compile('.*')))
