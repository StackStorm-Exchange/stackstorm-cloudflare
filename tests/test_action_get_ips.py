import mock
import requests
from CloudFlare.utils import user_agent

from cloudflare_base_action_test_case import CloudflareBaseActionTestCase

from get_ips import GetIPsAction

MOCK_DATA_SUCCESS = open(
    'tests/fixtures/get_ips_success.json').read()


class GetIPsActionTestCase(CloudflareBaseActionTestCase):
    action_cls = GetIPsAction
    maxDiff = None

    def test_run_is_instance(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, self.action_cls)

    @mock.patch('CloudFlare.network.requests')
    def test_run(self, mock_requests):
        action = self.get_action_instance(self.config_good)
        expected = {'ipv4_cidrs': [u'199.27.128.0/21'],
                    'ipv6_cidrs': [u'2400:cb00::/32']}

        response = requests.Response()
        response.status_code = 200
        response.url = "https://api.cloudflare.com/client/v4/ips"
        response.headers['Content-Type'] = 'application/json'
        response._content = MOCK_DATA_SUCCESS
        mock_session = mock.MagicMock()
        mock_session.get.return_value = response
        mock_requests.Session.return_value = mock_session

        result = action.run()

        self.assertEqual(result, expected)
        mock_session.get.assert_called_with("https://api.cloudflare.com/client/v4/ips",
                                            data=None,
                                            headers={'Content-Type': 'application/json',
                                                     'User-Agent': user_agent()},
                                            params={})
