# Dex

## What it is
Dex is an enterprise-ready personal CRM (Customer Relationship Management) and professional network intelligence platform designed to help executives, founders, software engineers, and autonomous AI agents manage relationships at scale. It aggregates contact data, interaction logs, email threads, and calendar events from platforms like LinkedIn, Google Workspace, Microsoft Outlook, and custom webhooks into a unified relational database.

In the early 2027 ecosystem, Dex serves as a key relationship context layer for AI agent workflows. Via the **Dex MCP Server** and **AI Skills** framework, frontier models (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4**, and **Qwen 3.6**) can query, update, and summarize professional networks through the **Model Context Protocol (MCP 3.1 / FastMCP 3.1)**.

## Architecture & Network Intelligence Ingestion Flow
Dex processes multi-source contact signals through automated background sync workers, normalizing interaction streams and exposing contact context to both human users and FastMCP 3.1 agentic tools.

```
+---------------------------------------------------------------------------------+
|                               External Data Sources                             |
|  +------------------+   +-------------------+   +----------------------------+  |
|  | LinkedIn Profile |   | Google Workspace  |   | Microsoft Outlook Calendar |  |
|  +--------+---------+   +---------+---------+   +-------------+--------------+  |
+-----------|-----------------------|---------------------------|-----------------+
            |                       |                           |
            v                       v                           v
+---------------------------------------------------------------------------------+
|                              Dex Ingestion Engine                               |
|  +---------------------------------------------------------------------------+  |
|  | OAuth Sync Workers & Webhook Receivers                                    |  |
|  +-------------------------------------+-------------------------------------+  |
|                                        |                                        |
|                                        v                                        |
|  +---------------------------------------------------------------------------+  |
|  | Contact Normalization, Deduplication & Interaction Graph Mapping           |  |
|  +-------------------------------------+-------------------------------------+  |
+----------------------------------------|----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                             Dex Relational Storage                              |
|  +---------------------------------------------------------------------------+  |
|  | Person Entities | Company Nodes | Touchpoint Timelines | AI Reminders     |  |
|  +-------------------------------------+-------------------------------------+  |
+----------------------------------------|----------------------------------------+
                                         |
            +----------------------------+----------------------------+
            |                                                         |
            v                                                         v
+---------------------------------------+ +---------------------------------------+
|          Dex Frontend & App           | |      FastMCP 3.1 Server / AI Skills   |
|  - Web UI & Mobile Client             | |  - Model Context Protocol (MCP 3.1)  |
|  - Browser Extension                  | |  - Natural Language Agent Tooling     |
+---------------------------------------+ +---------------------------------------+
                                                                      |
                                                                      v
                                          +---------------------------------------+
                                          |          Frontier AI Agents           |
                                          |  - Claude 5.6 / GPT-5.6 / Gemini 4.0  |
                                          |  - Claude Code / OpenClaw Integration |
                                          +---------------------------------------+
```

## What problem it solves
Maintaining meaningful professional connections becomes increasingly difficult as personal networks expand beyond hundreds of individuals. Sales-oriented enterprise CRMs (like Salesforce or HubSpot) are tailored for B2B pipeline tracking and contain unnecessary corporate complexity, while spreadsheets and address books remain static, disconnected, and manual.

Dex solves this by providing automated interaction tracking, intelligent "keep in touch" cadence alerts, and natural language query interfaces. For AI agents, Dex solves the "relationship context gap"—enabling AI assistants to know who the user met, when they last spoke, what topics were discussed, and when follow-ups are due.

## Where it fits in the stack
**Category**: AI Knowledge & Personal Information Management (PIM)
Dex operates at the **Knowledge Ops & User Context** layer of the homelab and workspace stack. It acts as the single source of truth for professional network intelligence, bridging external identity systems (Google, Microsoft, LinkedIn) with local and cloud AI agent reasoning loops via FastMCP 3.1.

## Feature Matrix & CRM Comparison

| Feature | Dex | Monica CRM | ArchiveBox | Folk CRM |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Target** | Individual Super-Connectors | Open-Source Personal CRM | CLI Web Archiver | Lightweight B2B Teams |
| **Data Hosting** | Cloud SaaS + Local Sync | Self-Hosted (PHP/Docker) | Self-Hosted (Python) | Cloud SaaS |
| **Native MCP 3.1 Support** | First-class (`@dex-crm/mcp-server`) | Community Adapters | Script Wrappers | API Gateway Required |
| **LinkedIn & Calendar Sync** | Automated Two-Way Sync | Manual Import / iCal | N/A | Chrome Extension Sync |
| **AI Relationship Insights** | Built-in AI Skills & Summaries | Basic Reminders | N/A | AI Column Formulas |
| **Mobile & Browser App** | iOS, Android, Chrome Extension | Responsive Web | Web UI | Web App |

## Operational Best Practices & Network Hygiene
1. **API Key Security**: Store `DEX_API_KEY` credentials in local environment secret vaults or Docker secrets rather than hardcoding them in MCP client configuration files.
2. **Sync Cadence Optimization**: Set calendar and email synchronization intervals to 15-minute windows to prevent API rate-limiting while maintaining fresh interaction data.
3. **Deduplication Checks**: Periodically run the built-in deduplication engine before executing automated agent batch updates to prevent duplicate contact entities.
4. **Privacy & Data Scoping**: Configure granular permissions when granting AI agents access to contact notes to protect sensitive personal relationship details.

