# DeerFlow

## What it is
DeerFlow is an open-source agentic research workflow project from ByteDance focused on deep-research style information gathering and synthesis.

## What problem it solves
It gives teams a starting point for building structured research agents instead of stitching together ad hoc search, scraping, and report-generation scripts.

## Where it fits in the stack
**Agents / Research Workflow**. It sits between agent orchestration frameworks and end-user research products.

## Typical use cases
- Deep research assistants that gather and synthesize sources
- Multi-step browsing and summarization workflows
- Internal research copilots that need repeatable task structure

## Strengths
- Open-source starting point from a large AI lab
- Clear fit for research-oriented agent workflows
- Useful reference architecture even if not adopted directly

## Limitations
- Research-agent projects often need significant adaptation before production use
- Governance, caching, and citation quality still need to be designed around the core workflow

## When to use it
- When you want a reference implementation for research-heavy agents
- When browsing, synthesis, and report generation are the core user workflow

## When not to use it
- When a simpler search API plus application logic is enough
- When you need a stable SaaS product rather than an open-source starting point

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free to inspect and adapt; runtime costs depend on models and infrastructure
- **Self-hostable**: Yes

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Symphony](symphony.md)

## Sources / References
- [GitHub Repository](https://github.com/bytedance/deer-flow)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
