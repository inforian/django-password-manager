#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

import pytz
from datetime import datetime, timedelta

# Django
import django

try:
    from django.core.urlresolvers import resolve, reverse, NoReverseMatch
except ImportError:
    from django.urls import resolve, reverse, NoReverseMatch

from django.conf import settings

from pass_manager.models import PasswordHistory


def is_authenticated(user):
    if django.VERSION >= (1, 10):
        return user.is_authenticated
    else:
        return user.is_authenticated()


def check_password_expired(user):
    """check Password expiry

    :return True if expired else False
    """
    if not settings.STORE_PASSWORD_HISTORY:
        return False

    expiry = getattr(settings, 'PASSWORD_EXPIRY_TIME')

    try:
        # get latest password info
        latest = user.password_history.latest("timestamp")
    except PasswordHistory.DoesNotExist:
        return False

    now = datetime.now(tz=pytz.UTC)
    expiration = latest.timestamp + timedelta(days=expiry)

    if expiration < now:
        return True
    else:
        return False
