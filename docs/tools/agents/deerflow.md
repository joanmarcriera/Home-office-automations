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

## Example company use cases
- **Strategy research**: compile competitor, pricing, and tooling landscape reports before major decisions.
- **Sales enablement**: research target accounts, competitors, and public signals before outreach.
- **Product discovery**: gather feature, documentation, and ecosystem evidence before choosing integrations.

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

## Selection comments
- DeerFlow is strongest when the work looks like "collect evidence, synthesize it, and produce an informed artifact."
- It is not the default choice for simple CRUD automations or fast transactional workflows.
- Pair it with [Tavily](../providers/tavily.md) for search, [mem0](mem0.md) for longitudinal memory, and [Browser Use](../automation_orchestration/browser-use.md) for interactive browsing gaps.

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free to inspect and adapt; runtime costs depend on models and infrastructure
- **Self-hostable**: Yes

## Getting started

### Installation
The recommended way to start DeerFlow is via Docker:
```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make config
make docker-init
make docker-start
```

### Usage
Access the DeerFlow UI at `http://localhost:2026` to start creating research tasks and managing sub-agents.

## CLI examples
```bash
# Initialize configuration and generate config.yaml
make config

# Start the application in development mode
make dev

# Run a specific research task via the CLI harness
python3 -m deerflow.harness run --task "competitor analysis for AI agents"
```

## API examples
```python
import requests

# Example of submitting a research task to the DeerFlow API
url = "http://localhost:2026/api/v1/tasks"
payload = {
    "title": "Agentic Framework Research",
    "prompt": "Analyze the top 5 open-source agent frameworks in 2026.",
    "model_config": {"model": "gpt-5-responses"}
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [mem0](mem0.md)
- [Symphony](symphony.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [GitHub Repository](https://github.com/bytedance/deer-flow)
- [ByteDance DeerFlow 2.0 Guide (Apidog)](https://apidog.com/blog/deer-flow-guide-2026/)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high
