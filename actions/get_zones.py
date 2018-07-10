from lib.actions import CloudflareBaseAction


class GetZonesAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        Get Cloudflare DNS Zones

        Args:
            None.

        Raises:
            CloudFlareAPIError: On HTTP Error or Invaild JSON.

        Returns:
            dict: containing DNS zones
        """
        return self.invoke(self.client.zones.get,  # pylint: disable=no-member
                           **kwargs)
