# Coveo

## What it is
Coveo is an enterprise AI platform that provides intelligent search, personalized recommendations, and advanced generative AI capabilities (Coveo Relevance Generative Answering / CRGA) to power digital experiences across e-commerce, customer self-service, and the digital workplace.

As of early 2027, Coveo natively integrates the **FastMCP 3.1 Task Protocol**, allowing its multi-source unified search index to be exposed as a secure, high-fidelity resource for autonomous agentic workflows powered by frontier models including **Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

```
+-----------------------------------------------------------------------------------+
|                                  Coveo Platform                                   |
|                                                                                   |
|  +-------------------------------------+   +-----------------------------------+  |
|  | Multi-Source Push & Native Connectors|   | Relevance Engine & Machine Learn  |  |
|  | - ServiceNow, Salesforce, SharePoint|   | - Automatic Query Recommendation  |  |
|  | - Slack, Confluence, Jira, GitHub   |   | - Smart Faceting & Vector Ranking |  |
|  +------------------+------------------+   +-----------------+-----------------+  |
|                     |                                        |                    |
|                     v                                        v                    |
|  +-----------------------------------------------------------------------------+  |
|  |              Coveo Unified Index & Permission Security Engine               |  |
|  |  - Document & Chunk-Level ACL Enforcement                                   |  |
|  |  - Hybrid Keyword + Dense Vector Indexing                                   |  |
|  +--------------------------------------+--------------------------------------+  |
|                                         |                                         |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Client & Agent Integration Layer                           |
|                                                                                   |
|  +-----------------------------------+     +-----------------------------------+  |
|  | Headless SDK / Atomic Web Comps   |     | FastMCP 3.1 Task Protocol Engine  |  |
|  | - E-commerce & Self-Service Web   |     | - Secure Grounding for Claude 5.6 |  |
|  +-----------------------------------+     +-----------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Enterprise knowledge is notoriously fragmented across dozens of disconnected SaaS platforms, legacy databases, file shares, and code repositories. Standard RAG architectures and raw vector databases struggle with enterprise security permissions, real-time index synchronization, and complex document metadata filtering.

Coveo solves these enterprise challenges through:
- **Unified Permissioned Search**: Respects source-level Access Control Lists (ACLs) so users and AI agents only see content they have explicit rights to access.
- **Hybrid Keyword & Dense Vector Retrieval**: Combines semantic embedding search with traditional exact-match keyword indexing for domain-specific technical queries.
- **Self-Optimizing Machine Learning**: Uses continuous clickstream and interaction data to automatically re-rank search results for maximal task completion.
- **Grounded Generative Answering (CRGA)**: Generates hallucination-free answers anchored directly to enterprise documents with inline citations.

## Where it fits in the stack
**Category**: Enterprise AI / Search & Recommendation Infrastructure. Coveo sits between enterprise data repositories (Salesforce, ServiceNow, SharePoint, Confluence, Jira) and front-end interaction channels (portals, web apps, agentic workflows).

```
+-----------------------------------------------------------------------------------+
|                          Enterprise Data Repositories                             |
|                                                                                   |
|   +------------------+   +-------------------+   +----------------------------+   |
|   | ServiceNow / CRM |   | Confluence / Jira |   | SharePoint / File Storage  |   |
|   +--------+---------+   +---------+---------+   +-------------+--------------+   |
|            |                       |                           |                  |
|            +-----------------------+---------------------------+                  |
|                                    |                                              |
|                                    v                                              |
|                       Coveo Connectors & Push API                                 |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+-----------------------------------------------------------------------------------+
|                            Coveo Relevance Cloud                                  |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   | Unified Hybrid Vector Index + ACL Permission Token Evaluator              |   |
|   +----------------------------------------+----------------------------------+   |
|                                            |                                      |
|                                            v                                      |
|   +---------------------------------------------------------------------------+   |
|   | Coveo Relevance Generative Answering (CRGA) & FastMCP 3.1 Gateway         |   |
|   +----------------------------------------+----------------------------------+   |
+--------------------------------------------|--------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------+
|                     Front-End Channels & Agent Ecosystem                          |
|                                                                                   |
|   +------------------------+   +----------------------+   +-------------------+   |
|   | Customer Service Web   |   | FastMCP 3.1 Agents   |   | Internal Slack Bot|   |
|   +------------------------+   +----------------------+   +-------------------+   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Enterprise RAG & Agent Grounding**: Serving as the secure vector and document retrieval engine for autonomous AI agents like Claude 5.6 or GPT-5.6.
- **Customer Service Ticket Deflection**: Providing grounded, AI-generated answers in help centers and support portals.
- **E-Commerce Intelligent Discovery**: Driving conversion with personalized product recommendations and dynamic faceting.
- **Workplace Knowledge Search**: Surfacing relevant internal documentation across Slack, Confluence, Jira, and GitHub for employees.

