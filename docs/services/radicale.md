# Radicale

Radicale is a small but powerful CalDAV and CardDAV server.

## Description
It is lightweight and easy to set up, providing a way to host your own calendars and contacts.

## When to use it
- When you want a simple, lightweight, and self-hosted CalDAV/CardDAV server for personal use.
- When you want to keep your calendars and contacts in a simple, file-based storage format.
- For syncing contacts and calendars across devices without relying on third-party cloud services.

## When not to use it
- If you need a full collaborative groupware suite with email and file storage (consider [Nextcloud](nextcloud.md) instead).
- If you require advanced sharing and permission features beyond simple user-based collection isolation.

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

### Python Example
Fetch collection details using the `requests` library:

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

### Curl Example
```bash
# Delete a collection
curl -u admin:password -X DELETE "http://localhost:5232/admin/calendar/"
```

## Links
- [Official Website](https://radicale.org/)
- [GitHub Repository](https://github.com/Kozea/Radicale)

## Alternatives
- [Nextcloud (Contacts/Calendar)](nextcloud.md)
- [Baikal](https://sabre.io/baikal/)

## Backlog
- Integration with Vikunja for shared task lists.

## Sources / References

- [Radicale Documentation](https://radicale.org/v3.html)
- [Installation Guide](https://radicale.org/v3.html#installation)

## Contribution Metadata

- Last reviewed: 2026-05-04
- Confidence: high
