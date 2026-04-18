# Dex

## What it is
Dex is a personal CRM (Customer Relationship Management) and networking tool designed to help individuals manage their professional and personal relationships. It aggregates contacts from various sources like LinkedIn, email, and calendars into a single, unified interface.

## What problem it solves
Maintaining meaningful connections becomes increasingly difficult as professional networks grow. Traditional CRMs are often built for sales teams and are too complex for individual use, while spreadsheets are static and manual. Dex automates contact sync and provides reminders to "keep in touch," reducing the cognitive overhead of networking.

## Where it fits in the stack
Dex sits in the **AI Assistants & Knowledge** layer of the homelab stack, specifically within personal information management. It recently expanded its capabilities with the **Dex MCP Server** and **AI Skills**, allowing AI agents (like Claude) to interact directly with a user's contact database.

## Typical use cases
- **Professional Networking:** Tracking follow-ups after conferences or meetings.
- **Job Searching:** Managing recruiters and interviewers.
- **Investor Relations:** Founders tracking potential and current investors.
- **Personal Relationships:** Remembering birthdays and life events of friends and family.

## Strengths
- **Agentic Integration:** Native support for the Model Context Protocol (MCP) and AI Skills.
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

## Related tools / concepts
- **[Monica CRM](https://www.monicahq.com/):** A popular open-source, self-hosted personal CRM alternative.
- **[MCP (Model Context Protocol)](../automation_orchestration/mcp-registry.md):** The protocol Dex uses to expose its tools to AI agents.
- **[Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md):** The environment where Dex AI skills are deployed.

## Sources / references
- [Official Website](https://getdex.com/)
- [Dex AI Skill Documentation](https://getdex.com/integrations/ai-skill/)
- [Dex MCP Server GitHub](https://github.com/dex-crm/mcp-server)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
