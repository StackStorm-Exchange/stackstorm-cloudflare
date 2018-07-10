import yaml
import json
import logging

from st2tests.base import BaseActionTestCase


class CloudflareBaseActionTestCase(BaseActionTestCase):

    def setUp(self):
        super(CloudflareBaseActionTestCase, self).setUp()

        logging.disable(logging.CRITICAL)  # disable logging
        self.config_good = self.load_fixture_yaml('config_good.yaml')
        self.config_blank = self.load_fixture_yaml('config_blank.yaml')

    def tearDown(self):
        super(CloudflareBaseActionTestCase, self).tearDown()
        logging.disable(logging.NOTSET)  # enable logging

    def load_fixture_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    def load_fixture_json(self, filename):
        return json.loads(self.get_fixture_content(filename))
