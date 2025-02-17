# Change Log

# 1.0.1

- Updated files to work with latest CI updates

# 1.0.0

- Fixed mocks for tests
- Drop Python 2.7 support

# 0.4.1

- Converted maintainer over to Encore Technologies
- `api_key` in pack config is now marked with `secure: true` so it will not leak
  sensitive data.
  
  Contributed by Nick Maludy (Encore Technologies)

# 0.4.0

- Migrated to using [python-cloudflare](https://github.com/cloudflare/python-cloudflare)
  instead of plain requests.
- Fixed API calls that require authentication by adding a new config parameters
  `api_email`. This new config parameter is required for any API calls that require
  authentication.
- Added support for handling paged results.
- Added new action `get_zones` that lists the DNS zones associated with your account.
- Added new action `get_zone_dns_records` that lists the DNS records in a zone.
  
  Above changes Contributed by Nick Maludy (Encore Technologies)

# 0.3.3

- Minor linting fixes
  
# 0.3.1

- Include a user-agent string in the headers, as this is now required
  to get a reply from the Cloudflare API.

# 0.3

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.

# 0.1

- First release with a single action (get_ips).
