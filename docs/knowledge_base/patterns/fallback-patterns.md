# Fallback Patterns

## What it is
Fallback and failover patterns are architectural strategies designed to ensure the resilience and availability of AI applications. They involve automatically switching between different Large Language Model (LLM) providers, models, or configurations when the primary system encounters an error, rate limit, or performance degradation.

## What problem it solves
The LLM ecosystem is prone to several types of failures that can disrupt service:
- **API Outages**: Primary providers (e.g., Anthropic, OpenAI) may experience downtime (5xx errors).
- **Rate Limiting**: Reaching Tier limits or unexpected spikes in traffic can result in 429 (Too Many Requests) errors.
- **Latency Spikes**: Network congestion or high demand can make a model too slow for real-time applications.
- **Quality Floor Misses**: A model might fail to follow complex instructions or return malformed structured data, requiring a retry with a more capable "frontier" model.

## Where it fits in the stack
Fallback patterns typically reside in the **Middleware or Gateway layer**. They sit between the application logic and the various inference providers, acting as a programmable traffic controller.

## Core Resilience Strategies

### 1. Static Failover (Ordered List)
This is the simplest pattern where an application has a prioritized list of models. If the first fails, it tries the second, and so on.
- **Example**: Try `Claude 3.5 Sonnet`, fallback to `GPT-4o`, then fallback to a local [Ollama](../../services/ollama.md) instance.

### 2. Dynamic Routing
Routing based on real-time metrics such as current provider latency, cost, or reported health status. Tools like [OpenRouter](../../tools/ai_knowledge/openrouter.md) often handle some of this internally, but application-level routing provides more control.

### 3. Cascading (Smart to Fast)
A strategy where a "smart" (and expensive) model is used for planning or complex reasoning, while "fast" (cheaper) models are used for execution or sub-tasks. If the cheaper model fails, the system "cascades" back to the smarter model.

### 4. Graceful Degradation
If the primary high-capability model is unavailable, the system switches to a lower-capability model and notifies the user that certain "advanced" features might be temporarily simplified.

## Key Implementation Tools
- **[Claude Code Router](../../tools/development_ops/claude-code-router.md)**: Specifically designed to proxy and route Claude Code requests to multiple providers like [DeepSeek](../../tools/providers/deepseek.md) or [Google Gemini](../../tools/ai_knowledge/google-gemini.md).
- **[LiteLLM](../../services/litellm.md)**: A universal proxy that supports load balancing and fallbacks across 100+ LLMs using OpenAI-compatible headers.
- **[Vercel AI Gateway](../../tools/providers/vercel-ai-gateway.md)**: Provides a unified interface for routing, fallbacks, and caching for edge-ready AI apps.
- **[Portkey](../../tools/providers/portkey.md)**: An enterprise-grade AI gateway with advanced retry logic, fallbacks, and observability.

## Technical Example: Gateway Configuration
Most gateways use a JSON or YAML configuration to define fallback chains. Below is a conceptual example for a fallback policy in a tool like [LiteLLM](../../services/litellm.md):

```json
{
  "fallback_policy": {
    "enabled": true,
    "strategy": "ordered",
    "targets": [
      "anthropic/claude-3-5-sonnet",
      "openai/gpt-4o",
      "deepseek/deepseek-chat"
    ],
    "retry_on": [429, 500, 503],
    "max_retries": 2
  }
}
```

## Best Practices
- **Timeout Management**: Set aggressive timeouts for the primary model so the fallback can trigger quickly without leaving the user waiting.
- **Header Propagation**: Ensure that metadata (like user IDs or session IDs) is preserved across fallback attempts for debugging.
- **Circuit Breakers**: If a provider fails multiple times in a short window, "trip" the circuit and stop sending requests to it for a cooldown period.
- **Cost Guardrails**: Monitor fallback usage closely; a cheaper model might be the primary, but failing over to a frontier model can significantly increase costs if not capped.

## Typical use cases
- **Frontier Failover**: Switching to GPT-4o if Claude 3.5 Sonnet is down.
- **Cost-Optimized Coding**: Using DeepSeek-V3 as primary and falling back to Sonnet only if the cheaper model fails.
- **Rate Limit Buffering**: Distributing load across multiple providers to avoid 429 errors.

## Strengths
- **Reliability**: Decouples application availability from individual provider uptime.
- **Cost Control**: Enables "cheapest-first" strategies with automatic escalation.
- **Performance**: Can route to the fastest available model based on real-time latency.

## Limitations
- **Latency**: Each failure and subsequent retry adds round-trip time.
- **State Management**: Ensuring session context (chat history) is correctly passed to the fallback model.
- **Inconsistent Outputs**: Different models may behave differently, potentially confusing downstream logic.

## When to use it
- In production environments where high availability (99.9%+) is required.
- For mission-critical agents that must complete tasks even during provider outages.
- When working with providers that have strict rate limits or inconsistent performance.

## When not to use it
- Simple internal prototypes or research projects where occasional failure is acceptable.
- Applications with extremely tight latency requirements where the overhead of a proxy or a retry is too high.

## Monitoring and Observability
Resilience is only visible when it works. Use logging to track:
- **Fallback Trigger Rate**: How often are you falling back?
- **Success Rate per Target**: Is the fallback model actually solving the problem?
- **Cost Differential**: How much is failover adding to your monthly spend?

## Related tools / concepts
- [Claude Code Router](../../tools/development_ops/claude-code-router.md)
- [LiteLLM](../../services/litellm.md)
- [Vercel AI Gateway](../../tools/providers/vercel-ai-gateway.md)
- [OpenRouter](../../tools/ai_knowledge/openrouter.md)

## Related Patterns
- [Routing](../../knowledge_base/patterns/index.md)
- [Guardrails](../../knowledge_base/patterns/index.md)
- [Multi-Agent Collaboration](../../knowledge_base/patterns/index.md)

## Sources / References
- [Anthropic: Implementing Fallbacks](https://docs.anthropic.com/claude/docs/resilience-and-fallbacks)
- [LiteLLM Documentation](https://docs.litellm.ai/docs/proxy/fallbacks)
- [Vercel AI SDK Failover](https://sdk.vercel.ai/docs/concepts/resilience)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
