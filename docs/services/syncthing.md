# Syncthing

## What it is
Syncthing is a continuous, decentralized file synchronization program. It allows you to synchronize files between two or more computers in real time, safely and securely, without relying on a central server or cloud provider.

## What problem it solves
Managing files across multiple devices (desktop, laptop, mobile, NAS) usually requires a central cloud service like Dropbox or Google Drive, which can pose privacy risks and incur subscription costs. Syncthing solves this by providing a peer-to-peer synchronization mechanism that keeps data entirely on your own hardware, ensuring data sovereignty and privacy.

## Where it fits in the stack
**Category**: Services / Data Synchronization. It sits in the **storage and sync** layer of a self-hosted environment, providing the backbone for data consistency across a private network.

## Typical use cases
- **Multi-Device File Sync**: Syncing a "Work" folder between a desktop and a laptop.
- **Automated Backups**: Backing up photos from an Android phone to a home server automatically.
- **Knowledge Base Sync**: Synchronizing a KeepassXC database or [Obsidian](../knowledge_base/README.md) vault across devices.
- **Agentic Configuration**: Distributing configuration files for [Claude skills](../knowledge_base/patterns/skills-best-practices.md) across a fleet of local agents.

## Strengths
- **Private and Secure**: Data never leaves your devices. Transfers are encrypted with TLS and authenticated using cryptographic certificates.
- **Decentralized**: No central server to fail or be compromised; it operates entirely peer-to-peer.
- **Efficient**: Uses a block-based synchronization algorithm to only transfer changed parts of files, saving bandwidth.
- **Cross-Platform**: Broad support for Linux, Windows, macOS, Android, and various BSDs.

## Limitations
- **Not a Backup Tool**: While it has file versioning, it is primarily for sync. Deleting a file on one device deletes it on all unless specific configurations like "Send Only" are used.
- **Initial Setup**: Connecting devices requires exchanging long Device IDs, which can be cumbersome for non-technical users.
- **No Native iOS App**: Due to OS limitations, there is no official iOS client, requiring third-party alternatives like Möbius Sync.

## When to use it
- When you need to sync files across multiple devices without relying on a central cloud provider.
- For private, encrypted, and decentralized data synchronization in a homelab environment.
- When you want to maintain full control over your data, bandwidth, and synchronization frequency.

## When not to use it
- If you need a full backup solution with deep historical versioning and off-site redundancy.
- If you require a collaborative real-time editing environment like Google Docs.
- For users who prefer a simple "link-based" sharing model common in centralized cloud services.

## Getting started

### Installation
Syncthing is available as a single binary. On Linux, it can be installed via the official APT repository or by downloading the latest release.

```bash
# Example: Download and extract for Linux 64-bit
curl -L https://github.com/syncthing/syncthing/releases/latest/download/syncthing-linux-amd64-v2.1.0.tar.gz | tar xz
cd syncthing-linux-amd64-*
./syncthing
```

### Basic Configuration
1. Start Syncthing: `./syncthing`. The Web GUI will open at `http://localhost:8384`.
2. On your **first device**, go to **Actions > Show ID** and copy the ID.
3. On your **second device**, click **Add Remote Device** and paste the ID.
4. Accept the connection on the first device to establish a trusted link.

## CLI examples

### Service Management
```bash
# Check the version and build information
syncthing --version

# Generate a new API key and configuration
syncthing --generate="/path/to/config"
```

### Reset GUI Access
```bash
# Reset the GUI password if you are locked out
syncthing --gui-password="newpassword" --gui-user="admin"
```

## API examples

### Fetching System Status (Python)
Syncthing's REST API is comprehensive. Find your API key in **Actions > Settings > General**.

```python
import requests

url = "http://localhost:8384/rest/system/status"
headers = {"X-API-Key": "YOUR_API_KEY"}

response = requests.get(url, headers=headers)
if response.ok:
    status = response.json()
    print(f"Syncthing Version: {status['version']}, Uptime: {status['uptime']}s")
```

### Triggering a Folder Scan (cURL)
```bash
curl -X POST -H "X-API-Key: <your_api_key>" \
     "http://localhost:8384/rest/db/scan?folder=default"
```

## Related tools / concepts
- [Nextcloud](nextcloud.md) — for a full suite of self-hosted cloud services
- [Rclone Automation](rclone-automation.md) — for syncing data to public cloud providers
- [Tailscale](tailscale.md) — to connect devices across different networks securely
- [Docker](../tools/infrastructure/docker.md) — for consistent deployment of Syncthing nodes
- [Storj](storj.md) — for decentralized, encrypted cloud storage
- [Immich](immich.md) — for self-hosted photo management (often paired with Syncthing)
- [Obsidian](../knowledge_base/README.md) — a popular knowledge base that uses Syncthing for mobile sync

## Sources / references
- [Official Website](https://syncthing.net/)
- [Syncthing Documentation](https://docs.syncthing.net/)
- [Syncthing REST API Reference](https://docs.syncthing.net/dev/rest.html)
- [Syncthing v2.1.0 Release Notes](https://github.com/syncthing/syncthing/releases/tag/v2.1.0)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
