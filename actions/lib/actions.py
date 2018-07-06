# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import six

from st2common.runners.base_action import Action


class CloudflareBaseAction(Action):
    API_HOST = "https://api.cloudflare.com"

    def __init__(self, config):
        super(CloudflareBaseAction, self).__init__(config)
        self.session = requests.Session()

        self.api_key = self.config.get('api_key')
        self.api_email = self.config.get('api_email')

    def send_user_error(self, message):
        """
        Prints an user error message.
        """
        print(message)

    def kwargs_to_params(self, **kwargs):
        params = {}
        for k, v in six.iteritems(kwargs):
            if k and v:
                params[k] = v
        return params

    def ensure_api_key_set(self):
        if not self.api_key:
            raise KeyError('This action requires "api_key" in the config and it is missing.')
        if not self.api_email:
            raise KeyError('This action requires "api_email" in the config and it is missing.')

    def _get(self, url, params=None, headers=None, api_key_required=False):
        """
        Issue a get request via requests.session()

        Args:
            url: The URL.
            headers: The Headers
            params: URL query parameters

        Returns:
            dict: Of JSON payload.

        Raises:
            ValueError: On HTTP error or Invalid JSON.
        """
        if headers is None:
            headers = {}

        if api_key_required:
            # raises if not set
            self.ensure_api_key_set()
            headers['X-Auth-Key'] = self.api_key
            headers['X-Auth-Email'] = self.api_email

        try:
            r = self.session.get(url,
                                 headers=headers,
                                 params=params)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ValueError("HTTP error: %s" % r.status_code)

        try:
            data = r.json()
        except ValueError:
            raise ValueError("Invalid JSON")
        else:
            return data
