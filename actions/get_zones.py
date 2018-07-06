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
        return self.invoke(self.client.zones.get, **kwargs)
