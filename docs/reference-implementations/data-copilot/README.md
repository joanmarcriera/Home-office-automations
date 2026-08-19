# Data Copilot Reference Implementations

## Overview
Data Copilot is an enterprise-grade agentic system pattern for executing natural language data intelligence over heterogeneous structured databases (SQL, Warehouses, Lakehouses). Standardized in early 2027, the Data Copilot pattern enables autonomous LLMs (such as **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**) to perform schema discovery, text-to-SQL generation, iterative query validation, deterministic result execution, and answer synthesis using the **FastMCP 3.1** protocol.

This directory contains detailed reference implementations, JSON validation schemas, architectural designs, and deployment templates.

## Architecture & System Flow

```
[User Query] ──> [Query Intent Analyzer] ──> [Schema RAG / FastMCP Registry]
                                                       │
[Answer Synthesis] <── [Result Formatter] <── [Query Execution & Guardrails] <── [Text-to-SQL Engine]
```

1. **Intent Analysis & Tool Search**: Parse natural language user intent and select targeted database schemas using FastMCP tool definitions.
2. **Schema RAG & Context Retrieval**: Retrieve minimal DDL schemas and foreign key constraints to prevent context window saturation.
3. **Guardrailed SQL Generation**: Generate dialect-specific SQL (PostgreSQL, Snowflake, ClickHouse) enforcing read-only permissions and row limits.
4. **Execution & Validation**: Execute query through sandboxed database connectors with automated syntax and semantic error recovery loops.
5. **Answer Synthesis**: Format structured row datasets into natural language insights and visualization specifications.

## Components & Module Index

| Component / Guide | Description | Target Specification |
| :--- | :--- | :--- |
| [Skeleton Guide](skeleton-guide.md) | Standardized repository layout and module structure for Data Copilot projects. | Production Deployment |
| [Answer Synthesis Schema](answer-synthesis-schema.md) | Strict Pydantic v2 / JSON Schema for structuring natural language answers and charts. | API Contracts |

## Related Architecture & Patterns
- [Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md) — Comprehensive architectural specification for enterprise Text-to-SQL runtimes.
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Dynamic schema retrieval strategies for multi-thousand table schemas.
- [MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) — Exposing SQL execution and schema inspection via Model Context Protocol (FastMCP 3.1).
- [SQL Validation Playbook](../../playbooks/data-copilot-sql-validation.md) — Playbook for automated query syntax checking, dry-runs, and SQL safety AST parsing.

## Python Execution Schema Example (Pydantic v2)

```python
from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

class QueryColumnMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str = Field(..., description="Column name returned by query")
    data_type: str = Field(..., description="SQL data type of column")

class DataCopilotQueryResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    query_id: str = Field(..., description="Unique query execution identifier")
    generated_sql: str = Field(..., description="Sanitized SQL query executed against backend")
    execution_time_ms: float = Field(..., description="Execution latency in milliseconds")
    row_count: int = Field(..., description="Number of rows returned")
    columns: List[QueryColumnMetadata] = Field(..., description="List of dataset columns")
    rows: List[Dict[str, Any]] = Field(..., description="Structured records returned")
    synthesis_narrative: str = Field(..., description="Natural language response synthesized by frontier model")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Model confidence in query accuracy")

# Example Usage
result = DataCopilotQueryResult(
    query_id="dc-exec-20270107-9942",
    generated_sql="SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department ORDER BY emp_count DESC LIMIT 5;",
    execution_time_ms=14.2,
    row_count=2,
    columns=[
        QueryColumnMetadata(name="department", data_type="VARCHAR"),
        QueryColumnMetadata(name="emp_count", data_type="BIGINT")
    ],
    rows=[
        {"department": "Engineering", "emp_count": 142},
        {"department": "Sales", "emp_count": 89}
    ],
    synthesis_narrative="Engineering is currently the largest department with 142 employees, followed by Sales with 89 employees.",
    confidence_score=0.98
)
```

## Security & Trust Boundaries
- **Strict Read-Only Enforcement**: All generated SQL must be validated via AST parsers (`sqlglot`) to restrict execution exclusively to `SELECT` statements.
- **Parametrized Queries & AST Analysis**: Disallow statement chaining (`\n;`), `DROP`, `TRUNCATE`, `UPDATE`, and `GRANT` keywords.
- **Tenant Isolation**: Row-level security (RLS) policies and tenant ID injection enforced at the connector proxy level.

## Sources / References
- [Data Copilot Project Case Study](../../reports/data-copilot-sprint-resolution.md)
- [Verification Report](../../reports/data-copilot-issue-verification.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
