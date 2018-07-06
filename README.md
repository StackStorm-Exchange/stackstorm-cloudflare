# Cloudflare Pack

A pack for interacting with the [Cloudflare API](https://api.cloudflare.com).

## Configuration

Copy the example configuration in [cloudflare.yaml.example](./cloudflare.yaml.example)
to `/opt/stackstorm/configs/cloudflare.yaml` and edit as required.

``` shell
cp /opt/stackstorm/packs/cloudflare/cloudflare.yaml.example /opt/stackstorm/configs/cloudflare.yaml
```

It should contain:

* ``api_key`` - Cloudflare API key, details [here](https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-)
* ``api_email`` - Cloudflare API email address (username)

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Actions

### get_ips

Returns the current IPs for the Cloudflare service, does not require an API key.

### get_zones

Returns a list of the current DNS Zones in your Cloudflare account. Requires an API key.

### get_zone_dns_records

Returns a list of the DNS Records in a given Zone. Requires an API key.
