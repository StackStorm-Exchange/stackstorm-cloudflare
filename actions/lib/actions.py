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

import CloudFlare
import six

from st2common.runners.base_action import Action


class CloudflareBaseAction(Action):

    def __init__(self, config):
        super(CloudflareBaseAction, self).__init__(config)
        self.api_key = self.config.get('api_key')
        self.api_email = self.config.get('api_email')
        self.client = CloudFlare.CloudFlare(email=self.api_email,
                                            token=self.api_key,
                                            raw=True)

    def kwargs_to_params(self, **kwargs):
        params = {}
        for k, v in six.iteritems(kwargs):
            if k and v:
                params[k] = v
        return params

    def invoke(self, func, *args, **kwargs):
        params = self.kwargs_to_params(**kwargs)
        paged_results = []
        page_number = 0
        while True:
            page_number += 1
            if page_number > 1:
                # only specify page number if we had paged results from
                # the first call, this way we don't send the `page` parameter
                # to calls that don't accept it
                # NOTE: the default page number = `
                params['page'] = page_number

            # invoke the Cloudflare API
            raw_results = func(*args, params=params)

            # do we have paged results
            if 'result_info' in raw_results:
                count = raw_results['result_info']['count']
                page = raw_results['result_info']['page']
                per_page = raw_results['result_info']['per_page']
                total_count = raw_results['result_info']['total_count']
                total_pages = raw_results['result_info']['total_pages']
                paged_results.extend(raw_results['result'])
            else:
                # we have non-paged results, return immediately
                return raw_results['result']

            if page_number == total_pages:
                break

        return paged_results
