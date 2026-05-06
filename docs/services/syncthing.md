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
The easiest way to install Syncthing on Linux is via the official APT repository (for Debian/Ubuntu) or by downloading the [pre-compiled binaries](https://syncthing.net/downloads/).

```bash
# Example: Download and extract for Linux 64-bit
curl -L https://github.com/syncthing/syncthing/releases/latest/download/syncthing-linux-amd64-v1.27.6.tar.gz | tar xz
cd syncthing-linux-amd64-*
./syncthing
```

### Hello World
1. Start Syncthing: `./syncthing`. The Web GUI will open at `http://localhost:8384`.
2. On your **first device**, go to **Actions > Show ID** and copy the long string.
3. On your **second device**, click **Add Remote Device** and paste the ID from the first device.
4. On the **first device**, a notification will appear; click **Add Device** to confirm.
5. In the **Default Folder** settings on either device, go to the **Sharing** tab and check the other device to start syncing files in `~/Sync`.

## CLI examples
The `syncthing` binary handles both service execution and configuration tasks:

```bash
# Generate a new API key and configuration without starting the GUI
syncthing --generate="/path/to/config"

# Reset the GUI password if you are locked out
syncthing --gui-password="newpassword" --gui-user="admin"

# Check the version and build information
syncthing --version
```

## API examples
Syncthing's REST API is comprehensive. Find your API key in **Actions > Settings > General**.

### Python Example
```python
import requests

# Fetch the current system status and resource usage
url = "http://localhost:8384/rest/system/status"
headers = {"X-API-Key": "YOUR_API_KEY"}

response = requests.get(url, headers=headers)
if response.ok:
    status = response.json()
    print(f"Syncthing Version: {status['version']}, Uptime: {status['uptime']}s")
```

### Curl Example
```bash
# Force a rescan of a specific folder (replace 'default' with your folder ID)
curl -X POST -H "X-API-Key: <your_api_key>" \
     "http://localhost:8384/rest/db/scan?folder=default"
```

## Links
- [Official Website](https://syncthing.net/)
- [Documentation](https://docs.syncthing.net/)

## Related tools / concepts
- [Nextcloud](nextcloud.md) (Alternative storage/sync)
- [Rclone Automation](rclone-automation.md) (For cloud sync)
- [Tailscale](tailscale.md) (For secure peer-to-peer connection)
- [Docker](../tools/infrastructure/docker.md) (Common deployment method)
- [Storj](storj.md) (Decentralized storage alternative)

## Backlog
- Configure selective sync for mobile devices.

## Sources / References

- [Getting Started Guide](https://docs.syncthing.net/intro/getting-started.html)
- [REST API Documentation](https://docs.syncthing.net/dev/rest.html)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
