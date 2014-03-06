#! /usr/bin/env python

# web-api.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import requests

from requests.compat import json


class Error(Exception):
    pass


class AuthError(Error):
    pass


class ClientError(Error):
    pass


class ServerError(Error):
    pass


class ApiClient():
    API_TEMPLATE = '{host}/v{version}/{endpoint}'
    API_HOST = 'https://api.kano.me'
    API_VERSION = '0'

    def __init__(self):
        self._session = requests.session()

    def _formatUrl(self, endpoint):
        return self.API_TEMPLATE.format(host=self.API_HOST,
                                        version=self.API_VERSION,
                                        endpoint=endpoint.strip("/"))

    def _request(self, method, endpoint, **kwargs):
        url = self._formatUrl(endpoint)

        action = getattr(self._session, method)
        response = action(url, **kwargs)

        try:
            response.raise_for_status()
        except requests.HTTPError:
            error = response.text
            try:
                error = json.loads(error)
            except (KeyError, ValueError):
                pass

            if response.status_code in (401, 403):
                raise AuthError(error)
            elif response.status_code in (400, 404, 405):
                raise ClientError(error)
            elif response.status_code >= 500:
                raise ServerError(error)
            else:
                raise Error(error)

        return response

    def get(self, endpoint, **kwargs):
        return self._request("get", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("post", endpoint, **kwargs)
