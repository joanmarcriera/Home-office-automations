# DeerFlow

## What it is
DeerFlow is an open-source agentic research workflow project from ByteDance focused on deep-research style information gathering and synthesis. By July 2026, it is recognized as a leading reference architecture for building high-autonomy research agents that utilize frontier models like **Claude 4.8 Opus**, **GPT-5.5**, and **Gemma 3**.

## What problem it solves
It gives teams a structured, production-oriented starting point for building research agents instead of stitching together ad hoc search, scraping, and report-generation scripts. It addresses the complexity of multi-step browsing, information extraction, and the "hallucination-free" synthesis of large volumes of disparate data. It is particularly effective for automated benchmarking when combined with the **MCP 3.0 Task Protocol**.

## Where it fits in the stack
**Agents / Research Workflow**. It sits between agent orchestration frameworks (like [LangGraph](../frameworks/langgraph.md)) and end-user research products, providing a specialized layer for deep-search and synthesis loops. It leverages the **MCP 3.0** ecosystem for standardized tool use and data retrieval.

## Typical use cases
- **Strategic Intelligence**: Compiling competitor, pricing, and tooling landscape reports.
- **Scientific Research**: Gathering and summarizing academic papers and technical documentation.
- **Sales Enablement**: Researching target accounts and public signals before outreach.
- **Content Creation**: Building informed briefs and backgrounders for technical articles.
- **Automated Evaluation**: Running research-heavy benchmarks as part of the MCP 3.0 Task Protocol.

## Strengths
- **Reference Architecture**: Provides a clear, battle-tested pattern for research-heavy workflows.
- **Open-Source**: Highly adaptable and self-hostable, allowing for deep customization.
- **High Fidelity**: Optimized for producing cited, evidence-backed reports.
- **Multi-Model Support**: Native support for **Claude 4.8 Opus**, **GPT-5.5**, and **Gemma 3**.
- **Task Protocol Ready**: Aligned with MCP 3.0 for structured research execution.

## Limitations
- **Complexity**: Requires significant adaptation for domain-specific production use cases.
- **Resource Intensive**: Running deep-research loops can incur high token costs and require robust caching.
- **Evolving Ecosystem**: Rapid changes in search APIs and model capabilities require frequent maintenance of the core workflow scripts.

## When to use it
- When you want a reference implementation for research-heavy agents that require evidence collection and synthesis.
- When you are building a custom research assistant and need a head start on browsing and report generation logic.
- When you need a self-hostable alternative to proprietary "AI Search" products.
- For standardized research tasks that must comply with the MCP 3.0 Task Protocol.

## When not to use it
- For simple, single-step search tasks where a basic [Tavily](../providers/tavily.md) API call is sufficient.
- When you require a stable, managed SaaS product with zero maintenance overhead.
- For fast, transactional workflows that don't involve deep research or synthesis.

## Getting started

### Installation
The recommended way to start DeerFlow is via Docker to ensure all dependencies and execution environments are isolated:
```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make config
make docker-init
make docker-start
```

### Configuration
Update the generated `config.yaml` with your API keys for search providers and your preferred LLM (e.g., `claude-4-8-opus-20260528` or `gemma-3-27b`).

## CLI examples
```bash
# Initialize configuration and generate config.yaml
make config

# Start the application in development mode
make dev

# Run a specific research task via the CLI harness
python3 -m deerflow.harness run --task "competitor analysis for AI agents" --model "claude-4-8-opus"
```

## API examples
```python
import requests

# Example of submitting a research task to the DeerFlow API
url = "http://localhost:2026/api/v1/tasks"
payload = {
    "title": "Agentic Framework Research",
    "prompt": "Analyze the top 5 open-source agent frameworks in 2026.",
    "model_config": {
        "model": "claude-4-8-opus-20260528",
        "temperature": 0.0
    }
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Related tools / concepts
- [Tavily](../providers/tavily.md) - Primary search provider for research agents.
- [Browser Use](../automation_orchestration/browser-use.md) - For interactive browsing and GUI-based data collection.
- [mem0](mem0.md) - Longitudinal memory for persistent agent knowledge.
- [Symphony](symphony.md) - Enterprise framework for autonomous software factories.
- [LangGraph](../frameworks/langgraph.md) - Orchestration for complex, cyclic agent workflows.
- [Aider](../development_ops/aider.md) - Git-native coding assistant with MCP integration.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) - The standard for connecting agents to tools and data.
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)
- [Perplexity Agent API](perplexity-agent-api.md)

## Sources / References
- [GitHub Repository](https://github.com/bytedance/deer-flow)
- [ByteDance DeerFlow 2.0 Guide (Apidog)](https://apidog.com/blog/deer-flow-guide-2026/)
- [Anthropic: Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
