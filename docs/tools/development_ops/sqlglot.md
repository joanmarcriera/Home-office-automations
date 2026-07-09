# SQLGlot

A no-dependency SQL parser, transpiler, optimizer, and engine written in Python.

## What it is
SQLGlot is a comprehensive SQL framework that enables parsing, transpiling, optimizing, and executing SQL across dozens of different dialects. In July 2026, it has become a foundational component for agentic data pipelines, providing the robust parsing necessary for [Gemma 3](../ai_knowledge/local_llms.md) and other models to interact safely with structured data. It supports **FastMCP 3.0** for high-performance schema discovery and query validation.

## What problem it solves
The proliferation of SQL dialects (Postgres, BigQuery, DuckDB, etc.) makes it difficult to write portable SQL or build generic tools that work across all of them. SQLGlot solves this by providing a unified Abstract Syntax Tree (AST) that can be transpiled into any supported dialect. It also addresses the safety concerns of agent-generated SQL by providing deep structural analysis to prevent malicious injections or inefficient "cartesian product" queries before they reach the database.

## Where it fits in the stack
**Development / Data Layer** — SQLGlot sits between the LLM generator (like [Claude 4.8](../ai_knowledge/claude.md)) and the physical database. It is often integrated into [Data Copilot](../../architecture/data-copilot-text-to-sql.md) as the primary validation and transpilation engine, ensuring that agent-generated intent is safely and accurately converted into executable code.

## Typical use cases
- **Multi-Dialect Transpilation**: Converting complex queries from Postgres to DuckDB for local analytical processing.
- **Agentic SQL Validation**: Inspecting LLM-generated SQL for prohibited mutations (DROP, DELETE) or PII access.
- **Query Optimization**: Automatically simplifying redundant joins or subqueries before execution to save compute.
- **Schema Mapping**: Translating natural language column references into the exact schema names via AST manipulation.

## Strengths
- **No Dependencies**: Extremely lightweight and easy to deploy in serverless or edge environments.
- **Dialect Support**: Supports 20+ dialects including Spark, Snowflake, and ClickHouse.
- **Powerful AST**: Allows for sophisticated programmatic manipulation of SQL structures.
- **Performance**: Highly optimized for speed, matching the low-latency requirements of **FastMCP 3.0** pipelines.

## Limitations
- **Python Only**: While a Rust port is in progress (as of 2026), the primary engine remains Python-based.
- **Complex Macro Support**: Some highly specific database-native macros may not transpile perfectly without custom rules.
- **Learning Curve**: The AST API is powerful but requires significant SQL knowledge to use effectively for complex transformations.

## When to use it
- When building "Text-to-SQL" applications that must be dialect-agnostic.
- When you need to programmatically analyze or modify SQL queries in an agentic workflow.
- When safety-gating database access for autonomous agents is a priority.
- For local data processing where lightweight, no-dependency tools are preferred.

## When not to use it
- For simple one-off queries where manual transpilation is faster.
- In non-Python environments (unless using a language bridge).
- When the target database uses highly proprietary, non-standard SQL extensions that are not yet supported.

## Getting started

### Installation
Install SQLGlot via pip:

```bash
pip install sqlglot
```

### Quick Transpile
The simplest use case is transpiling between dialects:

```python
import sqlglot
sql = "SELECT * FROM x LIMIT 10"
print(sqlglot.transpile(sql, read="postgres", write="duckdb")[0])
```

## CLI examples
SQLGlot provides a basic CLI for transpilation and formatting:

```bash
# Transpile a query from Postgres to Snowflake
sqlglot-cli --read postgres --write snowflake "SELECT * FROM table LIMIT 10"

# Pretty-print a complex SQL file
sqlglot-cli --pretty < query.sql

# Check the syntax of a SQL string against a specific dialect
sqlglot-cli --read bigquery "SELECT * FROM `project.dataset.table`"
```

## API examples

### Programmatic AST Manipulation
Add a filter to an existing query programmatically:

```python
from sqlglot import parse_one, exp

sql = "SELECT name FROM users"
expression = parse_one(sql)

# Append a WHERE clause
new_expression = expression.where("age > 18")
print(new_expression.sql())
# Output: SELECT name FROM users WHERE age > 18
```

### Static Safety Validation
Check for prohibited keywords in an agent-generated query:

```python
import sqlglot

def is_safe(sql):
    try:
        for expression in sqlglot.parse(sql):
            if any(isinstance(node, (sqlglot.exp.Drop, sqlglot.exp.Delete)) for node, *_ in expression.walk()):
                return False
        return True
    except sqlglot.errors.ParseError:
        return False

print(is_safe("DELETE FROM users")) # False
```

## Related tools / concepts
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — The primary architecture utilizing SQLGlot.
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — Practical safety patterns.
- [Claude 4.8](../ai_knowledge/claude.md) — Frontier model used for SQL generation.
- [Gemma 3](../ai_knowledge/local_llms.md) — Local model for privacy-first SQL synthesis.
- [FastMCP 3.0](../automation_orchestration/mcp.md) — Protocol for low-latency tool and data discovery.
- [DuckDB](../infrastructure/duckdb.md) — Common transpilation target for local analytics.
- [Jules](../ai_knowledge/jules.md) — Agent that orchestrates SQL-based maintenance tasks.

## Sources / References
- [SQLGlot GitHub Repository](https://github.com/tobymao/sqlglot)
- [Official Documentation](https://sqlglot.com/)
- [Text-to-SQL Safety Patterns (KnowledgeOps)](../../architecture/data-copilot-text-to-sql.md)

---
## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
