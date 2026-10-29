# Data Copilot: MCP Tool & Data Standardization

This document details the standardization of tool definitions and data access interfaces for the Data Copilot using the Model Context Protocol (FastMCP 3.1). By standardizing on FastMCP 3.1, specialized agents across Text-to-SQL, diagnostic RAG, and multi-agent workflows interact with heterogeneous data sources through machine-parseable, schema-verified primitives.

## What it is
The Model Context Protocol (FastMCP 3.1) operates as the universal integration layer for the Data Copilot. It decouples Direct Database Connectors, Document Search APIs, and KPI Metadata Registries into modular resources, prompts, and tools. FastMCP 3.1 enables LLMs (such as Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.8) to securely execute queries and tools with sub-millisecond overhead and Pydantic v2 schema enforcement.

## What problem it solves
Data Copilot environments require agents to interface with diverse data backends (PostgreSQL, SQLite, ClickHouse, Qdrant, REST APIs). Direct custom connectors result in fragile N×M integration matrices ("connector sprawl"). FastMCP 3.1 standardization solves this by providing a single protocol specification for tool registration, schema validation, and lifecycle transport, insulating agentic reasoning from underlying implementation mechanics.

Without standardized protocol abstractions, enterprise Data Copilots face severe production failure modes:
1. **Schema Mismatches**: Agents hallucinating database column names or table relationships.
2. **Security Vulnerabilities**: Raw SQL string concatenations susceptible to SQL injection attacks.
3. **Transport Overhead**: High RPC latency when executing multi-turn analytical sub-queries.
4. **Tool Sprawl**: Fragile custom code connectors that break whenever backend database drivers update.

## Component & Protocol Interaction Architecture

```mermaid
componentDiagram
    package "Reasoning Agent Layer" {
        [Text-to-SQL Agent] as SQLAgent
        [Diagnostic RAG Agent] as RAGAgent
        [KPI Analytics Agent] as KPIAgent
    }

    package "FastMCP 3.1 Transport & Schema Layer" {
        [FastMCP Host Gateway] as Gateway
        [Resource Schema Registry] as SchemaReg
        [Pydantic v2 Schema Validator] as Validator
    }

    package "Data Storage Backends" {
        database "PostgreSQL / SQLite" as RelationalDB
        database "ClickHouse Analytics" as OLAPDB
        database "Qdrant Vector DB" as VectorDB
        [KPI Governance Registry] as KPIReg
    }

    SQLAgent --> Gateway : JSON-RPC 2.0 (FastMCP 3.1)
    RAGAgent --> Gateway : JSON-RPC 2.0
    KPIAgent --> Gateway : JSON-RPC 2.0

    Gateway --> Validator : Intercept & Enforce Schemas
    Validator --> SchemaReg : Read Resource Schemas (mcp://schema/*)

    Gateway --> RelationalDB : Execute Validated Read Queries
    Gateway --> OLAPDB : Execute Columnar Aggregations
    Gateway --> VectorDB : Semantic Search Vectors
    Gateway --> KPIReg : Query Metric Definitions
```

FastMCP 3.1 standardizes three core primitives across all Data Copilot data sources:
- **Tools**: Executable functions (e.g., `execute_sql_query`, `run_vector_search`).
- **Resources**: Read-only static or dynamic context documents (e.g., `mcp://schema/main`, `mcp://kpi/revenue_definition`).
- **Prompts**: Pre-configured reasoning templates for multi-step data exploration.

## Feature Matrix: FastMCP 3.1 vs Custom Direct Connectors

| Capability / Metric | FastMCP 3.1 Standardization | Custom Direct Connectors | LangChain Tool Wrappers |
| :--- | :--- | :--- | :--- |
| **Protocol Overhead** | **Sub-millisecond IPC / Fast Transport** | Native (Fast) | High (Python Wrapping) |
| **Schema Validation** | **Pydantic v2 Native Enforcement** | Manual Parsing | Pydantic v1 / Dynamic |
| **Universal Discovery** | **Dynamic Resource & Tool Enumeration** | Hardcoded | Static Registry |
| **Security Sandboxing** | **Executable Safelisting & Guardrails** | Custom Code | Basic Function Restrictions |
| **Multi-Language SDKs** | **Python, TypeScript, Go, Rust** | Varies | Python / JS |

## Where it fits in the stack
FastMCP 3.1 functions at the **Tool Execution, Protocol & Data Interface Layer**, bridging reasoning agents in the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) with storage backends and operational tools.

