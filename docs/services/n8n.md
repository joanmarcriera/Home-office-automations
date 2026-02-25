# n8n Service Documentation

## Service Overview
n8n is an extendable workflow automation tool.

## Purpose / Business Value
Acts as the central orchestrator for the home automation and data pipeline, connecting disparate services.

## Why Self-Hosted
Privacy of automation logic and avoidance of per-execution fees in cloud alternatives.

## Data Location
`/mnt/<pool>/applications/n8n/`

## Backup Strategy
- Weekly database dumps.
- Workflow exports.
- ZFS snapshots of the config directory.

## Network Exposure
- **LAN**: Port 5678.
- **Reverse Proxy**: Exposed for webhook reception from cloud services.

## Authentication Method
Built-in user accounts.

## Dependencies
- Database (PostgreSQL recommended), Node.js.

## Resource Usage Notes
Memory usage can increase with the number of active workflows.

## Security Considerations
Secure the webhook endpoint. Use credentials for all node integrations.

## Maintenance Tasks
- Workflow monitoring and error handling.
- Database vacuuming.

## Upgrade Procedure
Update the docker image.