## Key technical features & FastMCP 3.1 integration
- **FastMCP 3.1 Protocol Support**: Exposes enterprise search as standard FastMCP tools (`coveo_search`, `coveo_get_document_chunks`) for agentic tool use.
- **Automatic Relevance Tuning (ART)**: Machine learning models that adjust item rankings based on historical user clicks and conversions.
- **Document Level Security (DLS)**: Syncs identity providers (Okta, Azure AD) to filter search results at query time according to user roles.
- **Custom Pipeline Rules**: Configurable query pipelines for query expansion, stop-word handling, thesaurus rules, and result boosting.

## Strengths
- **Enterprise-Grade Governance & Security**: Strict adherence to SOC2 Type II, ISO 27001, and HIPAA standards with native DLS enforcement.
- **Over 100 Pre-Built Connectors**: Instant indexing capabilities for major SaaS platforms without building custom ETL pipelines.
- **Hybrid Search Engine**: Combines BM25 lexical search with vector embedding search for high accuracy across both short product codes and long questions.
- **Proven Scale**: Built to handle index collections exceeding hundreds of millions of complex items with sub-100ms query latency.

## Limitations
- **Premium Enterprise Pricing**: High licensing cost compared to self-hosted vector databases (e.g., Qdrant or Milvus).
- **Implementation Complexity**: Requires initial configuration for data source schema mapping, pipeline rules, and permission syncing.

## When to use it
- When managing millions of complex documents or products where search relevance directly impacts enterprise revenue or support operational costs.
- For organizations requiring a secure, SOC2-compliant way to deploy Generative AI (RAG) over sensitive, permissioned enterprise data.
- When you need deep analytics into user search behavior to identify knowledge gaps and optimize business outcomes.

## When not to use it
- For simple, small-scale website search where basic tools like Elastic or Algolia provide sufficient functionality at lower cost.
- If looking for a purely open-source search engine with no licensing overhead (consider Solr or OpenSearch).
- For individual or small-team knowledge management where lightweight tools like Obsidian are more appropriate.

## Comparison Matrix

| Feature / Metric | Coveo | Glean | Elastic / Elasticsearch | Pinecone |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Target** | Enterprise Search & E-Commerce | Enterprise Workspaces | Developer Search Engine | Managed Vector Database |
| **Indexing Model** | Hybrid Lexical + Dense Vector | Hybrid Lexical + Dense Vector | BM25 + Vector (ELSER) | Pure Vector Embeddings |
| **Native Connectors** | 100+ Enterprise Connectors | 80+ Workplace Connectors | Limited / Custom Integrations | None (Requires ETL pipeline) |
| **ACL & Permission Sync**| Native DLS (Source-Level) | Native DLS (Source-Level) | Manual Filter Pipelines | Custom Metadata Filtering |
| **FastMCP 3.1 Support** | Native Protocol Binding | Native Protocol Binding | Custom Server Needed | Custom Server Needed |
| **Deployment Model** | Managed Cloud SaaS | Managed Cloud SaaS | Self-Hosted or Cloud | Managed Cloud SaaS |

## Getting started

1. Log in to the **Coveo Administration Console** and create an organization.
2. Navigate to **Sources** and add a new source (e.g., Push API or ServiceNow connector).
3. Generate an API Key with `Search` and `Execute Query` permissions.
4. Integrate using the Coveo Headless SDK or FastMCP 3.1 server extension.

