# DeerFlow

## What it is
DeerFlow is an open-source agentic research workflow project from ByteDance focused on deep-research style information gathering and synthesis. In June 2026, it serves as a high-performance framework for building research agents optimized for **Claude 4.8 Opus** and **GPT-5.5**, utilizing advanced search and reasoning loops to produce comprehensive reports.

## What problem it solves
It gives teams a starting point for building structured research agents instead of stitching together ad hoc search, scraping, and report-generation scripts. It addresses the "last mile" problem of research by automating the evidence collection and synthesis process, ensuring that agents don't just find links but actually interpret and summarize technical data.

## Where it fits in the stack
**Agents / Research Workflow**. It sits between agent orchestration frameworks (like LangGraph) and end-user research products, providing a specialized layer for information retrieval and document generation.

## Typical use cases
- **Deep Research Assistants**: Gather and synthesize sources into multi-page whitepapers or technical briefs.
- **Strategy Research**: Compiling competitor, pricing, and tooling landscape reports before major business decisions.
- **Sales Enablement**: Researching target accounts, competitors, and public signals before high-value outreach.
- **Product Discovery**: Gathering feature, documentation, and ecosystem evidence before choosing new technology integrations.

## Strengths
- **Open-Source Reference**: High-quality starting point from ByteDance, allowing for deep customization.
- **Structured Synthesis**: Excellent at maintaining multi-step research loops and producing informed artifacts.
- **Model Agnostic**: Optimized for frontier models like Claude 4.8 Opus while remaining compatible with a wide range of providers.
- **Interoperability**: Seamlessly integrates with the **Model Context Protocol (MCP)** for extended tool use.

## Limitations
- **Adaptation Overhead**: Research-agent projects often need significant domain-specific adaptation before production use.
- **Quality Control**: Governance, caching, and citation quality still need to be designed around the core workflow for enterprise-grade outputs.
- **Infrastructure Intensive**: Running deep-research loops can be token and time intensive compared to simple RAG.

## When to use it
- When you want a reference implementation for research-heavy agents that need to produce structured documents.
- When browsing, multi-source synthesis, and report generation are the core user workflows.
- When the work looks like "collect evidence, synthesize it, and produce an informed artifact."
- When you need to pair deep research with long-term memory solutions like [mem0](mem0.md).

## When not to use it
- When a simpler search API (like [Tavily](../providers/tavily.md)) plus basic application logic is enough.
- When you need a stable SaaS product rather than an open-source framework you have to manage.
- For simple CRUD automations or fast, transactional "one-shot" workflows.

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
Access the DeerFlow UI at `http://localhost:2026` to start creating research tasks and managing sub-agents. Configuration is managed via `config.yaml`.

## CLI examples
```bash
# Initialize configuration and generate config.yaml
make config

# Start the application in development mode
make dev

# Run a specific research task via the CLI harness using Claude 4.8 Opus
python3 -m deerflow.harness run --task "competitor analysis for AI agents" --model claude-4-8-opus
```

## API examples
```python
import requests

# Example of submitting a research task to the DeerFlow API in June 2026
url = "http://localhost:2026/api/v1/tasks"
payload = {
    "title": "Agentic Framework Research",
    "prompt": "Analyze the top 5 open-source agent frameworks in 2026.",
    "model_config": {
        "model": "claude-4-8-opus-20260528",
        "max_tokens": 4096
    }
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
- [LangGraph](../frameworks/langgraph.md)
- [Aider](../development_ops/aider.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Stagehand](../automation_orchestration/stagehand.md)

## Sources / References
- [GitHub Repository](https://github.com/bytedance/deer-flow)
- [ByteDance DeerFlow 2.0 Guide (Apidog)](https://apidog.com/blog/deer-flow-guide-2026/)
- [ByteDance AI Research Blog](https://research.bytedance.com/blog)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
