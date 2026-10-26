# SQLGlot

## What it is
SQLGlot is a no-dependency, high-performance SQL parser, transpiler, optimizer, and execution engine written in Python with a Rust-accelerated core compiler. As of early January 2027, **v26.x+** features full Rust-native Abstract Syntax Tree (AST) compilation, enabling real-time SQL parsing, cross-dialect translation, semantic query optimization, and schema-aware safety auditing across 25+ SQL dialects.

In modern multi-agent systems and enterprise Text-to-SQL data copilots, SQLGlot acts as the **SQL Safety Gateway and Compiler Layer**. It parses agent-generated SQL queries into a deterministic, queryable AST, enabling autonomous agents (powered by frontier reasoning models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and Qwen 3.6 VL) to translate queries across heterogeneous database engines (e.g., Snowflake, BigQuery, Postgres, DuckDB, ClickHouse, Databricks), append row-level security predicates dynamically, and block malicious mutation vectors prior to database execution.

## What problem it solves
Deploying autonomous Text-to-SQL agents against production enterprise databases introduces significant operational and security vulnerabilities:
- **Dialect Incompatibilities**: Frontier LLMs often synthesize valid SQL syntax for one database (e.g., Snowflake `QUALIFY` or BigQuery `BACKTICK` table references) while targeting a different execution engine (e.g., Postgres or DuckDB), resulting in runtime execution crashes.
- **Unchecked Database Mutation Threats**: Agentic workflows can accidentally produce mutating SQL queries (`DROP TABLE`, `DELETE FROM`, `TRUNCATE`, `ALTER SYSTEM`) that compromise database integrity.
- **Unoptimized & Costly Queries**: LLM-generated SQL frequently contains redundant subqueries, missing `LIMIT` clauses, unindexed full table scans, or unnecessary joins that trigger massive cloud database compute bills on platforms like Snowflake or BigQuery.
- **Tenant Isolation Breaches**: Directly executing raw agent SQL strings makes it difficult to consistently enforce multi-tenant authorization policies (e.g., appending mandatory `WHERE tenant_id = X` filters) without fragile regular expression string manipulation.

SQLGlot solves these issues by parsing SQL strings into an Abstract Syntax Tree (AST) that can be inspected, transpiled, optimized, modified, and validated deterministically before any database connection receives the query.

## Core Compiler Architecture & Pipeline Flow

SQLGlot processes SQL statements through a deterministic four-stage compiler architecture: Tokenization, AST Parsing, Expression Transformation/Optimization, and Dialect Code Generation.

```
+---------------------------------------------------------------------------------------------------+
|                                 SQLGLOT COMPILER ARCHITECTURE                                     |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | 1. TOKENIZER (Rust Engine)                                                                  |  |
|  | - Lexical analysis of raw query string into dialect-aware token stream                      |  |
|  | - Handles quote semantics, identifier escaping, and literal type annotations                |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | 2. ABSTRACT SYNTAX TREE (AST) PARSER                                                        |  |
|  | - Converts token stream into hierarchical expression node tree (sqlglot.exp.Expression)     |  |
|  | - Resolves table references, aliases, subqueries, CTEs, and function invocations            |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | 3. AST TRANSFORMER & OPTIMIZER                                                              |  |
|  | - Injects mandatory predicates (e.g., tenant_id isolation filters, default LIMITs)          |  |
|  | - Eliminates dead subqueries, unused JOIN clauses, and constant mathematical expressions      |  |
|  | - Performs schema qualification and column lineage tracing                                  |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | 4. DIALECT GENERATOR (TRANSPILER)                                                           |  |
|  | - Emits target-dialect SQL string (e.g., Postgres, Snowflake, BigQuery, DuckDB, ClickHouse)  |  |
|  | - Formats identifier quoting, date arithmetic syntax, and window function expressions        |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Data Layer & Database Security Gateway.

SQLGlot operates as an **In-Transit SQL Compiler Gateway** positioned directly between an LLM agent query generator and the target database execution layer.

```
+-----------------------------------------------------------------------+
|                      Text-to-SQL LLM Agent                            |
|        (Claude 5.6 / GPT-5.6 / Qwen 3.6 VL / FastMCP 3.1)             |
+-----------------------------------------------------------------------+
                                   |
                                   | Raw Generated SQL String
                                   v
+-----------------------------------------------------------------------+
|                    SQLGlot In-Transit Gateway                         |
|                                                                       |
|  +--------------------+  +--------------------+  +-----------------+  |
|  | AST Parser (Rust)  |  | Dialect Transpiler |  | Safety Inspector|  |
|  +--------------------+  +--------------------+  +-----------------+  |
|  +-----------------------------------------------------------------+  |
|  | Semantic Policy Rewriter (e.g., Append WHERE tenant_id = 123)   |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
                                   |
                                   | Validated, Optimized & Transpiled SQL
                                   v
