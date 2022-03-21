from lib.actions import CloudflareBaseAction


class GetZoneAccessRuleAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        List Access Rule in a Zone

        Args:
            zone_id: ID of the zone to delete from the access rule

        Raises:
            CloudFlareAPIError: On HTTP Error or Invaild JSON.

        Returns:
            list: containing the Access Rules
        """

        # grab URL components and remove from kwargs
        zone_id = kwargs['zone_id']
        del kwargs['zone_id']

        if 'configuration_target' in kwargs:
            kwargs['configuration.target'] = kwargs['configuration_target']
            del kwargs['configuration_target']

        if 'configuration_value' in kwargs:
            kwargs['configuration.value'] = kwargs['configuration_value']
            del kwargs['configuration_value']

        # invoke API call
        func = self.client.zones.firewall.access_rules.rules.get  # pylint: disable=no-member
        result = self.invoke(func, zone_id, **kwargs)
        return result
