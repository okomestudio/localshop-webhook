# -*- coding: utf-8 -*-
from __future__ import absolute_import


class WebhookError(Exception):
    pass


class SkipUpdate(WebhookError):
    pass
