from lib.actions import CloudflareBaseAction


class CreateZoneAccessRuleAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        Create Access Rule in a Zone

        Args:
            zone_id: ID of the zone to create the access rule
            mode: The action the access rule will apply to matched requests
            target_type: The address type to target in requests
            target: The address to target in requests
            notes: An optional note about the rule

        Raises:
            CloudFlareAPIError: On HTTP Error or Invaild JSON.

        Returns:
            dict: containing the Access Rule created
        """

        # grab URL components and remove from kwargs
        zone_id = kwargs['zone_id']
        del kwargs['zone_id']

        # set up target configuration
        target_config = {
                'target': kwargs['target_type'],
                'value': kwargs['target']
        }
        del kwargs['target_type']
        del kwargs['target']
        kwargs['configuration'] = target_config

        # invoke API call
        func = self.client.zones.firewall.access_rules.rules.post  # pylint: disable=no-member
        result = self.invoke(func, zone_id, **kwargs)
        return result
