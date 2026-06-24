# ClawRouter

## What it is
ClawRouter is an agent-native LLM router for OpenClaw-focused workflows.

## What problem it solves
It helps route model calls across multiple models and providers with low-latency decision logic, which is useful when agent workloads need better cost, speed, or model specialization control.

## Where it fits in the stack
**Infrastructure / Routing Layer**. It sits in the model-routing layer for agent systems, especially OpenClaw-centered stacks.

## Typical use cases
- Routing agent calls across different LLMs
- Cost-optimizing high-volume agent workflows
- Selecting specialized models for different OpenClaw tasks

## Strengths
- Designed for agent-native routing rather than generic API abstraction
- Clear fit for OpenClaw ecosystems
- Useful when model routing is a first-class operational concern

## Limitations
- More niche than general routing layers like LiteLLM
- Best fit is OpenClaw-heavy stacks, not every company AI stack

## When to use it
- When OpenClaw is a core part of your workflow and model routing matters
- When agent workloads need explicit cost and speed tuning across models

## When not to use it
- When a simpler router like [LiteLLM](../../services/litellm.md) is enough
- When the company is not using OpenClaw or similar agent-native environments

## Technical examples

### Cost-Based Routing Configuration
Configure ClawRouter to route simple tasks to cheaper models and complex reasoning to premium models.

```yaml
# clawrouter.yml example
routing_rules:
  - condition: "task_complexity == 'low'"
    target: "gpt-4o-mini"
    fallback: "claude-3-haiku"
  - condition: "task_complexity == 'high'"
    target: "claude-3-5-sonnet"
    fallback: "gpt-4o"

provider_priorities:
  - provider: "anthropic"
    weight: 0.8
  - provider: "openai"
    weight: 0.2
```

### Specialized Model Routing
Route specific agent actions to the best model for that domain (e.g., coding, browsing).

```yaml
action_routing:
  coding: "claude-3-5-sonnet"
  web_search: "gpt-4o"
  summarization: "claude-3-haiku"

# Example of dynamic routing based on agent state
dynamic_routing:
  - if: "agent_mode == 'fast'"
    target: "gpt-4o-mini"
  - if: "agent_mode == 'accurate'"
    target: "claude-3-5-sonnet"
```

### Technical Workflow: Provider Fallback
Ensure high availability by configuring automatic failover between providers.

```yaml
failover_groups:
  premium_reasoning:
    primary: "anthropic/claude-3-5-sonnet"
    secondary: "openai/gpt-4o"
    timeout_ms: 5000
    retry_attempts: 2
```

## Example company use cases
- **High-volume agent ops**: route routine OpenClaw actions to cheaper models while reserving premium models for harder steps.
- **Multi-model specialization**: use one model for browsing, another for code generation, and another for summarization.
- **Cost-aware experimentation**: compare routing strategies before standardizing a production model mix.

## Selection comments
- Use **ClawRouter** when routing is part of the agent architecture itself.
- Use **LiteLLM** for broader, provider-agnostic routing across many application teams.
- Use **OpenRouter** when you want one billing and access layer, not a deeper routing control plane.

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md)
- [LiteLLM](../../services/litellm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Aider](../development_ops/aider.md)
- [Zed](../development_ops/zed.md)
- [Tabnine](../development_ops/tabnine.md)

## Sources / References
- [GitHub Repository](https://github.com/BlockRunAI/ClawRouter)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
