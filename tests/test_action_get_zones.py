import yaml
import requests_mock
from mock import patch

from st2tests.base import BaseActionTestCase

from get_zones import GetZonesAction

__all__ = [
    'GetZonesActionTestCase'
]

MOCK_CONFIG_BLANK = yaml.safe_load(open(
    'tests/fixture/config_blank.yaml').read())
MOCK_CONFIG_FULL = yaml.safe_load(open(
    'tests/fixture/config_full.yaml').read())

MOCK_DATA_INVALID_JSON = "{'dd': doo}"
MOCK_DATA_SUCCESS = open(
    'tests/fixture/get_zones_success.json').read()
MOCK_DATA_FAIL = open(
    'tests/fixture/common_fail.json').read()


class GetZonesActionTestCase(BaseActionTestCase):
    action_cls = GetZonesAction

    def test_run_no_config(self):
        action = self.get_action_instance(MOCK_CONFIG_BLANK)
        self.assertRaises(ValueError, action.run)

    def test_run_is_instance(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        self.assertIsInstance(action, self.action_cls)
        self.assertEqual(action.api_key, "API-Key")
        self.assertEqual(action.api_email, "user@domain.tld")
        self.assertEqual(action.API_HOST, "https://api.cloudflare.com")

    @patch('get_zones.GetZonesAction.API_HOST', "mock://api.cloudflare.com")
    def test_run_status_404(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/zones",
                             status_code=404)

        self.assertRaises(ValueError,
                          action.run)

    @patch('get_zones.GetZonesAction.API_HOST', "mock://api.cloudflare.com")
    def test_run_invalid_json(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/zones",
                             text=MOCK_DATA_INVALID_JSON)

        self.assertRaises(ValueError,
                          action.run)

    @patch('get_zones.GetZonesAction.API_HOST', "mock://api.cloudflare.com")
    def test_run_success_true(self):
        expected = {
            'zones': [
                {
                    "id": "023e105f4ecef8ad9ca31a8372d0c353",
                    "name": "example.com",
                    "type": "full",
                }
            ],
            'messages': [
            ]
        }

        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/zones",
                             text=MOCK_DATA_SUCCESS)

        result = action.run()
        self.assertEqual(result, expected)

    @patch('get_ips.GetIPsAction.API_HOST', "mock://api.cloudflare.com")
    def test_run_success_false(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/zones",
                             text=MOCK_DATA_FAIL)
        self.assertRaises(Exception,
                          action.run)
