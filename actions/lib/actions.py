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
import copy
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
            if v is not None:
                params[k] = v
        return params

    def invoke(self, func, *args, **kwargs):
        # convert query arguments to parameters dict
        # removing any parameters with a value of None
        params = self.kwargs_to_params(**kwargs)

        results = []
        page_number = 1
        total_pages = 0

        # loop for all pages in results
        while True:
            if page_number > 1:
                # Only pass in the `page` parameter if we had paged results from
                # the first loop. This way we don't send the `page` parameter
                # to calls that don't accept it.
                # NOTE: the default page number = 1
                params['page'] = page_number

            # invoke the Cloudflare APIo
            raw_results = func(*args, params=copy.deepcopy(params))

            # do we have paged results
            if 'result_info' not in raw_results:
                # we have non-paged results, return those results verbatim
                # and stop iterating!
                results = raw_results['result']
                break
            else:
                # we have paged results, extract the total number of pages
                # and append this pages results to the list
                total_pages = raw_results['result_info']['total_pages']
                results.extend(raw_results['result'])

            # if we've iterated over all of the pages
            if page_number >= total_pages:
                break

            # go to next page
            page_number += 1

        return results
