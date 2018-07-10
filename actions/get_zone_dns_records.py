from lib.actions import CloudflareBaseAction


class GetZoneDnsRecordsAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        Get Cloudflare DNS Records in a Zone

        Args:
            zone_id: ID of the zone to get DNS records from

        Raises:
            CloudFlareAPIError: On HTTP Error or Invaild JSON.

        Returns:
            dict: containing DNS records
        """

        # grab URL components and remove from kwargs
        zone_id = kwargs['zone_id']
        del kwargs['zone_id']

        # invoke API call
        result = self.invoke(self.client.zones.dns_records.get, zone_id, **kwargs)
        return result
