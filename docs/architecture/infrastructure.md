# Home Lab Architecture Overview

## Infrastructure Environment: TrueNAS SCALE
The primary infrastructure for this home lab is built on **TrueNAS SCALE**, an open-source storage platform based on Debian GNU/Linux. It provides a robust foundation for running containerized services and managing large-scale ZFS storage pools.

### Core Components
1.  **ZFS Storage**: All persistent data is stored on ZFS pools (e.g., `tank`). This ensures data integrity with features like snapshots, replication, and self-healing.
2.  **App Management**: Services are deployed as Docker containers or Kubernetes pods (via TrueNAS Apps/Charts).
3.  **Network**: Services are primarily accessed over the local network (LAN) or securely via a **Tailscale** mesh network. A reverse proxy (Traefik/Nginx) handles TLS and subdomain routing.

## Service Interaction Map
Services are organized into a functional pipeline to handle information and automation.

### 1. Ingest & Storage
Raw data enters the system through email (IMAP), scanners, or manual uploads. It is stored in dedicated ZFS datasets within `/mnt/<pool>/applications/`.
- **Services**: [Paperless-ngx](../services/paperless-ngx.md), [Nextcloud](../services/nextcloud.md), [Syncthing](../services/syncthing.md), [qBittorrent](../services/qbittorrent.md).

### 2. Process & Understanding
Stored data is processed for OCR and analyzed using local reasoning engines.
- **Services**: [Ollama](../services/ollama.md), [LiteLLM](../services/litellm.md), [Paperless-AI](../services/paperless-ai.md), [Diskover](../services/diskover.md).

### 3. Automation & Orchestration
Workflows connect services to perform complex tasks, such as extracting events from documents and syncing them to calendars.
- **Services**: [n8n](../services/n8n.md), [Home Assistant](../services/home-assistant.md).

### 4. Productivity & Synchronization
The final outcomes are synced to user-facing applications like calendars, task managers, and knowledge bases.
- **Services**: [Vikunja](../services/vikunja.md), [Radicale](../services/radicale.md), [Obsidian](../tools/ai_knowledge/obsidian.md).

### 5. Benchmarking & Quality Assurance
Continuous evaluation of model performance and reasoning accuracy.
- **Services**: [HLE](../tools/benchmarking/humanitys-last-exam.md), [Terminal-Bench](../tools/benchmarking/terminal-bench.md), [Ollama Benchmark CLI](../tools/benchmarking/ollama-benchmark-cli.md).

## Backup & Recovery
- **Local**: Scheduled ZFS snapshots of all application datasets.
- **Offsite**: Periodic synchronization of critical datasets to cloud storage using [rclone](../services/rclone-automation.md).
- **Configuration**: All infrastructure-as-code and configuration files are version-controlled in this repository.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
