# AI Agent Frameworks & Integrations Hub

A comprehensive repository for comparing and connecting open-source AI agent frameworks, document management systems, and communication tools.

## Overview

The landscape of AI agents and their ability to interact with the world is rapidly evolving. This repository organizes information about the most popular AI frameworks and the essential integrations needed to build functional, real-world autonomous systems.

## Comparison: AI Agent Frameworks

| Framework | Languages | Superpower | Best For |
|-----------|-----------|------------|----------|
| **LangChain** | Python, JS/TS | Composability & Ecosystem | General-purpose agents & complex workflows |
| **LangGraph** | Python, JS/TS | State Machines & Control | Complex multi-step agents with conditional logic |
| **AutoGen** | Python | Collaborative Agent Chats | Research-backed multi-agent systems |
| **CrewAI** | Python | Role-based Delegation | 'AI Team' mental model and task orchestration |
| **LlamaIndex** | Python, TS | Data Ingestion & Retrieval | Knowledge-driven agents & RAG |
| **PydanticAI** | Python | Type Safety & Validation | Production-grade reliability with Pydantic |
| **Claude Agent SDK** | Python, TS | Official Claude Integration | Secure production deployments with Claude |
| **OpenAI Agents SDK** | Python, TS | Handoffs & Delegation | Lightweight, composable agents focused on delegation |
| **Google ADK** | Python, Java | Multi-language & UI/CLI | Gemini ecosystem and traditional software dev feel |
| **Agno** | Python | Speed & Minimal Code | High-performance agent fleets at scale |
| **Mastra** | TypeScript | TypeScript Native All-in-one | Modern web stack and Vercel ecosystem |

## Productivity & Communication Integrations

To be useful, agents need to connect to your documents, calendar, and email. Below are key tools and methods for these connections.

| Tool | Category | Key Connectivity | Use Case |
|------|----------|------------------|----------|
| **Paperless-ngx** | Document Management | REST API, IMAP, Samba | Archiving and retrieving personal documents |
| **Composio** | Integration Platform | MCP, Direct API, OAuth | 850+ toolkits for Gmail, Calendar, Slack, etc. |
| **Nylas** | Communication API | Unified API, MCP, CLI | Simplified access to 250+ email/calendar providers |
| **MCP Servers** | Protocol Standard | Stdio, SSE, Remote | Standardized tool access (Gmail, GCal, etc.) |

### Document Management (Paperless-ngx)
Paperless-ngx serves as a powerful "brain extension" for agents, allowing them to search through physical documents that have been digitized. Agents can connect via the **REST API** to query documents or use **IMAP** to feed new documents into the system.

### Calendar & Email Connectivity
- **Model Context Protocol (MCP)**: The de facto standard for connecting agents to tools. Use dedicated MCP servers for Google Calendar and Gmail to give agents native scheduling and communication powers.
- **Unified APIs (Nylas/Composio)**: These platforms abstract away the complexity of OAuth and provider-specific quirks, allowing an agent to work across Gmail, Outlook, and other providers with a single interface.

## Using the Hub Tool

We provide a Python script to help you explore and compare these frameworks and integrations directly from the CLI.

### Explore Agents
```bash
python3 scripts/compare_agents.py list
python3 scripts/compare_agents.py compare lang-chain pydantic-ai
python3 scripts/compare_agents.py details crew-ai
```

### Explore Integrations
```bash
python3 scripts/compare_agents.py list-int
python3 scripts/compare_agents.py details-int paperless-ngx
```

## Data Structure

The data is stored in the `data/` directory in JSON format:
- `data/agents.json`: Framework details.
- `data/integrations.json`: Connectivity and productivity tool details.

---
*Organized based on latest industry reports as of 2025.*
