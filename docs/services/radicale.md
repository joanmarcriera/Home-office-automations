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

### Running Radicale
To start the server with default settings (binds to `localhost:5232`):

```bash
python3 -m radicale
```

### Hello World
1. Access the web interface at `http://localhost:5232`.
2. Log in with any username and password (default configuration allows any login).
3. Use the web interface to create your first **Calendar** or **Address book** collection.

## CLI examples
The `radicale` module supports several command-line flags for configuration and maintenance:

```bash
# Print version information
python3 -m radicale --version

# Run verification of local collections storage
python3 -m radicale --verify-storage

# Start the server with a custom storage path and debug logging
python3 -m radicale --storage-filesystem-folder=/path/to/collections --debug
```

## API examples
As a CalDAV/CardDAV server, Radicale is accessed via standard DAV methods.

### Python Example
Using the `requests` library to fetch collections (requires authentication if configured):

```python
import requests

url = "http://localhost:5232/username/"
response = requests.request("PROPFIND", url, auth=("username", "password"), headers={"Depth": "1"})

print(response.text)
```

### Curl Example
```bash
# Create a new calendar collection
curl -u username:password -X MKCOL "http://localhost:5232/username/calendar/"
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

- Last reviewed: 2026-03-02
- Confidence: high
