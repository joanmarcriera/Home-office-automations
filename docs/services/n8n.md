# n8n

## What it is
n8n is an extendable, source-available workflow automation platform with a visual node editor, robust API integrations, and first-class support for AI-powered workflow steps. It allows users to build complex, multi-step automations that connect hundreds of different services.

## What problem it solves
It replaces repetitive manual operations across tools and teams. Unlike cloud-only automation products, it can be self-hosted, ensuring that workflow logic, execution history, and sensitive data stay within your private infrastructure. It addresses the need for secure, auditable, and highly customizable business and household process automation.

## Where it fits in the stack
**Automation & Orchestration**. It is the control plane for cross-tool business and personal processes, sitting between intake services (email, webhooks) and action-oriented tools (CRMs, databases, smart home devices).

## Typical use cases
- **Autonomous Document Operations**: Classifying incoming content, extracting entities (using [Instructor](../tools/frameworks/instructor.md)), and routing to [Paperless-ngx](paperless-ngx.md).
- **AI-Assisted Operations**: Triage, summarize, and draft responses via Claude 4.8 Opus or GPT-5.5, with human-in-the-loop approval gates.
- **MCP Bridge**: Exposing n8n workflows as tools to AI agents using the Model Context Protocol (MCP).
- **Home Automation Integration**: Coordinating complex smart home scenarios that exceed the logic capabilities of Home Assistant's native YAML.

## Strengths
- **Visual + Programmable**: Offers an intuitive drag-and-drop editor while allowing for advanced JavaScript expressions and custom node development.
- **Self-Hostable**: Ensures data privacy and infrastructure control.
- **v2.13.0+ Features**: Native Data Tables for internal state, 1Password/AWS Secrets Manager integration, and first-class MCP support.
- **Observability**: Detailed execution logs and standardized error handling via "Error Trigger" nodes.

## Limitations
- **Learning Curve**: Designing robust, error-tolerant flows requires strong data modeling skills.
- **Resource Management**: High-volume usage requires "Queue Mode" with Redis and a persistent PostgreSQL database for scaling.
- **Credential Security**: Requires explicit discipline in managing secrets and environment separation.

## When to use it
- When you need long-running, auditable business or personal automations.
- If data privacy and self-hosting are organizational requirements.
- For AI-assisted processes where you need clear human-approval boundaries and complex tool orchestration.

## When not to use it
- For trivial, one-off scripts with no recurring lifecycle.
- When you prefer a fully managed SaaS experience and do not want to own the maintenance of the automation infrastructure.
- For real-time, low-latency processing where microsecond overhead is unacceptable.

## Getting started

### Installation (Docker Compose)
Production-oriented baseline using PostgreSQL for persistence.

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - ./postgres_data:/var/lib/postgresql/data

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    depends_on:
      - postgres
    ports:
      - 5678:5678
    volumes:
      - ./n8n_data:/home/node/.n8n
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
    restart: unless-stopped
```

## CLI examples

### Workflow Export/Import
Managing n8n configuration as code.

```bash
# Export all workflows to separate JSON files for version control
docker compose exec n8n n8n export:workflow --all --separate --output=/files/workflows

# Import workflows from a specific directory
docker compose exec n8n n8n import:workflow --separate --input=/files/workflows
```

### Administrative Tasks
Checking version and status.

```bash
# Get the version of the running n8n instance
docker compose exec n8n n8n --version

# View last 50 execution errors from logs
docker logs n8n --tail 100 | grep -i "error"
```

## API examples

### Triggering a Workflow (Curl)
Starting a long-running process via a webhook trigger.

```bash
curl -X POST "http://n8n.local:5678/webhook/your-workflow-id" \
     -H "Content-Type: application/json" \
     -d '{"action": "start_triage", "target_id": "12345"}'
```

### Fetching Execution Status (Python)
Programmatically checking if an automation completed successfully.

```python
import requests

API_URL = "http://n8n.local:5678/api/v1/executions"
API_KEY = "YOUR_API_KEY"
headers = {"X-N8N-API-KEY": API_KEY}

def check_last_execution():
    response = requests.get(API_URL, headers=headers, params={"limit": 1})
    if response.status_code == 200:
        execution = response.json()['data'][0]
        print(f"Workflow: {execution['workflowId']}, Status: {execution['status']}")

if __name__ == "__main__":
    check_last_execution()
```

## Related tools / concepts
- [Ollama](ollama.md) — Local LLM backend for n8n AI nodes.
- [Home Assistant](home-assistant.md) — For smart home event orchestration.
- [Paperless-ngx](paperless-ngx.md) — Target for automated document ingestion.
- [Zapier](../tools/automation_orchestration/zapier.md) — Cloud-based automation alternative.
- [Make](../tools/automation_orchestration/make.md) — Alternative visual automation platform.
- [Tavily](../tools/providers/tavily.md) — For agentic search enrichment within workflows.
- [Authentik](authentik.md) — For SSO access management to the n8n UI.
- [Playwright](../tools/development_ops/playwright.md) — For browser automation fallback in workflows.

## Sources / References
- [Official Website](https://n8n.io/)
- [Documentation](https://docs.n8n.io/)
- [n8n AI Capabilities](https://docs.n8n.io/advanced-ai/)
- [Model Context Protocol (MCP) in n8n](https://docs.n8n.io/integrations/mcp/)

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
