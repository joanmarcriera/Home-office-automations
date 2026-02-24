# AI Agent Frameworks Comparison Hub

A comprehensive repository for comparing and connecting open-source AI agent frameworks.

## Overview

The landscape of AI agent frameworks is rapidly evolving. This repository organizes information about the most popular and capable open-source frameworks to help developers choose the right tool for their specific use case and understand how they can be connected.

## Comparison Table

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
| **DSPy** | Python | Prompt Optimization | Systematically optimizing agent behavior |
| **Mastra** | TypeScript | TypeScript Native All-in-one | Modern web stack and Vercel ecosystem |
| **Semantic Kernel** | Python, .NET, Java | Plugin Architecture | Enterprise integration and Microsoft ecosystem |
| **Haystack** | Python | Modular Search Pipelines | Search-based applications and RAG |
| **mcp-agent** | Python | MCP-optimized Patterns | Lightweight MCP development (Anthropic patterns) |
| **Upsonic** | Python | Security-first Approach | Financial sector and secure multi-agent scaling |

## Connecting Tools (MCP)

Most of these frameworks now support the **Model Context Protocol (MCP)**, an open protocol that standardizes how applications interact with LLMs. This allows agents built in different frameworks to connect to a shared ecosystem of tools and resources (like ClickHouse, GitHub, Slack, etc.).

### How it works:
- **MCP Servers** define sets of tools and resources.
- **Frameworks** act as MCP Clients that can discover and use these tools.
- This decoupling allows you to build a tool once as an MCP server and use it across any framework listed above.

## Using the Comparison Tool

We provide a Python script to help you explore and compare these frameworks directly from the CLI.

### List all agents
```bash
python3 scripts/compare_agents.py list
```

### Filter by language
```bash
python3 scripts/compare_agents.py list --lang TypeScript
```

### Compare two agents side-by-side
```bash
python3 scripts/compare_agents.py compare lang-chain pydantic-ai
```

### Get full details for an agent
```bash
python3 scripts/compare_agents.py details crew-ai
```

## Data Structure

The data is stored in `data/agents.json`, allowing for easy programmatic access and updates.

---
*Organized based on latest industry reports as of 2025.*
