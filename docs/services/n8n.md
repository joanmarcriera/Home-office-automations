# n8n

## What it is
n8n is an extendable, source-available workflow automation platform with a visual node editor, API integrations, and first-class support for AI-powered workflow steps.

## What problem it solves
It replaces repetitive manual operations across tools and teams. Unlike cloud-only automation products, it can be self-hosted, so workflow logic, execution history, and sensitive data stay in your environment.

## Where it fits in the stack
**Automation & Orchestration**. It is the control plane for cross-tool business processes.

## Typical use cases
- **Autonomous document/email operations**: classify incoming content, extract fields, route to owners.
- **Cross-system process automation**: connect email, CRM/ERP, ticketing, chat, storage, and databases.
- **AI-assisted operations**: triage, summarize, draft responses, and escalate only low-confidence cases.

## Strengths
- **Visual + programmable**: easy to build visually, still supports advanced expressions/logic.
- **Self-hostable**: private automation with infrastructure you control.
- **Broad integrations**: large ecosystem of built-in and community nodes.
- **Good ops model**: retries, execution logs, error workflows, queue mode.

## Limitations
- **Learning curve**: robust flows require strong data modeling and error handling.
- **Scale design required**: business-critical usage needs queue mode, persistent DB, and observability.
- **Credential discipline**: secrets management and environment separation must be done explicitly.

## When to use it
- You want long-running, auditable business automations.
- You need privacy and self-hosting.
- You want AI-assisted processes with clear human-approval boundaries.

## When not to use it
- For one-off scripts or tiny automations with no lifecycle.
- When you do not want to own operations/security for automation infrastructure.

## Licensing and cost
- **Source Available**: Yes (Fair-code license)
- **Cost**: Free (Self-hosted) / Paid (Cloud/Enterprise)
- **Self-hostable**: Yes

## Getting started

### Installation (Docker Compose, production-oriented baseline)
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
      - ./n8n_files:/files
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_HOST=n8n.local
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - NODE_ENV=production
    restart: unless-stopped
```

## Project definitions: JSON workflows and YAML infrastructure

If you want to version-control an n8n project:

- **Workflow definitions**: native n8n format is **JSON**.
- **Infrastructure/deployment**: usually **YAML** (`docker-compose.yml`, CI workflows, Kubernetes manifests).
- **Repository manifest (optional)**: your own YAML index for team governance can map business processes to workflow JSON files.

Example repository layout:

```text
automation-n8n/
  docker-compose.yml
  .env.example
  n8n/
    workflows/
      010-email-intake.json
      020-quote-draft.json
      030-shipment-updates.json
    workflow-manifest.yaml
  docs/
    runbook.md
```

Example `workflow-manifest.yaml` (repo convention, not native n8n format):

```yaml
project: wine-import-export-ops
owner: operations
workflows:
  - name: email-intake-and-triage
    file: n8n/workflows/010-email-intake.json
    criticality: high
  - name: quote-draft-and-follow-up
    file: n8n/workflows/020-quote-draft.json
    criticality: high
```

## CLI examples

```bash
# Export all workflows as separate JSON files
docker compose exec n8n n8n export:workflow --all --separate --output=/files/workflows

# Import all workflows from a folder
docker compose exec n8n n8n import:workflow --separate --input=/files/workflows

