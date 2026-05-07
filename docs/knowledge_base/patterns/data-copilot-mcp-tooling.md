# Data Copilot: MCP Tool & Data Standardization

This document outlines the standardization of tool and data access for the Data Copilot using the Model Context Protocol (MCP). By adopting MCP, we ensure that specialized agents in the Text-to-SQL pipeline can interact with diverse data sources (SQL, docs, APIs) through a unified, machine-parseable interface.

## Goal
Design a "free/cheap-first" standardization layer that allows the Data Copilot to scale across new domains without hard-coding database connectors or API clients.

## What it is
MCP Tool & Data Standardization for Data Copilot is a pattern that uses the Model Context Protocol (MCP) to provide a unified interface for AI agents to interact with various data sources and tools. It abstracts the underlying complexities of database connections, document retrieval, and API calls into a standardized set of resources and tools.

## What problem it solves
In a complex Data Copilot architecture, agents often need to access diverse data sources (SQL databases, internal documentation, KPI glossaries, etc.). Traditionally, this requires hard-coding connectors for each source, leading to brittle code and difficult scaling. MCP standardization solves this by providing a single protocol for all data interactions, making the system more modular, secure, and easier to extend.

## Where it fits in the stack
It sits in the **Orchestration and Tooling layer**, acting as the bridge between the AI agents (e.g., Intent Agent, SQL Generator) and the data storage or service providers (e.g., SQLite, Home Assistant, local files).

## Typical use cases
- Exposing a local SQLite database to a Text-to-SQL agent.
- Providing a search interface for technical documentation to a RAG-enabled agent.
- Standardizing access to a centralized KPI glossary across different analysts.
- Integrating live data from smart home devices via the Home Assistant API.

## Strengths
- **Decoupling**: Agents are no longer tied to specific database dialects or API implementations.
- **Security**: Allows for fine-grained access control and auditing at the protocol level.
- **Portability**: MCP servers can be easily swapped or moved without changing the agent logic.
- **Unified Interface**: Reduces the complexity of building and maintaining multiple custom connectors.

## Limitations
- **Overhead**: Introducing an abstraction layer can add slight latency to requests.
- **Protocol Maturity**: MCP is a relatively new protocol, and the ecosystem of servers is still growing.
- **Configuration**: Requires setting up and managing separate MCP server instances.

## When to use it
- When building a Data Copilot that needs to access multiple, diverse data sources.
- When you want to ensure a clean separation between agent logic and data access.
- When you need a scalable and secure way to expose local tools to AI agents.

## When not to use it
- For very simple, single-source applications where the overhead of MCP isn't justified.
- If your environment already has a well-established and standardized data access layer that isn't compatible with MCP.

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
For a home-office or small team setup, start with these three:
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
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)
- [Tool Calling & Model Context Protocol (MCP)](tool-calling-and-mcp.md)
- [Claude Tool Search](claude-tool-search.md)

## Sources / References
- [Model Context Protocol (MCP) Official Site](https://modelcontextprotocol.io/)
- [Anthropic: Introducing MCP](https://www.anthropic.com/news/model-context-protocol)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
- Related Issues: #187
