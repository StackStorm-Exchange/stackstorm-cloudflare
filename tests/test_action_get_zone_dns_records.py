import mock
import requests
from CloudFlare.utils import user_agent

from cloudflare_base_action_test_case import CloudflareBaseActionTestCase

from get_zone_dns_records import GetZoneDnsRecordsAction

MOCK_DATA_SUCCESS = open(
    'tests/fixtures/get_zone_dns_records_success.json').read()


class GetZoneDnsRecordsActionTestCase(CloudflareBaseActionTestCase):
    action_cls = GetZoneDnsRecordsAction

    def test_run_is_instance(self):
        action = self.get_action_instance(self.config_good)
        self.assertIsInstance(action, self.action_cls)

    @mock.patch('CloudFlare.network.requests')
    def test_run(self, mock_requests):
        action = self.get_action_instance(self.config_good)
        expected = [
            {
                "name": "abc.domain.tld",
                "content": "1.2.3.4",
                "zone_name": "domain.tld",
                "type": "A",
                "id": "41981e0023c8e1e375ffbc9b35a0fb4e",
                "zone_id": "023e105f4ecef8ad9ca31a8372d0c353"
            },
            {
                "name": "xyz.domain.tld",
                "content": "7.8.9.0",
                "zone_name": "domain.tld",
                "type": "A",
                "id": "bd461aba4b76229c9be2b77e4ef369af",
                "zone_id": "023e105f4ecef8ad9ca31a8372d0c353"
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

        result = action.run(zone_id="023e105f4ecef8ad9ca31a8372d0c353")

        self.assertEqual(result, expected)
        url = ("https://api.cloudflare.com/client/v4/zones/{}/dns_records"
               .format("023e105f4ecef8ad9ca31a8372d0c353"))
        mock_session.get.assert_called_with(url,
                                            data=None,
                                            headers={'X-Auth-Email': 'user@domain.tld',
                                                     'X-Auth-Key': 'API-Key',
                                                     'Content-Type': 'application/json',
                                                     'User-Agent': user_agent()},
                                            params={})
