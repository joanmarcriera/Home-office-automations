# Pipedream

## What it is
Pipedream is a low-code integration platform for developers that allows you to connect APIs, databases, and AI services to build complex workflows. It provides a unique blend of no-code triggers and actions with the ability to write custom code (Node.js, Python, Go, or Bash) at any step.

## What problem it solves
It simplifies the process of connecting disparate services by handling authentication (OAuth), event sourcing, and execution infrastructure. It allows developers to focus on the logic of their integrations rather than the boilerplate code required to talk to various APIs.

## Where it fits in the stack
**Automation & Orchestration**. It is a cloud-native alternative to tools like [Make](make.md) or [n8n](../../services/n8n.md), offering deeper "code-first" capabilities while still maintaining ease of use for simple automations.

## Typical use cases
- **AI Agents and Chatbots**: Connecting LLMs to real-time data sources and tools.
- **Webhook Processing**: Ingesting, inspecting, and routing webhooks from services like GitHub, Stripe, or custom apps.
- **Data Pipelines**: Moving and transforming data between SaaS applications and databases.
- **Custom Notifications**: Building sophisticated alerting systems based on multi-source event triggers.
- **API Orchestration**: Building new API endpoints that aggregate data from multiple backend services.

## Strengths
- **Massive Integration Library**: Supports over 3,000+ integrated apps with pre-built triggers and actions.
- **Code-Level Control**: Write any code in Node.js, Python, Go, or Bash within any step of a workflow.
- **Managed Auth**: Handles OAuth and key-based authentication automatically across its entire app library.
- **Source-Available**: Maintains an open registry of components on GitHub, allowing for community contributions and auditing.
- **Integrated KV Store**: Provides a built-in Key-Value store for maintaining state across workflow executions.

## Limitations
- **Cloud-Only**: Unlike n8n, there is no official self-hosted version, which may be a concern for strict data residency requirements.
- **Pricing Model**: Credits are consumed per execution and compute time, which requires monitoring for high-volume workflows.
- **Learning Curve**: While it has no-code features, getting the most out of it requires familiarity with at least one supported programming language.

## When to use it
- When you need a highly flexible automation platform that allows for custom code.
- When you are building AI agents that require stable, managed tool-calling interfaces to many SaaS apps.
- For processing high volumes of webhooks with complex logic.
- When you want to avoid managing the infrastructure for small integration scripts.

## When not to use it
- When you require a strictly self-hosted environment for privacy or security ([n8n](../../services/n8n.md) is better here).
- For very simple "if this then that" automations where [Zapier](zapier.md) or [IFTTT](https://ifttt.com/) might be simpler.
- When you have zero programming experience and need a purely visual tool.

## Getting started

1. **Sign Up**: Create an account at [pipedream.com](https://pipedream.com/).
2. **Create a Project**: Organize your workflows and resources into projects.
3. **Choose a Trigger**: Select from thousands of pre-built triggers (e.g., HTTP Webhook, Schedule, New Tweet).
4. **Add Steps**: Add pre-built actions or custom code steps to process your data.
5. **Connect Apps**: Authenticate with the services you need to use (e.g., Slack, Google Sheets).
6. **Deploy**: Turn on your workflow to start processing live events.

## Technical examples

### Custom Node.js Step with Managed Auth
Using a connected Slack account in a custom code step:

```javascript
// This step uses the "slack" app connection
export default defineComponent({
  props: {
    slack: { type: "app", app: "slack" },
  },
  async run({ steps, $ }) {
    const { WebClient } = await import('@slack/web-api');
    const web = new WebClient(this.slack.$auth.oauth_access_token);

    return await web.chat.postMessage({
      channel: '#general',
      text: `Hello from Pipedream! The previous step returned: ${steps.trigger.event.body.message}`,
    });
  },
})
```

### Python Webhook Handler
Extracting and transforming data from a POST request:

```python
def handler(pd: "pipedream"):
    # Access data from the HTTP trigger
    event = pd.steps["trigger"]["event"]
    body = event.get("body", {})

    # Process data
    processed_message = body.get("message", "No message found").upper()

    # Return data for use in future steps
    return {"message": processed_message}
```

## Related tools / concepts
- [Make](make.md)
- [n8n](../../services/n8n.md)
- [Zapier](zapier.md)
- [Skyvern](skyvern.md)
- [Browser Use](browser-use.md)
- [Webhook Ingestion](../../reference-implementations/paperless/webhook-ingestion.md)
- [Model Context Protocol (MCP)](mcp.md)

## Sources / references
- [Pipedream Documentation](https://pipedream.com/docs)
- [Pipedream GitHub Registry](https://github.com/PipedreamHQ/pipedream)
- [Pipedream REST API](https://pipedream.com/docs/rest-api/overview)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
