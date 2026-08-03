# Data Copilot: Reference Implementation

## What it is
This reference implementation provides a Python-based skeleton for the layered Text-to-SQL pipeline. By late October / November 2026, it has been optimized to leverage [Gemma 3](../../tools/ai_knowledge/local_llms.md) and Qwen 3.6 for low-cost schema pruning and the **MCP 3.1 Task Protocol** and FastMCP 3.1 for standardized tool orchestration. It demonstrates how to use Pydantic v2 for structured data exchange between the different agent layers, where to insert human corrections, and how to keep model routing configurable for free/cheap-first deployments.

## What problem it solves
- **Complexity in Text-to-SQL**: Breaks down a complex single-shot prompt into manageable agentic layers.
- **Data Leakage and Token Bloat**: Uses Column Pruning to ensure only relevant schema context is sent to the final SQL generator.
- **Lack of Control**: Provides explicit "Human-in-the-Loop" (HITL) points to correct agent mistakes before execution.
- **Cost Management**: Enables routing different tasks to different models (e.g., local Ollama for pruning, Claude 5.1 or GPT-5.5 for generation).

## Where it fits in the stack
**Reference Implementation**. It serves as a blueprint for building data-focused agents within the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) and integrates with the [Model Routing Guide](../../knowledge_base/model_routing_guide.md). It utilizes **FastMCP 3.1** for high-performance communication between the orchestration layer and database-specific MCP servers.

## Typical use cases
- **Self-Service Analytics**: Allowing non-technical users to query business databases using natural language.
- **Automated Reporting**: Generating SQL queries for scheduled dashboards without manual coding.
- **Database Exploration**: Helping developers quickly understand a large or unfamiliar schema through natural language questions.
- **Agentic Auditing**: Using agents to verify if historical SQL executions matched the intent.

## Strengths
- **High Precision**: Layered approach reduces the chance of hallucinations compared to single-shot SQL generation.
- **Cost-Effective**: Can use smaller models for early layers (routing, pruning) and reserve high-power models for final generation.
- **Type-Safe**: Pydantic v2 models provide strict validation for all inter-agent communication.
- **HITL Integration**: Built-in hooks for human review of table and column selection.

## Limitations
- **Latency**: Multiple agent calls increase the total time to generate a result.
- **Dependency**: Requires a well-documented schema (comments, types) for the pruning layer to work effectively.
- **Python-Centric**: This specific implementation is tied to the Python/Pydantic ecosystem.
- **Complexity**: Harder to maintain than a single prompt for very simple schemas.

## When to use it
- When building a **production-grade Text-to-SQL system** where accuracy and auditability are critical.
- If you have a **large database schema** that exceeds the context window of a single LLM prompt.
- When you need to **strictly control model costs** and routing (e.g., using local models for metadata tasks).

## When not to use it
- For **simple, single-table databases** where a basic RAG or direct prompt would suffice.
- If **ultra-low latency** is the primary requirement (sub-second response).
- In **legacy environments** where Python is not an available runtime.

## Getting started
To use this reference implementation, you need Python 3.11+ and the Pydantic library.

### Prerequisites
```bash
pip install pydantic asyncio requests
```

### Basic Setup
1.  Copy the `skeleton.py` (referenced below) to your local environment.
2.  Configure your LLM API keys or local [Ollama](../../services/ollama.md) endpoint.
3.  Define your schema in the format expected by the `TableAgent`.
4.  Run the main loop to process a natural language query.

## CLI examples
You can run the reference implementation from the command line to test different queries and model routes.

```bash
# Run a test query against the skeleton
python3 skeleton.py --query "Total sales in London last month" --model-route "gpt-4o-mini"

# Run with human review enabled
python3 skeleton.py --query "Show me top users" --hitl
```

## API examples
The skeleton exposes an asynchronous `process_query` function that can be integrated into larger agentic workflows. The following defines the Pydantic v2 interfaces for the Workspace Router, Intent Agent, Table Agent, Column Prune Agent, and SQL Generator.

```python
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional

class ColumnMetadata(BaseModel):
    name: str
    type: str
    description: str

    @field_validator('name')
    @classmethod
    def validate_col_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Column name cannot be empty.")
        return value.lower()

class TableMetadata(BaseModel):
    name: str
    columns: List[ColumnMetadata]

class PrunedSchema(BaseModel):
    tables: List[TableMetadata]
    intent_summary: str

# Example Agent Call for Column Pruning with Pydantic v2
async def prune_columns(table: TableMetadata, intent: str) -> List[str]:
    # Logic to call LLM (e.g., Gemma 3) and filter relevant columns
    pass

# Main Processing Loop
import asyncio
from skeleton import process_query

async def main():
    result = await process_query(
        "Who are the top 5 customers by revenue?",
        context={"user_id": 1234}
    )
    print(f"Generated SQL: {result.sql}")

if __name__ == "__main__":
    asyncio.run(main())
```

> **Note**: For the full implementation including model routing and HITL hooks, refer to the source `skeleton.py` in the repository.

## Related tools / concepts
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The broader framework this skeleton follows.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — For configuring the `ModelRoute` class.
- [SQL Validation Playbook](../../playbooks/data-copilot-sql-validation.md) — For ensuring the generated SQL is correct.
- [Ollama Service](../../services/ollama.md) — For local, free-tier execution of metadata layers.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — For agentic database discovery in late October / November 2026 (MCP 3.1 and FastMCP 3.1).
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) — The architectural pattern.
- [Answer Synthesis Schema](../metadata-schemas/audio-transcription.md) — Standardized output format.
- [GraphRAG Pattern](../../architecture/README.md) — For complex schema relationship mapping.
- [Late Interaction (ColBERT)](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — For precision retrieval in large schemas.
- [Claude Code Agent](../../tools/development_ops/claude-code.md) — For automated implementation of the SQL generator.

## Sources / References
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Asyncio](https://docs.python.org/3/library/asyncio.html)
- [Ollama Documentation](https://docs.ollama.com/)
- [LangGraph: Stateful Agentic RAG (2026)](https://medium.com/@vinodkrane/next-generation-agentic-rag-with-langgraph-2026-edition-d1c4c068d2b8)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
