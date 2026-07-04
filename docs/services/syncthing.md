# Syncthing

## What it is
Syncthing is a continuous, decentralized file synchronization program. It allows you to synchronize files between two or more computers in real time, safely and securely, without relying on a central server or cloud provider. In July 2026, it is a foundational service for [Local LLM](../tools/ai_knowledge/local_llms.md) deployments, enabling the synchronization of model weights, datasets, and [MCP 3.0](../tools/automation_orchestration/mcp.md) configurations across edge nodes.

## What problem it solves
Managing files across multiple devices usually requires a central cloud service, which can pose privacy risks and incur costs. Syncthing solves this by providing a peer-to-peer synchronization mechanism that keeps data entirely on your own hardware, ensuring data sovereignty. It is especially useful for synchronizing [Obsidian](../knowledge_base/README.md) vaults and [Claude skills](../knowledge_base/patterns/skills-best-practices.md) across private networks.

## Where it fits in the stack
**Category**: Services / Data Synchronization. It sits in the **storage and sync** layer of a self-hosted environment, providing the backbone for data consistency, often managed via [Docker](../tools/infrastructure/docker.md).

## Typical use cases
- **Multi-Device File Sync**: Syncing a "Work" folder between a desktop and a laptop.
- **Automated Backups**: Backing up photos from an Android phone to a home server automatically (often paired with [Immich](immich.md)).
- **Knowledge Base Sync**: Synchronizing an [Obsidian](../knowledge_base/README.md) vault or KeepassXC database across devices.
- **Local LLM Data Sync**: Distributing model weights and [MCP 3.0](../tools/automation_orchestration/mcp.md) tool configurations across a fleet of [Local LLM](../tools/ai_knowledge/local_llms.md) agents.

## Strengths
- **Private and Secure**: Data never leaves your devices. Transfers are encrypted with TLS and authenticated using cryptographic certificates.
- **Decentralized**: No central server to fail; it operates entirely peer-to-peer.
- **Efficient**: Uses a block-based synchronization algorithm to only transfer changed parts of files.
- **Cross-Platform**: Broad support for Linux, Windows, macOS, Android, and [Docker](../tools/infrastructure/docker.md).

## Limitations
- **Not a Backup Tool**: While it has file versioning, it is primarily for sync. Deleting a file on one device deletes it on all unless "Send Only" folders are used.
- **Initial Setup**: Connecting devices requires exchanging long Device IDs, which can be cumbersome.
- **No Native iOS App**: Requires third-party alternatives like Möbius Sync.
- **Resource Usage**: Can be resource-intensive when indexing very large [Local LLM](../tools/ai_knowledge/local_llms.md) datasets.

## When to use it
- When you need to sync files across multiple devices without relying on a central cloud provider.
- For private, encrypted, and decentralized data synchronization in a [self-hosted](../tools/infrastructure/docker.md) environment.
- When you want to maintain full control over your data, bandwidth, and synchronization frequency.

## When not to use it
- If you need a full backup solution with deep historical versioning (consider a dedicated backup service).
- If you require a collaborative real-time editing environment like Google Docs.
- For users who prefer a simple "link-based" sharing model common in centralized cloud services.

## Getting started

### Installation
Syncthing is available as a single binary. On Linux, it can be installed via the official APT repository or [Docker](../tools/infrastructure/docker.md).

```bash
# Example: Install using Docker for a persistent node
docker run -d \
  --name=syncthing \
  -p 8384:8384 -p 22000:22000/tcp -p 22000:22000/udp \
  -v /path/to/data:/var/syncthing \
  syncthing/syncthing:latest
```

### Basic Configuration
1. Start Syncthing and open the Web GUI at `http://localhost:8384`.
2. On your **first device**, go to **Actions > Show ID** and copy the ID.
3. On your **second device**, click **Add Remote Device** and paste the ID.
4. Accept the connection on the first device.
5. Create a folder and share it with the second device to begin synchronization.

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
# Trigger a scan for a specific folder (e.g., your Obsidian vault)
curl -X POST -H "X-API-Key: <your_api_key>" \
     "http://localhost:8384/rest/db/scan?folder=default"
```

## Related tools / concepts
- [Nextcloud](nextcloud.md) — full suite of self-hosted cloud services.
- [Rclone Automation](rclone-automation.md) — for syncing data to public cloud providers.
- [Tailscale](tailscale.md) — to connect devices across different networks securely.
- [Docker](../tools/infrastructure/docker.md) — for consistent deployment.
- [Local LLM](../tools/ai_knowledge/local_llms.md) — the primary consumer of synchronized weights and data.
- [Obsidian](../knowledge_base/README.md) — popular knowledge base using Syncthing for sync.
- [Immich](immich.md) — self-hosted photo management.
- [MCP 3.0](../tools/automation_orchestration/mcp.md) — protocol for tool configurations synced by Syncthing.

## Sources / references
- [Official Website](https://syncthing.net/)
- [Syncthing Documentation](https://docs.syncthing.net/)
- [Syncthing REST API Reference](https://docs.syncthing.net/dev/rest.html)
- [Self-Hosting Guide: Decentralized Sync](https://selfhosted.show/syncthing-guide)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
