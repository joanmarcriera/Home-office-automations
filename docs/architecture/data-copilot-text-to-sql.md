# Data Copilot: Layered Text-to-SQL Architecture

This document defines a robust, cost-effective pipeline for converting natural language questions into executable SQL queries. It uses a layered, multi-agent approach to handle complexity, minimize token usage, and ensure accuracy through specialized agents and human-in-the-loop (HITL) checkpoints.

## Overview

Traditional "one-shot" Text-to-SQL often fails on complex schemas or ambiguous questions. This architecture breaks the problem into five distinct layers, each with a narrow focus.

```mermaid
flowchart TD
    User([User Question]) --> Router[1. Workspace Router]
    Router --> Intent[2. Intent Agent]
    Intent --> Table[3. Table Agent]
    Table --> Prune[4. Column Prune Agent]
    Prune --> SQL[5. SQL Generator]
    SQL --> Output[/SQL Query/]

    subgraph HITL [Human-in-the-Loop]
        TableCheck{Verify Tables?}
        PruneCheck{Verify Columns?}
    end

    Table -.-> TableCheck
    TableCheck -- Approved --> Prune
    Prune -.-> PruneCheck
    PruneCheck -- Approved --> SQL
```

## Layers & Interfaces

### 1. Workspace Router
- **Role**: Identifies which "workspace" (database or domain) the question belongs to (e.g., Finance, Home Automation, Inventory).
- **Benefit**: Prevents the LLM from being overwhelmed by the entire repository's schema.
- **Model Recommendation**: Small/Fast (e.g., Qwen 2.5 0.8B or 2B via Ollama).
- **Interface**:
```json
{
  "workspace_id": "inventory",
  "description": "Home Inventory and Assets",
  "db_connection_string": "sqlite:///home_inventory.db"
}
```

### 2. Intent Agent
- **Role**: Refines the raw user question into a structured intent, identifying metrics, time ranges, and filters.
- **Input**: User question + Workspace context.
- **Output**: JSON object with intent parameters.
- **Interface**:
```json
{
  "metrics": ["quantity", "purchase_price"],
  "dimensions": ["category"],
  "filters": {"room": "Kitchen"},
  "time_range": "last_30_days"
}
```

### 3. Table Agent
- **Role**: Selects the minimal set of tables required to answer the intent.
- **HITL Point**: Optional user approval of selected tables to prevent joined-table explosions.
- **Pruning Strategy**: Semantic search over table descriptions (RAG) instead of dumping all table names.
- **Interface**:
```json
{
  "selected_tables": ["items", "categories"],
  "rationale": "Need 'items' for quantity/price and 'categories' for grouping."
}
```

### 4. Column Prune Agent
- **Role**: For the selected tables, identifies only the columns needed for the query.
- **Benefit**: Drastically reduces the prompt size for the final SQL generation, staying within small model context limits.
- **HITL Point**: Verification of critical columns (e.g., "Are you sure you want 'net_price' instead of 'gross_price'?").
- **Interface**:
```json
[
  {
    "table_name": "items",
    "columns": ["name", "quantity", "purchase_price", "category_id", "room"]
  },
  {
    "table_name": "categories",
    "columns": ["id", "name"]
  }
]
```

### 5. SQL Generator
- **Role**: Produces the final SQL query using the pruned schema and refined intent.
- **Input**: Intent JSON + Pruned Schema (Tables + Columns).
- **Output**: Valid SQL string.
- **Interface**:
```json
{
  "sql": "SELECT c.name, SUM(i.quantity) FROM items i JOIN categories c ON i.category_id = c.id WHERE i.room = 'Kitchen' GROUP BY c.name;"
}
```

## Cost & Model Routing

To maintain a "free/cheap-first" stack, we recommend the following model routing:

| Layer | Recommended Model | Rationale |
| :--- | :--- | :--- |
| Router | Qwen 2.5 0.8B (Local) | Low latency, simple classification. |
| Intent | Qwen 2.5 7B or Llama 3.1 8B | Needs better reasoning for metric extraction. |
| Table Selection | Groq (Llama 3.1 70B) | High accuracy for selection; remains free under Groq limits. |
| Column Pruning | Qwen 2.5 7B (Local) | Structured output is critical here. |
| SQL Generation | GPT-4o-mini or Claude 3.5 Haiku | High reliability for syntax at low cost. |

## Token Control & Schema Pruning Strategy

To minimize costs and stay within the context limits of smaller models, the following pruning strategies are used:

1.  **Semantic Table Filtering**: Instead of sending all table schemas, we use an embedding-based search (RAG) to find the top $N$ (usually 3-5) most relevant tables for the intent.
2.  **Column-Level Pruning**: Once tables are selected, only the primary keys, foreign keys, and columns identified by the **Column Prune Agent** are included in the final SQL generation prompt.
3.  **Schema metadata**: We include short comments in the schema (e.g., `-- type: categorical`) rather than raw data samples to keep token counts low.
4.  **Fallback Routing**: If a query fails on a local model (e.g. Qwen 2.5 7B), it is automatically routed to a more capable but expensive model (e.g. Claude 3.5 Sonnet) with the same pruned schema.

## Failure Modes & Mitigation

1. **Wrong Domain (Router Failure)**:
   - *Symptom*: Question about "eggs" routed to "Home Office" instead of "Grocy".
   - *Mitigation*: Provide a "Unsure" fallback that triggers a human clarification.
2. **Table Explosion (Table Agent Failure)**:
   - *Symptom*: Selecting 10+ tables for a simple query.
   - *Mitigation*: Hard limit on table count (e.g., max 4) and HITL verification.
3. **Metric Ambiguity**:
   - *Symptom*: User asks for "Total Sales" but schema has `subtotal`, `tax`, and `total`.
   - *Mitigation*: Intent agent must request clarification if multiple column matches are found in the metadata.

## When NOT to use Text-to-SQL

- **High-stakes Financial Audits**: Where 100% precision is required without human review.
- **Extremely Wide Tables**: Tables with 500+ columns (requires heavy RAG-based column selection first).
- **Non-Relational Complex Joins**: When the data resides across multiple incompatible silos (use a Multi-Agent RAG instead).

## Related tools / concepts
- [Data Copilot MCP Tooling](../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Answer Synthesis Schema](../reference-implementations/data-copilot/answer-synthesis-schema.md)

## Sources / References
- [Uber Engineering: Text-to-SQL at Scale](https://www.uber.com/en-GB/blog/text-to-sql-at-scale/)
- [SQL-Coder (Defog.ai)](https://github.com/defog-ai/sqlcoder)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
