# Consolidated Services Inventory

This table provides a high-level overview of all services running in the TrueNAS SCALE home lab environment.

| Service Name | Purpose | Image | Data Path | Exposure |
| :--- | :--- | :--- | :--- | :--- |
| **Nextcloud** | File Storage & Sync | `nextcloud:latest` | `/mnt/<pool>/applications/nextcloud/` | Reverse Proxy / LAN |
| **Paperless-ngx** | Document Management | `ghcr.io/paperless-ngx/paperless-ngx` | `/mnt/<pool>/applications/paperless-ngx/` | Reverse Proxy / LAN |
| **n8n** | Workflow Automation | `docker.n8n.io/n8nio/n8n` | `/mnt/<pool>/applications/n8n/` | Reverse Proxy / LAN |
| **Home Assistant** | Smart Home Control | `homeassistant/home-assistant` | `/mnt/<pool>/applications/home-assistant/` | Reverse Proxy / LAN |
| **Ollama** | Local LLM Runner | `ollama/ollama` | `/mnt/<pool>/applications/ollama/` | LAN / Tailscale |
| **Jellyfin** | Media Streaming | `jellyfin/jellyfin` | `/mnt/<pool>/applications/jellyfin/` | Reverse Proxy / LAN |
| **Vikunja** | Task Management | `vikunja/vikunja` | `/mnt/<pool>/applications/vikunja/` | Reverse Proxy / LAN |
| **Linkwarden** | Bookmark Manager | `ghcr.io/linkwarden/linkwarden` | `/mnt/<pool>/applications/linkwarden/` | Reverse Proxy / LAN |
| **Habitica** | Gamified Tasks | `habitica/habitica` | `/mnt/<pool>/applications/habitica/` | LAN / Tailscale |
| **Focalboard** | Project Management | `mattermost/focalboard` | `/mnt/<pool>/applications/focalboard/` | LAN / Tailscale |
| **qBittorrent** | Torrent Client | `linuxserver/qbittorrent` | `/mnt/<pool>/applications/qbittorrent/` | LAN (VPN) |
| **Jackett** | Tracker Proxy | `linuxserver/jackett` | `/mnt/<pool>/applications/jackett/` | LAN |
| **Diskover** | Disk Analysis | `diskover/diskover` | `/mnt/<pool>/applications/diskover/` | LAN |
| **Storj Node** | Decentralized Storage | `storjlabs/storagenode` | `/mnt/<pool>/applications/storj/` | WAN (Port Forward) |
| **Radicale** | CalDAV Server | `tomschroeder/radicale` | `/mnt/<pool>/applications/radicale/` | Reverse Proxy / LAN |
| **LiteLLM** | LLM Proxy | `ghcr.io/berriai/litellm` | `/mnt/<pool>/applications/litellm/` | LAN / Tailscale |
| **rclone** | Cloud Sync | `rclone/rclone` | `/mnt/<pool>/applications/rclone/` | N/A (CLI/Cron) |

---

## Infrastructure Gaps & Risks
- **Direct Discovery**: Automated service discovery was restricted due to lack of direct `k3s`/`midclt` access from the development environment. Documentation is based on "Known Services" requirements and expected TrueNAS patterns.
- **Secret Management**: Need to ensure all `.env` files are properly excluded from version control and secrets are managed via a dedicated manager (e.g., Vault or TrueNAS Secrets).
- **ZFS Dataset Alignment**: Verified dataset paths should be updated in the individual service files once the final pool structure is confirmed.
- **Monitoring**: Integration of a centralized monitoring stack (Prometheus/Grafana) is identified as a short-term roadmap item.
