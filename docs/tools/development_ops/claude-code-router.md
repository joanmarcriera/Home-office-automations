# Claude Code Router

## What it is
Claude Code Router (CCR) is a proxy and routing layer for the [Claude Code](./claude-code.md) CLI. It intercepts API requests from Claude Code and redirects them to various LLM providers (OpenRouter, DeepSeek, Gemini, Ollama, etc.) based on user-defined rules. As of late October / November 2026, it is the standard for benchmarking `claude-5-1-20261101` against GPT-5.5 and DeepSeek-V4, providing a unified interface for model-agnostic agentic workflows.

## What problem it solves
- **Cost Optimization**: Redirects expensive Claude 3.5/5.1 Sonnet requests to cheaper alternatives like DeepSeek-V4 or local models for background tasks.
- **Regional Access**: Enables users in regions where Anthropic is restricted to use Claude Code by proxying through other providers.
- **Model Flexibility**: Allows mixing and matching models for different tasks (e.g., reasoning vs. coding) within the same Claude Code session.
- **Compatibility Smoothing**: Uses a "Transformer" system to fix subtle differences between provider APIs (e.g., forcing tool usage or reasoning tags).
- **Latency Management**: Implements smart routing based on provider health and response times in crowded late 2026 inference markets.

## Where it fits in the stack
**Router / Gateway**. It sits between the agent (Claude Code) and the inference provider, acting as a programmable middleware. It is often used alongside [LiteLLM](../../services/litellm.md) for enterprise-grade load balancing.

## Typical use cases
- **DeepSeek Integration**: Using `DeepSeek-V4` for coding and reasoning tasks at a fraction of the cost of Claude 5.1.
- **Local Dev Loop**: Routing background tasks to a local [Ollama instance](../../services/ollama.md) (e.g., `qwen3.6-coder`) to save tokens.
- **Enterprise Proxying**: Centralizing API key management and logging for teams using Claude Code via [OpenRouter](../ai_knowledge/openrouter.md).
- **Automated Benchmarking**: Running identical coding tasks across Claude 5.1, GPT-5.5, and Gemini 4.0 to evaluate performance regressions.

## Strengths
- **Dynamic Switching**: Change models on-the-fly using the `/model` command within Claude Code.
- **Transformer System**: Built-in logic to enhance tool usage for models that struggle with instruction following (like DeepSeek).
- **Ease of Use**: Includes a web UI (`ccr ui`) and an interactive CLI (`ccr model`) for configuration.
- **GitHub Actions Support**: Built-in `NON_INTERACTIVE_MODE` for CI/CD workflows.
- **MCP 3.1 Discovery**: Integrated discovery of [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) tools and routing patterns using the MCP 3.1 Task Protocol.

## Limitations
- **Latency**: Adding a proxy layer introduces minor network overhead (typically <50ms).
- **Complexity**: Requires managing a configuration file and a local service.
- **Instruction Adherence**: While transformers help, non-Claude models may still struggle with Claude Code's complex multi-step prompts compared to native `claude-5-1-20261101` performance.

## When to use it
- Use when you want to use Claude Code with cheaper models (e.g., DeepSeek) to save costs.
- Use if you are in a region where direct access to Anthropic's API is restricted.
- Use when you need to route different types of tasks (background vs. planning) to different LLM providers like GPT-5.5.
- Use for multi-model developer environments where different features (like reasoning vs. speed) are required for different sub-tasks.

## When not to use it
- Not necessary if you have a Claude Code Max plan and don't mind the cost.
- Not for users who prefer a zero-configuration setup, as it requires managing a proxy service.
- When working in highly air-gapped environments where external proxies are prohibited.

## Getting started
Ensure Claude Code is installed:
```bash
npm install -g @anthropic-ai/claude-code
```

Install Claude Code Router:
```bash
npm install -g @musistudio/claude-code-router
```

Start the service:
```bash
ccr start
```