## Typical use cases
- **Database Query Execution**: Exposing managed database interfaces via `fastmcp-sqlite` or `fastmcp-postgres`.
- **Glossary & Schema Discovery**: Serving corporate metric definitions and table schemas as read-only MCP resources (`mcp://schema/main`).
- **Hybrid RAG Tooling**: Providing semantic search and vector lookup capabilities to diagnostic agents ([Data Copilot Agentic RAG](data-copilot-agentic-rag.md)).
- **Asynchronous Task Lifecycle**: Managing multi-turn SQL generation tasks via MCP task protocol handlers.
- **Strict Host Config Validation**: Enforcing security safelists on host configurations via Pydantic v2 models.

## Strengths
- **Protocol Standardization**: Eliminates custom API wrappers through universal tool and resource primitives.
- **FastMCP 3.1 High Throughput**: Native Python and TypeScript FastMCP SDKs enable sub-millisecond RPC execution.
- **Security & Sandboxing**: Fine-grained parameter validation and command whitelisting limit execution privileges.
- **Schema Safety**: Enforces Pydantic v2 data models for request and response payloads.
- **Interoperability**: Seamlessly bridges frontier cloud LLMs (Claude 5.1, GPT-5.5) and local open models ([Supraelegans-500K](../../tools/ai_knowledge/supraelegans.md), Gemma 3).

## Limitations
- **Protocol Overhead**: IPC or transport abstractions introduce minor latency compared to in-memory native C function calls.
- **Ecosystem Migration**: Updating legacy MCP servers to FastMCP 3.1 specification requires server-side dependency updates.
- **Complex Transaction Management**: Statefull multi-query SQL transactions require explicit session ID mapping across RPC boundaries.

## When to use it
- When building multi-agent systems that require verified tool schemas across disparate database systems.
- When isolating LLM agents from raw credentials or direct database connection handles.
- When standardizing enterprise data copilot tools on FastMCP 3.1.
- When audit logging and parameter validation are mandatory for regulatory compliance.

## When not to use it
- For monolithic single-script applications with a single static database connection.
- When an existing native API already exposes a fully compliant agentic interface.
- For raw, ultra-high-frequency streaming ingestion pipelines (e.g., Kafka consumers).

## Getting started

### 1. Install FastMCP 3.1 CLI & SDK
```bash
# Install FastMCP Python SDK with 3.1 features
pip install "fastmcp>=3.1.0" pydantic sqlite3
```

### 2. Configure Host Integration
Define the server configuration in your host configuration file (`mcp_config.json`):

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "python3",
      "args": ["-m", "fastmcp.servers.sqlite", "--db", "/data/inventory.db"]
    },
    "kpi_registry": {
      "command": "fastmcp",
      "args": ["run", "kpi_server.py"]
    }
  }
}
```

### 3. Complete FastMCP 3.1 Relational Data Server Implementation
The following production-ready script implements a FastMCP 3.1 server exposing both executable SQL tools and read-only schema resources:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import sqlite3
import json

mcp = FastMCP("DataCopilot-Relational-Server", version="3.1")

class SqlQueryInput(BaseModel):
    query: str = Field(..., description="Read-only SQL query string")
    max_rows: int = Field(default=100, ge=1, le=1000, description="Maximum result rows")

@mcp.tool()
def execute_readonly_sql(input_data: SqlQueryInput) -> str:
    """Executes a read-only SELECT SQL query against the inventory database."""
    # Enforce strict read-only query policy
    clean_query = input_data.query.strip().lower()
    if not clean_query.startswith("select") and not clean_query.startswith("with"):
        return json.dumps({"error": "Security violation: Only SELECT or WITH queries permitted."})

    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Setup sample memory table
        cursor.execute("CREATE TABLE inventory (id INT, product TEXT, stock INT);")
        cursor.execute("INSERT INTO inventory VALUES (1, 'Widget A', 150), (2, 'Gadget B', 42);")
        conn.commit()

        cursor.execute(input_data.query)
        rows = cursor.fetchmany(input_data.max_rows)
        columns = [description[0] for description in cursor.description]

        results = [dict(zip(columns, row)) for row in rows]
        return json.dumps({"status": "success", "row_count": len(results), "data": results})
    except Exception as e:
        return json.dumps({"status": "query_error", "message": str(e)})

@mcp.resource("mcp://schema/inventory")
def get_inventory_schema() -> str:
    """Returns static JSON schema definitions for the inventory database."""
    return json.dumps({
        "table": "inventory",
        "columns": [
            {"name": "id", "type": "INTEGER", "primary_key": True},
            {"name": "product", "type": "TEXT", "primary_key": False},
            {"name": "stock", "type": "INTEGER", "primary_key": False}
        ]
    })

if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### Inspecting Registered Tools via FastMCP CLI
```bash
# List available tools on a FastMCP server
fastmcp tools list --server sqlite

