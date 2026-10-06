# Guru

## What it is
Guru is an enterprise AI knowledge management and context platform that captures, verifies, and delivers organizational information directly into employee workflows (Slack, Microsoft Teams, Zendesk, Salesforce, web browsers). Built around a core philosophy of "verified knowledge," Guru replaces stale static wikis with a human-in-the-loop verification engine: subject matter experts (SMEs) are assigned explicit ownership of individual knowledge "Cards" and prompted to periodically re-verify information on automated schedules (e.g. every 30, 60, or 90 days).

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

## Typical use cases
- **Sales & Customer Support Enablement**: Delivering verified product specs, pricing objection handling, and troubleshooting flows directly into Zendesk or Salesforce sidebars.
- **Compliance & HR Policy Management**: Managing employee handbooks and security compliance policies with enforced quarterly SME re-verification schedules.
- **Agentic RAG Grounding**: Providing autonomous AI agents with a FastMCP 3.1 tool to retrieve verified facts prior to executing actions on external systems.
- **Universal Enterprise Search**: Synthesizing answers across integrated cloud drives, tickets, and internal cards with automated citation links.

## Strengths
- **Enforced Verification Lifecycle**: Automated workflows mandate periodic SME review, ensuring high information freshness and trust.
- **In-Context Omnipresence**: Browser extensions and deep Slack/Teams integrations eliminate context switching.
- **FastMCP 3.1 Task Protocol Integration**: Standardized tool schemas allow AI agents to search cards, check verification status, and create drafts.
- **Granular Access & Collection Permissions**: Enterprise Role-Based Access Control (RBAC) restricts sensitive HR/legal cards to authorized roles.

## Limitations
- **Verification Management Overhead**: Requires dedicated effort from team leads to review and approve cards on schedule.
- **Card Fragmentation Risk**: Without strict internal naming conventions, information can become scattered across too many micro-cards.
- **SaaS-Only Deployment**: No option for fully air-gapped, on-premises deployment (though REST APIs allow for local mirror indexing).

## When to use it
- When your organization suffers from outdated wiki documentation and high support escalation rates due to incorrect information.
- When you need to deliver verified knowledge into existing SaaS interfaces like Salesforce, Zendesk, or Slack.
- When building agentic RAG workflows where AI responses must be strictly anchored to human-verified facts.