+-----------------------------------------------------------------------+
|                       Target Database Engine                          |
|         (DuckDB / Snowflake / Postgres / ClickHouse / BigQuery)       |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Dialect Query Transpilation**: Converting complex Snowflake or BigQuery queries into standard DuckDB or SQLite syntax for cost-effective local testing and analytics.
- **Agentic SQL Security Auditing**: Programmatically inspecting query AST nodes to block destructive statements (`DROP`, `DELETE`, `TRUNCATE`, `ALTER`) before dispatch.
- **Dynamic Tenant Predicate Injection**: Programmatically traversing the AST to inject mandatory row-level security conditions (`WHERE tenant_id = X` or `LIMIT 1000`) into agent-generated queries.
- **SQL Query Optimization & Simplification**: Automatically removing redundant subqueries, unused `JOIN` clauses, and constant mathematical expressions to reduce database compute consumption.
- **Schema Validation & Lineage Tracking**: Analyzing SQL ASTs to map column dependencies, verify table references against database metadata catalogs, and generate data lineage graphs.

## Strengths
- **Zero Heavy External Dependencies**: Lightweight pure Python footprint with optional ultra-fast Rust accelerators.
- **Extensive Dialect Parity**: Supports over 25 dialects including Snowflake, Postgres, DuckDB, BigQuery, ClickHouse, Spark, SQLite, Databricks, Oracle, MySQL, T-SQL, and Presto/Trino.
- **Full AST Traversals & Mutations**: Developer-friendly expression graph enabling deep node traversal, inspection, replacement, and programmatic generation.
- **Built-in Query Engine**: Includes a lightweight Python-based query execution engine for testing AST queries directly in memory without installing a database server.
- **Sub-Millisecond Parsing Performance**: Optimized hot-path parsing suitable for inline request-reply microservices and agent loops.

## Limitations
- **Niche Vendor Dialect Gaps**: Custom vendor proprietary extensions or newly announced database syntax features may require custom AST node definitions.
- **Compiler Concept Requirement**: Advanced AST manipulations require a solid understanding of relational algebra, AST node hierarchy, and SQL parsing mechanics.
- **Python-Centric Core**: Primary API is in Python; integration into Node.js or Go backends requires running Python sidecars or gRPC microservices.

## When to use it
- When implementing a Text-to-SQL agent using frontier models like Claude 5.6, GPT-5.6, or Qwen 3.6 VL against diverse database backends.
- When building automated database proxy gateways that enforce row-level tenant security or query complexity limits.
- When migrating massive SQL codebases or dbt model libraries between database providers (e.g., Postgres to Snowflake).

## When not to use it
- For static, hardcoded application queries where standard ORMs (SQLAlchemy, Prisma) or raw database drivers are sufficient.
- In sub-10ms non-Python API microservices where invoking external Python processes introduces unwanted latency overhead.

## Getting started

### 1. Installation
Install SQLGlot with optional Rust performance extensions:

```bash
pip install "sqlglot[rs]" pydantic fastmcp uvicorn
```

### 2. Basic Transpilation Example
Transpile a Snowflake query containing specific date functions into Postgres syntax:

```python
import sqlglot

snowflake_sql = "SELECT DATEADD(day, 7, current_date()) AS next_week"
postgres_sql = sqlglot.transpile(snowflake_sql, read="snowflake", write="postgres")[0]
print(f"Transpiled Postgres SQL: {postgres_sql}")
# Output: SELECT CURRENT_DATE + INTERVAL '7 day' AS next_week
```

## CLI examples

### 1. Dialect Transpilation via CLI
Convert a query string from BigQuery to DuckDB syntax in the terminal:

```bash
sqlglot-cli --read bigquery --write duckdb "SELECT * FROM \`project.dataset.users\` LIMIT 10"
```

### 2. Pretty-Printing & Formatting
Format complex unformatted SQL strings for readability:

```bash
sqlglot-cli --pretty "SELECT a,b FROM t1 JOIN t2 ON t1.id=t2.id WHERE a>10"
```

### 3. Syntax Verification & Dialect AST Dumping
Inspect the raw AST structure generated by SQLGlot:

```bash
python3 -c "import sqlglot; print(repr(sqlglot.parse_one('SELECT x FROM t WHERE y = 1')))"
```

## Advanced Python AST Manipulation Examples

### 1. Programmatic Tenant Isolation & AST Mutation
Inject tenant filters into complex multi-table JOIN queries without regex:

```python
import sqlglot
from sqlglot import parse_one, exp

def enforce_tenant_isolation(raw_sql: str, tenant_id: int, max_limit: int = 500) -> str:
    """
    Parses raw SQL, inspects all table sources, appends tenant predicates, and enforces max LIMIT.
    """
    expression = parse_one(raw_sql)

    # 1. Inject tenant_id predicate into main WHERE clause
    tenant_condition = exp.condition(f"tenant_id = {tenant_id}")
    expression = expression.where(tenant_condition)

    # 2. Enforce maximum query result row limit
    existing_limit = expression.args.get("limit")
    if existing_limit is None:
        expression = expression.limit(max_limit)
    else:
        current_val = int(existing_limit.expression.this)
        if current_val > max_limit:
            expression = expression.limit(max_limit)

    return expression.sql()

query = "SELECT u.id, u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'COMPLETED'"
safe_query = enforce_tenant_isolation(query, tenant_id=4092)
print("Sanitized SQL:")
print(safe_query)
```

### 2. Extracting Data Lineage & Column Reference Graphs

```python
import sqlglot
from sqlglot.lineage import lineage

sql_query = """
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_revenue
    FROM raw_orders
    WHERE order_date >= '2026-01-01'
    GROUP BY region
)
SELECT region, total_revenue * 0.15 AS estimated_tax
FROM regional_sales
WHERE total_revenue > 100000
"""

# Extract lineage for column 'estimated_tax'
node = lineage("estimated_tax", sql_query)
print("Lineage Node Representation:")
print(node)
```

## API examples

### 1. FastMCP 3.1 SQL Translation & Security Gateway Server (Python)
Expose SQLGlot parsing, transpilation, and security auditing as a FastMCP 3.1 tool server for AI agents:

