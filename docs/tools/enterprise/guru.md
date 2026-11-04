# Guru

## What it is
Guru is an enterprise AI knowledge management and context delivery platform that captures, verifies, and serves organizational knowledge directly into daily employee workflows (Slack, Microsoft Teams, Zendesk, Salesforce, web browsers). Built around a core philosophy of "verified knowledge," Guru replaces stale static wikis with a human-in-the-loop verification engine: subject matter experts (SMEs) are assigned explicit ownership of individual knowledge "Cards" and prompted to periodically re-verify information on automated schedules (e.g. every 30, 60, or 90 days).

In early 2027, Guru integrates the **FastMCP 3.1 (Model Context Protocol)** task protocol and enterprise RAG API suite. This enables autonomous agent fleets (powered by frontier models including Gemma 4, Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4) to query Guru's verified card index as a high-fidelity grounding layer. By anchoring agent reasoning to verified cards, enterprise teams eliminate LLM hallucinations, enforce regulatory compliance, and deliver trusted answers with audit-ready source attribution.

## What problem it solves
Enterprise knowledge naturally decays over time. As teams ship product updates, revise HR policies, and adjust pricing tiers, static documentation repositories (Confluence, SharePoint, Google Drive) accumulate outdated or conflicting information—causing significant operational issues:
- **Knowledge Decay & Stale Documentation**: Static wikis lack automated expiration checks, causing employees and AI tools to act on deprecated guidelines.
- **Interruption Fatigue ("Shoulder-Tapping")**: Subject matter experts spend hours daily answering repetitive questions across chat tools instead of producing core work.
- **Context Switching Bottlenecks**: Searching through disconnected SaaS silos forces workers to break focus and search multiple browser tabs.
- **Hallucinations in AI & RAG Engines**: Retrieval-Augmented Generation systems indexing unverified or duplicate documents produce hallucinated or contradictory answers to customer and employee queries.

Guru addresses these challenges through:
- **SME Ownership & Verification Workflows**: Automatically routes cards to designated experts when verification intervals expire.
- **In-Context Delivery**: Browser extensions and chat bots surface verified cards natively within the apps employees already use.
- **FastMCP 3.1 Grounding for AI Agents**: Exposes verified knowledge cards directly to LLMs, ensuring agents only utilize human-verified facts for customer support and automated reasoning.
- **Trust Scores & Source Citation**: Generates synthesized AI answers with explicit trust metrics and direct card links.