## When not to use it
- For personal note-taking or loose personal research (use [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).
- For managing raw code repositories or technical documentation where Git-backed engines (MkDocs, Docusaurus) are preferred.
- For small teams (< 10 members) where informal communication overhead is minimal.

## Getting started

### Installation & API Access
Create a Guru developer API token from your admin settings (`Settings -> API Access`).

```bash
# Set credentials in environment
export GURU_USER_EMAIL="admin@company.com"
export GURU_API_TOKEN="usr_api_token_here"
```

## CLI examples

### Querying Cards via cURL
Search for verified cards matching a query string:

```bash
curl -s -X GET "https://api.getguru.com/api/v1/search/cards?q=compliance+policy" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Accept: application/json" | jq '.[] | {id: .id, title: .title, verificationState: .verificationState}'
```

### Listing Collections
Retrieve all accessible knowledge collections:

```bash
curl -s -X GET "https://api.getguru.com/api/v1/collections" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Accept: application/json" | jq '.[] | {id: .id, name: .name}'
```

## API examples

### Programmatically Creating a Verified Card
```python
import requests
import os

def create_guru_card(title: str, content_html: str, collection_id: str, verifier_email: str):
    user = os.environ.get("GURU_USER_EMAIL")
    token = os.environ.get("GURU_API_TOKEN")

    url = "https://api.getguru.com/api/v1/cards"
    payload = {
        "title": title,
        "content": content_html,
        "collectionId": collection_id,
        "shareStatus": "TEAM",
        "verificationInterval": 60,  # Require SME verification every 60 days
        "verifier": {"email": verifier_email}
    }

    response = requests.post(url, auth=(user, token), json=payload)
    response.raise_for_status()
    return response.json()

# Example invocation
new_card = create_guru_card(
    title="2027 AI Safety & RAG Grounding Protocols",
    content_html="<p>All AI agents must retrieve context from FastMCP 3.1 Guru server before taking external write actions.</p>",
    collection_id="col_security_101",
    verifier_email="security-sme@company.com"
)
print(f"Successfully created Guru Card ID: {new_card['id']}")
```

## FastMCP 3.1 Integration Pattern

Below is a complete FastMCP 3.1 tool server demonstrating how AI agents can search Guru knowledge cards and evaluate verification freshness before formulating responses:

```python
import os
import requests
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("GuruKnowledgeServer", version="3.1.0")

class GuruCardSummary(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    card_id: str = Field(..., description="Unique Guru card identifier")
    title: str = Field(..., description="Title of the knowledge card")
    snippet: str = Field(..., description="Excerpt or full HTML content")
    verification_state: str = Field(..., description="Verification state: 'TRUSTED' or 'UNVERIFIED'")
    last_verified_date: Optional[str] = Field(None, description="ISO timestamp of last SME verification")

    @field_validator("verification_state")
    @classmethod
    def validate_state(cls, val: str) -> str:
        normalized = val.upper().strip()
        if normalized not in {"TRUSTED", "UNVERIFIED", "NEEDS_VERIFICATION"}:
            raise ValueError(f"State {val} invalid. Must be TRUSTED, UNVERIFIED, or NEEDS_VERIFICATION")
        return normalized

class SearchCardsResult(BaseModel):
    query: str
    total_found: int
    trusted_cards_only: bool
    cards: List[GuruCardSummary] = Field(default_factory=list)

@mcp.tool()
def search_verified_knowledge(query: str, trusted_only: bool = True) -> str:
    """
    FastMCP tool to search Guru cards for grounded AI reasoning.
    Returns JSON string complying with SearchCardsResult schema.
    """
    user = os.environ.get("GURU_USER_EMAIL", "demo@company.com")
    token = os.environ.get("GURU_API_TOKEN", "demo_token")

    # Simulated API call to Guru Search
    simulated_cards = [
        GuruCardSummary(
            card_id="card_9901",
            title="Q1 2027 Enterprise Security & AI Guardrails",
            snippet="All FastMCP 3.1 tool integrations must utilize Pydantic v2 schemas for payload validation.",
            verification_state="TRUSTED",
            last_verified_date="2027-01-05T09:00:00Z"
        ),
        GuruCardSummary(
            card_id="card_9902",
            title="Legacy Password Rotation Policy",
            snippet="Rotate database credentials every 180 days.",
            verification_state="UNVERIFIED",
            last_verified_date="2025-06-10T12:00:00Z"
        )
    ]

    filtered = [c for c in simulated_cards if not trusted_only or c.verification_state == "TRUSTED"]

    result = SearchCardsResult(
        query=query,
        total_found=len(filtered),
        trusted_cards_only=trusted_only,
        cards=filtered
    )
    return result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Type-Safe Verification Schema (Pydantic v2)

The following Python schema demonstrates strict Pydantic v2 validation for card metadata, compliance tags, and verification SLA requirements:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

class CardVerificationConfig(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    card_id: str = Field(..., description="Guru Card ID")
    title: str = Field(..., min_length=3, max_length=150)
    collection_id: str = Field(...)
    verification_interval_days: int = Field(90, ge=14, le=365)
    owner_email: str = Field(...)
    tags: List[str] = Field(default_factory=list)

    @field_validator("owner_email")
    @classmethod
    def validate_email_domain(cls, val: str) -> str:
        if "@" not in val:
            raise ValueError("Invalid owner email address format")
        return val.lower().strip()

    @model_validator(mode="after")
    def enforce_compliance_verification_sla(self) -> "CardVerificationConfig":
        # Enforce maximum 30-day verification interval for high-risk compliance documentation
        if any(tag.lower() in {"compliance", "security", "gdpr", "hipaa"} for tag in self.tags):
            if self.verification_interval_days > 30:
                raise ValueError(
                    f"Compliance/Security cards (tags={self.tags}) require a verification interval <= 30 days."
                )
        return self

# Validation demonstration
config_payload = {
    "card_id": "card_sec_2027",
    "title": "HIPAA Patient Data Access Procedures",
    "collection_id": "col_medical_ops",
    "verification_interval_days": 30,
    "owner_email": "compliance-officer@health.org",
    "tags": ["hipaa", "security", "patient-privacy"]
}

validated_config = CardVerificationConfig(**config_payload)
print("Validated Guru Verification Config:", validated_config.model_dump_json(indent=2))
```

## Related tools / concepts
- [Dashworks](dashworks.md): Unified AI search platform for enterprise workspaces.
- [Glean](glean.md): Enterprise search and knowledge management platform.
- [Coveo](coveo.md): AI-powered enterprise search and recommendation engine.
- [Notion AI](../ai_knowledge/notion-ai.md): AI workspace and documentation platform.
- [Obsidian](../ai_knowledge/obsidian.md): Local-first personal knowledge management system.
- [Logseq](../ai_knowledge/logseq.md): Privacy-focused local knowledge graph engine.
- [SilverBullet](../intake_storage/silverbullet.md): Extensible open-source wiki system.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Open standard for model-tool interoperability.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Patterns for autonomous AI agent execution.

## Sources / references
- [Guru Official Web Platform](https://www.getguru.com/)
- [Guru Developer API Documentation](https://developer.getguru.com/reference/guru-api-overview)
- [Guru FastMCP 3.1 Integration Specs](https://github.com/getguru/mcp-server-guru)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
