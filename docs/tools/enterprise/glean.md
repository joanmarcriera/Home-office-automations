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
- **Glean Assistant**: A generative AI chat interface that answers questions based on the company's internal documentation and conversation history.
- **Glean Agents**: Specialized AI agents that can automate workflow actions based on retrieved insights.
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

### API Example
Glean provides a REST API for searching programmatically. Below is a Python example using the `requests` library.

```python
import requests

API_KEY = "your_glean_api_key"
GLEAN_DOMAIN = "your-company.glean.com"

def search_glean(query):
    url = f"https://{GLEAN_DOMAIN}/api/v1/search"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "pageSize": 5
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Example usage
# results = search_glean("How do I set up my VPN?")
# print(results)
```

## Strengths
- **Relevance**: Superior search ranking compared to basic app-specific search.
- **Security**: Robust enterprise-grade security, including SOC2 compliance and deep permission integration.
- **Actionable AI**: Moves beyond just finding files to answering questions and performing tasks via agents.

## Limitations
- **Cost**: High-tier enterprise pricing; may not be cost-effective for very small teams.
- **Implementation Time**: Full indexing and fine-tuning the knowledge graph can take time for large organizations.

## When to use it
- When your organization has information spread across 10+ different SaaS platforms (Slack, Jira, Drive, GitHub, etc.).
- When employees spend significant time searching for "who knows what" or "where is that doc."
- When you need a permissions-aware AI assistant that only reveals information the user is authorized to see.

## When not to use it
- For very small teams (e.g., <20 people) where information is easily managed in one or two tools.
- If you only need to search public web data (use [Perplexity](../ai_knowledge/perplexity.md) instead).
- If your primary knowledge base is exclusively in [Notion](../ai_knowledge/notion-ai.md) or [Confluence](https://www.atlassian.com/software/confluence) and you don't use other tools heavily.

## Related tools / concepts
- [Notion AI](../ai_knowledge/notion-ai.md) (Internal knowledge search within Notion)
- [Perplexity](../ai_knowledge/perplexity.md) (Alternative for external/web search)
- [Hebbia](hebbia.md) (Analytical synthesis for finance/legal)
- [Fyxer AI](fyxer.md) (Executive assistant and inbox management)
- [Ramp](ramp.md) (Financial automation and spend management)
- [tldv](tldv.md) (Meeting transcription and knowledge extraction)
- [Langfuse](../process_understanding/langfuse.md) (Observability for custom LLM integrations)
- [AgentOps](../process_understanding/agentops.md) (Monitoring for autonomous agents)
- [n8n](../../services/n8n.md) (Workflow automation across enterprise tools)

## Sources / References
- [Glean Definitive Guide to Enterprise Search](https://www.glean.com/blog/the-definitive-guide-to-ai-based-enterprise-search-for-2025)
- [Glean 2026 AI Predictions](https://www.glean.com/blog/2026-ai-predictions-with-friends)

## Contribution Metadata
- Last reviewed: 2026-05-10
- Confidence: high
