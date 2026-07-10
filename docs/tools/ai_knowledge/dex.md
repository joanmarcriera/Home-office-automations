# Dex

## What it is
Dex is a personal CRM (Customer Relationship Management) and networking tool designed to help individuals manage their professional and personal relationships. It aggregates contacts from various sources like LinkedIn, email, and calendars into a single, unified interface.

## What problem it solves
Maintaining meaningful connections becomes increasingly difficult as professional networks grow. Traditional CRMs are often built for sales teams and are too complex for individual use, while spreadsheets are static and manual. Dex automates contact sync and provides reminders to "keep in touch," reducing the cognitive overhead of networking.

## Where it fits in the stack
Dex sits in the **AI Assistants & Knowledge** layer of the homelab stack, specifically within personal information management. It recently expanded its capabilities with the **Dex MCP Server** and **AI Skills**, allowing AI agents (like Claude 4.8, GPT-5.5, and [Gemma 3](local_llms.md)) to interact directly with a user's contact database via the **MCP 3.0 Task Protocol**.

## Typical use cases
- **Professional Networking:** Tracking follow-ups after conferences or meetings.
- **Job Searching:** Managing recruiters and interviewers.
- **Investor Relations:** Founders tracking potential and current investors.
- **Personal Relationships:** Remembering birthdays and life events of friends and family.
- **Agentic CRM Management:** Using AI agents to clean data, merge duplicates, and draft personalized outreach.

## Strengths
- **Agentic Integration:** Native support for the **MCP 3.0 Task Protocol** and AI Skills. Works out-of-the-box with [Claude Code](../development_ops/claude-code.md).
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

#### Remote HTTP Configuration (July 2026)
For headless agents or [OpenClaw](../development_ops/openclaw.md) setups, Dex now supports Streamable HTTP transport via the **MCP 3.0 Task Protocol**:

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

### Python (MCP Client)
Using the MCP SDK to interact with Dex:

```python
from mcp.client import Client

async with Client("https://api.getdex.com/mcp", token="YOUR_DEX_API_KEY") as client:
    contacts = await client.call_tool("search_contacts", {"query": "Jules"})
    for contact in contacts:
        print(f"Found: {contact['name']} ({contact['email']})")
```

### JavaScript (Fetch)
```javascript
const response = await fetch('https://api.getdex.com/v1/contacts', {
  headers: {
    'Authorization': 'Bearer YOUR_DEX_API_KEY'
  }
});
const data = await response.json();
console.log(data);
```

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
- [ClawHub](https://www.clawhub.ai/) (Skill marketplace)

## Sources / references
- [Official Website](https://getdex.com/)
- [Dex AI Skill Documentation](https://getdex.com/integrations/ai-skill/)
- [Dex MCP Server GitHub](https://github.com/dex-crm/mcp-server)
- [ClawHub Dex Skill](https://www.clawhub.ai/skills/dex)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
