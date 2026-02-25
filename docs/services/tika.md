# Apache Tika Service Documentation

## Service Overview
Apache Tika is a content analysis toolkit that detects and extracts metadata and text from over a thousand different file types.

## Purpose / Business Value
Provides a "Swiss Army knife" for document parsing. Essential for extracting content from complex files (Excel, PPT, PDF) before they are indexed by Paperless-ngx or processed by LLMs.

## Why Self-Hosted
To process sensitive documents locally without sending them to cloud-based extraction services.

## Data Location
- **Config**: /mnt/<pool>/applications/tika/
- **Temp**: /tmp/tika-server/

## Backup Strategy
- Stateless service; configuration backups via ZFS snapshots.

## Network Exposure
- **LAN**: Port 9998 (Server mode).
- **Internal**: Primarily accessed by Paperless-ngx or n8n.

## Authentication Method
None by default; usually protected by network isolation or reverse proxy basic auth.

## Dependencies
- Java Runtime Environment (if not in Docker).

## Resource Usage Notes
Moderate; memory usage spikes when parsing very large or complex documents.

## Security Considerations
Isolate the service from the public internet. Ensure it runs with limited permissions.

## Maintenance Tasks
- Monitoring for parsing errors in logs.

## Upgrade Procedure
Update the docker image.
