from lib.actions import CloudflareBaseAction


class DeleteZoneAccessRuleAction(CloudflareBaseAction):
    def run(self, **kwargs):
        """
        Delete Access Rule in a Zone

        Args:
            zone_id: ID of the zone to delete from the access rule
            rule_id: ID of the rule to delete

        Raises:
            CloudFlareAPIError: On HTTP Error or Invaild JSON.

        Returns:
            dict: containing the Access Rule deleted
        """

        # grab URL components and remove from kwargs
        zone_id = kwargs['zone_id']
        del kwargs['zone_id']

        rule_id = kwargs['rule_id']
        del kwargs['rule_id']

        # invoke API call
        func = self.client.zones.firewall.access_rules.rules.delete  # pylint: disable=no-member
        result = self.invoke(func, zone_id, rule_id, **kwargs)
        return result