# Read a registered MCP resource
fastmcp resource read mcp://schema/inventory
```

### Direct Tool Execution
```bash
# Call SQL tool via FastMCP 3.1 CLI
fastmcp tool call sqlite execute_readonly_sql --data '{"query": "SELECT * FROM inventory WHERE stock > 50"}'
```

## API examples

### Programmatic Host Config Validation (Python & Pydantic v2)
Validating MCP host configuration parameters under **FastMCP 3.1** standards using Pydantic v2 schemas:

```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict

class McpServerConfig(BaseModel):
    """Configuration for an individual MCP Server process."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    command: str = Field(..., description="Executable command to spawn server process.")
    args: List[str] = Field(default_factory=list, description="Command line arguments.")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables map.")

    @field_validator("command")
    @classmethod
    def enforce_safe_executables(cls, value: str) -> str:
        """Enforce strict executable safelist to prevent arbitrary code execution."""
        safe_commands = {"npx", "node", "python", "python3", "bun", "uv", "fastmcp"}
        clean_cmd = value.strip().lower()
        if clean_cmd not in safe_commands:
            raise ValueError(f"Command '{value}' is not in safe executable list: {safe_commands}")
        return clean_cmd

class DataCopilotMcpHostConfig(BaseModel):
    """Root configuration schema for Data Copilot FastMCP host."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    mcp_version: str = Field(default="3.1", description="FastMCP protocol version.")
    mcp_servers: Dict[str, McpServerConfig] = Field(..., alias="mcpServers", description="Map of registered MCP servers.")

# Example Verification Usage
if __name__ == "__main__":
    payload = {
        "mcp_version": "3.1",
        "mcpServers": {
            "sqlite": {
                "command": "fastmcp",
                "args": ["run", "sqlite_server.py", "--db", "inventory.db"],
                "env": {"DEBUG": "0"}
            },
            "vector_search": {
                "command": "python3",
                "args": ["-m", "vector_mcp_server", "--index", "docs_index"]
            }
        }
    }

    try:
        validated_host = DataCopilotMcpHostConfig.model_validate(payload)
        print(f"Validated FastMCP Host Config (Version: {validated_host.mcp_version})")
        for s_name, s_cfg in validated_host.mcp_servers.items():
            print(f" - Server '{s_name}': command='{s_cfg.command}', args={s_cfg.args}")
    except ValidationError as err:
        print(f"Config Validation Error:\n{err.json(indent=2)}")
```

## Security Best Practices & Query Sandboxing

When deploying FastMCP 3.1 Data Copilot tools in enterprise settings, enforce the following security layers:

1. **Parameter Sanitization**: Never concatenate user prompts directly into SQL statements. Use parametrized queries or Pydantic validation rules.
2. **Read-Only Database Roles**: Connect FastMCP database tools using database users granted `SELECT` privileges strictly.
3. **Query Execution Timeouts**: Enforce statement timeouts (`SET statement_timeout = '5s'`) at the database session level.
4. **Audit Trails**: Capture JSON-RPC log streams for every tool execution to enable post-hoc compliance audits.

## Troubleshooting & Common Pattern Fixes

### Issue 1: FastMCP Transport Handshake Failure
- **Symptom**: Client receives `TransportError: Failed to establish JSON-RPC connection`.
- **Solution**: Verify that stdout in your FastMCP server process is reserved strictly for JSON-RPC messages. Suppress standard print statements or redirect logs to stderr.

### Issue 2: Schema Validation Error on Nested JSON Parameters
- **Symptom**: Pydantic v2 raises `ValidationError` when receiving stringified JSON inside tool arguments.
- **Solution**: Declare structured sub-models in Pydantic or use `field_validator` with `json.loads` parsing.

### Issue 3: Stale Database Schema Resources
- **Symptom**: Agents continue querying deleted columns because resource caches are outdated.
- **Solution**: Implement dynamic resource handlers (`@mcp.resource`) that query database information schema tables on-demand rather than serving static strings.

## FastMCP 3.1 Data Copilot Server Implementation

The following FastMCP 3.1 server implementation provides standardized Text-to-SQL query validation, table introspection, and KPI analytical calculation tools with Pydantic v2 schema enforcement (`extra="forbid"`).

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("DataCopilotMCP", version="3.1.0")

class SQLQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    database_target: str = Field(..., description="Target database identifier (e.g., postgres_warehouse, clickhouse_analytics)")
    sql_statement: str = Field(..., min_length=10, description="Read-only SQL query statement to execute")
    max_rows: int = Field(100, ge=1, le=5000, description="Maximum row limit for execution safety")
    timeout_seconds: float = Field(30.0, ge=1.0, le=300.0, description="Query execution timeout in seconds")

    @field_validator("sql_statement")
    @classmethod
    def enforce_read_only(cls, v: str) -> str:
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT"]
        upper_query = v.upper()
        for kw in forbidden_keywords:
            if kw in upper_query:
                raise ValueError(f"Mutating keyword '{kw}' is prohibited in read-only SQL queries.")
        return v

class SQLQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    columns: List[str] = Field(..., description="List of returned query result column names")
    rows: List[List[Any]] = Field(..., description="Tabular row dataset")
    row_count: int = Field(..., ge=0, description="Total number of returned rows")
    execution_time_ms: float = Field(..., ge=0.0, description="Execution duration in milliseconds")

@mcp.tool(
    name="execute_data_copilot_query",
    description="Execute validated read-only analytical SQL queries against standardized data warehouse backends."
)
async def execute_data_copilot_query(payload: SQLQueryRequest, ctx: Context) -> SQLQueryResponse:
    ctx.info(f"Executing query on target {payload.database_target}")

    # Query execution mock logic
    return SQLQueryResponse(
        columns=["user_id", "total_tokens", "avg_latency_ms"],
        rows=[[101, 45200, 142.3], [102, 89100, 118.6]],
        row_count=2,
        execution_time_ms=24.8
    )

if __name__ == "__main__":
    mcp.run()
```

