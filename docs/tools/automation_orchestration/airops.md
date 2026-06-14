# AirOps

## What it is
AirOps is a platform for building and scaling AI-powered applications and workflows. It provides a collaborative environment for teams to design prompts, test models, and deploy AI "tools" that can be integrated into existing business systems.

## What problem it solves
AirOps addresses the difficulty of moving AI from a simple chat interface into a scalable, production-ready tool. It provides the necessary infrastructure for prompt versioning, model orchestration, and secure data handling, allowing companies to build internal AI tools quickly. It is optimized for frontier models like `claude-4-8-opus-20260528` and GPT-5.5.

## Where it fits in the stack
**Automation & Orchestration / Enterprise AI Platform**. It acts as the enterprise-grade middle layer between foundation models and business applications.

## Typical use cases
- **Custom AI SaaS**: Building and hosting a specialized AI application for external customers.
- **Internal Tooling**: Creating AI assistants for customer support, sales, or marketing teams.
- **Data Enrichment**: Using AI to process and add value to large datasets in real-time.
- **Knowledge Management**: Building RAG systems over internal company documentation with high accuracy.
- **Enterprise Agentic Workflows**: Orchestrating multi-step AI tasks with built-in monitoring and guardrails.

## Strengths
- **Collaborative Design**: Designed for teams (product managers, engineers, and domain experts) to work together on prompt engineering and workflow design.
- **Scalability**: Enterprise-grade infrastructure capable of handling millions of AI requests with high availability.
- **Robust Integrations**: Connects easily to databases (Postgres, Snowflake), APIs, and popular business tools (Slack, HubSpot).
- **Monitoring & Analytics**: Provides deep insights into model performance, token usage, and user interactions.
- **Prompt Versioning**: Native support for managing and testing multiple versions of prompts.

## Limitations
- **Commercial Platform**: Primarily a paid service with an enterprise focus, which may be overkill for solo developers.
- **Complexity**: Offers a wide range of features that might take time to master compared to simpler "no-code" tools.
- **Closed Source**: The underlying orchestration platform is proprietary.

## When to use it
- When you need a robust, scalable platform to manage complex AI processes across a team.
- For rapid prototyping and deployment of AI tools into existing enterprise business systems.
- When collaborative prompt design and versioning are critical to the project's success.
- For building RAG systems that require enterprise-level security and data handling.

## When not to use it
- For individual open-source projects where cost-effectiveness is the primary concern (consider [Dify](../ai_knowledge/dify.md) or [Flowise](../ai_knowledge/flowise.md)).
- If the requirement is for a local-first agent that interacts with a private filesystem without cloud dependencies.
- For strictly offline or air-gapped environments.

## Getting started
1. Sign up for an account at [AirOps.com](https://www.airops.com/).
2. Navigate to the API section in your workspace settings to generate an API Key.
3. Design your workflow or tool in the AirOps Studio.
4. Publish your workflow to make it accessible via API.
5. Set up your [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) within the platform.

## CLI examples

```bash
# Trigger a workflow via CURL (Webhook execute)
curl --request POST \
  --url 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/webhook_async_execute?auth_token=YOUR_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{ "input_variable": "Custom Value" }'

# Check the status of an execution
curl -G 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/executions/YOUR_EXECUTION_UUID' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## API examples

### Trigger a workflow via Python
```python
import requests
import json

api_key = "YOUR_API_KEY"
app_uuid = "YOUR_APP_UUID"
url = f"https://app.airops.com/public_api/airops_apps/{app_uuid}/webhook_async_execute"

payload = {
    "query": "Summarize the latest financial report for Apple",
    "context": "Focus on revenue growth and AI investments"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Related tools / concepts
- [Gumloop](gumloop.md) — Visual AI automation for smaller teams and individuals.
- [Dify](../ai_knowledge/dify.md) — Open-source alternative for LLM app development.
- [Langfuse](../process_understanding/langfuse.md) — Observability and prompt management.
- [Helicone](../process_understanding/helicone.md) — LLM observability and caching proxy.
- [Zapier](zapier.md) — General-purpose automation.
- [Parea](../process_understanding/parea.md) — Platform for testing and monitoring LLM apps.
- [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) — Security patterns for enterprise AI.

## Sources / references
- [AirOps Official Website](https://www.airops.com/)
- [AirOps Documentation](https://docs.airops.com/)
- [AirOps API Reference](https://docs.airops.com/api-reference)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
