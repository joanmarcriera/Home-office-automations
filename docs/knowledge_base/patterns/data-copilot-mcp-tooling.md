# Data Copilot: MCP Tool & Data Standardization

This document outlines the standardization of tool and data access for the Data Copilot using the Model Context Protocol (MCP 3.0). By adopting MCP, we ensure that specialized agents in the Text-to-SQL pipeline can interact with diverse data sources (SQL, docs, APIs) through a unified, machine-parseable interface.

## What it is
The Model Context Protocol (MCP) serves as the universal interface for the Data Copilot, abstracting the complexities of direct database connections, document parsing, and API calls into a standardized set of resources and tools. It provides a unified interface for AI agents, such as [Gemma 3](../../tools/ai_knowledge/local_llms.md), to interact with various data sources and tools, acting as a secure proxy that translates agentic intent into technical execution.

## What problem it solves
In a complex Data Copilot architecture, agents often need to access diverse data sources (SQL databases, internal documentation, KPI glossaries, etc.). Traditionally, this requires hard-coding connectors for each source, leading to brittle code and difficult scaling (the "N+1 connector problem"). MCP standardization solves this by providing a single protocol for all data interactions, making the system more modular, secure, and easier to extend while decoupling the reasoning engine from implementation details.

## Where it fits in the stack
It sits in the **Orchestration and Tooling layer**, between the reasoning agents (e.g., Intent Agent, SQL Generator) and the data storage or service providers (e.g., SQLite, PostgreSQL, Home Assistant, local files). It effectively bridges the gap between the [Orchestration Layer](../../architecture/data-copilot-text-to-sql.md) and the raw **Data Layer**.

## Typical use cases
- **Database Access**: Exposing a local SQLite database to a Text-to-SQL agent via `mcp-server-sqlite`.
- **Documentation RAG**: Providing a search interface for technical documentation to a RAG-enabled agent.
- **KPI Standardization**: Accessing a centralized KPI glossary resource to prevent calculation hallucinations.
- **Live State Integration**: Querying real-time data from IoT devices or external APIs via the Home Assistant MCP server.
- **Agentic Workflows**: Allowing agents to perform actions like creating Jira tickets or sending Slack messages through a unified tool interface.

## Strengths
- **Decoupling**: Agents are no longer tied to specific database dialects or API implementations.
- **Security**: Allows for fine-grained access control, auditing, and "least privilege" enforcement at the protocol level.
- **Portability**: MCP servers can be easily swapped or moved without changing the agent reasoning logic.
- **Unified Interface**: Reduces the complexity of building and maintaining multiple custom connectors for diverse data types.

## Limitations
- **Overhead**: Introducing an abstraction layer can add slight network latency to requests.
- **Protocol Maturity**: While MCP 3.0 is a significant milestone, the ecosystem of servers for specialized databases is still growing.
- **Configuration**: Requires setting up and managing separate MCP server instances, which adds initial setup complexity.

## When to use it
- When building a multi-agent system that needs to access multiple, diverse data sources.
- When you want to ensure a clean separation between agent logic and data access.
- When you need a scalable and secure way to expose local tools to AI agents.
- For "free/cheap-first" architectures where local data sources must be integrated with cloud LLMs.

## When not to use it
- For very simple, single-source applications where the overhead of MCP isn't justified.
- If your environment already has a well-established and standardized data access layer that isn't compatible with MCP.
- When the data source already provides a native, highly optimized agentic interface that meets all security needs.

## Getting started

### 1. Install an MCP Server
The easiest way to start is by installing a standard server, such as the SQLite server.

```bash
# Install the MCP SQLite server globally
npm install -g @modelcontextprotocol/server-sqlite
```

### 2. Configure the Server
Create a configuration for your agent host (e.g., Claude Desktop or a custom orchestrator) to point to your database.

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "--db",
        "/path/to/your/database.db"
      ]
    }
  }
}
```

### 3. Initialize MCP Client
Use the MCP SDK to connect your Data Copilot agents to the server.

```python
from mcp import Client, StdioServerParameters

# Define connection parameters
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-sqlite", "--db", "inventory.db"]
)

# Initialize client and connect
async with Client(server_params) as client:
    await client.initialize()
    # Now tools and resources are available to the agent
```

## CLI examples

### Listing Available Tools
Check which tools are exposed by an MCP server to the Data Copilot.
```bash
mcp-cli tools list --server sqlite
```

### Reading a Resource
Access a specific resource, such as a schema definition or KPI glossary.
```bash
mcp-cli resources read mcp://sqlite/schema/main
```

### Executing a Tool Call
Manually trigger a tool call for testing the data pipeline.
```bash
mcp-cli tools call sqlite execute_query --params '{"sql": "SELECT count(*) FROM users"}'
```

## API examples

### Calling a Tool from an Agent (TypeScript)
Example of an agentic tool call to fetch data via MCP.

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

async function runQuery(client: Client, sql: string) {
  const result = await client.callTool({
    name: "execute_query",
    arguments: { sql }
  });

  console.log("Query Results:", result.content);
}
```

### Serving a Custom Resource (Python)
Standardizing a KPI Glossary as an MCP resource.

```python
from mcp.server import Server

server = Server("kpi-glossary")

@server.list_resources()
async def list_resources():
    return [
        {
            "uri": "glossary://metrics",
            "name": "Corporate KPI Glossary",
            "mimeType": "application/json"
        }
    ]

@server.read_resource("glossary://metrics")
async def read_resource(uri):
    return "{\"net_margin\": \"(Revenue - Expenses) / Revenue\"}"

server.run()
```

### Multi-Server Orchestration
Connecting a Data Copilot agent to multiple MCP servers simultaneously.

```python
async with MultiServerClient() as manager:
    await manager.add_server("db", server_params_sqlite)
    await manager.add_server("docs", server_params_files)

    # Agent can now reason across both SQL and Documentation
    response = await agent.think("Find the Net Margin formula in docs and then calculate it for Q2")
```

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) — The primary orchestration framework.
- [Agent Protocols](../agent_protocols.md) — Broader context on MCP and other standards.
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md) — Using MCP for document retrieval.
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — Validating queries generated via MCP tools.
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md) — Standardizing output formats.
- [Tool Calling & Model Context Protocol (MCP)](tool-calling-and-mcp.md) — Deep dive into the protocol itself.
- [Claude Tool Search](claude-tool-search.md) — Discovery patterns for MCP tools.

## Sources / references
- [Model Context Protocol (MCP) Official Site](https://modelcontextprotocol.io/)
- [Anthropic: Introducing MCP](https://www.anthropic.com/news/model-context-protocol)
- [MCP Python SDK (GitHub)](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK (GitHub)](https://github.com/modelcontextprotocol/typescript-sdk)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
