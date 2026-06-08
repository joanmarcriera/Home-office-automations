# Glean

## What it is
Glean is an AI-powered enterprise search and knowledge management platform that connects all of a company's disparate data sources—from Slack and Google Drive to Jira and GitHub—into a single, unified search and chat experience.

## What problem it solves
It eliminates "information silos" by providing a centralized gateway to institutional knowledge. Glean understands the context of a company's people, projects, and permissions, allowing employees to find exactly what they need without having to know which specific app the information lives in.

## Where it fits in the stack
**Enterprise Search / Knowledge Management Layer**. It serves as the primary "connective tissue" for information discovery across the organization.

## Key Features
- **Unified Search**: Search across 100+ popular SaaS applications with a single query.
- **Enterprise Knowledge Graph**: Maps the relationships between people, documents, and activities to deliver context-aware results.
- **Glean Assistant**: A generative AI coworker (Claude 4.7 and GPT-5.5 optimized) that answers questions based on internal documentation.
- **Glean Waldo**: A specialized agentic search model that delivers frontier intelligence with ~50% lower latency and ~25% fewer tokens.
- **Glean Canvas**: An interactive workspace for synthesizing information and generating presentations or interactive pages.
- **MCP Gateway**: Provides secure, governed access to enterprise context for external agents using the Model Context Protocol.
- **Health Agents**: Specialized agents for proactive infrastructure monitoring and assessing health across cloud deployments.
- **Permissions-Aware**: Strictly respects existing source-system permissions; users only see information they are already authorized to access.

## Typical use cases
- **Employee Onboarding**: Helping new hires find internal policies, project history, and key contacts.
- **Customer Support**: Enabling support agents to find technical answers across internal wikis and past tickets.
- **Engineering Productivity**: Finding relevant code documentation, Jira issues, and architectural decisions across repositories.

## Getting started
Glean is an enterprise-grade SaaS platform. It typically requires administrative integration with the company's SSO and primary SaaS providers.

### Minimal Concepts
1.  **Connectors**: The integrations used to pull data from external apps (e.g., Slack Connector).
2.  **Verification**: A feature where subject matter experts can "verify" specific answers to ensure accuracy.
3.  **Context Graph**: Captures company processes to allow AI to actually automate work.

## CLI examples
> [!NOTE]
> Glean is an enterprise search platform and does not provide an official public CLI for end-users as of June 2026. Administrative tasks are managed via the web console.

## API examples
Glean provides a REST API for searching programmatically. Below is a Python example using the `requests` library.

```python
import requests

API_KEY = "your_glean_api_key"
GLEAN_DOMAIN = "your-company.glean.com"

def search_glean(query):
    # API v1 Endpoint (2026 pattern)
    api_url = f"https://{GLEAN_DOMAIN}/api/v1/search"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "pageSize": 5,
        "model": "gpt-5.5" # Optional: Specify model preference if permitted
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
```

## Strengths
- **Relevance**: Superior search ranking compared to basic app-specific search.
- **Security**: Robust enterprise-grade security (Glean Protect), including SOC2 compliance and deep permission integration.
- **Actionable AI**: Moves beyond just finding files to performing tasks via agent orchestration and the Agentic Engine.

## Limitations
- **Cost**: High-tier enterprise pricing; may not be cost-effective for very small teams.
- **Implementation Time**: Full indexing and fine-tuning the knowledge graph can take time for large organizations.

## When to use it
- When your organization has information spread across 10+ different SaaS platforms (Slack, Jira, Drive, GitHub, etc.).
- When employees spend significant time searching for "who knows what" or "where is that doc."
- When you need a permissions-aware AI assistant (GPT-5.5 or Claude 4.7 based) that only reveals information the user is authorized to see.

## When not to use it
- For very small teams (e.g., <20 people) where information is easily managed in one or two tools.
- If you only need to search public web data (use [Perplexity](../ai_knowledge/perplexity.md) instead).
- If your primary knowledge base is exclusively in [Notion](../ai_knowledge/notion-ai.md) or [Confluence](https://www.atlassian.com/software/confluence).

## Related tools / concepts
- [Notion AI](../ai_knowledge/notion-ai.md) (Internal knowledge search within Notion)
- [Perplexity](../ai_knowledge/perplexity.md) (Alternative for external/web search)
- [Hebbia](hebbia.md) (Analytical synthesis for finance/legal)
- [Fyxer AI](fyxer.md) (Executive assistant and inbox management)
- [Ramp](ramp.md) (Financial automation and spend management)
- [tldv](tldv.md) (Meeting transcription and knowledge extraction)
- [Langfuse](../process_understanding/langfuse.md) (Observability for custom LLM integrations)
- [AgentOps](../process_understanding/agentops.md) (Monitoring for autonomous agents)
- [n8n](../../services/n8n.md) (Workflow automation)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (Standard for tool-agent connectivity)

## Sources / References
- [Glean Blog](https://www.glean.com/blog)
- [Glean Waldo: Agentic Search Model](https://www.glean.com/blog/waldo-launch)
- [Introducing MCP in Glean](https://www.glean.com/blog/mcp-mar-drop-2026)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