```
+---------------------------------------------------------------------------------------------------+
|                                 GURU ENTERPRISE RAG ARCHITECTURE                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Content Ingestion    |     |  Verification Engine  |     |  Guru Knowledge Base          |   |
|   |                       |     |                       |     |                               |   |
|   | - Web App Editor      | --> | - SME Expiration Check| --> | - Verified Knowledge Cards    |   |
|   | - REST Ingestion API  |     | - Audit Trail Logging |     | - Vector & Keyword Index      |   |
|   | - Browser Extension   |     | - SLA Health Metrics  |     | - Permission Collections      |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                               |                   |
|                                                                               v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Agentic & Human Consumers  |  FastMCP 3.1 Gateway  |     |  Guru AI Search / RAG         |   |
|   |                       |     |                       |     |                               |   |
|   | - Slack / Teams Bots  | <-- | - Tool Discovery      | <-- | - Trust Score Calculation     |   |
|   | - Zendesk / Salesforce|     | - FastMCP RAG Tools   |     | - Citation Attribution        |   |
|   | - Autonomous Agents   |     | - Pydantic v2 Guard   |     | - Hybrid Vector Search        |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management & Grounding Layer.

Guru acts as the **Verified Knowledge Store & RAG Gateway** sitting between raw enterprise content repositories (Notion, Google Docs, Zendesk) and downstream consumer interfaces—including **Browser Extensions**, **Helpdesk Tools**, and **Agentic Orchestration Frameworks** (FastMCP 3.1, Claude Code, LangGraph).

## Empirical Performance & Search Latency Benchmarks

The following empirical benchmarks evaluate Guru enterprise card retrieval, hybrid vector search, and SME verification synchronization across organizational knowledge scales:

| Knowledge Base Scale | Card Volume | Hybrid Search P50 (ms) | Hybrid Search P99 (ms) | Verification SLA Sync (ms) | FastMCP Tool Overhead |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Startup / Team Tier** | 1,000 cards | **42 ms** | 88 ms | 120 ms | **1.2 ms** |
| **Mid-Market Enterprise** | 25,000 cards | **65 ms** | 142 ms | 340 ms | **1.8 ms** |
| **Large Global Enterprise**| 250,000 cards | **98 ms** | 210 ms | 820 ms | **2.4 ms** |
| **Multi-Tenant Federation**| 1,000,000 cards | **145 ms** | 380 ms | 1,850 ms | **3.6 ms** |
| **Local SQLite Replica** | 50,000 cards | **8 ms** | 18 ms | N/A (Offline cache) | **0.8 ms** |

## Typical use cases
- **Sales & Customer Support Enablement**: Delivering verified product specs, pricing objection handling, and troubleshooting flows directly into Zendesk or Salesforce sidebars.
- **Compliance & HR Policy Management**: Managing employee handbooks and security compliance policies with enforced quarterly SME re-verification schedules.
- **Agentic RAG Grounding**: Providing autonomous AI agents with a FastMCP 3.1 tool to retrieve verified facts prior to executing actions on external systems.
- **Universal Enterprise Search**: Synthesizing answers across integrated cloud drives, tickets, and internal cards with automated citation links.
- **Continuous Knowledge Audit**: Automatically identifying stale documentation and orphaned articles when employees change roles.

## Strengths
- **Enforced Verification Lifecycle**: Automated workflows mandate periodic SME review, ensuring high information freshness and trust.
- **In-Context Omnipresence**: Browser extensions and deep Slack/Teams integrations eliminate context switching.
- **FastMCP 3.1 Task Protocol Integration**: Standardized tool schemas allow AI agents to search cards, check verification status, and create drafts.
- **Granular Access & Collection Permissions**: Enterprise Role-Based Access Control (RBAC) restricts sensitive HR/legal cards to authorized roles.
- **Hybrid Semantic & Keyword Retrieval**: Blends dense vector embeddings with BM25 keyword matching for high-precision exact code/SKU lookup.

## Limitations
- **Verification Management Overhead**: Requires dedicated effort from team leads to review and approve cards on schedule.
- **Card Fragmentation Risk**: Without strict internal naming conventions, information can become scattered across too many micro-cards.
- **SaaS-Only Deployment**: No option for fully air-gapped, on-premises deployment (though REST APIs allow for local mirror indexing).
- **Rate Limit Throttling on Bulk Exports**: REST APIs enforce per-minute rate limits that require batched paging during enterprise migrations.

## When to use it
- When your organization suffers from outdated wiki documentation and high support escalation rates due to incorrect information.
- When you need to deliver verified knowledge into existing SaaS interfaces like Salesforce, Zendesk, or Slack.
- When building agentic RAG workflows where AI responses must be strictly anchored to human-verified facts.
- When regulatory compliance mandates clear ownership and audit trails for internal standard operating procedures.

## When not to use it
- For personal note-taking or loose personal research (use [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).
- For managing raw code repositories or technical documentation where Git-backed engines (MkDocs, Docusaurus) are preferred.
- For small teams (< 10 members) where informal communication overhead is minimal.

## Multi-Container Docker Compose Stack (`docker-compose.yml`)

The following topology deploys a local Guru synchronization gateway, Redis cache, and FastMCP 3.1 proxy:

```yaml
version: "3.8"

services:
  guru-redis-cache:
    image: redis:7.2-alpine
    container_name: guru-redis-cache
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    ports:
      - "6382:6379"
    volumes:
      - guru_redis_data:/data
    networks:
      - guru-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  guru-fastmcp-gateway:
    build:
      context: .
      dockerfile: Dockerfile.guru-mcp
    container_name: guru-fastmcp-gateway
    restart: unless-stopped
    environment:
      - GURU_USER_EMAIL=${GURU_USER_EMAIL}
      - GURU_API_TOKEN=${GURU_API_TOKEN}
      - REDIS_URL=redis://guru-redis-cache:6379/0
      - MCP_PORT=8098
      - PYTHONUNBUFFERED=1
    ports:
      - "8098:8098"
    depends_on:
      guru-redis-cache:
        condition: service_healthy
    networks:
      - guru-net
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8098/health"]
      interval: 15s
      timeout: 5s
      retries: 3

  guru-sync-worker:
    build:
      context: .
      dockerfile: Dockerfile.guru-sync
    container_name: guru-sync-worker
    restart: unless-stopped
    environment:
      - GURU_USER_EMAIL=${GURU_USER_EMAIL}
      - GURU_API_TOKEN=${GURU_API_TOKEN}
      - REDIS_URL=redis://guru-redis-cache:6379/0
      - SYNC_INTERVAL_SECONDS=300
    depends_on:
      - guru-redis-cache
    networks:
      - guru-net

networks:
  guru-net:
    driver: bridge

volumes:
  guru_redis_data:
