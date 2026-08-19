# Claude Code Router

## What it is
Claude Code Router (CCR) is a proxy and routing layer for the [Claude Code](./claude-code.md) CLI. It intercepts API requests from Claude Code and redirects them to various LLM providers (OpenRouter, DeepSeek, Gemini, Ollama, etc.) based on user-defined rules. As of early 2027, it is the standard for benchmarking frontier models such as `claude-5-1` against GPT-5.5, Gemini 4.0 Pro/Flash, and DeepSeek-V4, providing a unified interface for model-agnostic agentic workflows and FastMCP 3.1 tooling integrations.

## What problem it solves
- **Cost Optimization**: Redirects expensive Claude 5.1 Sonnet/Opus requests to cheaper alternatives like DeepSeek-V4 or local models for routine background tasks.
- **Regional Access**: Enables users in regions where Anthropic API endpoints are restricted to use Claude Code by proxying through other supported providers.
- **Model Flexibility**: Allows mixing and matching models for different task domains (e.g., formal mathematical reasoning vs. high-speed boilerplate generation) within the same active Claude Code session.
- **Compatibility Smoothing**: Uses a "Transformer" system to bridge structural differences between provider APIs (e.g., enforcing tool parameter validation or normalizing reasoning tags).
- **Latency & Reliability Management**: Implements smart routing based on real-time provider health checks and response latency in dynamic inference markets.

## Where it fits in the stack
**Router / Gateway**. It sits between the agent ([Claude Code](./claude-code.md)) and the upstream inference provider, acting as a programmable middleware. It is frequently deployed alongside [LiteLLM](../../services/litellm.md) for enterprise-grade load balancing and token rate-limit management.

## Typical use cases
- **DeepSeek Integration**: Directing complex code generation and reasoning tasks to `DeepSeek-V4` at a fraction of the token cost of Claude 5.1.
- **Local Dev Loop**: Routing lightweight background queries to a local [Ollama instance](../../services/ollama.md) (e.g., `qwen3.8-coder`) to eliminate external API reliance and maintain privacy.
- **Enterprise Proxying**: Centralizing API key management, observability, and cost auditing for engineering teams using Claude Code via [OpenRouter](../ai_knowledge/openrouter.md).
- **Automated Benchmarking**: Executing multi-file refactoring tasks across Claude 5.1, GPT-5.5, and Gemini 4.0 Pro to evaluate model regressions and accuracy.

## Strengths
- **Dynamic Switching**: Instantly switch underlying active models using the `/model` command within an active Claude Code interaction.
- **Transformer System**: Built-in AST and payload manipulation to guarantee tool-use compatibility for non-Anthropic models.
- **Ease of Use**: Features a lightweight web management dashboard (`ccr ui`) alongside an interactive CLI selector (`ccr model`).
- **CI/CD Native**: Full support for headless operation via `NON_INTERACTIVE_MODE` in automated GitHub Actions pipelines.
- **MCP 3.1 Discovery**: Native compatibility with the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) FastMCP 3.1 Task Protocol.

## Limitations
- **Latency Overhead**: Routing requests through a local or intermediate proxy introduces slight network latency (typically <50ms).
- **Operational Complexity**: Requires running and maintaining a local background proxy daemon.
- **Instruction Adherence Gap**: While API transformers significantly improve prompt compatibility, non-Claude models may occasionally drift on intricate multi-step agentic directives compared to native `claude-5-1` execution.

## When to use it
- When optimizing API token expenditure by routing secondary agent tasks to high-throughput, low-cost models.
- When requiring proxy access to Anthropic models from restricted geographical regions.
- When configuring multi-provider fallback chains to guarantee uptime during upstream provider outages.
- When running automated evaluations across multiple frontier models under identical Claude Code project prompts.

## When not to use it
- When operating under a direct Claude Code Max tier where multi-provider routing is unneeded.
- When strict zero-dependency policy prohibits running background proxy daemons.
- In zero-trust air-gapped environments that restrict local loopback network listeners.

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

Configure your target model route:
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

# Check provider health, latency, and throughput metrics
ccr health
```

## API examples

### Advanced Routing Patterns (YAML)
CCR supports advanced declarative routing rules defined in `rules.yaml` that trigger on prompt regex patterns or tool capabilities:

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
This Python snippet validates CCR configuration files, model transformers, and failover policies using strict **Pydantic v2** models.

```python
import json
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class FallbackPolicy(BaseModel):
    enabled: bool = Field(default=True, description="Enable automated failover to alternate model targets")
    strategy: str = Field(default="ordered", description="Failover strategy algorithm")
    targets: List[str] = Field(description="Priority list of model target routes")
    retry_on: List[int] = Field(
        default_factory=lambda: [429, 502, 503],
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

def validate_ccr_config(raw_json: str) -> Optional[CCRConfig]:
    try:
        data = json.loads(raw_json)
        config = CCRConfig.model_validate(data)
        return config
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.")
    except ValidationError as e:
        print(f"CCR Configuration Validation failed: {e.errors()}")
    return None

if __name__ == "__main__":
    sample_config = """
    {
      "fallback_policy": {
        "enabled": true,
        "strategy": "ordered",
        "targets": ["deepseek/deepseek-chat", "anthropic/claude-5-1"],
        "retry_on": [429, 502, 503]
      },
      "models": {
        "deepseek/deepseek-chat": {
          "transformers": ["tooluse", "inject_reasoning_reminder"]
        }
      },
      "rules": [
        {
          "name": "heavy-coding",
          "if": "query.matches(/refactor/)",
          "then": "deepseek/deepseek-chat"
        }
      ]
    }
    """
    parsed = validate_ccr_config(sample_config)
    if parsed:
        print(f"Validated CCR configuration with {len(parsed.rules)} rules successfully.")
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
- Last reviewed: 2027-01-07
- Confidence: high
