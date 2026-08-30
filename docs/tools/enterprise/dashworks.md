# Dashworks

## What it is
Dashworks is an AI-powered search and knowledge management platform designed to enable teams to find and synthesize information across all their internal applications through a unified, conversational interface. As of early 2027, Dashworks has fully adopted the **FastMCP 3.1 Task Protocol**, serving as a critical "Internal Brain" for agents using **Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

## What problem it solves
It effectively eliminates the "information silo" problem by centralizing access to data fragmented across tools like Slack, Google Drive, Jira, Confluence, GitHub, and Notion. Dashworks allows users and AI agents to ask natural language questions and receive grounded, cited answers based on the organization's collective intelligence, significantly reducing time wasted on manual information retrieval.

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management. It acts as the primary Retrieval-Augmented Generation (RAG) layer for an organization, connecting frontier models to proprietary, permissioned data. It sits between internal productivity apps and the agentic execution layer (like [Agno](../agents/agno.md) or [LangGraph](../frameworks/langgraph.md)).

## Typical use cases
- **Universal Knowledge Retrieval**: Instantly finding project specifications, HR policies, or technical documentation across multi-app environments.
- **Agentic Context Injection**: Providing real-time, grounded facts to [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) to prevent hallucinations during decision-making.
- **Automated Team Summarization**: Generating weekly project progress reports by synthesizing cross-platform communication and document updates.
- **Dynamic Onboarding**: Answering new hires' queries about internal processes using the existing knowledge base as the single source of truth.

## Strengths
- **Vast Connector Ecosystem**: Native, high-performance connectors for over 100+ enterprise SaaS and on-premise applications.
- **Permissions-First Architecture**: Strictly respects existing access controls from source systems to ensure data sovereignty and privacy.
- **Synthesized Answers with Citations**: Delivers natural language responses backed by direct links to the source documents for verification.
- **FastMCP 3.1 Native**: Easily exposed as a set of tools and resources for any MCP-compliant agent, facilitating "Computer Use" over internal data.

## Limitations
- **Third-Party SaaS Trust**: Requires indexing enterprise metadata and content on Dashworks' managed infrastructure, which may be a hurdle for some compliance regimes.
- **Indexing Latency**: There is typically a minor delay (minutes) between an update in a source system (e.g., a new Slack message) and its availability in the search index.
- **Scaling Costs**: Pricing models are often per-user, which can become significant as an organization grows compared to self-hosted vector databases.

## When to use it
- When team productivity is visibly hampered by information fragmentation across too many applications.
- If you need a "plug-and-play" enterprise RAG solution that requires minimal engineering overhead to maintain.
- For organizations that need a secure, audited way to provide internal context to AI agents and frontier models.

## When not to use it
- In highly regulated industries (e.g., defense, certain financial sectors) that mandate 100% on-premise data residency and zero external SaaS indexing.
- For very small teams where all information is contained within a single tool (e.g., a single Notion workspace).
- If you require deep, proprietary model fine-tuning on a specific domain that exceeds standard RAG capabilities.

## Getting started
Dashworks is a SaaS platform. Integration typically involves:
1. Connecting your company's core applications (Slack, Google Workspace, etc.) via the Dashworks Admin Console.
2. Configuring user permissions and single sign-on (SSO).
3. Accessing knowledge via the Dashworks Web App, Browser Extension, or the **FastMCP 3.1** server for agentic use.

## CLI examples
Dashworks functionality can be integrated into CLI workflows via standard HTTP requests or the unofficial community-maintained Dash-CLI.

```bash
# Query the Dashworks index for a specific project status
curl -X POST https://api.dashworks.ai/v1/search \
  -H "Authorization: Bearer ${DASHWORKS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the timeline for the Gemma 4 deployment?",
    "stream": false
  }'
```

## API examples
The Dashworks API is the primary method for injecting organizational knowledge into automated pipelines and custom agent prompts.

```python
import requests
import os

def query_internal_brain(question: str):
    """Interfaces with Dashworks to retrieve internal knowledge for an agent."""
    url = "https://api.dashworks.ai/v1/search"
    api_key = os.environ.get("DASHWORKS_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": question,
        "max_results": 5,
        "include_citations": True
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Example: An agent verifying compliance against local retention policies
compliance_data = query_internal_brain("What are our data retention rules for 2027?")
print(f"Grounded Answer: {compliance_data.get('answer')}")
```

### Dashworks Configuration Validation with Strict Pydantic v2 Schema
The following robust Python example uses **Pydantic v2** to programmatically validate Dashworks integration and query configurations, ensuring that only allowed systems are targeted and queries are structurally sound.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. Define Dashworks Search Request Configuration schema
class DashworksQueryConfig(BaseModel):
    query: str = Field(..., min_length=5, max_length=1000)
    allowed_sources: List[str] = Field(default_factory=lambda: ["slack", "google-drive", "github"])
    max_citations: int = Field(default=5, ge=1, le=20)
    filter_by_date: Optional[str] = Field(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$")
    strict_permissions: bool = Field(default=True)

    @model_validator(mode="after")
    def restrict_untrusted_sources(self) -> "DashworksQueryConfig":
        untrusted = [s for s in self.allowed_sources if s not in ["slack", "google-drive", "github", "jira", "confluence"]]
        if untrusted:
            raise ValueError(f"Sources contain untrusted or unsupported systems: {untrusted}")
        return self

# 2. Example representation of raw input parameters
raw_input = {
    "query": "Timeline and status report for Gemma 4 and FastMCP 3.1",
    "allowed_sources": ["slack", "github", "jira"],
    "max_citations": 8,
    "filter_by_date": "2027-01-07",
    "strict_permissions": True
}

# 3. Validate query configurations using Pydantic v2
try:
    validated_config = DashworksQueryConfig.model_validate(raw_input)
    print("Dashworks search configuration is valid!")
    print(f"Target Sources: {', '.join(validated_config.allowed_sources)}")
    print(f"Filter Date: {validated_config.filter_by_date}")
except ValidationError as e:
    print(f"Dashworks Query Validation failed with errors: {e.json()}")
```

## Related tools / concepts
- [Glean](glean.md) — The primary enterprise competitor for unified internal search and AI.
- [Guru](guru.md) — A knowledge management tool focused on verified "info cards" and wiki workflows.
- [Coveo](coveo.md) — An enterprise search and recommendation platform with deep customization.
- [Notion AI](../ai_knowledge/notion-ai.md) — Native AI search capabilities within the Notion workspace.
- [Elastic](elastic.md) — The underlying search technology used by many custom-built indexes.
- [Pinecone](../infrastructure/pinecone.md) — Leading vector database for building bespoke enterprise RAG stacks.
- [Langfuse](../process_understanding/langfuse.md) — Used for monitoring and observing the performance of internal search queries.

## Sources / references
- [Dashworks Official Website](https://www.dashworks.ai/)
- [Dashworks Developer Portal](https://docs.dashworks.ai/)
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
