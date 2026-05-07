# Data Copilot: MCP Tool & Data Standardization

This document outlines the standardization of tool and data access for the Data Copilot using the Model Context Protocol (MCP). By adopting MCP, we ensure that specialized agents in the Text-to-SQL pipeline can interact with diverse data sources (SQL, docs, APIs) through a unified, machine-parseable interface.

## What it is
The Model Context Protocol (MCP) serves as the universal interface for the Data Copilot, abstracting the complexities of direct database connections, document parsing, and API calls into a standardized set of resources and tools.

## What problem it solves
It eliminates the "N+1 connector problem" where every new data source requires a custom integration. It also decouples the reasoning engine (LLM) from the data implementation details, allowing for safer, audited, and cost-effective data access.

## Where it fits in the stack
It sits between the **Orchestration Layer** (n8n, LangGraph) and the **Data Layer** (PostgreSQL, SQLite, Markdown docs). It acts as a secure proxy that translates agentic intent into technical execution.

## Typical use cases
- Exposing a local SQLite database to a cloud-based LLM without exposing the full database.
- Providing real-time documentation retrieval for agentic RAG workflows.
- Standardizing metric definitions across different business units using a shared KPI glossary resource.

## Strengths
- **Decoupling**: Agents don't need to know if they are talking to SQL or a REST API.
- **Security**: Granular control over what resources/tools are exposed.
- **Portability**: MCP servers can be moved or swapped without changing the agent logic.

## Limitations
- **Overhead**: Adds a lightweight network layer between the agent and the data.
- **Maturity**: Ecosystem is still evolving; some specialized databases may lack off-the-shelf MCP servers.

## When to use it
- When building a multi-agent system that needs to access diverse data types.
- When security and auditing of data access are high priorities.
- For "free/cheap-first" architectures where local data sources must be integrated with cloud LLMs.

## When not to use it
- For extremely simple, single-script automations where a direct DB connection is faster to implement.
- When the data source already provides a native, highly optimized agentic interface that meets all security needs.

## Goal
Design a "free/cheap-first" standardization layer that allows the Data Copilot to scale across new domains without hard-coding database connectors or API clients.

## MCP Integration Matrix

| Tool Type | MCP Capability | Cost Profile | Implementation |
| :--- | :--- | :--- | :--- |
| **SQL Database** | Query/Resource | Free (OSS) | `mcp-server-sqlite` or `mcp-server-postgres` |
| **Documentation** | Resource (Text) | Free (Local) | `mcp-server-files` over Markdown docs |
| **KPI Glossary** | Resource (JSON) | Free (Local) | Custom JSON Resource server |
| **External APIs** | Tool (REST) | Low (API Keys) | `fetch` or specialized MCP servers (e.g., Jira, Slack) |
| **Metadata** | Resource (Schema) | Free (Local) | SQL introspection MCP server |

## Resource vs Tool Patterns

When designing MCP servers for Data Copilots, follow these patterns:
- **Resources**: Use for static or slowly changing context (e.g., Schema, KPI definitions, archived SOPs). The agent "reads" these to build its world model.
- **Tools**: Use for actions or live data retrieval (e.g., `execute_query`, `fetch_current_weather`, `create_jira_ticket`). The agent "calls" these to interact with the world.

## Concrete MCP Integration Examples

### 1. SQL Query Server
- **Role**: Provides the `execute_query` tool to the SQL Generator agent.
- **Example**: `mcp-server-sqlite --db inventory.db`.
- **Standardization**: Ensures all SQL generators receive schema context in the same format.

### 2. Documentation RAG (Docs Retrieval)
- **Role**: Allows the Intent Agent to look up domain definitions in the "Knowledge Base".
- **Example**: MCP server exposing `docs/services/` as searchable resources.
- **Benefit**: No need for a heavy Vector DB for small, high-density SOP documents.

### 3. KPI & Metric Glossary
- **Role**: Centralized source of truth for metric definitions (e.g., "What is Net Margin?").
- **Example**: A JSON-file resource server mapped to `data/kpi_glossary.json`.
- **Standardization**: Prevents LLMs from hallucinating calculation logic.

### 4. Home Assistant API Tool
- **Role**: Enables the Copilot to query live state (e.g., current power usage) for hybrid diagnostic queries.
- **Example**: MCP server wrapping Home Assistant REST API.

### 5. Metadata/Schema Inspector
- **Role**: Provides the Table and Column Prune agents with up-to-date schema information.
- **Benefit**: Decouples the agent from the specific DB dialect (SQLite vs Postgres).

## Minimal MCP Server Set for Small Teams
For a home-office or small team setup, start with these:
1.  **Filesystem MCP**: Exposes Markdown docs and JSON configurations.
2.  **SQL MCP**: Specific to your primary database (e.g., SQLite).
3.  **Fetch MCP**: For lightweight web requests/API integrations.

## Migration Path from Hard-coded Connectors
1.  **Phase 1 (Shadow)**: Deploy MCP servers alongside existing Python connectors.
2.  **Phase 2 (Abstraction)**: Update Pydantic models in the Data Copilot pipeline to accept MCP resource URIs instead of raw connection strings.
3.  **Phase 3 (Cutover)**: Replace direct `sqlite3` or `requests` calls with `mcp_client.call_tool()`.

## Security & Auth Boundaries
- **Least Privilege**: SQL MCP servers should use read-only credentials with `LIMIT` enforcement.
- **Auditability**: All MCP tool calls are logged by the agent orchestrator (n8n or LangGraph).
- **Authentication**: MCP servers should be restricted to the local network/Tailscale mesh with token-based access.
- **Network Isolation**: For high-security home labs, run MCP servers in a dedicated "Automation" VLAN or a Tailscale "tag" group that only allows connections from the agent orchestrator node.

## Related tools / concepts
- [Data Copilot Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)
- [Tool Calling & Model Context Protocol (MCP)](tool-calling-and-mcp.md)
- [Claude Tool Search](claude-tool-search.md)

## Sources / References
- [Model Context Protocol (MCP) Official Site](https://modelcontextprotocol.io/)
- [Anthropic: Introducing MCP](https://www.anthropic.com/news/model-context-protocol)

## Contribution Metadata
- Last reviewed: 2026-07-15
- Confidence: high
- Related Issues: #187
