# Paperless-ngx Service Documentation

## Service Overview
Paperless-ngx is a document management system that transforms your physical documents into a searchable online archive.

## Purpose / Business Value
Eliminates paper clutter and provides rapid, searchable access to all family and office documents.

## Why Self-Hosted
Privacy of sensitive personal documents is paramount.

## Data Location
`/mnt/<pool>/applications/paperless-ngx/`

## Backup Strategy
- ZFS snapshots of the document and metadata datasets.
- Exporting the database using `document_exporter` periodically.

## Network Exposure
- **LAN**: Port 8000.
- **Reverse Proxy**: Secure remote access for document lookup.

## Authentication Method
Built-in authentication.

## Dependencies
- Redis, PostgreSQL, Tika (optional), Gotenberg (optional).

## Resource Usage Notes
Moderate; indexing and OCR can be CPU intensive.

## Security Considerations
Isolate the web interface. Regularly update to ensure OCR vulnerabilities are patched.

## Maintenance Tasks
- Monitoring the consumption directory.
- Running the document sanity checker.

## Upgrade Procedure
Update the docker image and run migrations.
