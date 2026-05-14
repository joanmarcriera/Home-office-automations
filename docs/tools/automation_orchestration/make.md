# Make (formerly Integromat)

## What it is
Make is a visual automation platform that allows you to design, build, and automate anything from tasks and workflows to apps and systems. It uses a "no-code" approach to connect hundreds of different web services through a drag-and-drop scenario builder.

## What problem it solves
Enables non-developers to create complex multi-step automations connecting different apps and services through a visual interface. It handles authentication, data mapping, and scheduling, significantly reducing the engineering effort required to build integrations between SaaS products.

## Where it fits in the stack
**Automation & Orchestration**. Serves as a cloud-based automation platform, an alternative to self-hosted tools like n8n. It is ideal for workflows that primarily involve third-party cloud services (SaaS) where an official API integration is preferred over custom scripts.

## Typical use cases
- Building multi-step workflows connecting cloud services (e.g., Typeform to Slack to Google Sheets)
- Automating data transformations and transfers between applications using built-in functions
- Creating integrations for services that lack native connections via its "HTTP Request" module
- Processing incoming webhooks from external services to trigger internal actions

## Strengths
- **Visual Scenario Builder**: Highly intuitive drag-and-drop interface with real-time execution tracking.
- **Large Integration Library**: Supports 1000+ pre-built connectors for popular SaaS tools.
- **Advanced Logic**: Supports branching, filtering, error handling, and iterators/aggregators natively.
- **Data Mapping**: Extremely flexible system for transforming data between different formats without code.

## Limitations
- **Cloud-hosted only**: No self-hosting option for privacy-first or local-only homelab setups.
- **Operational Cost**: Pricing is based on the number of "operations" and data transfer volume, which can scale quickly.
- **Proprietary**: Workflows are locked into the Make platform and cannot be easily exported to other systems.

## When to use it
- When you need a no-code automation platform with a strong visual editor for SaaS-to-SaaS workflows.
- When the required integrations are already available as official modules.
- When you need a reliable, managed service that handles OAuth and API maintenance automatically.

## When not to use it
- When privacy requires self-hosted automation or local data processing (use [n8n](../../services/n8n.md) or [LocalFlow](../frameworks/langflow.md) instead).
- When the automation involves significant local file system or hardware access.
- When you need full programmatic control over the execution environment or custom library support.

## Getting started

1. **Sign up**: Create an account at [Make.com](https://www.make.com/).
2. **Create a Scenario**: Click "Create a new scenario" and choose a trigger (e.g., "Webhooks").
3. **Add Modules**: Click the plus icon to add actions from other apps.
4. **Link and Map**: Connect the modules and map the output fields from one module to the input of the next.
5. **Run and Schedule**: Test the scenario manually, then set the schedule to "On" to automate it.

## API / Technical examples

### Incoming Webhook Pattern
Make provides a unique URL for every webhook trigger. You can send data to this URL from any device or script.

```bash
# Sending JSON data to a Make webhook
curl -X POST https://hook.eu1.make.com/your-unique-id \
     -H "Content-Type: application/json" \
     -d '{"event": "door_open", "sensor": "back_gate", "timestamp": "2026-05-14T03:30:00Z"}'
```

### JSON Transform Function
Inside a module, you can use Excel-like functions to transform data:
`{{upper(1.name)}}` converts the name field to uppercase.
`{{formatDate(now; "YYYY-MM-DD")}}` returns the current date in ISO format.

### Error Handling
Make allows adding "Error handlers" (like `Ignore`, `Rollback`, `Resume`) to specific modules to handle API failures or timeouts gracefully.

## Related tools / concepts

- [n8n](../../services/n8n.md)
- [Zapier](zapier.md)
- [Pipedream](pipedream.md)
- [IFTTT](https://ifttt.com/)
- [Skyvern](skyvern.md)
- [Browser Use](browser-use.md)
- [Webhook Ingestion](../../reference-implementations/paperless/webhook-ingestion.md)
- [Home Assistant](../../services/home-assistant.md)

## Sources / references
- [Official Website](https://www.make.com/)
- [Make Academy (Training)](https://academy.make.com/)
- [Make API Documentation](https://www.make.com/en/api-documentation)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
