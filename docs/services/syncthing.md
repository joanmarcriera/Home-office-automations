# Syncthing

Syncthing is a continuous file synchronization program.

## Description
It synchronizes files between two or more computers in real time, safely and securely.

## Getting started

### Installation
Download the latest binary for your operating system from the [official downloads page](https://syncthing.net/downloads/).

### Running Syncthing
Simply run the `syncthing` binary to start the service and open the web GUI:

```bash
./syncthing
```

The admin GUI will be available at `http://localhost:8384/`.

## CLI examples
The `syncthing` binary supports several command-line arguments:

```bash
# Show version information
syncthing --version

# Generate a new configuration and keys in the specified directory
syncthing --generate="/path/to/config"

# Set the GUI listen address
syncthing --gui-address="0.0.0.0:8384"
```

## API examples
Syncthing provides a REST API. Authenticate using the `X-API-Key` header:

```bash
# Get system version
curl -X GET -H "X-API-Key: <your_api_key>" \
     "http://localhost:8384/rest/system/version"
```

## Links
- [Official Website](https://syncthing.net/)
- [Documentation](https://docs.syncthing.net/)

## Alternatives
- [Resilio Sync](https://www.resilio.com/) (Non-OSS)
- [Nextcloud](nextcloud.md)

## Backlog
- Configure selective sync for mobile devices.

## Sources / References

- [Getting Started Guide](https://docs.syncthing.net/intro/getting-started.html)
- [REST API Documentation](https://docs.syncthing.net/dev/rest.html)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