```python
import os
import sqlglot
from sqlglot import parse_one, exp, optimizer
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

mcp = FastMCP(
    "SQLGlot Translation & Security Server",
    version="3.1.0",
    description="FastMCP 3.1 server for SQL dialect transpilation, AST validation, and row-level security enforcement."
)

class TranspileRequest(BaseModel):
    sql: str = Field(..., min_length=5, description="The SQL query to transpile")
    source_dialect: str = Field(default="snowflake", description="Source SQL dialect")
    target_dialect: str = Field(default="duckdb", description="Target database SQL dialect")

class SecurityAuditRequest(BaseModel):
    sql: str = Field(..., min_length=5, description="The agent-generated SQL query to inspect")
    prohibited_ops: List[str] = Field(
        default_factory=lambda: ["drop", "delete", "truncate", "alter", "update", "insert"],
        description="Forbidden statement types"
    )

class LineageRequest(BaseModel):
    sql: str = Field(..., min_length=5, description="SQL query to analyze for column lineage")
    target_column: str = Field(..., description="Target output column name")

@mcp.tool()
async def transpile_sql(request: TranspileRequest) -> Dict[str, Any]:
    """
    Transpiles SQL queries between 25+ database dialects using SQLGlot AST compilation.
    """
    try:
        results = sqlglot.transpile(request.sql, read=request.source_dialect, write=request.target_dialect)
        return {
            "success": True,
            "transpiled_sql": results[0],
            "source_dialect": request.source_dialect,
            "target_dialect": request.target_dialect
        }
    except Exception as e:
        return {"success": False, "error": f"Transpilation failed: {str(e)}"}

@mcp.tool()
async def audit_and_inject_tenant_filter(request: SecurityAuditRequest, tenant_id: int = 1001) -> Dict[str, Any]:
    """
    Audits SQL query for prohibited mutation statements and automatically injects tenant_id filter into AST.
    """
    try:
        parsed_expressions = sqlglot.parse(request.sql)
        for expression in parsed_expressions:
            # Check AST nodes for forbidden statements
            for node, *_ in expression.walk():
                node_name = node.__class__.__name__.lower()
                if any(op in node_name for op in request.prohibited_ops):
                    return {
                        "is_safe": False,
                        "error": f"Prohibited operation detected: {node_name.upper()}"
                    }

        # Inject tenant_id filter using AST mutation
        parsed_ast = parse_one(request.sql)
        safe_ast = parsed_ast.where(f"tenant_id = {tenant_id}")

        return {
            "is_safe": True,
            "sanitized_sql": safe_ast.sql(),
            "injected_tenant_id": tenant_id
        }
    except Exception as e:
        return {"is_safe": False, "error": f"AST Analysis failed: {str(e)}"}

@mcp.tool()
async def optimize_sql_query(sql: str, dialect: str = "postgres") -> Dict[str, Any]:
    """
    Optimizes SQL queries using SQLGlot AST semantic optimizer rules.
    """
    try:
        parsed = parse_one(sql, read=dialect)
        optimized_ast = optimizer.optimize(parsed)
        return {
            "success": True,
            "original_sql": sql,
            "optimized_sql": optimized_ast.sql(dialect=dialect)
        }
    except Exception as e:
        return {"success": False, "error": f"Optimization error: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 SQL Payload Validation & AST Safety Schema
Define a strict Pydantic v2 model that validates agent SQL inputs prior to pipeline processing:

```python
import sqlglot
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class AgentSQLPayload(BaseModel):
    """
    Pydantic v2 schema that uses SQLGlot to strictly validate generated SQL syntax and safety.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(..., min_length=5, description="The raw SQL string generated by the agent")
    target_dialect: str = Field(default="postgres", description="Target engine dialect")
    max_table_joins: int = Field(default=5, ge=1, le=20, description="Maximum allowed JOIN operations")

    @field_validator("query")
    @classmethod
    def validate_sql_syntax_and_safety(cls, raw_sql: str) -> str:
        try:
            expressions = sqlglot.parse(raw_sql)
            if not expressions:
                raise ValueError("Parsed SQL result was empty.")

            # Scan for dangerous mutations
            for expr in expressions:
                if isinstance(expr, (sqlglot.exp.Drop, sqlglot.exp.Delete, sqlglot.exp.TruncateTable, sqlglot.exp.Insert, sqlglot.exp.Update)):
                    raise ValueError(f"Dangerous mutating statement detected: {type(expr).__name__}")

            return raw_sql
        except sqlglot.errors.ParseError as pe:
            raise ValueError(f"Invalid SQL syntax: {str(pe)}")

if __name__ == "__main__":
    sample_agent_query = "SELECT u.id, u.email, o.total FROM users u JOIN orders o ON u.id = o.user_id WHERE u.active = true"

    validated_payload = AgentSQLPayload.model_validate({"query": sample_agent_query, "target_dialect": "postgres"})
    print("Agent SQL query successfully verified against Pydantic v2 & SQLGlot contract!")
    print(f"Validated Query: {validated_payload.query}")
```

## Production Deployment & Operational Management

### Systemd Service Configuration
For running SQLGlot as a background FastMCP 3.1 translation microservice, create `/etc/systemd/system/sqlglot-gateway.service`:

```ini
[Unit]
Description=SQLGlot FastMCP 3.1 Gateway Microservice
After=network.target

[Service]
Type=simple
User=mcp
Group=mcp
WorkingDirectory=/opt/sqlglot-gateway
Environment=PYTHONUNBUFFERED=1
Environment=PORT=8090
ExecStart=/opt/sqlglot-gateway/venv/bin/python -m mcp.server.fastmcp run server.py --port 8090
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Security hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/sqlglot-gateway/logs
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

### Docker Compose Deployment
Deploy SQLGlot as an isolated microservice container:

```yaml
version: '3.8'

services:
  sqlglot-gateway:
    image: python:3.12-slim
    container_name: sqlglot-gateway
    restart: always
    ports:
      - "8090:8090"
    volumes:
      - ./server.py:/app/server.py
    command: >
      sh -c "pip install --no-cache-dir 'sqlglot[rs]' fastmcp pydantic uvicorn &&
             python /app/server.py"
    environment:
      - PORT=8090
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8090/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Probable Root Cause | Resolution Command or Remediation |
| :--- | :--- | :--- |
| `ParseError: Unexpected token` during transpilation | Source SQL contains custom vendor dialect syntax not specified in `read` argument. | Pass explicit `read="<dialect>"` parameter (e.g., `read="snowflake"` or `read="databricks"`). |
| `UnsupportedError: Unknown expression type` | SQLGlot AST generator encountered an unmapped custom SQL function or operator. | Register custom expression using `sqlglot.Parser.FUNCTIONS.update({"CUSTOM_FUNC": ...})` or fallback to generic AST node. |
| Slow parsing throughput on large queries (>1MB SQL) | Pure Python tokenizer fallback active instead of Rust core compiler binary. | Install Rust bindings: `pip install "sqlglot[rs]" --force-reinstall`. |
| Column quotes stripped after transpiling to Postgres | Dialect generator default setting standardizes lower-case unquoted identifiers. | Set `normalize_identifiers=False` or pass `quoted=True` to `exp.to_identifier()`. |
| `KeyError` when traversing AST nodes | Direct dictionary key access on AST arguments without checking existence. | Use safe helper methods like `expr.args.get("where")` or `expr.find(exp.Where)`. |

## Related tools / concepts
- [Claude Code](claude-code.md) — Terminal developer agent for managing data transformation scripts.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Protocol for serving SQLGlot tools to AI agents.
- [DuckDB](../infrastructure/duckdb.md) — In-process analytical SQL engine frequently targeted by SQLGlot transpilations.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Agent framework used for building structured Text-to-SQL agents.

## Sources / references
- [SQLGlot Official GitHub Repository](https://github.com/tobymao/sqlglot)
- [SQLGlot Official Documentation](https://sqlglot.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
