# Syncthing

## What it is
Syncthing is a continuous, decentralized file synchronization program. It allows you to synchronize files between two or more computers in real time, safely and securely, without relying on a central server or cloud provider.

## What problem it solves
Managing files across multiple devices (desktop, laptop, mobile, NAS) usually requires a central cloud service like Dropbox or Google Drive, which can pose privacy risks and incur subscription costs. Syncthing solves this by providing a peer-to-peer synchronization mechanism that keeps data entirely on your own hardware.

## Where it fits in the stack
**Category**: Services / Data Synchronization. It sits in the **storage and sync** layer of a self-hosted environment, ensuring data consistency across the network.

## Typical use cases
- Syncing a "Work" folder between a desktop and a laptop.
- Automatically backing up photos from an Android phone to a home server.
- Synchronizing a KeepassXC database or Obsidian vault across multiple devices.
- Distributing configuration files across a fleet of servers.

## Strengths
- **Private and Secure**: Data never leaves your devices. Transfers are encrypted and authenticated.
- **Decentralized**: No central server to fail or be compromised.
- **Efficient**: Uses a block-based synchronization algorithm to only transfer changed parts of files.
- **Cross-Platform**: Runs on Linux, Windows, macOS, Android, and various BSDs.

## Limitations
- **Not a Backup Tool**: While it has file versioning, it is primarily for sync. Deleting a file on one device deletes it on all (unless "Send Only" is configured).
- **Initial Setup**: Connecting devices requires exchanging long Device IDs, which can be cumbersome for non-technical users.
- **No Native iOS App**: Due to OS limitations, there is no official iOS client (though third-party "Möbius Sync" exists).

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
curl -L https://github.com/syncthing/syncthing/releases/latest/download/syncthing-linux-amd64-v2.1.0.tar.gz | tar xz
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

## Licensing and cost
- **Open Source**: Yes (MPL-2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Nextcloud](nextcloud.md) — for a full suite of cloud services beyond just sync
- [Rclone Automation](rclone-automation.md) — for syncing data to public cloud providers
- [Tailscale](tailscale.md) — to connect devices across different networks securely
- [Docker](../tools/infrastructure/docker.md) — for consistent deployment in a homelab
- [Storj](storj.md) — for decentralized, encrypted cloud storage
- [Immich](immich.md) — for self-hosted photo management (often paired with Syncthing)

## Advanced Configuration (v2.1.0+)

### Folder Grouping
Syncthing v2.1.0 introduces **Folder Grouping** to the Web GUI, allowing you to categorize folders into logical sets (e.g., "Work", "Personal", "Backups"). This is purely a UI enhancement and does not affect the underlying sync protocol. To group folders, use the "Edit" dialog for a folder and set a group name in the "General" tab.

### Proxy Support
Syncthing now supports global proxy configuration for all outgoing connections, including discovery and relay servers. This is useful for environments with restricted internet access.
- **SOCKS5/HTTP**: Configurable via `config.xml` or the GUI under **Actions > Settings > Connections**.
- **Environment Variables**: Use `all_proxy` or `https_proxy` to direct traffic through a local tunnel.

## Selective Sync & Ignore Patterns
Syncthing allows fine-grained control over which files are synchronized using `.stignore` files. This is particularly useful for mobile devices with limited storage or for excluding temporary build artifacts.

### Using .stignore
Create a file named `.stignore` in the root of your shared folder. Each line defines a pattern to ignore:

```text
// Ignore temporary files
(?i)~*
*.tmp

// Ignore specific directories
/node_modules
/target
/.cache

// Ignore by file extension
*.log
```

### Mobile Selective Sync
On Android, you can enable "Selective Sync" in the Syncthing app settings for a specific folder. This allows you to see the file structure without downloading the actual content until requested. For iOS (Möbius Sync), utilize "Ignore Patterns" to prevent large directories from syncing to the device.

## Backlog
- [x] Perform quarterly technical freshness audit.

## Sources / References
- [Official Website](https://syncthing.net/)
- [Getting Started Guide](https://docs.syncthing.net/intro/getting-started.html)
- [REST API Documentation](https://docs.syncthing.net/dev/rest.html)

## Contribution Metadata
- Last reviewed: 2026-05-25
- Confidence: high
