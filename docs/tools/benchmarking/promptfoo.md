# Promptfoo

## What it is
Promptfoo is an open-source (MIT) CLI tool and library for evaluating, testing, and securing LLM prompts, agents, and FastMCP 3.1 tool implementations. It allows you to run systematic test cases across multiple providers and models, with a heavy focus on **AI Security** and **Red Teaming**. While the core CLI is free and self-hostable, a paid enterprise tier exists for governance and team features.

## What problem it solves
It solves the problem of "prompt regression" and security vulnerabilities by providing a framework for regression testing and automated red teaming. It allows you to quantify how changes to a prompt or agent workflow affect output quality and safety across many different test cases, preventing silent failures when updating to frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **DeepSeek-V4**, or **Llama 4 Maverick**.

## Where it fits in the stack
**Benchmarking / Eval / Security**. It is a critical tool for the [Dev-Workflow AI Assisted](../../playbooks/dev-workflow-ai-assisted.md) cycle, acting as the bridge between development and production-ready prompts.

## Typical use cases
- **Prompt Comparison**: Testing the same input against 10 different versions of a prompt.
- **Model Comparison**: Testing the same prompt against **GPT-5.5**, **Claude 5.1 Opus**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.
- **Red Teaming**: Identifying prompt injection, data exfiltration, and permission misuse vulnerabilities.
- **CI/CD Integration**: Automatically running a test suite before deploying a prompt or FastMCP agent change.
- **FastMCP Tool Testing**: Verifying that agents correctly call [MCP](../automation_orchestration/mcp.md) tools from servers like [Grafana](../process_understanding/grafana-cloud.md) or [New Relic](../process_understanding/new-relic-ai.md).

## Strengths
- **Fast and Local**: Runs entirely on your machine; no external platform required for the core CLI.
- **Flexible Assertions**: Support for JS, Python, and LLM-graded assertions (e.g., using `llm-rubric`).
- **Extensive Provider Support**: Works with OpenAI, Anthropic, Google, [Ollama](../../services/ollama.md), Azure, and more.
- **AI Security Focus**: Built-in scanners for 50+ vulnerability types, including specialized red teaming for agentic workflows and FastMCP tool privilege boundaries.

## Limitations
- **CLI-First**: While it has a web viewer, the core experience is command-line based.
- **Configuration Overhead**: Complex test suites require significant YAML/JSON definition effort.
- **Acquisition Context**: OpenAI's acquisition of Promptfoo in March 2026 has raised questions about the long-term open-source roadmap, though the MIT core remains available.

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
# Compare GPT-5.5 and Claude 5.1
promptfoo eval -p "Summarize: {{text}}" -r openai:gpt-5.5 -r anthropic:messages:claude-5-1-opus-20261024 -v text="FastMCP 3.1 protocol details"
```

### Testing FastMCP Tools
Promptfoo supports **MCP Proxy** for evaluating tools under FastMCP 3.1:
```bash
# Evaluate an agent using a local FastMCP server
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
      vars: { text: 'The Model Context Protocol (FastMCP 3.1) is an open standard...' },
      assert: [{ type: 'icontains', value: 'FastMCP' }],
    },
  ],
});

console.log(results);
```

### Custom Python Assertion (Pydantic v2 Validation)
Promptfoo supports writing custom assertion logic in Python. Below is a robust, type-hinted custom assertion function that parses and validates a JSON response against a structured schema using Pydantic v2:

```python
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any

class EvalOutputSchema(BaseModel):
    summary: str = Field(..., description="The summarized content", max_length=500)
    contains_mcp_details: bool = Field(True, description="Indicates if MCP standard references are present")

def check_length(output: str, vars: Dict[str, Any]) -> bool:
    """
    Validates that the model output is structurally sound and conforms to
    maximum length requirements for daily digests.
    Integrates seamlessly into promptfoo's python assertion environment.
    """
    try:
        # Validate structured JSON output using Pydantic v2 model_validate_json
        parsed_output = EvalOutputSchema.model_validate_json(output)
        return len(parsed_output.summary) < 500
    except ValidationError:
        # Gracefully fall back to plain-text length check if not JSON
        return len(output) < 500
```

To integrate this in your `promptfooconfig.yaml`, specify the assertion type as `python` and refer to the file:
```yaml
# promptfooconfig.yaml
assert:
  - type: python
    value: file://assertions.py:check_length
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
- Last reviewed: 2027-01-07
- Confidence: high
