# Playbook: Data Copilot SQL Validation & Repair

## What it is
A technical blueprint and operational framework for validating AI-generated SQL queries before they reach the database. It establishes a "guardrail" system that combines static analysis, dynamic dry-runs, and LLM-based semantic checks to ensure safety, performance, and correctness.

## What problem it solves
Prevents "hallucinated" SQL from causing data breaches (SQL injection), performance degradation (cross-joins on large tables), or business errors (incorrect metric calculations).

## Where it fits in the stack
It operates within the **Inference Pipeline**, specifically between the **SQL Generation Agent** and the **Database Execution Engine**.

## Typical use cases
- **Automated PII Masking**: Ensuring that any query targeting the `users` table automatically excludes `email` or `password_hash` columns.
- **Query Optimization**: Catching unindexed filters in natural language questions like "Show me every transaction since 2010" before they scan millions of rows.
- **Dialect Conversion**: Automatically correcting minor syntax errors when an LLM trained on Postgres tries to query a SQLite database.
- **Safety Enforcement**: Blocking `DROP TABLE` or `DELETE` commands that might be generated due to prompt injection or model hallucination.
- **Home automation bots**: Triggering database-driven actions (e.g., "Show me my energy usage") with guaranteed safety.

## Strengths
- **Defense in Depth**: Multiple layers of validation ensure that even if one check misses a risk, another will likely catch it.
- **Reduced Hallucinations**: The self-correction loop allows the model to learn from its own mistakes in real-time.
- **Cost Savings**: Prevents expensive, inefficient queries from consuming excessive cloud database resources.
- **Safety**: Multi-layered defense against malicious or accidental query errors.

## Limitations
- **Validation Latency**: Each check adds overhead to the total response time.
- **Rule Maintenance**: Policy allowlists must be updated whenever the database schema changes.
- **LLM-as-a-Judge Bias**: Semantic validation using a second LLM is not 100% foolproof and may itself hallucinate.

## When to use it
- In any production environment where LLMs generate SQL queries for live databases.
- When working with high-volume or highly sensitive data.
- When utilizing smaller, less reliable models for SQL generation that require a "safety net."

## When not to use it
- **Development/Sandbox Environments**: Where risks are low and rapid prototyping is more important than strict validation.
- **Read-Only Public Datasets**: If the data is already public and the database is small enough that performance is not a concern.
- **Fixed-Query Systems**: If the AI is just selecting from a set of pre-written, human-verified SQL queries.

## Getting started

To implement basic static validation, use the `sqlglot` library to parse and inspect generated queries.

```python
import sqlglot
from sqlglot import exp

def is_query_safe(sql_query: str, allowed_tables: list[str]) -> bool:
    try:
        # Parse the SQL into an expression tree
        expressions = sqlglot.parse(sql_query)

        for expression in expressions:
            # 1. Check for forbidden mutation keywords
            if any(isinstance(node, (exp.Delete, exp.Drop, exp.Update, exp.Insert, exp.Alter))
                   for node, *_ in expression.walk()):
                print("Error: Mutation detected.")
                return False

            # 2. Verify table allowlist
            for table in expression.find_all(exp.Table):
                if table.name.lower() not in [t.lower() for t in allowed_tables]:
                    print(f"Error: Table '{table.name}' not in allowlist.")
                    return False

            # 3. Ensure LIMIT is present (optional but recommended)
            if not expression.find(exp.Limit):
                print("Warning: No LIMIT clause found. Appending default limit.")
                # Logic to append LIMIT could go here

        return True
    except sqlglot.errors.ParseError as e:
        print(f"Syntax Error: {e}")
        return False

# Example Usage
query = "SELECT * FROM users; DROP TABLE products;"
tables = ["items", "categories"]
print(f"Is safe: {is_query_safe(query, tables)}")
```

## The Validation Pipeline

