# Task Decomposition: Batch 92 (Service Maintenance & Health)

This report implements **Action C** for the remaining technical debt and feature backlogs identified in the `docs/services/` directory. These items are divided into thematic sub-batches for future Ralph-loop runs.

## Sub-Batch 92.1: Automation & Integration (High Priority)
Focus on connecting existing services via n8n or specialized APIs.
- [x] `docs/services/n8n.md`: Add golden test fixtures for 20 real-world wine trade email scenarios.
- [x] `docs/services/n8n.md`: Add weekly Jules report: top 3 automation gaps and proposed PRs.
- [x] `docs/services/tika.md`: Integrate with n8n for automated PDF-to-Markdown conversion.
- [x] `docs/services/habitica.md`: API integration for automated habit scoring based on n8n workflows.

## Sub-Batch 92.2: Networking & Security
Focus on hardening and infrastructure access.
- [x] `docs/services/tailscale.md`: Setup Tailscale Exit Node on TrueNAS SCALE.
- [x] `docs/services/tailscale.md`: Configure MagicDNS for easy service access.
- [x] `docs/services/tailscale.md`: Add an ACL example for separating family devices from automation runners.
- [x] `docs/services/qbittorrent.md`: Setup WireGuard VPN killswitch for the qBittorrent container.
- [x] `docs/services/portracker.md`: Set up alerts for unexpected port changes.

## Sub-Batch 92.3: Media & Content Management
Focus on enriching the media stack and archival automation.
- [x] `docs/services/jellyfin.md`: Integrate with Gelli (Android music client).
- [x] `docs/services/plex.md`: Configure Plex Meta Manager for automated collection management.
- [x] `docs/services/tubearchivist.md`: Configure automated downloads for subscribed channels.
- [x] `docs/services/kiwix.md`: Set up automated downloads for new ZIM files.
- [x] `docs/services/linkwarden.md`: Browser extension integration.

## Sub-Batch 92.4: Productivity & Storage
Focus on utility accessibility and data durability.
- [ ] `docs/services/it-tools.md`: Host locally on TrueNAS for offline developer support.
- [ ] `docs/services/drawio.md`: Set up self-hosted instance on TrueNAS for offline access.
- [ ] `docs/services/storj.md`: Configure as a backup target for Rclone.
- [ ] `docs/services/rclone-automation.md`: Implement bandwidth throttling during business hours.
- [ ] `docs/services/rclone-automation.md`: Set up healthcheck notifications for failed syncs.
- [ ] `docs/services/grocy.md`: Set up barcode scanning via mobile app.
- [ ] `docs/services/focalboard.md`: Sync with Nextcloud Tasks.
- [ ] `docs/services/speedtest.md`: Create a dashboard for visualizing speedtest results over time.

---
- Status: Actionable backlog created.
- Next Step: Process Sub-Batch 92.1 in the next Ralph-loop run.
- Date: 2026-05-24
- Created by: Jules
