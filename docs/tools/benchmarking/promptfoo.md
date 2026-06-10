# Promptfoo

## What it is
Promptfoo is an open-source CLI tool and library for evaluating, testing, and securing LLM prompts and models. It allows you to run systematic test cases across multiple providers and models, with a heavy focus on **AI Security** and **Red Teaming**.

## What problem it solves
It solves the problem of "prompt regression" and security vulnerabilities by providing a framework for regression testing and automated red teaming. It allows you to quantify how changes to a prompt affect output quality and safety across many different test cases.

## Where it fits in the stack
**Benchmarking / Eval / Security**. It is a critical tool for the [Dev-Workflow AI Assisted](../../playbooks/dev-workflow-ai-assisted.md) cycle.

## Typical use cases
- **Prompt Comparison**: Testing the same input against 10 different versions of a prompt.
- **Model Comparison**: Testing the same prompt against **GPT-5.5**, **Claude 4.7**, and **Llama 4 Maverick**.
- **Red Teaming**: Identifying prompt injection, data exfiltration, and permission misuse vulnerabilities.
- **CI/CD Integration**: Automatically running a test suite before deploying a prompt change.

## Strengths
- **Fast and Local**: Runs entirely on your machine; no external platform required for the core CLI.
- **Flexible Assertions**: Support for JS, Python, and LLM-graded assertions (e.g., using `llm-rubric`).
- **Extensive Provider Support**: Works with OpenAI, Anthropic, [Ollama](../../services/ollama.md), Azure, and more.
- **AI Security Focus**: Built-in scanners for 50+ vulnerability types.

## Limitations
- **CLI-First**: While it has a web viewer, the core experience is command-line based.
- **Configuration Overhead**: Complex test suites require significant YAML/JSON definition effort.
- **Acquisition Uncertainty**: OpenAI's acquisition of Promptfoo in March 2026 has raised questions about the long-term open-source roadmap.

## When to use it
- To systematically improve the reliability and safety of your LLM prompts.
- To prevent regressions when updating models or prompts in an automation workflow.
- To perform automated security audits of AI agents before production deployment.

## When not to use it
- For one-off, casual chats with an LLM.
- If you require a purely visual, no-code evaluation environment.

## Licensing and cost
- **Open Source**: Yes (MIT).
- **Cost**: Free (Core CLI); Paid enterprise tier for governance and team features.
- **Self-hostable**: Yes.

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
# Compare GPT-5.5 and Claude 4.7
promptfoo eval -p "Summarize: {{text}}" -r openai:gpt-5.5 -r anthropic:messages:claude-4-7 -v text="MCP protocol details"
```

### Exporting Results
```bash
# Export evaluation results to a CSV file
promptfoo eval --output results.csv
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
    # Standardize variable naming: API_URL, API_TOKEN
    return len(output) < 500

# Used in promptfooconfig.yaml as:
# assert:
#   - type: python
#     value: file://assertions.py:check_length
```

## Model Context Protocol (MCP) Support
Promptfoo supports **MCP Proxy** and **Bedrock Converse MCP**, allowing you to evaluate tools and agents that use the [Model Context Protocol](../automation_orchestration/mcp.md).

### Testing MCP Tools
You can use Promptfoo to verify that an agent correctly calls MCP tools (like those provided by the [Grafana](../process_understanding/grafana-cloud.md) or [New Relic](../process_understanding/new-relic-ai.md) MCP servers) when given specific prompts.

## Related tools / concepts
- [LangSmith](langsmith.md)
- [AgentOps](../process_understanding/agentops.md)
- [Ragas](../process_understanding/ragas.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Ollama](../../services/ollama.md)
- [Claude](../ai_knowledge/claude.md)

## Sources / References
- [Promptfoo Official Website](https://www.promptfoo.dev/)
- [Promptfoo GitHub Repository](https://github.com/promptfoo/promptfoo)
- [AI Security & Red Teaming with Promptfoo](https://www.promptfoo.dev/docs/red-team/)
- [OpenAI Acquisition Announcement (March 2026)](https://www.openai.com/blog/openai-acquires-promptfoo/)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