Configure your first model:
```bash
ccr model openrouter/anthropic/claude-5-1
```

## CLI examples
```bash
# Set the active model for the router
ccr model deepseek/deepseek-chat

# Launch Claude Code through the router
ccr code

# Open the web-based configuration UI
ccr ui

# Check provider health and latency
ccr health
```

## API examples

### Advanced Routing Patterns (YAML)
CCR supports advanced routing rules defined in `rules.yaml` that can trigger based on query intent or tool-use requirements.

```yaml
rules:
  - name: "heavy-coding"
    if: "query.matches(/refactor|implement/)"
    then: "deepseek/deepseek-chat"
    transformer: "deepseek_v4_coding"
  - name: "mcp-routing"
    if: "tools.include('brave_search')"
    then: "google/gemini-4.0-flash"
```

### Python Routing Rules and Fallback Validation with Pydantic v2
This Python snippet validates the router configurations, routing rules, and fallback structures using **Pydantic v2**.

```python
import json
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class FallbackPolicy(BaseModel):
    enabled: bool = Field(default=True, description="Enable automated failover to alternate model targets")
    strategy: str = Field(default="ordered", description="Failover strategy algorithm")
    targets: List[str] = Field(description="Priority list of model target routes")
    retry_on: List[int] = Field(
        default_factory=lambda: [429, 503],
        validation_alias="retry_on",
        description="HTTP status codes triggering fallback"
    )

class TransformerConfig(BaseModel):
    transformers: List[str] = Field(default_factory=list, description="List of active API transformer middleware plugins")

class RouterRules(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(description="Unique identifier rule name")
    condition: str = Field(validation_alias="if", description="Matching condition evaluated against query context or tool use")
    target: str = Field(validation_alias="then", description="Primary model route target")
    transformer: Optional[str] = Field(None, description="Optional payload transformer identifier")

class CCRConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    fallback_policy: FallbackPolicy = Field(validation_alias="fallback_policy")
    models: Dict[str, TransformerConfig] = Field(default_factory=dict)
    rules: List[RouterRules] = Field(default_factory=list)

# Demonstration of parsing and validating configs
def validate_ccr_config(raw_json: str) -> Optional[CCRConfig]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2
        config = CCRConfig.model_validate(data)
        return config
    except json.JSONDecodeError:
        print("Invalid JSON.")
    except ValidationError as e:
        print(f"CCR Configuration Validation failed: {e.errors()}")
    return None

# Example CCR config data:
# sample_config = """
# {
#   "fallback_policy": {
#     "enabled": true,
#     "strategy": "ordered",
#     "targets": ["deepseek/deepseek-chat", "anthropic/claude-5-1-20261101"],
#     "retry_on": [429, 503]
#   },
#   "models": {
#     "deepseek/deepseek-chat": {
#       "transformers": ["tooluse", "inject_reasoning_reminder"]
#     }
#   },
#   "rules": [
#     {
#       "name": "heavy-coding",
#       "if": "query.matches(/refactor/)",
#       "then": "deepseek/deepseek-chat"
#     }
#   ]
# }
# """
# config_obj = validate_ccr_config(sample_config)
```

## Related tools / concepts
- [Claude Code](./claude-code.md)
- [Aider](./aider.md)
- [LiteLLM](../../services/litellm.md)
- [MCP](../automation_orchestration/mcp.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Ollama](../../services/ollama.md)
- [DeepSeek](../providers/deepseek.md)
- [Fallback Patterns](../../knowledge_base/patterns/fallback-patterns.md)

## Sources / references
- [Official GitHub](https://github.com/musistudio/claude-code-router)
- [Project Motivation Blog Post](https://github.com/musistudio/claude-code-router/blob/main/blog/en/project-motivation-and-how-it-works.md)
- [Transformers & Tool Usage Blog Post](https://github.com/musistudio/claude-code-router/blob/main/blog/en/maybe-we-can-do-more-with-the-route.md)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
