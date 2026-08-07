# SQLGlot

## What it is
SQLGlot is a no-dependency, high-performance SQL parser, transpiler, optimizer, and engine written in Python. As of late December 2026, **v25.x+** features substantial Rust-based parsing components that drastically optimize abstract syntax tree (AST) compilation, making it a crucial component for agentic database integration.

## What problem it solves
In multi-agent architectures (e.g., [Data Copilot](../../architecture/data-copilot-text-to-sql.md)), autonomous agents frequently generate database queries. However, raw generated SQL often contains syntactic errors, incompatible dialects (e.g., executing Postgres syntax on a DuckDB cluster), or malicious/mutating injection vulnerabilities. SQLGlot parses any query into an AST, allowing comprehensive schema analysis, transpilation to 20+ dialects, optimization, and strict safety validation before execution.

## Where it fits in the stack
**Development / Data Layer**. It acts as an **In-Transit SQL Gateway**, sitting directly between an LLM agent generator (such as Claude 5.1, GPT-5.5, or Qwen 3.6) and the destination database connection layer.

## Typical use cases
- **Dialect Transpilation**: Seamlessly converting complex Postgres or BigQuery queries to standard DuckDB format for cost-effective local analytics.
- **Agentic SQL Safety Audits**: Programmatically scanning SQL ASTs to block mutating operators (like `DROP`, `DELETE`, `TRUNCATE`) or illegal database joins.
- **AST-Based Semantic Rewrites**: Dynamically appending row-level security filters (e.g., `WHERE tenant_id = X`) to user-generated SQL queries before database execution.
- **Query Optimization**: Automatically simplifying redundant nested queries, unused joins, and mathematical expressions to reduce database compute requirements.

## Strengths
- **No Heavy Dependencies**: Pure Python footprint with optional ultra-fast Rust accelerators.
- **Broad Dialect Support**: Robust support for Snowflake, Spark, clickhouse, Presto, DuckDB, SQLite, and 15+ others.
- **Extensible AST Engine**: Highly developer-friendly AST node representation allowing deep traversal and semantic modifications.
- **Excellent Performance**: Optimized for hot paths in high-throughput data processing workflows.

## Limitations
- **Dialect Parity Lag**: Extremely niche, newly introduced database features or proprietary vendor extensions might require custom AST extensions.
- **Rust Transition**: The complete transition of parsing operations to Rust is ongoing, meaning some complex custom macros still run on Python logic.
- **Complex AST Traversal**: Navigating nested expressions and relational joins requires solid SQL compilation theory knowledge.

## When to use it
- When implementing a "Text-to-SQL" pipeline utilizing models like Qwen 3.6, Llama 4, or Gemma 3.
- When creating automated agents that need to compile and execute SQL safely across heterogeneous database environments.
- When query performance optimization or structural AST scanning is required inside database-proxies or tools.

## When not to use it
- For basic database interactions utilizing simple, hardcoded queries where raw DB adapters (e.g., `pg` or `sqlite3`) are perfectly sufficient.
- In low-latency Node.js or Go backends where invoking Python subprocesses introduces unacceptable overhead (unless wrapped in a dedicated microservice).

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
- [Text-to-SQL Dialect Mapping Techniques](https://github.com/tobymao/sqlglot/blob/main/posts/transpiling_sql.md)

---
## Contribution Metadata
- Last reviewed: 2026-12-19
- Confidence: high
