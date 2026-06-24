# Fallback Patterns

## What it is
Fallback and failover patterns are architectural strategies designed to ensure the resilience and availability of AI applications. They involve automatically switching between different Large Language Model (LLM) providers, models, or configurations when the primary system encounters an error, rate limit, or performance degradation. In June 2026, these have evolved into **Self-Healing Agentic Loops**, where the agent itself detects failures and negotiates alternatives via the Model Control Protocol (MCP 3.0).

## What problem it solves
The LLM ecosystem is prone to several types of failures that can disrupt service:
- **API Outages**: Primary providers (e.g., Anthropic Claude 4.8, OpenAI GPT-5.5) may experience downtime (5xx errors).
- **Rate Limiting**: Reaching Tier limits or unexpected spikes in traffic can result in 429 (Too Many Requests) errors.
- **Latency Spikes**: Network congestion or high demand can make a model too slow for real-time applications.
- **Quality Floor Misses**: A model might fail to follow complex instructions or return malformed structured data, requiring a retry with a more capable "frontier" model.
- **Tool Selection Failure**: An agent might fail to select the correct MCP tool, requiring a fallback to a reasoning-heavy model to re-evaluate the plan.

## Where it fits in the stack
Fallback patterns typically reside in the **Middleware or Gateway layer**, but increasingly also within the **Agent Orchestration layer**. They sit between the application logic and the various inference providers, acting as a programmable traffic controller that ensures durable execution.

## Typical use cases
- **Frontier Failover**: Switching to GPT-5.5 if Claude 4.8 is down or rate-limited.
- **Cost-Optimized Coding**: Using DeepSeek-V3 as primary and falling back to Claude 3.5 Sonnet only if the cheaper model fails a validation check.
- **Rate Limit Buffering**: Distributing load across multiple providers (e.g., OpenRouter, AWS Bedrock, Azure OpenAI) to avoid 429 errors.
- **Self-Healing Infrastructure**: Automatically switching from a failing local [K3s](../../tools/infrastructure/k3s.md) inference node to a cloud provider.

## Strengths
- **Reliability**: Decouples application availability from individual provider uptime.
- **Cost Control**: Enables "cheapest-first" strategies with automatic escalation only when needed.
- **Performance**: Can route to the fastest available model based on real-time latency monitoring.
- **Durable Reasoning**: Ensures that complex agentic workflows don't collapse due to a single transient model error.

## Limitations
- **Latency**: Each failure and subsequent retry adds round-trip time to the user experience.
- **State Management**: Ensuring session context (chat history) is correctly passed and "translated" (if necessary) to the fallback model.
- **Inconsistent Outputs**: Different models may behave differently (e.g., GPT-5.5 vs Claude 4.8), potentially confusing downstream logic if not normalized.

## When to use it
- In production environments where high availability (99.9%+) is required for AI services.
- For mission-critical agents that must complete tasks even during provider outages.
- When working with providers that have strict rate limits or inconsistent performance profiles.

## When not to use it
- Simple internal prototypes or research projects where occasional failure is acceptable and low cost is the only priority.
- Applications with extremely tight latency requirements (sub-100ms) where the overhead of a proxy or a retry is prohibited.

## Getting started
To implement fallback patterns, you should first identify your primary and secondary models.
1. **Define your Chain**: Decide the order of models (e.g., Claude 4.8 -> GPT-5.5 -> Gemini 3.5 Flash).
2. **Select a Gateway**: Use a tool like [LiteLLM](../../services/litellm.md) or [Portkey](../../tools/providers/portkey.md) to manage the logic.
3. **Configure Timeouts**: Set aggressive timeouts (e.g., 5-10s) to trigger failover quickly.
4. **Implement Circuit Breakers**: Prevent "thundering herd" issues by temporarily disabling a provider that is consistently failing.

## CLI examples
Using `litellm` to run a proxy with fallbacks defined:

```bash
# Start litellm proxy with a config file
litellm --config config.yaml

# Example config.yaml snippet
# model_list:
#   - model_name: my-fast-model
#     litellm_params:
#       model: anthropic/claude-3-5-haiku
#   - model_name: my-fallback-model
#     litellm_params:
#       model: openai/gpt-4o-mini
```

Using `curl` to test a gateway with fallback headers:

```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "Hello!"}],
    "metadata": {
      "fallbacks": ["gpt-4o", "gemini-1.5-pro"]
    }
  }'
```

## API examples
Example using the Vercel AI SDK to implement model switching:

```typescript
import { generateText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';

async function generateWithFallback(prompt: string) {
  try {
    // Primary attempt
    return await generateText({
      model: anthropic('claude-4-8-sonnet'),
      prompt: prompt,
    });
  } catch (error) {
    console.error('Primary model failed, falling back to GPT-5.5');
    // Fallback attempt
    return await generateText({
      model: openai('gpt-5-5-preview'),
      prompt: prompt,
    });
  }
}
```

Python example using the `litellm` library:

```python
import litellm

response = litellm.completion(
    model="anthropic/claude-3-5-sonnet",
    messages=[{"role": "user", "content": "hi"}],
    fallbacks=["openai/gpt-4o", "google/gemini-1.5-pro"]
)
```

## Related tools / concepts
- [Claude Code Router](../../tools/development_ops/claude-code-router.md) — Specialized proxy for dev workflows.
- [LiteLLM](../../services/litellm.md) — Universal proxy with native fallback support.
- [Vercel AI Gateway](../../tools/providers/vercel-ai-gateway.md) — Edge-ready routing and fallbacks.
- [Portkey](../../tools/providers/portkey.md) — Enterprise-grade AI gateway and observability.
- [OpenRouter](../../tools/ai_knowledge/openrouter.md) — Unified API for model routing and failover.
- [Model Routing Guide](../model_routing_guide.md) — Best practices for selecting models.
- [Self-Healing Agentic Loops](../self-healing-agentic-loops.md) — Advanced autonomous recovery patterns.
- [Self-Healing Infrastructure](../../knowledge_base/self-healing-agent-research.md) — Research on autonomous system repair.

## Sources / References
- [Anthropic: Implementing Fallbacks](https://docs.anthropic.com/claude/docs/resilience-and-fallbacks)
- [LiteLLM Documentation](https://docs.litellm.ai/docs/proxy/fallbacks)
- [Vercel AI SDK Failover](https://sdk.vercel.ai/docs/concepts/resilience)
- [Model Control Protocol (MCP 3.0) Specification](https://modelcontrolprotocol.org)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
