# Claude Code Router

## What it is
Claude Code Router (CCR) is a proxy and routing layer for the [Claude Code](./claude-code.md) CLI. It intercepts API requests from Claude Code and redirects them to various LLM providers (OpenRouter, DeepSeek, Gemini, Ollama, etc.) based on user-defined rules.

## What problem it solves
- **Cost Optimization**: Redirects expensive Claude 3.5 Sonnet requests to cheaper alternatives like DeepSeek-V3 or local models for background tasks.
- **Regional Access**: Enables users in regions where Anthropic is restricted to use Claude Code by proxying through other providers.
- **Model Flexibility**: Allows mixing and matching models for different tasks (e.g., reasoning vs. coding) within the same Claude Code session.
- **Compatibility Smoothing**: Uses a "Transformer" system to fix subtle differences between provider APIs (e.g., forcing tool usage or reasoning tags).

## Where it fits in the stack
**Category**: Router / Tool

## Typical use cases
- **DeepSeek Integration**: Using `DeepSeek-V3` for coding and `DeepSeek-R1` for "Plan Mode" at a fraction of the cost of Claude 3.5.
- **Local Dev Loop**: Routing background tasks to a local Ollama instance (e.g., `qwen2.5-coder`) to save tokens.
- **Enterprise Proxying**: Centralizing API key management and logging for teams using Claude Code.

## Strengths
- **Dynamic Switching**: Change models on-the-fly using the `/model` command within Claude Code.
- **Transformer System**: Built-in logic to enhance tool usage for models that struggle with instruction following (like DeepSeek).
- **Ease of Use**: Includes a web UI (`ccr ui`) and an interactive CLI (`ccr model`) for configuration.
- **GitHub Actions Support**: Built-in `NON_INTERACTIVE_MODE` for CI/CD workflows.

## Limitations
- **Latency**: Adding a proxy layer introduces minor network overhead.
- **Complexity**: Requires managing a configuration file and a local service.
- **Instruction Adherence**: While transformers help, non-Claude models may still struggle with Claude Code's complex multi-step prompts.

## When to use it
- Use when you want to use Claude Code with cheaper models (e.g., DeepSeek) to save costs.
- Use if you are in a region where direct access to Anthropic's API is restricted.
- Use when you need to route different types of tasks (background vs. planning) to different LLM providers.

## When not to use it
- Not necessary if you have a Claude Code Max plan and don't mind the cost.
- Not for users who prefer a zero-configuration setup, as it requires managing a proxy service.

## Getting started

### Installation
```bash
# Ensure Claude Code is installed
npm install -g @anthropic-ai/claude-code

# Install Claude Code Router
npm install -g @musistudio/claude-code-router
```

### Basic Configuration
Start the service to generate the default config at `~/.claude-code-router/config.json`:
```bash
ccr start
```

### Usage
To run Claude Code through the router:
```bash
ccr code
```
Alternatively, use `eval "$(ccr activate)"` to set environment variables globally in your shell session, allowing you to use the standard `claude` command.

## Usage Examples and Ideas
- **Custom Routing Scripts**: Use a `custom-router.js` to route specific queries (e.g., "explain this code") to specialized models.
- **Subagent Routing**: Use `<CCR-SUBAGENT-MODEL>` tags in prompts to force specific sub-tasks to certain models.
- **Preset Management**: Export and share configurations using `ccr preset export`.

## Known Issues and Workarounds
- **DeepSeek Tool Usage**: DeepSeek sometimes stops using tools in long conversations.
  - **Workaround**: Use the `tooluse` transformer, which injects a system reminder and sets `tool_choice: "required"`.
- **GLM Reasoning**: GLM models often fail to think because of Claude Code's heavy system prompt.
  - **Workaround**: Use a custom transformer to inject expert reasoning instructions and force `<reasoning_content>` tags.
- **Gemini Compatibility**: Gemini's tool calls lack IDs and have specific type restrictions.
  - **Workaround**: Use the built-in `gemini` transformer to normalize requests.

## Roadmap
The project maintains an active list of features and bug fixes on GitHub:
- [GitHub Issues](https://github.com/musistudio/claude-code-router/issues)
- [GitHub Discussions](https://github.com/musistudio/claude-code-router/discussions)

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (but you pay for the underlying LLM providers)
- **Self-hostable**: Yes

## Related tools / concepts
- [Claude Code](./claude-code.md)
- [Aider](./aider.md)
- [LiteLLM](../../services/litellm.md)
- [Model Context Protocol (MCP)](../../knowledge_base/agent_protocols.md)

## Sources / References
- [Official GitHub](https://github.com/musistudio/claude-code-router)
- [Project Motivation Blog Post](https://github.com/musistudio/claude-code-router/blob/main/blog/en/project-motivation-and-how-it-works.md)
- [Transformers & Tool Usage Blog Post](https://github.com/musistudio/claude-code-router/blob/main/blog/en/maybe-we-can-do-more-with-the-route.md)

## Contribution Metadata
- Last reviewed: 2026-03-02
- Confidence: high