## Typical use cases
- **Professional Network Nurturing**: Tracking follow-up tasks and conversation history after industry conferences or investor meetings.
- **Executive & Advisory Relationship Management**: Managing board members, advisors, and key external partners with structured cadence reminders.
- **Autonomous Agent Outreach Support**: Enabling AI agents (like [Claude Code](../development_ops/claude-code.md) or [OpenClaw](../development_ops/openclaw.md)) to draft personalized email follow-ups using full historical contact context.
- **Job Search & Candidate Tracking**: Tracking recruiters, hiring managers, and interview feedback during career transitions.

## Strengths
- **Native MCP 3.1 Integration**: First-class `@dex-crm/mcp-server` package allows AI models to query relationship graphs without custom scraping.
- **Cross-Platform Availability**: Synchronized across iOS, Android, desktop web, and browser extensions.
- **Automated Sync Workers**: Continuous background integration with Google Calendar, Outlook, and LinkedIn eliminates manual logging.
- **User Experience**: Modern, clean user interface optimized for personal productivity and quick note entry.

## Limitations
- **SaaS Model**: Data is hosted on managed Dex cloud infrastructure rather than 100% self-hosted local databases.
- **Subscription Required**: Advanced features like unlimited contact sync and automated LinkedIn enrichment require paid plans.
- **Third-Party API Limits**: External calendar and email providers may enforce strict rate limits during initial bulk backfills.

## When to use it
- When you maintain a large professional network and require automated interaction logging across email, calendar, and LinkedIn.
- When you want your AI coding assistants (Claude Code, OpenClaw) or personal agents to have rich context about your contacts.
- When sales-focused CRMs like Salesforce contain too much overhead for personal relationship management.

## When not to use it
- If you strictly require 100% self-hosted, air-gapped infrastructure (use [Monica CRM](../../services/radicale.md) or local SQL databases instead).
- When managing multi-stage B2B enterprise sales pipelines with revenue attribution and deal stages.

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

#### Remote HTTP Configuration
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

### FastMCP 3.1 Dex Integration Server (Python)
The following Python script demonstrates building a custom FastMCP 3.1 wrapper around the Dex API to expose enriched contact tools for agent workflows:

```python
import os
import requests
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("dex-relationship-server", version="3.1.0")

class ContactQuery(BaseModel):
    query: str = Field(..., description="Name, company, or title search term")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum contacts to return")

class ContactNote(BaseModel):
    contact_id: str = Field(..., description="Dex contact unique identifier")
    note_text: str = Field(..., min_length=3, description="Interaction summary or note")

@mcp.tool()
def search_dex_contacts(params: ContactQuery) -> dict:
    """Search Dex CRM contacts by keyword or name."""
    api_key = os.getenv("DEX_API_KEY", "demo_key")
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://api.getdex.com/v1/contacts/search?q={params.query}&limit={params.limit}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def add_interaction_note(params: ContactNote) -> dict:
    """Append a new meeting or call note to a Dex contact entry."""
    api_key = os.getenv("DEX_API_KEY", "demo_key")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = f"https://api.getdex.com/v1/contacts/{params.contact_id}/notes"

    try:
        response = requests.post(url, headers=headers, json={"text": params.note_text}, timeout=10)
        response.raise_for_status()
        return {"status": "success", "note_added": params.note_text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### Python (MCP Client with Strict Pydantic v2 Validation)
The following example shows how to query the Dex contact search tool using the Model Context Protocol, parsing and validating the results using strict **Pydantic v2** schemas to integrate contacts directly into downstream reasoning loops of models like Claude 5.6 and GPT-5.6.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class ContactInteraction(BaseModel):
    date: str = Field(..., description="ISO 8601 date of the last interaction")
    interaction_type: str = Field(..., description="Type of interaction (e.g., Email, Meeting, Call)")
    notes: Optional[str] = Field(None, description="Notes recorded during the interaction")

class DexContact(BaseModel):
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
    query: str = Field(..., description="The search string queried")
    results_count: int = Field(..., ge=0, description="Total number of matching results")
    contacts: List[DexContact] = Field(default_factory=list, description="List of validated contacts")

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
                    "notes": "Reviewed the Ralph-loop Batch 821 docs quality standards."
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

## Related tools / concepts
- [Monica CRM](../../services/radicale.md) — Self-hosted open-source personal CRM alternative.
- [Gemma 3](local_llms.md) — Open-weight local model family.
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Tool integration standard.
- [Claude Code](../development_ops/claude-code.md) — Agentic coding CLI tool.
- [OpenClaw](../development_ops/openclaw.md) — Autonomous personal assistant framework.
- [Jules](jules.md) — Self-contained coding agent environment.
- [Obsidian](obsidian.md) — Local markdown knowledge base.

## Sources / references
- [Official Website](https://getdex.com/)
- [Dex AI Skill Documentation](https://getdex.com/integrations/ai-skill/)
- [Dex MCP Server GitHub](https://github.com/dex-crm/mcp-server)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
