# Pipedream

## What it is
Pipedream is a low-code integration platform for developers that allows you to connect APIs, databases, and AI services to build complex workflows. It provides a unique blend of no-code triggers and actions with the ability to write custom code (Node.js, Python, Go, or Bash) at any step. As of June 2026, it features native **MCP 3.0** integration and a built-in "Agentic Workflow Builder" powered by Claude 4.8.

## What problem it solves
It simplifies the process of connecting disparate services by handling authentication (OAuth), event sourcing, and serverless execution infrastructure. It allows developers to focus on the logic of their integrations—and the orchestration of AI agents—rather than the boilerplate code required to talk to various APIs or manage persistent state.

## Where it fits in the stack
Pipedream sits in the **Automation & Orchestration** layer. It acts as the "connective tissue" for agentic systems, providing stable, managed tool-calling interfaces to thousands of SaaS applications and local services through its gateway.

## Typical use cases
- **AI Agents and Chatbots**: Connecting frontier models to real-time data sources and execution tools (Slack, GitHub, Discord).
- **Agentic Webhook Handlers**: Ingesting, reasoning over, and acting upon webhooks from services like Stripe or custom apps.
- **Data Synthesizers**: Moving and transforming data between SaaS applications and vector databases for RAG.
- **Custom Agentic Notifications**: Building sophisticated alerting systems where an AI agent triages multi-source event triggers.
- **Serverless API Orchestration**: Building new, agent-ready API endpoints that aggregate data from multiple backend services.

## Strengths
- **Massive Integration Library**: Supports over 5,000+ integrated apps with pre-built, production-tested triggers and actions.
- **Code-Level Flexibility**: Write any code in Node.js, Python, Go, or Bash within any step, with access to all standard libraries and `pip`/`npm` packages.
- **Native MCP 3.0 Support**: Can act as either an MCP host or client, allowing Claude to use Pipedream workflows as tools.
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
2. **Add an AI Step**: Use the "Claude" or "OpenAI" pre-built actions to process incoming data.
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

### Python Workflow Step (Stateful)
Accessing a Pipedream Data Store to maintain state between runs.

```python
def handler(pd: "pipedream"):
    # Access a managed Data Store
    count = pd.inputs["data_store"].get("run_count", 0)

    # Update the count
    new_count = count + 1
    pd.inputs["data_store"].put("run_count", new_count)

    return {"run_count": new_count}
```

### Node.js Action with Native Fetch
Making an authenticated call to a connected service.

```javascript
export default defineComponent({
  props: {
    google_sheets: { type: "app", app: "google_sheets" },
  },
  async run({ steps, $ }) {
    // Auth is managed automatically by Pipedream
    const response = await fetch("https://sheets.googleapis.com/v4/spreadsheets/...", {
      headers: { Authorization: `Bearer ${this.google_sheets.$auth.oauth_access_token}` },
    });
    return await response.json();
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
- [Agentic Automation with Pipedream (2026 Blog)](https://pipedream.com/blog/agentic-workflows-mcp)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-24