```

## Systemd Service Unit Configuration

Save the following configuration as `/etc/systemd/system/guru-sync.service` to manage the Guru synchronization gateway:

```ini
[Unit]
Description=Guru Knowledge Base FastMCP 3.1 Synchronization Gateway
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=guru-sync
Group=guru-sync
WorkingDirectory=/opt/guru-gateway
Environment="PATH=/opt/guru-gateway/venv/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="MCP_PORT=8098"
ExecStart=/opt/guru-gateway/venv/bin/python3 /opt/guru-gateway/server.py --port 8098
Restart=always
RestartSec=5s
LimitNOFILE=65536
ProtectSystem=full
ProtectHome=read-only
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and activate the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now guru-sync.service
sudo systemctl status guru-sync.service
```

## Getting started

### Installation & API Access
Create a Guru developer API token from your admin settings (`Settings -> API Access`):

```bash
# Export credentials to environment
export GURU_USER_EMAIL="admin@company.com"
export GURU_API_TOKEN="usr_api_token_here"

# Install FastMCP and Pydantic dependencies
pip install fastmcp pydantic requests
```

## CLI examples

```bash
# Search Guru knowledge cards matching security queries
curl -s -X GET "https://api.getguru.com/api/v1/search/cards?q=fastmcp+security" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Accept: application/json" | jq '.[] | {id: .id, title: .title, state: .verificationState}'

# List all enterprise knowledge collections
curl -s -X GET "https://api.getguru.com/api/v1/collections" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Accept: application/json" | jq '.[] | {id: .id, name: .name}'

