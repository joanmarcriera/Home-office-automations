# Radicale

Radicale is a small but powerful CalDAV and CardDAV server.

## Description
It is lightweight and easy to set up, providing a way to host your own calendars and contacts.

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

## CLI examples
The `radicale` module supports several command-line flags:

```bash
# Print version
python3 -m radicale --version

# Run verification of local collections storage
python3 -m radicale --verify-storage

# Start with debug logging enabled
python3 -m radicale --debug
```

## API examples
As a CalDAV/CardDAV server, Radicale is accessed via standard DAV methods. You can use `curl` to create a collection:

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