## CLI examples

```bash
# Install the Coveo CLI
npm install -g @coveo/cli

# Log in to your Coveo organization
coveo auth:login --orgId enterprise-org-123

# Create a new Push source for custom agent data indexing
coveo source:push:create "Agentic-Documentation"

# List active sources and their indexing status
coveo source:list --columns id,name,status,itemCount
```

## API examples

### 1. Programmatic Querying with Python
```python
import os
import requests

COVEO_API_KEY = os.environ.get("COVEO_API_KEY")
COVEO_ORG_ID = os.environ.get("COVEO_ORG_ID")

def search_coveo(query: str, user_email: str) -> dict:
    url = f"https://platform.cloud.coveo.com/rest/search/v2?organizationId={COVEO_ORG_ID}"
    headers = {
        "Authorization": f"Bearer {COVEO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "searchHub": "Agentic-Support",
        "user": user_email,
        "numberOfResults": 5
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    res = search_coveo("How do I request GPU quota in Kubernetes?", "engineer@company.com")
    print(f"Retrieved {len(res.get('results', []))} grounded results.")
```

### 2. FastMCP 3.1 Integration Server
```python
import os
import json
import urllib.request
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("coveo-enterprise-search")

COVEO_API_KEY = os.environ.get("COVEO_API_KEY", "")
COVEO_ORG_ID = os.environ.get("COVEO_ORG_ID", "")

@mcp.tool()
def coveo_enterprise_search(query: str, user_identity: str) -> Dict[str, Any]:
    """Queries the Coveo enterprise hybrid index respecting user permissions via FastMCP 3.1."""
    url = f"https://platform.cloud.coveo.com/rest/search/v2?organizationId={COVEO_ORG_ID}"
    headers = {
        "Authorization": f"Bearer {COVEO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "context": {"user": user_identity},
        "numberOfResults": 5
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = [
                {
                    "title": item.get("title"),
                    "uri": item.get("clickUri"),
                    "excerpt": item.get("excerpt")
                }
                for item in data.get("results", [])
            ]
            return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### 3. Strict Pydantic v2 Schema Validation
```python
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator

class CoveoQueryPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., min_length=2, max_length=1000, description="User search query")
    organization_id: str = Field(..., description="Coveo Organization Identifier")
    search_hub: str = Field("default", description="Analytics search hub tag")
    user_context: Dict[str, str] = Field(default_factory=dict, description="Security ACL context key-values")
    number_of_results: int = Field(10, ge=1, le=100, description="Max items to retrieve")
    pipeline: Optional[str] = Field(None, description="Target Coveo Query Pipeline")

    @field_validator("organization_id")
    @classmethod
    def validate_org_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("organization_id cannot be empty")
        return v.strip()

# Example Usage
try:
    payload = CoveoQueryPayload(
        query="High availability database failover procedures",
        organization_id="my-enterprise-org-id",
        search_hub="DevOps-Portal",
        user_context={"role": "SiteReliabilityEngineer", "dept": "Infrastructure"},
        number_of_results=10
    )
    print("Validated Coveo Payload:")
    print(payload.model_dump_json(indent=2))
except Exception as err:
    print(f"Validation Error: {err}")
```

## Related tools / concepts
- **[Glean](glean.md)**: Enterprise knowledge discovery and AI search platform.
- **[Elastic](elastic.md)**: Open-source search and analytics engine.
- **[Pinecone](../infrastructure/pinecone.md)**: Cloud-native vector database for custom RAG pipelines.
- **[Dashworks](dashworks.md)**: Unified AI search for productivity tools.
- **[FastMCP 3.1 Protocol](../automation_orchestration/mcp.md)**: Protocol standard for agentic tool integration.

## Sources / references
- [Coveo Official Platform Portal](https://www.coveo.com/)
- [Coveo Developer Documentation](https://docs.coveo.com/)
- [Coveo Relevance Generative Answering Architecture](https://www.coveo.com/en/platform/generative-answering)

---
## Contribution Metadata
- Last reviewed: 2026-10-07
- Confidence: high
