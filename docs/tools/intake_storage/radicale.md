# Radicale

## What it is
Radicale is a complete CalDAV (calendar) and CardDAV (contact) server solution. It is a small but powerful application.

## What problem it solves
It provides a dedicated, lightweight, and simple self-hosted server for syncing calendars and contacts without the overhead of a full suite like Nextcloud.

## Where it fits in the pipeline
**Store / Sync**

## Typical use cases (in this homelab / family automation context)
- **Minimalist Calendar Hosting**: Running a low-resource server specifically for family calendar sync.
- **Private Contacts Backup**: Hosting a private address book that is not shared with large cloud providers.

## Integration points
- **CalDAV/CardDAV Clients**: Native support in Android (via DAVx5), iOS, and Thunderbird.
- **Home Assistant**: Can be used as the calendar backend for smart home automations.

## Licensing and cost
- **Open Source**: Yes (GPL-3.0)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Extremely lightweight and fast.
- Simple configuration (often just a single file).
- Supports various storage backends (file system, database).

## Limitations
- No built-in web interface for managing events (requires a separate client).
- Limited built-in user management features compared to Nextcloud.

## Alternatives / Related tools
- **Nextcloud**
- **Baïkal**
- **Google Calendar**

## Links
- [Official Website](https://radicale.org/)
- [GitHub](https://github.com/Kozea/Radicale)
