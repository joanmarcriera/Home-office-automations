# Paperless-AI Service Documentation

## Service Overview
Paperless-AI adds a RAG-powered chat interface and semantic search to Paperless-ngx.

## Purpose / Business Value
Allows for natural language querying of the document archive, making it easier to extract information from stored files.

## Why Self-Hosted
To keep the indexing and reasoning of sensitive documents within the private infrastructure.

## Data Location
`/mnt/<pool>/applications/paperless-ai/`

## Backup Strategy
- Configuration and indexing state backed up via ZFS snapshots.

## Network Exposure
- **LAN**: Accessible via its own web UI or integrated into Paperless-ngx.

## Authentication Method
Pass-through from Paperless-ngx or standalone.

## Dependencies
- Paperless-ngx (API), Ollama or other LLM provider.

## Resource Usage Notes
Memory intensive due to vector storage and LLM inference.

## Security Considerations
Ensure API keys for LLM providers are secured.

## Maintenance Tasks
- Re-indexing when large amounts of new documents are added to Paperless.

## Upgrade Procedure
Update the docker image.
