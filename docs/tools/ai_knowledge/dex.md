# Dex

## What it is
Dex is a personal CRM (Customer Relationship Management) and networking tool designed to help individuals manage their professional and personal relationships. It aggregates contacts from various sources like LinkedIn, email, and calendars into a single, unified interface.

## Architecture & System Overview
Dex integrates individual communication channels into a centralized contact graph exposed to agentic environments via FastMCP 3.1 servers.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            DEX INTEGRATION ARCHITECTURE                          │
└──────────────────────────────────────────────────────────────────────────────────┘

   Raw Ingestion Channels            Dex Core Infrastructure            FastMCP 3.1 Gateway
 ┌────────────────────────┐       ┌───────────────────────────┐      ┌────────────────────────┐
 │ - LinkedIn Sync        │──────>│ - Unified Contact Graph   │─────>│ - FastMCP 3.1 Server   │
 │ - Google/Outlook Cal   │       │ - Touchpoint Timelines    │      │ - MCP Tools & Skills   │
 │ - Email Metadata       │       │ - Reminder Rules Engine   │      │ - Streamable HTTP      │
 └────────────────────────┘       └───────────────────────────┘      └────────────────────────┘
                                                                                 │
                                                                                 ▼
                                                                     ┌────────────────────────┐
                                                                     │ Agentic Execution Pool │
                                                                     │ - Claude Code          │
                                                                     │ - OpenClaw / Jules     │
                                                                     └────────────────────────┘
```

## What problem it solves
Maintaining meaningful connections becomes increasingly difficult as professional networks grow. Traditional CRMs are often built for sales teams and are too complex for individual use, while spreadsheets are static and manual. Dex automates contact sync and provides reminders to "keep in touch," reducing the cognitive overhead of networking.

## Where it fits in the stack
Dex sits in the **AI Assistants & Knowledge** layer of the homelab stack, specifically within personal information management. In early 2027, it expanded its capabilities with the **Dex MCP Server** and **AI Skills**, allowing frontier AI models (such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4**, **Gemma 4**, and **Qwen 3.6**) to interact directly with a user's contact database via the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** specifications.

## Typical use cases
- **Professional Networking:** Tracking follow-ups after meetings or conferences.
- **Job Searching:** Managing recruiters and interviewers.
- **Investor Relations:** Founders tracking potential and current investors.
- **Personal Relationships:** Remembering birthdays and life events of friends and family.
- **Agentic CRM Management:** Using AI agents to clean data, merge duplicates, and draft personalized outreach.

## Comparison Matrix

| Feature | Dex CRM | Monica CRM | Hubspot Personal | Notion CRM |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Individual networking & relationships | Self-hosted personal CRM | Sales pipelines | Flexible database manual CRM |
| **Hosting Model** | Cloud Managed SaaS | Self-hosted Docker | Cloud Managed SaaS | Cloud Managed SaaS |
| **MCP 3.1 Native** | Yes (FastMCP 3.1 Server) | Community plugin | No | Community plugin |
| **LinkedIn Integration**| Browser extension sync | Manual import | Premium add-on | Manual / Web Clipper |
| **Calendar Sync** | Automated 2-way | Basic CalDAV | Automated 2-way | Third-party widget |

## Strengths
- **Agentic Integration:** Native support for **MCP 3.1 / FastMCP 3.1** and AI Skills. Works out-of-the-box with [Claude Code](../development_ops/claude-code.md).
- **Cross-Platform:** Available as a web app, mobile app, and browser extension.
- **Automation:** Two-way sync with Google Calendar, Outlook, and LinkedIn.
- **Clean UI:** Optimized for individual productivity rather than corporate sales pipelines.

## Limitations
- **Subscription Model:** Requires a paid subscription for full features (e.g., unlimited contacts, advanced sync).
- **Privacy Trade-offs:** Requires access to sensitive personal data (email, calendar, LinkedIn) to provide full value.
- **Proprietary:** Unlike self-hosted solutions, your data resides on Dex's servers.

## When to use it
Use Dex if you are a "super-connector," freelancer, or professional whose success depends on maintaining a large, active network and you want your AI assistant to have context about who you know.

## When not to use it
Avoid Dex if you prefer a fully self-hosted, offline-first approach to personal data, or if your networking needs are simple enough to be handled by a basic contact list or calendar.

## Getting started

### Local Setup (MCP Server)
To allow your AI agent (like [Claude Desktop](../development_ops/claude-code.md) or [Gemma 3](local_llms.md)) to access Dex, add the following to your configuration:

#### Standard Stdio Configuration
```json
{
  "mcpServers": {
    "dex": {
      "command": "npx",
      "args": ["-y", "@dex-crm/mcp-server"],
      "env": {
        "DEX_API_KEY": "YOUR_DEX_API_KEY"
      }
    }
  }
}
```

#### Remote HTTP Configuration (January 2027)
For headless agents or [OpenClaw](../development_ops/openclaw.md) setups, Dex supports Streamable HTTP transport via the **MCP 3.1 / FastMCP 3.1** protocols:

```json
{
  "mcpServers": {
    "dex-remote": {
      "url": "https://api.getdex.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_DEX_API_KEY"
      }
    }
  }
}
```

### Enabling AI Skills
1. Log in to your Dex account.
2. Navigate to **Settings > Integrations**.
3. Enable the **AI Skills** toggle.
4. Your agent will now be able to search contacts, add notes, and manage follow-ups via natural language.

## CLI examples

### Installation
The Dex CLI is part of the MCP server package:
```bash
npm install -g @dex-crm/mcp-server
```

### Usage
```bash
# List tools available via the Dex MCP server
dex-mcp list-tools