# Export credentials for backup/migration (handle securely)
docker compose exec n8n n8n export:credentials --all --output=/files/credentials.json
```

## How to use AI to run n8n operations (not only AI nodes inside workflows)

Use AI in three roles around n8n:

1. **Designer role**: convert SOPs into workflow specs, node maps, and test cases.
2. **Operator role**: review failed executions, classify root cause, propose retries/fixes.
3. **Optimizer role**: identify manual bottlenecks and propose new automations weekly.

Guardrails:

- AI can propose/create/update workflows and documentation.
- AI cannot approve legal commitments, banking actions, or final contractual terms.
- High-risk actions require human approval nodes and explicit audit logs.

## Example: Wine import/export email automation program

Goal: n8n handles most email operations end-to-end while humans keep control of legal and banking decisions.

Core workflows:

1. **Inbound email triage**
- Trigger: IMAP/Gmail new email.
- Steps: classify (`supplier`, `customer`, `logistics`, `compliance`, `finance`), extract entities (product, quantity, Incoterm, destination, ETA).
- Output: route to CRM/ERP/ticket queue and attach suggested response draft.

2. **Quote request automation**
- Trigger: inbound RFQ emails.
- Steps: fetch current catalog/pricing rules, draft quote reply, create follow-up tasks, schedule reminder if no response.
- Output: ready-to-send draft + SLA timer.

3. **Shipment status and exception handling**
- Trigger: forwarder/carrier updates by email/API.
- Steps: parse status, update shipment record, notify customer on milestones, escalate delays/anomalies.
- Output: near-real-time customer comms without manual copy/paste.

4. **Collections and accounts comms (non-payment execution)**
- Trigger: invoice due/overdue event.
- Steps: send reminders, track response sentiment, escalate disputed cases.
- Output: n8n drives communication cadence; finance team approves/executes payment actions externally.

5. **Compliance document orchestration**
- Trigger: missing/updated document request.
- Steps: request docs, validate required fields, route to legal/compliance for approval.
- Output: complete compliance packet ready for human sign-off.

### Human-only boundaries (explicit)

- Bank transfers, payment approval, and settlement.
- Legal review/approval of contracts and regulatory commitments.
- Any action above predefined risk threshold.

### Minimal AI prompt contract for email triage

```text
Classify this email into one of:
supplier, customer, logistics, compliance, finance, spam.

Return strict JSON:
{
  "category": "...",
  "urgency": "low|medium|high",
  "entities": {
    "counterparty": "",
    "product": "",
    "quantity": "",
    "destination": "",
    "incoterm": ""
  },
  "needs_human_approval": true|false,
  "reason": ""
}
```

## How to keep this n8n capability expanding over time (Jules loop)

Use a recurring Jules task focused on n8n value growth:

1. Pull top failed/slow executions from last 24h.
2. Propose one additive workflow improvement.
3. Add one new test case for that workflow.
4. Open a PR with workflow JSON + docs update + rollback note.

This keeps n8n improving as an operating system for your business processes, not just as isolated automations.

## Useful AI-adjacent integrations
- [Tavily](../tools/providers/tavily.md) is a good fit when workflows need web search or research enrichment before summarization or routing.
- [Playwright](../tools/development_ops/playwright.md) is useful when the target system lacks a stable API and a browser automation fallback is acceptable.
- [Supabase](../tools/infrastructure/supabase.md) works well as lightweight state storage for workflow memory, queue snapshots, or approval state outside n8n itself.
- [Replicate](../tools/providers/replicate.md) and [ElevenLabs](../tools/ai_knowledge/elevenlabs.md) are useful when automations need media generation rather than text-only inference.

## Related tools / concepts
- [Ollama](ollama.md) (Use as AI backend)
- [Zapier](../tools/automation_orchestration/zapier.md) (Alternative)
- [Make](../tools/automation_orchestration/make.md) (Alternative)
- [OpenRouter](../tools/ai_knowledge/openrouter.md) (Multi-provider LLM routing for prompts/models)
- [Home Assistant](home-assistant.md) (Example of broader automation ecosystem integration)

## Backlog
- Add reusable sub-workflows: `email-triage`, `risk-gating`, `human-approval`.
- Add golden test fixtures for 20 real-world wine trade email scenarios.
- Add SLO dashboard: execution latency, failure rate, manual handoff rate.
- Add weekly Jules report: top 3 automation gaps and proposed PRs.

## Sources / References
- [Official Website](https://n8n.io/)
- [Documentation](https://docs.n8n.io/)
- [Self-hosting n8n](https://docs.n8n.io/hosting/)
- [n8n AI capabilities](https://docs.n8n.io/advanced-ai/)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
