# Claude Code Router

## What it is
Claude Code Router (CCR) is an intelligent proxy and routing layer for the [Claude Code](./claude-code.md) CLI. It intercepts API requests from Claude Code and redirects them to various LLM providers (OpenRouter, DeepSeek, Gemini, Ollama, etc.) based on user-defined rules. As of June 2026, it is the standard for benchmarking `claude-4-8-opus-20260528` against GPT-5.5 and Llama 4 Maverick within agentic workflows.

## What problem it solves
- **Cost Optimization**: Redirects expensive Claude 4.8 Sonnet/Opus requests to cheaper alternatives like DeepSeek-V4 or local models for routine background tasks.
- **Regional Access**: Enables users in regions where Anthropic is restricted to use Claude Code by proxying through other providers.
- **Model Flexibility**: Allows mixing and matching models for different tasks (e.g., reasoning vs. coding) within the same Claude Code session.
- **Compatibility Smoothing**: Uses a "Transformer" system to fix subtle differences between provider APIs (e.g., forcing tool usage or reasoning tags).

## Where it fits in the stack
**Router / Gateway**. It sits between the agent ([Claude Code](./claude-code.md)) and the inference provider, acting as a programmable middleware for multi-model orchestration.

## Typical use cases
- **DeepSeek Integration**: Using `DeepSeek-V4` for coding and `DeepSeek-R1` for "Plan Mode" at a fraction of the cost of Claude 4.8.
- **Local Dev Loop**: Routing background tasks to a local [Ollama instance](../../services/ollama.md) (e.g., `qwen2.5-coder`) to save tokens and maintain privacy.
- **Enterprise Proxying**: Centralizing API key management and logging for teams using Claude Code via [OpenRouter](../ai_knowledge/openrouter.md).
- **Benchmark Execution**: Systematically routing identical tasks to different models to evaluate performance parity in real-time.

## Strengths
- **Dynamic Switching**: Change models on-the-fly using the `/model` command within Claude Code or via the CCR CLI.
- **Transformer System**: Built-in logic to enhance tool usage for models that struggle with complex instruction following.
- **Ease of Use**: Includes a web UI (`ccr ui`) and an interactive CLI (`ccr model`) for configuration.
- **GitHub Actions Support**: Built-in `NON_INTERACTIVE_MODE` for CI/CD workflows and automated repository maintenance.
- **MCP 3.0 Support**: Native discovery and routing for [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) tools.

## Limitations
- **Latency**: Adding a proxy layer introduces minor network overhead (typically <50ms).
- **Complexity**: Requires managing a configuration file and running a local service process.
- **Instruction Adherence**: While transformers help, non-Claude models may still struggle with Claude Code's complex multi-step prompts compared to native Anthropic performance.

## When to use it
- Use when you want to use Claude Code with cheaper models (e.g., DeepSeek) to save costs during development.
- Use if you are in a region where direct access to Anthropic's API is restricted.
- Use when you need to route different types of tasks (background vs. planning) to different LLM providers like GPT-5.5.

## When not to use it
- Not necessary if you have a Claude Code Max plan and don't mind the cost.
- Not for users who prefer a zero-configuration setup, as it requires managing a proxy service.
- When absolute minimal latency is required for real-time interactive pair programming.

## Getting started
### 1. Installation
Ensure Claude Code is installed:
```bash
npm install -g @anthropic-ai/claude-code
```

Install Claude Code Router:
```bash
npm install -g @musistudio/claude-code-router
```

### 2. Initialization
Start the service and configure your first provider:
```bash
ccr start
```

### 3. Usage
Launch Claude Code through the router:
```bash
ccr code
```

## CLI examples
```bash
# Set the active model for the router
ccr model deepseek/deepseek-chat

# Launch Claude Code through the router with a specific profile
ccr code --profile research

# Open the web-based configuration UI
ccr ui

# List all supported models and their transformer status
ccr list --transformers
```

## API examples

### Advanced Routing Patterns (YAML)
CCR supports advanced routing rules defined in `rules.yaml` that can trigger based on query intent or tool-use requirements.

```yaml
rules:
  - name: "heavy-coding"
    if: "query.matches(/refactor|implement/)"
    then: "deepseek/deepseek-chat"
    transformer: "deepseek_v3_coding"
  - name: "mcp-routing"
    if: "tools.include('brave_search')"
    then: "google/gemini-2.0-flash-exp"
```

### Fallback and Retry Strategies
Configure automatic fallback to a frontier model like `claude-4-8-opus-20260528` if the cheaper model fails:

```json
{
  "fallback_policy": {
    "enabled": true,
    "strategy": "ordered",
    "targets": ["deepseek/deepseek-chat", "anthropic/claude-4-8-opus-20260528"],
    "retry_on": [429, 503]
  }
}
```

### Troubleshooting: Fixing Tool Usage
If a model fails to call tools, enable the `tooluse` transformer:
```json
{
  "models": {
    "deepseek/deepseek-chat": {
      "transformers": ["tooluse", "inject_reasoning_reminder"]
    }
  }
}
```

## Related tools / concepts
- [Claude Code](./claude-code.md)
- [Aider](./aider.md)
- [LiteLLM](../../services/litellm.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Ollama](../../services/ollama.md)
- [Fallback Patterns](../../knowledge_base/patterns/fallback-patterns.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Official GitHub](https://github.com/musistudio/claude-code-router)
- [Project Motivation Blog Post](https://github.com/musistudio/claude-code-router/blob/main/blog/en/project-motivation-and-how-it-works.md)
- [Transformers & Tool Usage Blog Post](https://github.com/musistudio/claude-code-router/blob/main/blog/en/maybe-we-can-do-more-with-the-route.md)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high
