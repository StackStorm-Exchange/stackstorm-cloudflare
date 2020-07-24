import mock
import requests
from CloudFlare.utils import user_agent

from cloudflare_base_action_test_case import CloudflareBaseActionTestCase

from get_zones import GetZonesAction

MOCK_DATA_SUCCESS = open(
    'tests/fixtures/get_zones_success.json').read()


class GetZonesActionTestCase(CloudflareBaseActionTestCase):
    action_cls = GetZonesAction

    def test_run_is_instance(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, self.action_cls)

    @mock.patch('CloudFlare.network.requests')
    def test_run(self, mock_requests):
        action = self.get_action_instance(self.config_good)
        expected = [
            {
                "id": "023e105f4ecef8ad9ca31a8372d0c353",
                "name": "example.com",
                "type": "full"
            }
        ]

        response = requests.Response()
        response.status_code = 200
        response.url = "https://api.cloudflare.com/client/v4/zones"
        response.headers['Content-Type'] = 'application/json'
        response._content = MOCK_DATA_SUCCESS
        mock_session = mock.MagicMock()
        mock_session.get.return_value = response
        mock_requests.Session.return_value = mock_session

        result = action.run()

        self.assertEqual(result, expected)
        mock_session.get.assert_called_with("https://api.cloudflare.com/client/v4/zones",
                                            data=None,
                                            headers={'X-Auth-Email': 'user@domain.tld',
                                                     'X-Auth-Key': 'API-Key',
                                                     'Content-Type': 'application/json',
                                                     'User-Agent': user_agent()},
                                            params={})