1.  **Syntactic Validation**: Does the SQL run? (Dry-run)
2.  **Policy Validation**: Does it violate security rules? (Allowlists, row limits)
3.  **Semantic Validation**: Does it match the intended metrics/filters? (LLM-as-a-Judge)

### 1. Syntax Validation (Dry-Run)
Before returning or executing, the system must perform a `EXPLAIN` or a dry-run with `LIMIT 0`.
- **Low-cost implementation**: Use the local SQLite `EXPLAIN QUERY PLAN` or a temporary in-memory DB to verify syntax without hitting production data.

### 2. Policy Validation Checklist
Every query must pass these automated checks:
- [x] **Row Limits**: Does the query have a `LIMIT` clause? (Hard cap e.g., 1000).
- [x] **Table Allowlist**: Does it only touch tables defined in the Workspace context?
- [x] **No Mutations**: Does it contain forbidden keywords like `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `GRANT`?
- [x] **PII/PHI Masking**:
  - Sensitive columns (e.g., `ssn`, `password_hash`) must be excluded from the `SELECT` list.
  - If a sensitive column is needed for filtering (e.g., `user_id`), it must be hashed or replaced with a pseudonym in the final output returned to the UI.

### 3. Semantic Validation & Risk Taxonomy
A query can be syntactically perfect but business-incorrect.

| Risk Type | Symptom | Example |
| :--- | :--- | :--- |
| **Syntactic Pass** | Query runs but is slow. | Missing a join condition (Cross Join). |
| **Metric Drift** | Wrong column for a metric. | Using `subtotal` instead of `total_including_tax`. |
| **Filter Failure** | Wrong time range or scope. | Showing "Global" data when asked for "UK only". |
| **Join Explosion** | Joining too many tables. | Joining 5 tables to answer a 1-table question. |
| **Performance Risk** | Missing indexes or scans. | Querying a 10M row table without an indexed filter. |

### 4. Self-Correction Loop (Repair)
If validation fails, the "SQL Repair" flow is triggered:
1.  **Capture Error**: Gather the SQL + Error Message (from DB) or Policy Violation (from Guardrail).
2.  **Prompt Generator**: Feed the error back to the LLM using a repair template.
3.  **Retry Limit**: Max 2 retries. If still failing, trigger "Stop and Escalate".

### 5. Stop and Escalate Criteria
Stop the automated flow and notify a human if:
1.  **Ambiguous Metric**: Multiple valid columns match the user's intent.
2.  **Permission Denied**: The query attempts to access a restricted schema.
3.  **Repair Timeout**: Max retries reached without a valid query.
4.  **Complex Logic**: The intent requires a logic depth the current model cannot reliably produce.

## Low-Cost Implementation Options
- **SQLGlot (Local Static Analysis)**: Use SQLGlot to parse the generated SQL and check for structural issues (e.g., cross-joins) or forbidden keywords without requiring a live database or an LLM call.
- **Pydantic Guardrails**: Use Pydantic to validate the *structure* of the SQL intent before generation.
- **Small Model Judge**: Use a small local model (Qwen 2.5 7B) specifically to check the generated SQL against the policy checklist.

## Related tools / concepts
- [Data Copilot Architecture](../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Answer Synthesis Schema](../reference-implementations/data-copilot/answer-synthesis-schema.md)
- [Tool Calling & Model Context Protocol (MCP)](../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Fiddler AI Guardrails](../tools/process_understanding/fiddler.md)
- [LastMile AI Eval](../tools/process_understanding/lastmile.md)
- [Ragas Evaluation Metrics](../tools/process_understanding/ragas.md)
- [Langfuse Tracing](../tools/process_understanding/langfuse.md)
- [Pydantic AI Framework](../tools/frameworks/pydantic-ai.md)

## Sources / References
- [SQLGlot Documentation](https://github.com/tobymao/sqlglot)
- [Guardrails AI](https://www.guardrailsai.com/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
- Related Issues: #189
