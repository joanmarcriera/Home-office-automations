# Radicale

## What it is
Radicale is a small but powerful CalDAV (calendar) and CardDAV (contact) server. It is written in Python and is designed to be lightweight and easy to set up.

## What problem it solves
It allows individuals and small groups to host their own calendars and contacts privately, without relying on large corporate cloud providers. It uses a simple, file-based storage format (iCalendar and vCard), making it easy to backup and manage.

## Where it fits in the stack
**Category**: Services / Calendar & Tasks. It serves as the primary "Intake & Storage" layer for personal scheduling and contact data.

## Typical use cases
- Syncing personal calendars across desktop (Thunderbird) and mobile (Android/iOS) devices.
- Hosting a shared family calendar.
- Storing a private address book that is accessible from multiple devices.
- Serving as a backend for task management tools that support CalDAV.

## Strengths
- **Lightweight**: Minimal CPU and memory usage.
- **Simple Storage**: Uses standard .ics and .vcf files on disk.
- **Extensible**: Supports various authentication backends (htpasswd, LDAP, remote user).
- **Standards-Compliant**: Works with a wide range of CalDAV and CardDAV clients.

## Limitations
- **No Built-in Web Client**: Primarily designed to be used with external clients, though it has a minimal admin UI.
- **Single-Server Focus**: Not designed for massive, multi-server deployments.

## When to use it
- When you want a simple, self-hosted solution for syncing calendars and contacts.
- When you value data privacy and want to own your scheduling data in a simple format.

## When not to use it
- For enterprise-grade collaboration with complex resource booking and email integration (use [Nextcloud](nextcloud.md) or SOGo).
- If you require a full-featured web interface for managing appointments.

## Getting started

### Installation
Install Radicale using `pip`:

```bash
python3 -m pip install --upgrade radicale
```

### Basic Setup
For a secure setup, create a configuration file and a users file:

```bash
# Create a user 'admin' with a password (requires htpasswd from apache2-utils)
htpasswd -c /path/to/users admin

# Create a basic config (config.ini)
cat <<EOF > config.ini
[auth]
type = htpasswd
htpasswd_filename = /path/to/users
htpasswd_encryption = autodetect

[server]
hosts = 0.0.0.0:5232
EOF
```

### Running Radicale
```bash
python3 -m radicale --config config.ini
```

### Hello World
1. Access the web interface at `http://localhost:5232`.
2. Log in with the username and password you created via `htpasswd`.
3. Click **Create new collection** and choose **Calendar**.
4. Name your collection (e.g., "Work") and click **Create**.
5. You now have a CalDAV URL you can use in clients like Thunderbird or DAVx⁵.

## CLI examples
The `radicale` module provides several maintenance and configuration utilities:

```bash
# Verify the integrity of the local collections storage
python3 -m radicale --verify-storage

# Check the version of the installed Radicale package
python3 -m radicale --version

# Verify a specific item file (e.g., a .ics file) for errors
python3 -m radicale --verify-item /path/to/collection/item.ics
```

## API examples
Radicale is a CalDAV/CardDAV server and uses standard HTTP methods like `PROPFIND` and `MKCOL`.

### Python (Listing Collections)
```python
import requests

url = "http://localhost:5232/admin/"
# PROPFIND is used to discover collections
response = requests.request(
    "PROPFIND",
    url,
    auth=("admin", "your_password"),
    headers={"Depth": "1"}
)

print(f"Collections for admin:\n{response.text}")
```

### curl (Deleting a Collection)
```bash
curl -u admin:password -X DELETE "http://localhost:5232/admin/calendar/"
```

## Licensing and cost
- **Open Source**: Yes (GPL-3.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Nextcloud (Contacts/Calendar)](nextcloud.md) (Alternative storage)
- [Vikunja](vikunja.md) (Task management)
- [DAVx⁵](https://www.davx5.com/) (Standard Android sync client)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) (To expose CalDAV to AI agents)
- [Google Calendar](../tools/calendar_tasks/google_calendar.md) (Public alternative)

## Sources / References
- [Official Website](https://radicale.org/)
- [GitHub Repository](https://github.com/Kozea/Radicale)
- [Radicale Documentation](https://radicale.org/v3.html)

## Backlog

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
