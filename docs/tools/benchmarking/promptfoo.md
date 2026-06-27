# Promptfoo

## What it is
Promptfoo is an open-source (MIT) CLI tool and library for evaluating, testing, and securing LLM prompts and models. It allows you to run systematic test cases across multiple providers and models, with a heavy focus on **AI Security** and **Red Teaming**. While the core CLI is free and self-hostable, a paid enterprise tier exists for governance and team features.

## What problem it solves
It solves the problem of "prompt regression" and security vulnerabilities by providing a framework for regression testing and automated red teaming. It allows you to quantify how changes to a prompt affect output quality and safety across many different test cases, preventing silent failures when updating to models like **Claude 4.8** or **GPT-5.5**.

## Where it fits in the stack
**Benchmarking / Eval / Security**. It is a critical tool for the [Dev-Workflow AI Assisted](../../playbooks/dev-workflow-ai-assisted.md) cycle, acting as the bridge between development and production-ready prompts.

## Typical use cases
- **Prompt Comparison**: Testing the same input against 10 different versions of a prompt.
- **Model Comparison**: Testing the same prompt against **GPT-5.5**, **Claude 4.8 Opus**, and **Llama 4 Maverick**.
- **Red Teaming**: Identifying prompt injection, data exfiltration, and permission misuse vulnerabilities.
- **CI/CD Integration**: Automatically running a test suite before deploying a prompt change.
- **MCP Tool Testing**: Verifying that agents correctly call [MCP](../automation_orchestration/mcp.md) tools from servers like [Grafana](../process_understanding/grafana-cloud.md) or [New Relic](../process_understanding/new-relic-ai.md).

## Strengths
- **Fast and Local**: Runs entirely on your machine; no external platform required for the core CLI.
- **Flexible Assertions**: Support for JS, Python, and LLM-graded assertions (e.g., using `llm-rubric`).
- **Extensive Provider Support**: Works with OpenAI, Anthropic, [Ollama](../../services/ollama.md), Azure, and more.
- **AI Security Focus**: Built-in scanners for 50+ vulnerability types, including specialized red teaming for agentic workflows.

## Limitations
- **CLI-First**: While it has a web viewer, the core experience is command-line based.
- **Configuration Overhead**: Complex test suites require significant YAML/JSON definition effort.
- **Acquisition Uncertainty**: OpenAI's acquisition of Promptfoo in March 2026 has raised questions about the long-term open-source roadmap, though the MIT core remains available.

## When to use it
- To systematically improve the reliability and safety of your LLM prompts.
- To prevent regressions when updating models or prompts in an automation workflow.
- To perform automated security audits of AI agents before production deployment.

## When not to use it
- For one-off, casual chats with an LLM.
- If you require a purely visual, no-code evaluation environment.

## Getting started

### Installation
```bash
npm install -g promptfoo
```

### Initialization
```bash
# Initialize a new project
promptfoo init
```

### Basic Evaluation
1. Define your prompts and tests in `promptfooconfig.yaml`.
2. Run the eval:
```bash
promptfoo eval
```

## CLI examples

### Running Red Teaming Scans
```bash
# Run a red team evaluation against a specific target
promptfoo redteam run --config redteam.yaml
```

### Comparing Models Side-by-Side
```bash
# Compare GPT-5.5 and Claude 4.8
promptfoo eval -p "Summarize: {{text}}" -r openai:gpt-5.5 -r anthropic:messages:claude-4-8-opus-20260528 -v text="MCP 3.0 protocol details"
```

### Testing MCP Tools
Promptfoo supports **MCP Proxy** for evaluating tools:
```bash
# Evaluate an agent using a local MCP server
promptfoo eval --mcp-server http://localhost:8000/mcp
```

## API examples

### Programmatic Evaluation (TypeScript)
```typescript
import promptfoo from 'promptfoo';

const results = await promptfoo.evaluate({
  prompts: ['Summarize this: {{text}}'],
  providers: ['openai:gpt-5.5'],
  tests: [
    {
      vars: { text: 'The Model Context Protocol (MCP) is an open standard...' },
      assert: [{ type: 'icontains', value: 'MCP' }],
    },
  ],
});

console.log(results);
```

### Custom Python Assertion
```python
def check_length(output, vars):
    # Ensure the output is concise for daily digests
    return len(output) < 500

# Used in promptfooconfig.yaml as:
# assert:
#   - type: python
#     value: file://assertions.py:check_length
```

## Related tools / concepts
- [LangSmith](langsmith.md) — Enterprise observability and evaluation.
- [AgentOps](../process_understanding/agentops.md) — Session replays and execution graphs for agents.
- [Ragas](../process_understanding/ragas.md) — Evaluation framework for RAG pipelines.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for extending agent capabilities.
- [Ollama](../../services/ollama.md) — Local inference engine for evaluation.
- [Claude](../ai_knowledge/claude.md) — Frontier model frequently used as a judge.
- [Grok-3](../ai_knowledge/grok.md) — Real-time data search for evaluation context.
- [Dev-Workflow AI Assisted](../../playbooks/dev-workflow-ai-assisted.md) — Playbook for using evals in development.

## Sources / References
- [Promptfoo Official Website](https://www.promptfoo.dev/)
- [Promptfoo GitHub Repository](https://github.com/promptfoo/promptfoo)
- [AI Security & Red Teaming with Promptfoo](https://www.promptfoo.dev/docs/red-team/)
- [OpenAI Acquisition Announcement (March 2026)](https://www.openai.com/blog/openai-acquires-promptfoo/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
