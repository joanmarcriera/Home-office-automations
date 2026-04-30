# Playbook: Data Copilot SQL Validation & Repair

This playbook defines the guardrails required to ensure that AI-generated SQL is safe, performant, and semantically correct before execution. It includes a multi-stage validation pipeline and a self-correction loop for common failures.

## Goal
Implement enterprise-safe validation for Text-to-SQL outputs, preventing data leaks, expensive queries, or incorrect metric definitions.

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

## 5. Stop and Escalate Criteria
Stop the automated flow and notify a human if:
1.  **Ambiguous Metric**: Multiple valid columns match the user's intent.
2.  **Permission Denied**: The query attempts to access a restricted schema.
3.  **Repair Timeout**: Max retries reached without a valid query.
4.  **Complex Logic**: The intent requires a logic depth the current model cannot reliably produce.

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
