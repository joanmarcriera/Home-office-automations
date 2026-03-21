# Syncthing

Syncthing is a continuous file synchronization program.

## Description
It synchronizes files between two or more computers in real time, safely and securely.

## When to use it
- When you need to sync files across multiple devices without relying on a central cloud provider.
- For private, encrypted, and decentralized data synchronization.
- When you want to maintain full control over your data and bandwidth.

## When not to use it
- If you need a backup solution with historical versioning (Syncthing is primarily for sync, though it has basic versioning).
- If you require a collaborative editing environment like Google Docs or Microsoft 365.
- For users who prefer a simple "link-based" sharing model common in centralized cloud services.

## Getting started

### Installation
Download the latest binary for your operating system from the [official downloads page](https://syncthing.net/downloads/).

### Running Syncthing
Simply run the `syncthing` binary to start the service and open the web GUI:

```bash
./syncthing
```

### Hello World
1. After starting Syncthing, the admin GUI will open automatically at `http://localhost:8384/`.
2. Click on **Actions** (top right) and select **Show ID**.
3. This unique **Device ID** is what you will share with your other devices to establish a secure connection.

## CLI examples
The `syncthing` binary supports several command-line arguments for configuration and management:

```bash
# Show version information
syncthing --version

# Generate a new configuration and keys in the specified directory
syncthing --generate="/path/to/config"

# Set the GUI listen address manually
syncthing --gui-address="0.0.0.0:8384"
```

## API examples
Syncthing provides a REST API. Authenticate using the `X-API-Key` header (found in the Web GUI under Actions > Settings).

### Python Example
```python
import requests

url = "http://localhost:8384/rest/system/version"
headers = {
    "X-API-Key": "YOUR_API_KEY"
}

response = requests.get(url, headers=headers)
print(response.json())
```

### Curl Example
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
