# Pipedream

## What it is
Pipedream is a low-code integration platform for developers that allows you to connect APIs, databases, and AI services to build complex workflows. It provides a unique blend of no-code triggers and actions with the ability to write custom code (Node.js, Python, Go, or Bash) at any step. As of early 2027, it features native **FastMCP 3.1 Task Protocol** integration and a built-in "Agentic Workflow Builder" powered by Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.

## What problem it solves
It simplifies the process of connecting disparate services by handling authentication (OAuth), event sourcing, and serverless execution infrastructure. It allows developers to focus on the logic of their integrations—and the orchestration of AI agents—rather than the boilerplate code required to talk to various APIs or manage persistent state.

## Where it fits in the stack
Pipedream sits in the **Automation & Orchestration** layer. It acts as the "connective tissue" for agentic systems, providing stable, managed tool-calling interfaces to thousands of SaaS applications and local services through its gateway.

## Typical use cases
- **AI Agents and Chatbots**: Connecting frontier models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra) to real-time data sources and execution tools (Slack, GitHub, Discord).
- **Agentic Webhook Handlers**: Ingesting, reasoning over, and acting upon webhooks from services like Stripe or custom apps.
- **Data Synthesizers**: Moving and transforming data between SaaS applications and vector databases for RAG.
- **Custom Agentic Notifications**: Building sophisticated alerting systems where an AI agent triages multi-source event triggers.
- **Serverless API Orchestration**: Building new, agent-ready API endpoints that aggregate data from multiple backend services.

## Strengths
- **Massive Integration Library**: Supports over 5,000+ integrated apps with pre-built, production-tested triggers and actions.
- **Code-Level Flexibility**: Write any code in Node.js, Python, Go, or Bash within any step, with access to all standard libraries and `pip`/`npm` packages.
- **Native FastMCP 3.1 Support**: Acts as either a FastMCP host or client, supporting the complete FastMCP 3.1 Task Protocol specification for routing execution payloads.
- **Managed Auth & Vault**: Handles OAuth and key-based authentication automatically; includes an encrypted secret vault.
- **Stateful Workflows**: Built-in Key-Value store and Data Stores for maintaining state across asynchronous executions.
- **Real-Time Monitoring**: Deep observability into execution logs, step-by-step data inspection, and error handling.

## Limitations
- **Cloud-Only Execution**: No official self-hosted runner, which may be a constraint for high-security on-premise data (consider [n8n](../../services/n8n.md) for self-hosting).
- **Execution Credit Model**: High-volume, compute-intensive workflows can become expensive under the per-invocation pricing model.
- **Learning Curve**: While visual, the platform's power is unlocked through code, requiring developer familiarity with supported languages.

## When to use it
- When you need a flexible, cloud-native automation platform that allows for custom code and complex logic.
- When building AI agents that require managed, authenticated access to many SaaS tools.
- For processing high volumes of diverse webhooks with AI-driven reasoning or triage.
- When you want to minimize infrastructure management for integration scripts and agent tools.

## When not to use it
- When you require a strictly self-hosted environment for privacy or compliance (use [n8n](../../services/n8n.md)).
- For very simple, non-technical "if this then that" tasks where [Zapier](zapier.md) might be faster.
- For extremely high-throughput, low-latency data processing where the serverless cold-start or proxy overhead is prohibitive.

## Getting started

