# Ollama Service Documentation

## Service Overview
Ollama allows for running open-source large language models (LLMs) locally.

## Purpose / Business Value
Provides a private reasoning engine for home automation and coding assistance without data leaving the home lab.

## Why Self-Hosted
To ensure absolute privacy of AI queries and reduce reliance on cloud LLM providers.

## Data Location
`/mnt/<pool>/applications/ollama/`

## Backup Strategy
- Model weights can be re-downloaded; configuration datasets should be snapshotted.

## Network Exposure
- **LAN**: Port 11434.
- **Tailscale**: For remote coding assistance (Aider/VS Code).

## Authentication Method
None by default (usually used internally); can be secured via proxy.

## Dependencies
- High-performance CPU or GPU.

## Resource Usage Notes
High; requires significant CPU/GPU resources and RAM depending on the model being run.

## Security Considerations
Do not expose the Ollama API directly to the public internet.

## Maintenance Tasks
- Monitoring memory usage.
- Updating models to the latest versions.

## Upgrade Procedure
Update the Ollama binary or Docker image.