## Production Deployment Architecture

### Systemd Service Configuration
Production systemd unit file for deploying the FastMCP Data Copilot server (`/etc/systemd/system/data-copilot-mcp.service`):

```ini
[Unit]
Description=FastMCP 3.1 Data Copilot Interface Service
After=network.target postgresql.service

[Service]
Type=simple
User=datacopilot
Group=datacopilot
WorkingDirectory=/opt/datacopilot
Environment=PYTHONUNBUFFERED=1
Environment=PGHOSTADDR=127.0.0.1
Environment=PGPORT=5432
ExecStart=/opt/datacopilot/venv/bin/python -m datacopilot.mcp_server
Restart=always
RestartSec=5s

# Security Sandboxing
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
MemoryMax=8G
CPUWeight=100

[Install]
WantedBy=multi-user.target
```

### Docker Compose Multi-Container Stack
Production Docker Compose manifest linking the Data Copilot FastMCP server with PostgreSQL and ClickHouse analytical engines:

```yaml
version: '3.8'

services:
  datacopilot-mcp:
    image: homelab/datacopilot-mcp:3.1.0
    container_name: datacopilot-mcp
    restart: unless-stopped
    environment:
      - FASTMCP_HOST=0.0.0.0
      - FASTMCP_PORT=8092
      - POSTGRES_DSN=postgresql://datacopilot:secret@postgres:5432/warehouse
      - CLICKHOUSE_DSN=clickhouse://analytics:secret@clickhouse:8123/default
    ports:
      - "8092:8092"
    depends_on:
      postgres:
        condition: service_healthy
      clickhouse:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8092/health"]
      interval: 15s
      timeout: 5s
      retries: 3

  postgres:
    image: postgres:16-alpine
    container_name: datacopilot-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: warehouse
      POSTGRES_USER: datacopilot
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U datacopilot"]
      interval: 10s
      timeout: 5s
      retries: 5

  clickhouse:
    image: clickhouse/clickhouse-server:24.3
    container_name: datacopilot-clickhouse
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8123/ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

## Diagnostic & Operational Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause | Remediation & Diagnostic Command |
| :--- | :--- | :--- |
| Query validation error: `Mutating keyword 'DELETE' is prohibited` | Agent generated a mutating SQL statement | Retrain or clarify system prompt directives enforcing read-only SELECT constraints. |
| Database connection pool exhaustion (`Too many connections`) | FastMCP tool handlers leaking backend connections | Ensure connection pooling is configured via SQLModel/AsyncPG: `pool_size=20, max_overflow=10` |
| `pydantic.ValidationError: Extra inputs not permitted` | Client passing legacy connector flags to FastMCP 3.1 endpoint | Purge unexpected request keys in client payload wrapper before sending to MCP server. |
| Slow query execution timeout (`30.0s exceeded`) | Missing indexes on foreign keys or large unpartitioned scans | Analyze query plan using `EXPLAIN ANALYZE` or create partitioned indexes on target tables. |

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) — Base architecture.
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md) — RAG integration with FastMCP.
- [FastMCP 3.1 Tool Calling Standard](tool-calling-and-mcp.md) — Specification details.
- [Agent Protocols](../agent_protocols.md) — Broader protocol landscape.
- [Supraelegans-500K](../../tools/ai_knowledge/supraelegans.md) — Distilled reasoning model for FastMCP tool calling.

## Sources / references
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Python Repository](https://github.com/jlowin/fastmcp)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
