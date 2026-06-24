# Data Copilot: Layered Text-to-SQL Architecture

## What it is
Data Copilot is a high-performance, cost-optimized pipeline architecture for converting natural language questions into executable SQL queries. It employs a **Layered Multi-Agent** approach to decompose complex Text-to-SQL tasks into specialized stages. In June 2026, it utilizes **MCP 3.0** for database discovery and **Claude 4.8/GPT-5.5** for high-fidelity reasoning, while maintaining local-first execution for simpler queries via **Llama 4 (8B/70B)**.

## What problem it solves
Traditional "one-shot" Text-to-SQL approaches often fail on complex schemas (100+ tables), ambiguous intents, or large-scale data environments, often leading to "context window exhaustion" and high token costs. Data Copilot solves this by breaking the problem into modular steps—routing, intent extraction, table selection, column pruning, and SQL generation—drastically reducing token usage and increasing query accuracy through aggressive schema pruning.

## Where it fits in the stack
**Data Access & Analytics Layer** — It acts as an intelligent intermediary between natural language interfaces (Chat Assistants) and relational databases (SQLite, Postgres, BigQuery). It sits above the [Inference Plane](../services/litellm.md) and integrates with the [Automated Contribution System](./automated_contributions.md) for self-healing metadata updates.

## Typical use cases
- **Natural Language BI**: Allowing non-technical users to query metrics like "weekly growth" or "inventory turnover".
- **Home Lab Observability**: Querying [Home Assistant](../services/home-assistant.md) or [Actual Budget](../services/actual-budget.md) databases for historical trends.
- **Automated Data Reporting**: Generating on-demand reports from [Homebox](../services/homebox.md) or [Grocy](../services/grocy.md) without manual SQL.
- **Autonomous Error Correction**: Agents using Text-to-SQL to verify their own database-backed task state.

## Strengths
- **Token Efficiency**: Reduces prompt size by >90% by only sending pruned schema cards to the final generator.
- **Accuracy**: Specialized agents (Table Agent, Prune Agent) minimize hallucinations by focusing on narrow sub-tasks.
- **Cost-Optimized Routing**: Routes simple steps to local models (**Llama 4 8B**) and escalates to frontier models only when needed.
- **Governance**: Integrated **SQL Policy Validators** (using `sqlglot`) prevent unsafe or mutation-based queries.

## Limitations
- **Sequential Latency**: Multi-agent pipelines introduce more overhead than single-shot prompts.
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
Assign models to each layer (Router, Intent, Table, Prune, SQL) in your [LiteLLM](../services/litellm.md) config. Prefer local models for Routing/Pruning.

### 3. Initialize the SQL Validator
Ensure `scripts/sql_validator.py` is configured with your table allowlists and mutation blocking policies.

### 4. Human-in-the-Loop (HITL) Checkpoints
Enable HITL for "Table Selection" and "Column Pruning" steps during initial deployment to build trust and refine schema descriptions.

## CLI examples
Interact with the Data Copilot pipeline via the repository's internal CLI:

```bash
# Run a full Text-to-SQL pipeline for a user question
python3 scripts/sql_validator.py --query "What was our total grocery spend last month?" --workspace grocy

# Test only the Table Selection agent
python3 scripts/sql_validator.py --task table-selection --intent "total_inventory_value" --workspace inventory

# Validate a raw SQL query against safety policies
python3 scripts/sql_validator.py --validate "SELECT * FROM users; DROP TABLE orders;" --workspace finance
```

## API examples
Integrate the layered architecture into your Python-based agent workflows:

```python
from scripts.sql_validator import DataCopilotPipeline

# Initialize the pipeline with MCP discovery
pipeline = DataCopilotPipeline(workspace="finance", agent_level="high-confidence")

# Process a natural language question
result = pipeline.execute("Show me transactions over $500 in the last 30 days")

if result.is_safe:
    print(f"Generated SQL: {result.sql}")
    # Execute safely via internal data connector
    data = result.execute_query()
```

## Related tools / concepts
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — Detailed safety playbook.
- [Multi-Agent KnowledgeOps](./multi_agent_knowledgeops.md) — Governance for agentic pipelines.
- [Automated Contribution System](./automated_contributions.md) — Metadata ingestion flows.
- [LiteLLM Proxy](../services/litellm.md) — Unified inference plane for routing.
- [Home Assistant](../services/home-assistant.md) — Primary data source for automation.
- [Actual Budget](../services/actual-budget.md) — Primary data source for finance.
- [Jules Agent](../tools/ai_knowledge/jules.md) — Core execution agent for the hub.
- [SQLGlot](../../tools/development_ops/sqlglot.md) — Engine for SQL parsing and safety.

## Sources / references
- [Uber Engineering: Text-to-SQL at Scale](https://www.uber.com/en-GB/blog/text-to-sql-at-scale/)
- [SQL-Coder (Defog.ai)](https://github.com/defog-ai/sqlcoder)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/)
- [Llama 4: Open Intelligence Benchmark](https://ai.meta.com/llama/)

---
## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
