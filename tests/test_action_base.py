from get_ips import GetIPsAction
from cloudflare_base_action_test_case import CloudflareBaseActionTestCase

import json
import mock
import requests
from CloudFlare.exceptions import CloudFlareAPIError

MOCK_DATA_INVALID_JSON = "{'dd': doo}"


class BaseActionTestCase(CloudflareBaseActionTestCase):
    # use GetIPsAction because CloudflareBaseAction is abstract
    action_cls = GetIPsAction

    def test_init_blank(self):
        action = self.get_action_instance(self.config_blank)
        self.assertEquals(action.api_key, None)
        self.assertEquals(action.api_email, None)
        self.assertEquals(action.client._base.token, None)
        self.assertEquals(action.client._base.email, None)

    def test_init_good(self):
        action = self.get_action_instance(self.config_good)
        self.assertEquals(action.api_key, "API-Key")
        self.assertEquals(action.api_email, "user@domain.tld")
        self.assertEquals(action.client._base.token, "API-Key")
        self.assertEquals(action.client._base.email, "user@domain.tld")

    def test_kwargs_to_params(self):
        action = self.get_action_instance({})
        kwargs_dict = {"test_std": "value1",
                       "test_none": None,
                       "test_list": [],
                       "test_dict": {},
                       "test_int": 1}

        # run
        result = action.kwargs_to_params(**kwargs_dict)

        # assert
        self.assertEquals(result, {"test_std": "value1",
                                   "test_list": [],
                                   "test_dict": {},
                                   "test_int": 1})

    def test_invoke_paging(self):
        action = self.get_action_instance({})
        params = {'sort': 'desc',
                  'name': 'stackstorm',
                  'empty': None}
        pages = [
            {
                'result': [1, 2, 3],
                'result_info':
                {
                    "total_pages": 3
                }
            },
            {
                'result': [4, 5, 6],
                'result_info':
                {
                    "total_pages": 3
                }
            },
            {
                'result': [7, 8, 9],
                'result_info':
                {
                    "total_pages": 3
                }
            }
        ]

        mock_func = mock.MagicMock()
        mock_func.side_effect = pages

        result = action.invoke(mock_func, "zone_id", **params)

        # asserts
        self.assertEquals(result, [1, 2, 3, 4, 5, 6, 7, 8, 9])

        # ensure we called with the proper page numbers, in the proper order
        expected_calls = [
            mock.call("zone_id",
                      params={'sort': 'desc',
                              'name': 'stackstorm'}),
            mock.call("zone_id",
                      params={'sort': 'desc',
                              'name': 'stackstorm',
                              'page': 2}),
            mock.call("zone_id",
                      params={'sort': 'desc',
                              'name': 'stackstorm',
                              'page': 3}),
        ]
        mock_func.assert_has_calls(expected_calls)

    def test_invoke_paging_single(self):
        action = self.get_action_instance({})
        params = {'sort': 'desc',
                  'name': 'stackstorm',
                  'empty': None}
        pages = [
            {
                'result': [1, 2, 3],
                'result_info':
                {
                    "total_pages": 1
                }
            }
        ]

        mock_func = mock.MagicMock()
        mock_func.side_effect = pages

        result = action.invoke(mock_func, "arg", **params)

        # asserts
        self.assertEquals(result, [1, 2, 3])

        # ensure we called with the no page number
        expected_calls = [
            mock.call("arg",
                      params={'sort': 'desc',
                              'name': 'stackstorm'})
        ]
        mock_func.assert_has_calls(expected_calls)

    def test_invoke_no_paging(self):
        action = self.get_action_instance({})
        params = {'sort': 'desc',
                  'name': 'stackstorm',
                  'empty': None}
        mock_func = mock.MagicMock()
        mock_func.return_value = {
            'result': [1, 2, 3],
        }

        result = action.invoke(mock_func, "zone_id", **params)

        # asserts
        self.assertEquals(result, [1, 2, 3])

        # ensure we called with no page number
        expected_calls = [
            mock.call("zone_id",
                      params={'sort': 'desc',
                              'name': 'stackstorm'}),
        ]
        mock_func.assert_has_calls(expected_calls)

    @mock.patch('CloudFlare.network.requests')
    def test_run_status_404(self, mock_requests):
        action = self.get_action_instance(self.config_good)

        response = requests.Response()
        response.status_code = 404
        response.url = "https://api.cloudflare.com/client/v4/ips"
        response.headers['Content-Type'] = 'application/json'
        response._content = json.dumps({
            "success": False,
            "errors": [
                {
                    "code": 404
                }
            ],
            "result": "bad stuff"
        })
        mock_session = mock.MagicMock()
        mock_session.get.return_value = response
        mock_requests.Session.return_value = mock_session

        self.assertRaises(CloudFlareAPIError,
                          action.run)

    @mock.patch('CloudFlare.network.requests')
    def test_run_invalid_json(self, mock_requests):
        action = self.get_action_instance(self.config_good)

        response = requests.Response()
        response.status_code = 200
        response.url = "https://api.cloudflare.com/client/v4/ips"
        response.headers['Content-Type'] = 'application/json'
        response._content = MOCK_DATA_INVALID_JSON
        mock_session = mock.MagicMock()
        mock_session.get.return_value = response
        mock_requests.Session.return_value = mock_session

        self.assertRaises(CloudFlareAPIError,
                          action.run)

    @mock.patch('CloudFlare.network.requests')
    def test_run_success_false(self, mock_requests):
        action = self.get_action_instance(self.config_good)

        response = requests.Response()
        response.status_code = 200
        response.url = "https://api.cloudflare.com/client/v4/ips"
        response.headers['Content-Type'] = 'application/json'
        response._content = json.dumps({
            "success": False,
            "errors": [
                {
                    "code": 200
                }
            ],
            "result": "bad stuff"
        })
        mock_session = mock.MagicMock()
        mock_session.get.return_value = response
        mock_requests.Session.return_value = mock_session

        self.assertRaises(CloudFlareAPIError,
                          action.run)
