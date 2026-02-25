# LiteLLM Service Documentation

## Service Overview
LiteLLM is a universal proxy for LLM APIs, providing a unified interface for multiple providers.

## Purpose / Business Value
Simplifies the management of multiple AI models, handling failovers, retries, and budget tracking for all AI-powered services in the home lab.

## Why Self-Hosted
To provide a secure, centralized gateway for all local and cloud AI models.

## Data Location
`/mnt/<pool>/applications/litellm/`

## Backup Strategy
- `config.yaml` backup.
- Environment variable secrets stored in a secure manager.

## Network Exposure
- **LAN**: Port 4000.
- **Tailscale**: Private access for AI-powered development tools.

## Authentication Method
Master key or virtual keys for different services.

## Dependencies
- Connectivity to external LLM APIs (OpenAI, Anthropic, etc.) or local Ollama instances.

## Resource Usage Notes
Lightweight CPU usage; low RAM requirement.

## Security Considerations
Protect the master key. Do not expose the management UI to the WAN.

## Maintenance Tasks
- Monitoring API costs and usage.
- Updating configurations when new models are released.

## Upgrade Procedure
Update the docker image.
