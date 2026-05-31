# Data Copilot: Reference Implementation

## What it is

This reference implementation provides a Python-based skeleton for the layered Text-to-SQL pipeline. It demonstrates how to use Pydantic for structured data exchange between the different agent layers, where to insert human corrections, and how to keep model routing configurable for free/cheap-first deployments.

## What problem it solves

- **Complexity in Text-to-SQL**: Breaks down a complex single-shot prompt into manageable agentic layers.
- **Data Leakage and Token Bloat**: Uses Column Pruning to ensure only relevant schema context is sent to the final SQL generator.
- **Lack of Control**: Provides explicit "Human-in-the-Loop" (HITL) points to correct agent mistakes before execution.

## Where it fits in the stack

**Reference Implementation**. It serves as a blueprint for building data-focused agents within the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) and integrates with the [Model Routing Guide](../../knowledge_base/model_routing_guide.md).

## Typical use cases

- **Self-Service Analytics**: Allowing non-technical users to query business databases using natural language.
- **Automated Reporting**: Generating SQL queries for scheduled dashboards without manual coding.
- **Database Exploration**: Helping developers quickly understand a large or unfamiliar schema through natural language questions.

## Strengths

- **High Precision**: Layered approach reduces the chance of hallucinations compared to single-shot SQL generation.
- **Cost-Effective**: Can use smaller models for early layers (routing, pruning) and reserve high-power models for final generation.
- **Type-Safe**: Pydantic models provide strict validation for all inter-agent communication.

## Limitations

- **Latency**: Multiple agent calls increase the total time to generate a result.
- **Dependency**: Requires a well-documented schema (comments, types) for the pruning layer to work effectively.
- **Python-Centric**: This specific implementation is tied to the Python/Pydantic ecosystem.

## When to use it

- When building a **production-grade Text-to-SQL system** where accuracy and auditability are critical.
- If you have a **large database schema** that exceeds the context window of a single LLM prompt.
- When you need to **strictly control model costs** and routing.

## When not to use it

- For **simple, single-table databases** where a basic RAG or direct prompt would suffice.
- If **ultra-low latency** is the primary requirement (sub-second response).
- In **legacy environments** where Python is not an available runtime.

## Implementation Skeleton

The following script defines the interfaces for the Workspace Router, Intent Agent, Table Agent, Column Prune Agent, and SQL Generator.

```python
--8<-- "docs/reference-implementations/data-copilot/skeleton.py"
```

> **Note**: This implementation uses a mock execution pattern. In a production environment, you would replace the print statements with calls to your LLM provider (e.g., Ollama, Groq, or OpenAI).

## Key Features (May 2026 Update)

- **Asynchronous Execution**: Uses `asyncio` for non-blocking agent calls.
- **Type Safety**: Leverages Pydantic v2.10+ for high-performance validation across layers.
- **May 2026 Model Baseline**: Pre-configured with routes for **Gemini 3.5 Flash** (high-speed intent) and **Claude 4.7 Sonnet** (precise SQL generation).
- **Human correction points**: `review_table_selection()` and `review_pruned_schema()` show how a reviewer can correct wrong tables or wrong metric columns without restarting the whole pipeline.
- **Token controls**: `TokenStats` and `ModelRoute` capture estimated schema tokens, pruning ratios, prompt ceilings, and fallback routes.

## Related tools / concepts

- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — the broader framework this skeleton follows.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — for configuring the `ModelRoute` class.
- [Agentic RAG & Hybrid Retrieval](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — how this skeleton fits into broader diagnostic analytics.
- [SQLGlot Integration](../../tools/development_ops/sqlglot.md) — used for validating the generated SQL.
- [Ollama Service](../../services/ollama.md) — for local, free-tier execution of the routing layers.
- [Groq Provider](../../tools/providers/groq.md) — high-speed inference for the SQL generation layer.

## Sources / References
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Asyncio](https://docs.python.org/3/library/asyncio.html)
- [Gemini 3.5 Flash Benchmarks](https://blog.google/technology/ai/google-gemini-may-2026-update/)
- [Claude 4.7 Pricing and Capability Guide](https://docs.anthropic.com/en/docs/about-claude/models)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high
