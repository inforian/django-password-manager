#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

from pass_manager import utils

from urllib.parse import urlparse, urlunparse
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict

from django.conf import settings


class ExpiredPassworMixin(object):
    """
        This Mixin is used to check Expiry date of password.
        Also we will store user Password to maintain the history of his passwords as per `PASSWORD_HISTORY_LIFE`.
        So that we can check that user cannot use same Password as he had used in Past.
    """

    def initial(self, request, *args, **kwargs):
        print("111")
        if utils.is_authenticated(request.user) and not request.user.is_staff:
            next_url = utils.resolve(request.path).url_name
            # Authenticated users must be allowed to access
            # "change password" page and "log out" page.
            # even if password is expired.
            if next_url not in [settings.ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL,
                                settings.ACCOUNT_LOGOUT_URL,
                                ]:
                print('in middlware 222')
                # import ipdb;ipdb.set_trace()
                if utils.check_password_expired(request.user):
                    print('in middlware 333')

                    change_password_url = utils.reverse(settings.ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL)
                    url_bits = list(urlparse(change_password_url))
                    querystring = QueryDict(url_bits[4], mutable=True)
                    url_bits[4] = querystring.urlencode(safe="/")

                    return Response({'detail': urlunparse(url_bits)},
                                    status=status.HTTP_307_TEMPORARY_REDIRECT)
                    # self.finalized_response(request, url_bits)

    def finalizeddd_response(self, request, response, *args, **kwargs):
        """

        """

        return Response({'detail': urlunparse(response)},
                        status=status.HTTP_307_TEMPORARY_REDIRECT)