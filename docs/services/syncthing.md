# Syncthing

## What it is
Syncthing is a continuous, decentralized file synchronization program. It allows you to synchronize files between two or more computers in real time, safely and securely, without relying on a central server or cloud provider.

In late October / November 2026, Syncthing is a foundational service for decentralized edge networks and [Local LLMs](../tools/ai_knowledge/local_llms.md) (such as Gemma 3, Qwen 3.6, Llama 4, and Claude 5.1 edge configurations). It is widely utilized to synchronize massive LLM model weights, fine-tuning datasets, and [Model Context Protocol (MCP 3.1)](../tools/automation_orchestration/mcp.md) settings seamlessly across multiple homelab and remote edge nodes.

## What problem it solves
Managing files across multiple devices usually requires a central cloud service, which can pose privacy risks and incur high monthly subscription fees. Syncthing solves this by providing a peer-to-peer synchronization mechanism that keeps data entirely on your own hardware, ensuring complete data sovereignty.

In the AI-native workspace, Syncthing solves the bandwidth and latency challenges of distributing model updates to local inference servers. Instead of pulling multi-gigabyte GGUF weights repeatedly from Hugging Face over public WANs, homelab nodes can use local peer-to-peer synchronization to distribute model updates across the private network. It also guarantees secure, automated sync for private [Obsidian](../knowledge_base/multi-calendar-conflict-research.md) vaults and configuration stores.

## Where it fits in the stack
**Category**: Services / Data Synchronization. It sits in the **storage and sync** layer of a self-hosted environment, providing the backbone for data consistency, often managed via [Docker](../tools/infrastructure/docker.md).

## Typical use cases
- **Multi-Device File Sync**: Syncing a "Work" folder between a desktop and a laptop.
- **Automated Backups**: Backing up photos from an Android phone to a home server automatically (often paired with [Immich](immich.md)).
- **Knowledge Base Sync**: Synchronizing an [Obsidian](../knowledge_base/multi-calendar-conflict-research.md) vault or KeyPassXC database across devices.
- **Local LLM Data Sync**: Distributing model weights and [MCP 3.1](../tools/automation_orchestration/mcp.md) tool configurations across a fleet of local LLM agents.
- **Edge Deployment Ingestion**: Deploying automation scripts or workflow rules across a cluster of local [n8n](n8n.md) runners.

## Strengths
- **Private and Secure**: Data never leaves your devices. Transfers are encrypted with TLS and authenticated using cryptographic certificates.
- **Decentralized**: No central server to fail; it operates entirely peer-to-peer.
- **Efficient**: Uses a block-based synchronization algorithm to only transfer changed parts of files.
- **Cross-Platform**: Broad support for Linux, Windows, macOS, Android, and [Docker](../tools/infrastructure/docker.md).

## Limitations
- **Not a Backup Tool**: While it has file versioning, it is primarily for sync. Deleting a file on one device deletes it on all unless "Send Only" folders are used.
- **Initial Setup**: Connecting devices requires exchanging long Device IDs, which can be cumbersome.
- **No Native iOS App**: Requires third-party alternatives like Möbius Sync.
- **Resource Usage**: Can be resource-intensive when indexing very large LLM datasets.

## When to use it
- When you need to sync files across multiple devices without relying on a central cloud provider.
- For private, encrypted, and decentralized data synchronization in a self-hosted environment.
- When distributing multi-gigabyte LLM model weights across several local machines or Raspberry Pi 5 edge nodes.
- To maintain full control over your data, bandwidth, and synchronization frequency.

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

### Programmatic Syncthing Status Validation with Pydantic v2 (Python)
Checking the status of the local Syncthing service and validating the JSON API response against schema expectations.

```python
import os
import requests
from typing import Dict, Any
from pydantic import BaseModel, Field, field_validator

class SyncthingStatus(BaseModel):
    version: str = Field(..., description="Syncthing server version")
    uptime_seconds: int = Field(..., alias="uptime", description="Server uptime in seconds", ge=0)
    is_rest_enabled: bool = Field(default=True, description="Indicates if REST API is active")

    @field_validator("version")
    @classmethod
    def validate_version_format(cls, v: str) -> str:
        if not v.startswith("v") and not v[0].isdigit():
            raise ValueError("Invalid Syncthing version format")
        return v

# Main check function
def fetch_and_validate_status():
    api_key = os.environ.get("SYNCTHING_API_KEY", "default_dummy_key")
    url = "http://localhost:8384/rest/system/status"
    headers = {"X-API-Key": api_key}

    try:
        # For demonstration, mock a response if local service isn't active
        # In production, use: response = requests.get(url, headers=headers).json()
        mock_response = {
            "version": "v1.29.0",
            "uptime": 3600
        }

        status = SyncthingStatus.model_validate(mock_response)
        print("Validated Syncthing Status:", status.model_dump(by_alias=True))
    except Exception as e:
        print("Failed to validate system status:", e)

if __name__ == "__main__":
    fetch_and_validate_status()
```

### Triggering a Folder Scan (cURL)
```bash
# Trigger a scan for a specific folder (e.g., your Obsidian vault)
curl -X POST -H "X-API-Key: <your_api_key>" \
     "http://localhost:8384/rest/db/scan?folder=default"
```

## Related tools / concepts
- [Nextcloud](nextcloud.md) — Full suite of self-hosted cloud services.
- [Rclone Automation](rclone-automation.md) — For syncing data to public cloud providers.
- [Tailscale](tailscale.md) — To connect devices across different networks securely.
- [Docker](../tools/infrastructure/docker.md) — For consistent containerized deployment.
- [Local LLM](../tools/ai_knowledge/local_llms.md) — The primary consumer of synchronized weights and data.
- [Obsidian](../knowledge_base/multi-calendar-conflict-research.md) — Popular knowledge base using Syncthing for sync.
- [Immich](immich.md) — Self-hosted photo management.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Protocol for tool configurations synced by Syncthing.
- [n8n](n8n.md) — Workflow automation tool that can be triggered by folder scan completions.

## Sources / references
- [Official Website](https://syncthing.net/)
- [Syncthing Documentation](https://docs.syncthing.net/)
- [Syncthing REST API Reference](https://docs.syncthing.net/dev/rest.html)
- [Self-Hosting Guide: Decentralized Sync](https://selfhosted.show/syncthing-guide)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
