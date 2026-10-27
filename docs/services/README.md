# Self-Hosted Services

This directory contains documentation for services that are typically self-hosted in a homelab environment (e.g., TrueNAS SCALE).

## 🚀 Key Services
- [**n8n**](n8n.md) - Workflow automation.
- [**Nextcloud**](nextcloud.md) - Content collaboration.
- [**Ollama**](ollama.md) - Local LLM inference.
- [**Paperless-ngx**](paperless-ngx.md) - Document management.
- [**Tailscale**](tailscale.md) - Secure mesh networking.
- [**Immich**](immich.md) - High-performance photo management.
- [**Actual Budget**](actual-budget.md) - Privacy-focused personal finance.

## 📂 Full List
Refer to the [Main README](../index.md) or the `scripts/compare_agents.py` CLI tool for a complete list of all 90+ tools and services.

## When not to use it
- When cloud SaaS managed offerings provide strict SLAs and zero infrastructure maintenance overhead required by your enterprise.
- For non-persistent or temporary proof-of-concept tasks where container orchestration costs outweigh SaaS subscription costs.

## Getting started
Deploy core self-hosted services via Docker Compose on your local server:

```bash
docker pull n8nio/n8n:latest
docker pull ollama/ollama:latest
```

## CLI examples
Inspect and manage running self-hosted container services:

```bash
docker ps --filter "label=com.docker.compose.project=homelab"
docker logs --tail 50 ollama
docker exec -it n8n n8n export:workflow --all
```

## API examples
Verify service health endpoints programmatically:

```python
import urllib.request
import json

def check_ollama_health(host: str = "http://localhost:11434") -> str:
    req = urllib.request.Request(f"{host}/api/tags")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return f"Ollama operational with {len(data.get('models', []))} models loaded."

if __name__ == "__main__":
    print(check_ollama_health())
```
