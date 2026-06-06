# Data Copilot Reference Implementations

## Overview
Data Copilot is a set of patterns and reference implementations for building AI agents capable of interacting with structured data, primarily through Text-to-SQL and automated data analysis. This directory contains detailed schemas, guides, and templates for implementing these patterns.

## Components

| Implementation | Description |
| :--- | :--- |
| [Skeleton Guide](skeleton-guide.md) | Standardized project structure for Data Copilot implementations. |
| [Answer Synthesis Schema](answer-synthesis-schema.md) | JSON schemas for structuring natural language answers from data results. |

## Related Architecture & Patterns
- [Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [SQL Validation Playbook](../../playbooks/data-copilot-sql-validation.md)

## Typical Workflow
1. **Query Intent Recognition**: Understanding what the user is asking for in terms of data.
2. **Schema Retrieval**: Fetching relevant database schema information.
3. **SQL Generation**: Generating a valid SQL query based on the intent and schema.
4. **Execution & Validation**: Running the query and validating results.
5. **Answer Synthesis**: Converting raw data into a natural language response.

## Sources / References
- [Data Copilot Project Case Study](../../reports/data-copilot-sprint-resolution.md)
- [Verification Report](../../reports/data-copilot-issue-verification.md)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
