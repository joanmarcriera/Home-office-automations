# n8n

## What it is
n8n is an extendable, source-available workflow automation tool that allows you to connect various services and automate tasks using a visual node-based editor.

## What problem it solves
It eliminates the need for manual repetition of tasks between different software platforms. Unlike cloud-only alternatives, it can be self-hosted, keeping your automation logic and data private. It also provides advanced AI nodes for building complex AI-driven workflows.

## Where it fits in the stack
**Automation & Orchestration**. It acts as the "glue" between your various services, databases, and AI models.

## Typical use cases
- **Autonomous Document Processing**: Automatically extracting data from emails/documents and saving it to a database using LLMs.
- **AI Agents**: Creating complex multi-step agents that can search the web, interact with APIs, and perform logic.
- **Data Synchronization**: Keeping data in sync between CRM, project management tools, and local databases.

## Strengths
- **Visual Interface**: Easy to build and debug complex logic.
- **Self-Hostable**: Full control over your data and workflows.
- **Extensible**: Supports custom JavaScript nodes and community-contributed nodes.
- **Native AI Integration**: First-class support for LangChain-based AI nodes.

## Limitations
- **Learning Curve**: Advanced workflows require understanding of data structures and expressions.
- **Resource Usage**: Can be memory-intensive when running many complex concurrent workflows.

## When to use it
- When you need to automate complex business or home-office processes.
- If you require privacy for your automation logic.
- For building AI-powered workflows that integrate with multiple tools.

## When not to use it
- For extremely simple, one-off automations where a basic script suffices.
- If you prefer a completely managed, hands-off cloud service (though n8n Cloud exists).

## Licensing and cost
- **Source Available**: Yes (Fair-code license)
- **Cost**: Free (Self-hosted) / Paid (Cloud/Enterprise)
- **Self-hostable**: Yes

## Getting started

### Installation (Docker Compose)
```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    ports:
      - 5678:5678
    volumes:
      - ./n8n_data:/home/node/.n8n
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
    restart: unless-stopped
```

## Related tools / concepts
- [Ollama](ollama.md) (Use as AI backend)
- [Zapier](../tools/automation_orchestration/zapier.md) (Alternative)
- [Make](../tools/automation_orchestration/make.md) (Alternative)

## Backlog
- Create a reusable sub-workflow for AI document processing.
- Implement error handling with automated retry logic.

## Sources / References
- [Official Website](https://n8n.io/)
- [Documentation](https://docs.n8n.io/)
- [Pipedream](https://pipedream.com/)

## Contribution Metadata
- Last reviewed: 2026-03-08
- Confidence: medium
