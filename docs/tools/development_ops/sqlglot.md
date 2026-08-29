# SQLGlot

## What it is
SQLGlot is a no-dependency, high-performance SQL parser, transpiler, optimizer, and engine written in Python with a Rust-accelerated core. As of early January 2027, **v26.x+** features full Rust-based AST compilation that optimizes syntax tree generation and dialect transpilation for real-time agentic database pipelines.

## What problem it solves
In multi-agent architectures (e.g., [Data Copilot](../../architecture/data-copilot-text-to-sql.md)), autonomous agents frequently generate complex database queries using frontier models like **Claude 5.6**, **GPT-5.6**, or **Qwen 3.6 VL**. However, raw generated SQL often contains dialect inconsistencies (e.g., running Snowflake syntax on a local DuckDB cluster), structural inefficiencies, or mutating injection vulnerabilities. SQLGlot parses any query into a deterministic Abstract Syntax Tree (AST), enabling comprehensive schema analysis, transpilation across 25+ dialects, query optimization, and strict safety validation prior to execution.

## Where it fits in the stack
**Development / Data Layer**. It acts as an **In-Transit SQL Gateway**, sitting directly between an LLM agent generator and the downstream database execution layer.

## Typical use cases
- **Dialect Transpilation**: Converting complex Postgres, BigQuery, or Snowflake queries to standard DuckDB format for cost-effective local analytics.
- **Agentic SQL Safety Audits**: Programmatically scanning SQL ASTs to block mutating operators (like `DROP`, `DELETE`, `TRUNCATE`) or illegal database joins.
- **AST-Based Semantic Rewrites**: Dynamically appending row-level security filters (e.g., `WHERE tenant_id = X`) to user- or agent-generated SQL queries before database execution.
- **Query Optimization**: Automatically simplifying redundant subqueries, unused joins, and mathematical expressions to reduce database compute requirements.

## Strengths
- **No Heavy External Dependencies**: Pure Python footprint with optional ultra-fast Rust accelerators.
- **Broad Dialect Parity**: Robust support for Snowflake, Spark, ClickHouse, Presto, DuckDB, Postgres, SQLite, BigQuery, and 20+ others.
- **Extensible AST Engine**: Developer-friendly AST node representation allowing deep traversal, inspection, and semantic modifications.
- **High Throughput**: Sub-millisecond parsing and transformation optimized for hot paths in continuous microservices.

## Limitations
- **Dialect Parity Lag**: Niche, proprietary vendor extensions or newly released database syntax may require custom AST node definitions.
- **Compiler Knowledge Requirement**: Complex AST modifications require a solid understanding of relational algebra and compilation theory.
- **Language Boundaries**: Integrating SQLGlot into non-Python backends (e.g., Node.js or Go) requires running dedicated Python sidecars or microservices.

## When to use it
- When implementing a "Text-to-SQL" pipeline utilizing frontier models like Qwen 3.6 VL, Claude 5.6, or GPT-5.6.
- When creating automated agents that compile and execute SQL safely across heterogeneous database environments.
- When query performance optimization or structural AST scanning is required inside database proxies.

## When not to use it
- For static, hardcoded queries where raw DB adapters (e.g., `pg` or `sqlite3`) are sufficient.
- In low-latency Node.js or Go backends where invoking external Python processes introduces unacceptable latency (unless hosted as a persistent gRPC service).

## Getting started

### Installation
Install SQLGlot via pip:
```bash
pip install sqlglot
```

### Basic Setup
Transpile a standard SQL statement from BigQuery syntax to DuckDB format:
```python
import sqlglot

sql = "SELECT * FROM `project.dataset.users` LIMIT 100"
transpiled = sqlglot.transpile(sql, read="bigquery", write="duckdb")[0]
print(transpiled)
# Output: SELECT * FROM "project"."dataset"."users" LIMIT 100
```

## CLI examples
SQLGlot provides a lightweight CLI for transpilation, syntax checking, and quick query formatting.

### Shell-Based Transpilation
```bash
sqlglot-cli --read postgres --write snowflake "SELECT name, age FROM users WHERE age > 18"
```

### Formatting Complex Queries (Pretty Print)
```bash
sqlglot-cli --pretty < query.sql
```

### Syntax and Dialect Verification
```bash
sqlglot-cli --read duckdb "SELECT * FROM read_csv_auto('data.csv') LIMIT 5"
```

## API examples

### Programmatic AST Manipulation
Inject dynamic filters into an existing query using Python's AST representation:
```python
from sqlglot import parse_one, exp

# Parse raw SQL into expression AST
query = parse_one("SELECT id, email FROM users")

# Programmatically append filter logic
safe_query = query.where("is_active = true")
print(safe_query.sql())
# Output: SELECT id, email FROM users WHERE is_active = true
```

### Strict Python & Pydantic v2 Query Safety Validator
Integrate SQLGlot with a Pydantic v2 payload validation structure to build a strict Text-to-SQL security boundary:

```python
import sqlglot
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class SQLQueryPayload(BaseModel):
    raw_query: str = Field(..., description="The agent-generated SQL query.")
    target_dialect: str = Field("postgres", description="Target database dialect.")
    prohibited_operations: List[str] = Field(
        default_factory=lambda: ["drop", "delete", "truncate", "alter"]
    )

    @field_validator("raw_query")
    @classmethod
    def validate_and_sanitize_sql(cls, v: str, info) -> str:
        prohibited = info.data.get("prohibited_operations", ["drop", "delete", "truncate"])
        try:
            # Parse query using SQLGlot to inspect AST nodes
            parsed_expressions = sqlglot.parse(v)
            for expression in parsed_expressions:
                for node, *_ in expression.walk():
                    # Check if AST node matches prohibited mutations
                    node_name = node.__class__.__name__.lower()
                    if any(op in node_name for op in prohibited):
                        raise ValueError(f"Prohibited database operation detected: {node_name.upper()}")
            return v
        except sqlglot.errors.ParseError as e:
            raise ValueError(f"Invalid SQL Syntax: {str(e)}")

# Executing safe query validation
try:
    payload = SQLQueryPayload(
        raw_query="DROP TABLE production_users;",
        target_dialect="postgres"
    )
except ValueError as err:
    print(f"Intercepted threat: {err}")
```

## Related tools / concepts
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md)
- [Claude Code](claude-code.md)
- [ripgrep (rg)](ripgrep.md)
- [Aider](aider.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Pydantic AI](../frameworks/pydantic-ai.md)
- [OpenAI Agents SDK](../frameworks/openai-agents-sdk.md)
- [AG2](../frameworks/ag2.md)

## Sources / references
- [SQLGlot GitHub Repository](https://github.com/tobymao/sqlglot)
- [SQLGlot Official Documentation & API Reference](https://sqlglot.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.org)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
