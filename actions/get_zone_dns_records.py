from lib.actions import CloudflareBaseAction


class GetZoneDnsRecordsAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        Get Cloudflare DNS Records in a Zone

        Args:
            None.

        Raises:
            ValueError: On HTTP Error or Invaild JSON.
            requests.exceptions.MissingSchema: If https:// missing from
                                               api_host.
            Exception: On "success": false from API.

        Returns:
            dict: containing DNS records
        """

        results = {}
        url = "{}/client/v4/zones/{}/dns_records".format(self.API_HOST,
                                                         kwargs['zone_id'])
        params = self.kwargs_to_params(**kwargs)
        data = self._get(url, params, api_key_required=True)

        if data['success'] is True:
            results['messages'] = data['messages']
            results['zones'] = data['result']
            return results
        else:
            for error in data['errors']:
                self.send_user_error(error)

            raise Exception("Error from Cloudflare: {}".format(data['errors']))
