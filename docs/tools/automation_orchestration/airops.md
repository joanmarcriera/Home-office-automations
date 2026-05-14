# AirOps

## What it is
AirOps is a platform for building and scaling AI-powered applications and workflows. It provides a collaborative environment for teams to design prompts, test models, and deploy AI "tools" that can be integrated into existing business systems.

## What problem it solves
AirOps addresses the difficulty of moving AI from a simple chat interface into a scalable, production-ready tool. It provides the necessary infrastructure for prompt versioning, model orchestration, and secure data handling, allowing companies to build internal AI tools quickly.

## Where it fits in the stack
**Category**: Automation & Orchestration / Enterprise AI Platform

## Typical use cases
- **Custom AI SaaS**: Building and hosting a specialized AI application for external customers.
- **Internal Tooling**: Creating AI assistants for customer support, sales, or marketing teams.
- **Data Enrichment**: Using AI to process and add value to large datasets in real-time.
- **Knowledge Management**: Building RAG systems over internal company documentation.

## Strengths
- **Collaborative**: Designed for teams (product managers, engineers, and domain experts) to work together on AI.
- **Scalable**: Handles the infrastructure needed to run millions of AI requests.
- **Integrations**: Connects easily to databases, APIs, and popular business tools.
- **Monitoring & Analytics**: Provides deep insights into how your AI tools are being used.

## Limitations
- **Commercial Platform**: Primarily a paid service with enterprise focus.
- **Complexity**: Offers a wide range of features that might take time to master.

## When to use it
- **Enterprise AI Workflows**: When you need a robust, scalable platform to manage complex AI processes across a team.
- **Rapid Prototyping for Business**: When the goal is to quickly deploy AI tools into existing business systems without building custom infrastructure.
- **Collaborative Design**: When product managers and domain experts need to participate directly in prompt and workflow design.

## When not to use it
- **Individual Open-Source Projects**: For simple, solo projects, open-source alternatives like Dify or Flowise might be more cost-effective.
- **Highly Custom Local Agents**: If the requirement is for a local-first agent that interacts with a private filesystem, tools like Open Interpreter or Goose are better suited.
- **Strictly Offline Use**: Being a cloud-based platform, it is not suitable for environments with strict air-gapped or offline requirements.

## Getting started
1.  Sign up for an account at [AirOps.com](https://www.airops.com/).
2.  Navigate to the API section in your workspace settings to generate an API Key.
3.  Design your workflow or tool in the AirOps Studio.
4.  Publish your workflow to make it accessible via API.

## API examples
**Trigger a workflow via webhook**:
```bash
curl --request POST \
  --url 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/webhook_async_execute?auth_token=YOUR_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{ "input_variable": "Custom Value" }'
```

## Related tools / concepts
- [Gumloop](gumloop.md)
- [Dify](../ai_knowledge/dify.md)
- [Flowise](../ai_knowledge/flowise.md)
- [Parea](../process_understanding/parea.md)
- [Zapier](zapier.md)
- [Langfuse](../process_understanding/langfuse.md) (Observability integration)
- [Helicone](../process_understanding/helicone.md) (Alternative LLM observability)

## Sources / references
- [AirOps Official Website](https://www.airops.com/)
- [AirOps Documentation](https://docs.airops.com/)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
