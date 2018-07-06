from lib.actions import CloudflareBaseAction


class GetZonesAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        Get Cloudflare DNS Zones

        Args:
            None.

        Raises:
            ValueError: On HTTP Error or Invaild JSON.
            requests.exceptions.MissingSchema: If https:// missing from
                                               api_host.
            Exception: On "success": false from API.

        Returns:
            dict: containing DNS zones
        """

        results = {}
        url = "{}/client/v4/zones".format(self.API_HOST)
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