# Test contact search via CLI
dex-mcp call search_contacts --query "Jules"
```

## API examples

### Python (MCP Client with Strict Pydantic v2 Validation)
The following example shows how to query the Dex contact search tool using the Model Context Protocol, parsing and validating the results using strict **Pydantic v2** schemas to integrate contacts directly into downstream reasoning loops of models like Claude 5.6 and GPT-5.6.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# Define strict Pydantic v2 schemas for contact modeling
class ContactInteraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: str = Field(..., description="ISO 8601 date of the last interaction")
    interaction_type: str = Field(..., description="Type of interaction (e.g., Email, Meeting, Call)")
    notes: Optional[str] = Field(None, description="Notes recorded during the interaction")

class DexContact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="Unique Dex contact identifier")
    first_name: str = Field(..., min_length=1, description="Given name of the contact")
    last_name: Optional[str] = Field(None, description="Family name of the contact")
    email: Optional[EmailStr] = Field(None, description="Primary verified email address")
    company: Optional[str] = Field(None, description="Current associated organization")
    title: Optional[str] = Field(None, description="Professional job title")
    last_interaction: Optional[ContactInteraction] = Field(None, description="Details of the latest touchpoint")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name

class DexContactSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., description="The search string queried")
    results_count: int = Field(..., ge=0, description="Total number of matching results")
    contacts: List[DexContact] = Field(default_factory=list, description="List of validated contacts")

# Simulated MCP Client tool call and strict Pydantic v2 validation
async def fetch_and_validate_contacts(query_str: str) -> DexContactSearchResponse:
    simulated_raw_payload = {
        "query": query_str,
        "results_count": 1,
        "contacts": [
            {
                "id": "dex_usr_8923a",
                "first_name": "Jules",
                "last_name": "Agent",
                "email": "jules@example.com",
                "company": "Cognitive Automation Corp",
                "title": "Principal Systems Engineer",
                "last_interaction": {
                    "date": "2026-11-26",
                    "interaction_type": "Meeting",
                    "notes": "Reviewed the Ralph-loop Batch 316 freshness audits."
                }
            }
        ]
    }

    validated_response = DexContactSearchResponse.model_validate(simulated_raw_payload)
    return validated_response

if __name__ == "__main__":
    response = asyncio.run(fetch_and_validate_contacts("Jules"))
    print(f"Validated Search Query: '{response.query}' (Found {response.results_count} contact(s))")
    for contact in response.contacts:
        print(f"Name: {contact.full_name}")
        print(f"Email: {contact.email}")
        print(f"Company: {contact.company} | Title: {contact.title}")
        if contact.last_interaction:
            print(f"Last Touchpoint: {contact.last_interaction.date} via {contact.last_interaction.interaction_type}")
            print(f"Notes: {contact.last_interaction.notes}")
```

### FastMCP 3.1 Server Integration Pattern
Exposes Dex CRM capabilities via FastMCP 3.1 to support agentic contact lookup and touchpoint recording.

```python
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "dex-crm-server",
    instructions="Provides FastMCP 3.1 tools to search contacts, log touchpoints, and fetch networking reminders."
)

class ContactSearchInput(BaseModel):
    query: str = Field(..., description="Name, company, or title keyword to search.")

class LogInteractionInput(BaseModel):
    contact_id: str = Field(..., description="Dex contact ID.")
    note: str = Field(..., description="Summary of interaction.")
    interaction_type: str = Field("Meeting", description="Interaction modality (e.g. Email, Call, Meeting).")

@mcp.tool()
async def search_dex_contacts(input_data: ContactSearchInput) -> List[Dict[str, Any]]:
    """Searches Dex personal CRM for matching contacts."""
    dex_api_url = f"https://api.getdex.com/v1/contacts?search={input_data.query}"
    headers = {"Authorization": "Bearer YOUR_DEX_API_KEY"}

    async with httpx.AsyncClient() as client:
        res = await client.get(dex_api_url, headers=headers)
        res.raise_for_status()
        return res.json().get("contacts", [])

@mcp.tool()
async def log_dex_touchpoint(input_data: LogInteractionInput) -> Dict[str, Any]:
    """Logs a new touchpoint interaction in Dex for a specific contact."""
    dex_api_url = f"https://api.getdex.com/v1/contacts/{input_data.contact_id}/interactions"
    headers = {"Authorization": "Bearer YOUR_DEX_API_KEY"}
    payload = {
        "type": input_data.interaction_type,
        "note": input_data.note
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(dex_api_url, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting
- **API Token Security**: Store `DEX_API_KEY` securely in `.env` files or secret managers rather than hardcoding in MCP configurations.
- **Rate Limit Handling**: When running automated contact deduplication scripts, implement exponential backoff to handle Dex HTTP 429 rate limits.
- **Contact Merging Safeguards**: Always require explicit agent confirmation prior to executing irreversible contact merge operations.

## Related tools / concepts
- [Monica CRM](../../services/radicale.md) (Self-hosted alternative)
- [Gemma 3](local_llms.md)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Jules](jules.md)
- [Notion AI](notion-ai.md)
- [Obsidian](obsidian.md)
- [Logseq](logseq.md)
- [ClawHub](clawhub.md) (Skill marketplace)

## Sources / references
- [Official Website](https://getdex.com/)
- [Dex AI Skill Documentation](https://getdex.com/integrations/ai-skill/)
- [Dex MCP Server GitHub](https://github.com/dex-crm/mcp-server)
- [ClawHub Dex Skill](https://www.clawhub.ai/skills/dex)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
