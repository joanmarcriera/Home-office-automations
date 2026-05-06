# Data Copilot: Reference Implementation

This reference implementation provides a Python-based skeleton for the layered Text-to-SQL pipeline. It demonstrates how to use Pydantic for structured data exchange between the different agent layers, where to insert human corrections, and how to keep model routing configurable for free/cheap-first deployments.

## Implementation Skeleton

The following script defines the interfaces for the Workspace Router, Intent Agent, Table Agent, Column Prune Agent, and SQL Generator.

```python
--8<-- "docs/reference-implementations/data-copilot/skeleton.py"
```

> **Note**: This implementation uses a mock execution pattern. In a production environment, you would replace the print statements with calls to your LLM provider (e.g., Ollama, Groq, or OpenAI).

## Key Features

- **Asynchronous Execution**: Uses `asyncio` for non-blocking agent calls.
- **Type Safety**: Leverages Pydantic models to ensure consistent data structures across layers.
- **Modularity**: Each layer is a distinct method, allowing for independent model routing (e.g., using a local small model for routing and a hosted mini/Haiku-class model for SQL generation).
- **Human correction points**: `review_table_selection()` and `review_pruned_schema()` show how a reviewer can correct wrong tables or wrong metric columns without restarting the whole pipeline.
- **Token controls**: `TokenStats` and `ModelRoute` capture estimated schema tokens, pruning ratios, prompt ceilings, and fallback routes.

## Sources / References
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Asyncio](https://docs.python.org/3/library/asyncio.html)
- [Ollama documentation](https://docs.ollama.com/)
- [OpenAI API pricing](https://openai.com/api/pricing)
- [Claude pricing documentation](https://docs.claude.com/en/docs/about-claude/pricing)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
