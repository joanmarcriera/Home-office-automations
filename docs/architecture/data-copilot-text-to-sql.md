# Data Copilot: Layered Text-to-SQL Architecture

## What it is
Data Copilot is a high-performance, cost-optimized pipeline architecture for converting natural language questions into executable SQL queries. It employs a **Layered Multi-Agent** approach to decompose complex Text-to-SQL tasks into specialized stages. In late October / November 2026, it utilizes the **Model Context Protocol (MCP 3.1) Task Protocol** for standardized database discovery, and **Claude 5.1** or **GPT-5.5** for high-fidelity reasoning, while maintaining local-first execution for simpler queries via **Gemma 3**, **Qwen 3.6**, or **Llama 4**.

## What problem it solves
Traditional "one-shot" Text-to-SQL approaches often fail on complex schemas (100+ tables), ambiguous intents, or large-scale data environments, leading to "context window exhaustion" and high token costs. Data Copilot solves this by breaking the problem into modular steps—routing, intent extraction, table selection, column pruning, and SQL generation—drastically reducing token usage and increasing query accuracy through aggressive schema pruning. It enables **Agentic SQL Synthesis** where models iteratively refine queries based on structural feedback.

## Where it fits in the stack
**Data Access & Analytics Layer** — It acts as an intelligent intermediary between natural language interfaces (Chat Assistants) and relational databases (SQLite, Postgres, BigQuery). It sits above the [Inference Plane](../services/litellm.md) and integrates with the [Automated Contribution System](./automated_contributions.md) for self-healing metadata updates. It utilizes **FastMCP 3.1** for ultra-low latency tool discovery.

## Typical use cases
- **Natural Language BI**: Allowing non-technical users to query metrics like "weekly growth" or "inventory turnover".
- **Home Lab Observability**: Querying [Home Assistant](../services/home-assistant.md) or [Actual Budget](../services/actual-budget.md) databases for historical trends.
- **Automated Data Reporting**: Generating on-demand reports from [Homebox](../services/homebox.md) or [Grocy](../services/grocy.md) without manual SQL.
- **Autonomous Error Correction**: Agents using Text-to-SQL to verify their own database-backed task state via **MCP 3.1 Task Protocol**.

## Strengths
- **Token Efficiency**: Reduces prompt size by >90% by only sending pruned schema cards to the final generator.
- **Accuracy**: Specialized agents (Table Agent, Prune Agent) minimize hallucinations by focusing on narrow sub-tasks.
- **Cost-Optimized Routing**: Routes simple steps to local models (**Gemma 3** or **Llama 4**) and escalates to frontier models only when needed.
- **Governance**: Integrated **SQL Policy Validators** (using [SQLGlot](../tools/development_ops/sqlglot.md)) prevent unsafe or mutation-based queries.

## Limitations
- **Sequential Latency**: Multi-agent pipelines introduce more overhead than single-shot prompts, though **FastMCP 3.1** minimizes this.
- **Schema Dependency**: Requires high-quality table/column descriptions in the database metadata for best results.
- **Orchestration Complexity**: Requires managing multiple prompts, JSON interfaces, and state handoffs between layers.

## When to use it
- When querying complex schemas with dozens or hundreds of tables and complex join paths.
- When token cost management is a priority for high-volume agentic applications.
- When transparent, auditable reasoning steps are required for data-driven decisions.

## When not to use it
- For simple, single-table databases where one-shot prompts are faster and cheaper.
- For sub-second real-time querying where the latency of multi-stage LLM calls is unacceptable.
- When data resides in unstructured silos requiring pure RAG instead of relational SQL.

## Getting started

### 1. Register Database Workspaces
Define your database connections and high-level descriptions in your workspace config:
```json
{
  "workspace_id": "home_finance",
  "db_path": "sqlite:///actual_budget.db",
  "description": "Family budgeting and transaction history"
}
```

### 2. Configure Model Routing
Assign models to each layer (Router, Intent, Table, Prune, SQL) in your [LiteLLM](../services/litellm.md) config. Prefer local models like [Gemma 3](../tools/ai_knowledge/local_llms.md) for Routing/Pruning.

### 3. Initialize the SQL Validator
Ensure `scripts/sql_validator.py` is configured with your table allowlists and mutation blocking policies, leveraging [SQLGlot](../tools/development_ops/sqlglot.md).

