# Playbook: Data Copilot SQL Validation & Repair

## What it is
The Data Copilot SQL Validation & Repair playbook is a standardized operational framework for ensuring the safety, performance, and correctness of AI-generated SQL queries. It establishes a "guardrail" system that sits between the LLM generator and the live production database, automatically catching and fixing errors before they cause impact.

## What problem it solves
Text-to-SQL systems are prone to three main risks: **security leaks** (accessing unauthorized data), **performance degradation** (running expensive cross-joins that crash the DB), and **semantic inaccuracy** (returning a result that runs but answers the wrong question). This playbook provides a structured way to mitigate these risks and includes a "self-healing" loop to reduce human intervention.

## Goal
Implement enterprise-safe validation for Text-to-SQL outputs, preventing data leaks, expensive queries, or incorrect metric definitions.

## Where it fits in the stack
This playbook sits in the **Playbooks** section of the repository. It defines the runtime safety procedures for the **Orchestration** layer (Data Copilot architecture) and protects the **Intake & Storage** layer (the underlying databases). It uses tools from the **Development & Ops** layer (like SQLGlot) for implementation.

## The Validation Pipeline

1.  **Syntactic Validation**: Does the SQL run? (Dry-run)
2.  **Policy Validation**: Does it violate security rules? (Allowlists, row limits)
3.  **Semantic Validation**: Does it match the intended metrics/filters? (LLM-as-a-Judge)

## 1. Syntax Validation (Dry-Run)
Before returning or executing, the system must perform a `EXPLAIN` or a dry-run with `LIMIT 0`.
- **Low-cost implementation**: Use the local SQLite `EXPLAIN QUERY PLAN` or a temporary in-memory DB to verify syntax without hitting production data.

## 2. Policy Validation Checklist
Every query must pass these automated checks:
- [ ] **Row Limits**: Does the query have a `LIMIT` clause? (Hard cap e.g., 1000).
- [ ] **Table Allowlist**: Does it only touch tables defined in the Workspace context?
- [ ] **No Mutations**: Does it contain forbidden keywords like `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `GRANT`?
- [ ] **PII/PHI Control**: Are sensitive columns (e.g., `ssn`, `password_hash`, `private_notes`) excluded?

## Typical use cases
- **Automated PII Masking**: Ensuring that any query targeting the `users` table automatically excludes `email` or `password_hash` columns.
- **Query Optimization**: Catching unindexed filters in natural language questions like "Show me every transaction since 2010" before they scan millions of rows.
- **Dialect Conversion**: Automatically correcting minor syntax errors when an LLM trained on Postgres tries to query a SQLite database.
- **Safety Enforcement**: Blocking `DROP TABLE` or `DELETE` commands that might be generated due to prompt injection or model hallucination.

## 3. Semantic Validation & Risk Taxonomy
A query can be syntactically perfect but business-incorrect.

| Risk Type | Symptom | Example |
| :--- | :--- | :--- |
| **Syntactic Pass** | Query runs but is slow. | Missing a join condition (Cross Join). |
| **Metric Drift** | Wrong column for a metric. | Using `subtotal` instead of `total_including_tax`. |
| **Filter Failure** | Wrong time range or scope. | Showing "Global" data when asked for "UK only". |
| **Join Explosion** | Joining too many tables. | Joining 5 tables to answer a 1-table question. |
| **Performance Risk** | Missing indexes or scans. | Querying a 10M row table without an indexed filter. |

## 4. Self-Correction Loop (Repair)
If validation fails, the "SQL Repair" flow is triggered:
1.  **Capture Error**: Gather the SQL + Error Message (from DB) or Policy Violation (from Guardrail).
2.  **Prompt Generator**: Feed the error back to the LLM: "Your query failed due to [Error]. Rewrite it adhering to the schema and policy."
3.  **Retry Limit**: Max 2 retries. If still failing, trigger "Stop and Escalate".

## Strengths
- **Defense in Depth**: Multiple layers of validation ensure that even if one check misses a risk, another will likely catch it.
- **Reduced Hallucinations**: The self-correction loop allows the model to learn from its own mistakes in real-time.
- **Cost Savings**: Prevents expensive, inefficient queries from consuming excessive cloud database resources.

## Limitations
- **Validation Latency**: Each check adds overhead to the total response time.
- **Rule Maintenance**: Policy allowlists must be updated whenever the database schema changes.
- **LLM-as-a-Judge Bias**: Semantic validation using a second LLM is not 100% foolproof and may itself hallucinate.

## 5. Stop and Escalate Criteria
Stop the automated flow and notify a human if:
1.  **Ambiguous Metric**: Multiple valid columns match the user's intent.
2.  **Permission Denied**: The query attempts to access a restricted schema.
3.  **Repair Timeout**: Max retries reached without a valid query.
4.  **Complex Logic**: The intent requires a logic depth the current model cannot reliably produce.

## When to use it
- In any production-facing Text-to-SQL system where users have direct access to query tools.
- When working with high-volume or sensitive data that requires strict access controls.
- When utilizing smaller, less reliable models for SQL generation that require a "safety net."

## When not to use it
- **Development/Sandbox Environments**: Where risks are low and rapid prototyping is more important than strict validation.
- **Read-Only Public Datasets**: If the data is already public and the database is small enough that performance is not a concern.
- **Fixed-Query Systems**: If the "AI" is just selecting from a set of pre-written, human-verified SQL queries.

## Low-Cost Implementation Options
- **SQLGlot (Local Static Analysis)**: Use SQLGlot to parse the generated SQL and check for structural issues (e.g., cross-joins) or forbidden keywords without requiring a live database or an LLM call. It can also be used to automatically inject `LIMIT` clauses.
- **Pydantic Guardrails**: Use Pydantic to validate the *structure* of the SQL intent before generation.
- **Small Model Judge**: Use a small local model (Qwen 2.5 7B) specifically to check the generated SQL against the policy checklist.

## Sources / References
- [SQLGlot Documentation](https://github.com/tobymao/sqlglot)
- [Guardrails AI](https://www.guardrailsai.com/)

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
- Related Issues: #189