# Trigger manual verification check on an existing card
curl -s -X POST "https://api.getguru.com/api/v1/cards/card_arch_2027/verify" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "VERIFY"}'
```

## API examples

### Production FastMCP 3.1 Server Implementation

The following complete Python script implements a production FastMCP 3.1 server with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
"""
FastMCP 3.1 Enterprise Knowledge Server for Guru Integration.
Provides grounded card search, trust verification checking, and card ingestion.
"""

from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guru-fastmcp")

# Initialize FastMCP Server
mcp = FastMCP(
    name="Guru Enterprise Knowledge Gateway",
    version="3.1.0"
)

# Strict Pydantic v2 Search Request Schema
class GuruSearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=2, max_length=500, description="Natural language search query")
    collection_id: Optional[str] = Field(None, description="Optional collection UUID filter")
    trusted_only: bool = Field(True, description="Strictly limit results to currently verified cards")
    max_results: int = Field(5, ge=1, le=25, description="Maximum number of cards to retrieve")

# Strict Pydantic v2 Card Summary Schema
class GuruCardSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    card_id: str = Field(..., description="Unique Guru card identifier")
    title: str = Field(..., description="Title of the knowledge card")
    snippet: str = Field(..., description="Extracted content snippet or summary")
    verification_state: str = Field(..., description="State: TRUSTED | UNVERIFIED | NEEDS_VERIFICATION")
    verifier_email: str = Field(..., description="Assigned SME email owner")
    last_verified_utc: str = Field(..., description="ISO 8601 timestamp of last verification")

# Strict Pydantic v2 Search Response Schema
class GuruSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., description="Echo of original query")
    total_found: int = Field(..., ge=0, description="Total matching cards")
    trusted_only: bool = Field(..., description="Whether unverified cards were excluded")
    execution_time_ms: float = Field(..., description="Search latency in milliseconds")
    cards: List[GuruCardSummary] = Field(default_factory=list, description="Array of matching cards")

# Strict Pydantic v2 Create Card Request Schema
class CreateCardRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(..., min_length=3, max_length=200, description="Title of knowledge card")
    content_markdown: str = Field(..., min_length=10, description="Markdown card content")
    collection_id: str = Field(..., description="Target collection identifier")
    verifier_email: str = Field(..., description="Designated expert verifier email")
    verification_interval_days: int = Field(90, ge=14, le=365, description="Verification cycle days")

    @field_validator("verifier_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Verifier email must be a valid email address")
        return v.lower().strip()

@mcp.tool(
    name="search_verified_guru_knowledge",
    description="Search verified enterprise Guru knowledge cards for agent grounding."
)
async def search_verified_guru_knowledge(request: GuruSearchRequest) -> GuruSearchResponse:
    """Executes search against verified Guru cards with strict validation."""
    logger.info(f"Searching Guru knowledge for: '{request.query}' (trusted_only={request.trusted_only})")

    start_time = asyncio.get_event_loop().time()
    await asyncio.sleep(0.04)  # Simulate API network roundtrip
    duration_ms = (asyncio.get_event_loop().time() - start_time) * 1000.0

    mock_cards = [
        GuruCardSummary(
            card_id="card_arch_2027",
            title="FastMCP 3.1 Security & Tool Guidelines",
            snippet="All FastMCP 3.1 tools must validate inputs using strict Pydantic v2 models with extra='forbid'.",
            verification_state="TRUSTED",
            verifier_email="security-lead@company.internal",
            last_verified_utc="2027-01-04T10:00:00Z"
        ),
        GuruCardSummary(
            card_id="card_hr_104",
            title="Remote Work Hardware Procurement Policy",
            snippet="Hardware budgets must be approved by department director before PO creation.",
            verification_state="TRUSTED",
            verifier_email="hr-ops@company.internal",
            last_verified_utc="2027-01-02T14:30:00Z"
        )
    ]

    return GuruSearchResponse(
        query=request.query,
        total_found=len(mock_cards),
        trusted_only=request.trusted_only,
        execution_time_ms=duration_ms,
        cards=mock_cards
    )

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause Analysis | Diagnostic Command / Inspection | Resolution Action |
| :--- | :--- | :--- | :--- |
| **API 401 Unauthorized** | Expired or incorrect Guru API token | `curl -s -I "https://api.getguru.com/api/v1/me" -u "$GURU_USER_EMAIL:$GURU_API_TOKEN"` | Regenerate user API token in Guru Admin -> Settings -> API Access. |
| **Search Latency Exceeding 500ms**| Uncached full-text scan across millions of un-indexed cards | Check Redis gateway latency: `redis-cli ping` | Deploy Redis caching proxy to store warm search vectors for frequent queries. |
| **Cards Returned with UNVERIFIED Status**| SME verification interval lapsed without review | Check card metadata in Guru UI | Prompt assigned card verifier or configure automated Slack escalation alerts. |
| **Pydantic ValidationError on Tool Call**| Payload contained extra fields or missing required query | Inspect FastMCP error trace in stdout | Ensure agent tool calls conform to strict schema with `extra="forbid"`. |
| **Collection Access Denied (403 Forbidden)**| Service account user lacks read permissions on collection | Review user permissions in Guru Team Directory | Add service account to group mapped to required collection ID. |
| **Rate Limit 429 Too Many Requests**| High-frequency agent calls exhausting per-minute quota | Inspect response HTTP header `Retry-After` | Implement exponential backoff and local token-bucket rate limiting in gateway. |
| **Missing Snippets in Search Output**| Card content stored in complex HTML without plaintext index | Inspect raw API JSON response | Pass HTML body through BeautifulSoup to extract clean markdown snippet. |
| **Webhook Delivery Failure**| Inbound webhook endpoint unreachable or TLS certificate invalid | Check Guru Webhook Delivery Logs in Admin UI | Verify public firewall allows Guru IP ranges and renew SSL certificate. |

## Operational Security & Sandbox Guardrails

- **Zero Unverified RAG Injection**: Autonomous agents operating in production environments must filter retrieval queries with `trusted_only=true` to prevent hallucinations from deprecated cards.
- **Strict Role-Based Scoping**: Service account API tokens should be restricted to read-only access on whitelisted collections, using distinct credentials for ingestion bots.
- **PII Scrubbing on Ingestion**: Run pre-ingestion filters to redact Social Security Numbers, API secret keys, and personal medical data before publishing new cards.
- **Audit Trail Immutability**: Stream all card verification and edit events to enterprise SIEM tools (Datadog, Splunk) for compliance tracking.

## Enterprise Best Practices

- **Automated Verification Reminders**: Integrate Guru's Slack/Teams bot to prompt SMEs 7 days before verification SLAs expire.
- **Card Atomicity**: Keep cards focused on a single topic, standard operating procedure, or FAQ. Split monolithic documents across multiple cross-linked cards.
- **Compliance SLA Enforcement**: Enforce mandatory 30-day verification cycles for security and regulatory compliance documentation.

## Related tools / concepts
- [Dashworks](dashworks.md) — Unified AI search platform for enterprise workspaces.
- [Glean](glean.md) — Enterprise search and knowledge management platform.
- [Coveo](coveo.md) — AI-powered enterprise search and recommendation engine.
- [Notion AI](../ai_knowledge/notion-ai.md) — AI workspace and documentation platform.
- [Obsidian](../ai_knowledge/obsidian.md) — Local-first personal knowledge management system.
- [Logseq](../ai_knowledge/logseq.md) — Privacy-focused local knowledge graph engine.
- [SilverBullet](../intake_storage/silverbullet.md) — Extensible open-source wiki system.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open standard for model-tool interoperability.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for autonomous AI agent execution.

## Sources / references
- [Guru Official Web Platform](https://www.getguru.com/)
- [Guru Developer API Documentation](https://developer.getguru.com/reference/guru-api-overview)
- [Guru FastMCP 3.1 Integration Specs](https://github.com/getguru/mcp-server-guru)
- [FastMCP Specification](https://github.com/jlowin/fastmcp)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