### 4. Human-in-the-Loop (HITL) Checkpoints
Enable HITL for "Table Selection" and "Column Pruning" steps during initial deployment to build trust and refine schema descriptions.

## CLI examples
Interact with the Data Copilot pipeline via the repository's internal CLI:

```bash
# Run a full Text-to-SQL pipeline for a user question
python3 scripts/sql_validator.py --query "What was our total grocery spend last month?" --workspace grocy

# Test only the Table Selection agent
python3 scripts/sql_validator.py --task table-selection --intent "total_inventory_value" --workspace inventory

# Validate a raw SQL query against safety policies using Task Protocol
python3 scripts/sql_validator.py --validate "SELECT * FROM users;" --use-task-protocol
```

## API examples
Integrate the layered architecture into your Python-based agent workflows, leveraging Pydantic v2 validation for structured inputs and safety flags:

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

class SQLValidationRequest(BaseModel):
    """Pydantic v2 schema for an SQL query validation request."""
    query: str = Field(description="The natural language query or raw SQL to validate")
    workspace: str = Field(description="Database workspace context (e.g., grocy, finance)")
    allow_joins: bool = Field(default=True, description="Whether multi-table joins are permitted")
    max_rows: int = Field(default=100, description="Upper bound on result rows returned")

    @field_validator("workspace")
    @classmethod
    def validate_workspace(cls, value: str) -> str:
        allowed = ["grocy", "finance", "inventory", "home_assistant"]
        if value.lower() not in allowed:
            raise ValueError(f"Workspace must be one of: {allowed}")
        return value.lower()

class SQLValidationResult(BaseModel):
    """Pydantic v2 schema for SQL query validation outcomes."""
    is_safe: bool = Field(description="Whether the query complies with safety policies")
    generated_sql: Optional[str] = Field(default=None, description="The sanitized SQL query generated")
    explanation: str = Field(description="Audit explanation or error reasoning")
    execution_time_ms: Optional[float] = Field(default=None, description="Latency details if run")

def validate_and_compile_sql(req: SQLValidationRequest) -> SQLValidationResult:
    """Simulates validating and compiling an SQL request under MCP 3.1."""
    if "drop" in req.query.lower() or "delete" in req.query.lower():
        return SQLValidationResult(
            is_safe=False,
            explanation="Unsafe query detected: mutations (DROP/DELETE) are strictly prohibited."
        )

    # Simulating generated query based on intent
    compiled_sql = f"SELECT SUM(spend) FROM {req.workspace}_transactions LIMIT {req.max_rows};"
    return SQLValidationResult(
        is_safe=True,
        generated_sql=compiled_sql,
        explanation="Query successfully verified against safety policies.",
        execution_time_ms=14.2
    )

# Example Usage:
if __name__ == "__main__":
    request_obj = SQLValidationRequest(
        query="What is the total spent?",
        workspace="finance",
        max_rows=50
    )
    result = validate_and_compile_sql(request_obj)
    print(result.model_dump_json(indent=2))
```

## Related tools / concepts
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — Detailed safety playbook.
- [Multi-Agent KnowledgeOps](./multi_agent_knowledgeops.md) — Governance for agentic pipelines.
- [Automated Contribution System](./automated_contributions.md) — Metadata ingestion flows.
- [LiteLLM Proxy](../services/litellm.md) — Unified inference plane for routing.
- [SQLGlot](../tools/development_ops/sqlglot.md) — Engine for SQL parsing and safety.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Privacy-first local model for schema pruning.
- [FastMCP 3.1](../tools/automation_orchestration/mcp.md) — High-performance tool hosting.
- [Actual Budget](../services/actual-budget.md) — Primary data source for finance.
- [Home Assistant](../services/home-assistant.md) — Primary data source for automation.

## Sources / references
- [Uber Engineering: Text-to-SQL at Scale](https://www.uber.com/en-GB/blog/text-to-sql-at-scale/)
- [SQL-Coder (Defog.ai)](https://github.com/defog-ai/sqlcoder)
- [MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/)
- [Gemma 3: Open Models for Agentic Workflows](https://ai.google.dev/gemma)

---
## Contribution Metadata
- Last reviewed: 2026-11-20
- Confidence: high