### Account Setup
Create an account at [pipedream.com](https://pipedream.com/).

### Creating an Agentic Workflow
1. **Choose a Trigger**: Select a source like an HTTP Webhook or a scheduled interval.
2. **Add an AI Step**: Use the "Claude 5.6" or "GPT-5.6" pre-built actions to process incoming data.
3. **Add an Action**: Use a pre-built app action (e.g., "Slack - Send Message") and pass the AI output to it.
4. **Deploy**: Workflows are live immediately upon deployment.

## CLI examples
The Pipedream CLI (`pd`) allows for managing workflows, logs, and components from the terminal.

```bash
# Install the CLI
curl https://pipedream.com/install.sh | sh

# List your active workflows
pd list workflows

# Tail logs for a specific workflow
pd logs <workflow_id>

# Deploy a local code component as a workflow
pd deploy my_workflow.js
```

## API examples

### Python Webhook & State Validation (Pydantic v2)
In modern serverless integrations, validating the dynamic state and external webhooks is critical to prevent cascading agent failures. This Python example runs inside a Pipedream step, executing strict **Pydantic v2** validation on incoming event objects and stateful data stores.

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Define the incoming event validation schema
class WebhookTriggerEvent(BaseModel):
    event_id: str = Field(..., description="Unique UUID of the triggering event")
    source: str = Field(..., description="Name of the source service (e.g., github, stripe)")
    payload: Dict[str, Any] = Field(..., description="Dynamic payload content dict")
    timestamp: int = Field(..., description="Unix timestamp of the event initiation")

# Define state structure for Key-Value Data Store
class StatefulWorkflowContext(BaseModel):
    run_count: int = Field(default=0, ge=0, description="Invocation counter")
    last_processed_id: Optional[str] = Field(None, description="Last event ID processed successfully")

def handler(pd: "pipedream"):
    # 1. Ingest and validate incoming event data from Pipedream trigger step
    raw_event = pd.steps["trigger"]["event"]

    try:
        event = WebhookTriggerEvent.model_validate(raw_event)
        print(f"Validated webhook event {event.event_id} from {event.source}")
    except ValidationError as e:
        print(f"Trigger validation error: {e.json()}")
        return {"status": "error", "message": "Invalid webhook payload schema"}

    # 2. Access and validate stateful Pipedream Data Store
    raw_store = pd.inputs["data_store"]
    state_dict = {
        "run_count": raw_store.get("run_count", 0),
        "last_processed_id": raw_store.get("last_processed_id", None)
    }

    try:
        state = StatefulWorkflowContext.model_validate(state_dict)
    except ValidationError as e:
        print(f"Stateful store corrupted, resetting context. Errors: {e.json()}")
        state = StatefulWorkflowContext()

    # 3. Update state parameters
    state.run_count += 1
    state.last_processed_id = event.event_id

    # 4. Save state back to Pipedream Data Store
    raw_store.put("run_count", state.run_count)
    raw_store.put("last_processed_id", state.last_processed_id)

    return {
        "status": "success",
        "current_run": state.run_count,
        "processed_event_id": state.last_processed_id
    }
```

### Node.js Action with Native Fetch (FastMCP 3.1 Integrated)
Making an authenticated call to a connected service while adhering to FastMCP 3.1 Task Protocol schemas.

```javascript
export default defineComponent({
  props: {
    google_sheets: { type: "app", app: "google_sheets" },
    mcp_payload: { type: "object", label: "FastMCP 3.1 Task Payload", optional: true }
  },
  async run({ steps, $ }) {
    // Auth is managed automatically by Pipedream
    const response = await fetch("https://sheets.googleapis.com/v4/spreadsheets/...", {
      headers: { Authorization: `Bearer ${this.google_sheets.$auth.oauth_access_token}` },
    });
    const sheetsData = await response.json();

    return {
      success: true,
      data: sheetsData,
      mcp_meta: this.mcp_payload || {}
    };
  },
})
```

## Related tools / concepts
- [Make](make.md) - Visual automation with strong logic support.
- [n8n](../../services/n8n.md) - Open-source, self-hosted workflow automation.
- [Zapier](zapier.md) - Enterprise-standard no-code integration.
- [Gumloop](../automation_orchestration/gumloop.md) - AI-native workflow orchestration.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) - Standard for agent-tool communication.
- [Webhook Ingestion](../../playbooks/dev-workflow-ai-assisted.md) - Common architectural pattern for Pipedream.

## Sources / References
- [Official Website](https://pipedream.com/)
- [Pipedream Documentation](https://pipedream.com/docs)
- [Pipedream Component Registry (GitHub)](https://github.com/PipedreamHQ/pipedream)
- [Pipedream REST API Reference](https://pipedream.com/docs/api/rest/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2027-01-07
