# LangSmith

## What it is
LangSmith is a unified platform for debugging, testing, evaluating, and monitoring LLM applications. It is part of the LangChain ecosystem but can be used with any LLM framework.

## What problem it solves
It addresses the "black box" nature of LLMs by providing full visibility into the execution traces of complex chains and agents. It also provides tools for creating evaluation datasets, running automated tests, and monitoring production performance.

## Where it fits in the stack
Benchmarking / Observability

## Typical use cases
- Debugging complex agentic workflows by inspecting intermediate steps and tool calls.
- Creating "golden" datasets for regression testing.
- Monitoring production applications for cost, latency, and quality.
- Collaborative prompt engineering and testing.

## Strengths
- Deep integration with LangChain and LangGraph.
- Powerful trace visualization and filtering.
- Supports manual and automated evaluation.
- Hub for sharing and versioning prompts.

## Limitations
- Proprietary SaaS (though self-hosting is available for enterprise).
- Can add latency if not configured correctly (though usually negligible).
- Learning curve for advanced evaluation features.

## When to use it
- When building complex LLM applications that require tracing for debugging.
- When transitioning from prototype to production and needing reliability metrics.
- When collaborating with a team on prompt engineering.

## When not to use it
- For very simple, single-call LLM scripts where a full observability platform is overkill.
- If strict data privacy requirements forbid sending traces to a third-party SaaS (and enterprise self-hosting is not feasible).

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Free tier available, paid tiers for higher volume/enterprise)
- **Self-hostable**: Yes (Enterprise only)

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [LangGraph](../agents/langgraph.md)
- [Benchmarking](./index.md)

## Sources / References
- [Official Website](https://www.langchain.com/langsmith)
- [Docs](https://docs.smith.langchain.com/)

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
