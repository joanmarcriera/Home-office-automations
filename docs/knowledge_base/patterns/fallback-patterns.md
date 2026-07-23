# Fallback Patterns

## What it is
Fallback and failover patterns are architectural strategies designed to ensure the resilience and availability of AI applications. They involve automatically switching between different Large Language Model (LLM) providers, models, or configurations when the primary system encounters an error, rate limit, or performance degradation. In July 2026, these have evolved into "Self-Healing Agentic Loops" that can autonomously remediate provider failures.

## What problem it solves
The LLM ecosystem is prone to several types of failures that can disrupt service:
- **API Outages**: Primary providers (e.g., Anthropic, OpenAI) may experience downtime (5xx errors).
- **Rate Limiting**: Reaching Tier limits or unexpected spikes in traffic can result in 429 (Too Many Requests) errors.
- **Latency Spikes**: Network congestion or high demand can make a model too slow for real-time applications.
- **Quality Floor Misses**: A model might fail to follow complex instructions or return malformed structured data, requiring a retry with a more capable "frontier" model like Claude 5.1 or GPT-5.5.
- **ClawJacked Vulnerabilities**: Emerging 2026-era exploits that target specific model versions, necessitating immediate fallback to a secured, sandboxed alternative.

## Where it fits in the stack
Fallback patterns typically reside in the **Middleware or Gateway layer**. They sit between the application logic and the various inference providers, acting as a programmable traffic controller. In modern agentic architectures, they are integrated into the **Durable State** layer (e.g., [Temporal](../../tools/orchestration/temporal.md)) to ensure task completion across retries.

## Typical use cases
- **Frontier Failover**: Switching to GPT-5.5 if Claude 5.1 is down.
- **Cost-Optimized Coding**: Using DeepSeek-V4 as primary and falling back to Sonnet 5.1 only if the cheaper model fails a unit test.
- **Rate Limit Buffering**: Distributing load across multiple providers ([OpenRouter](../../tools/ai_knowledge/openrouter.md), [LiteLLM](../../services/litellm.md)) to avoid 429 errors.
- **Self-Healing Remediation**: Automatically switching to a local [Ollama](../../services/ollama.md) instance for critical system remediation when external APIs are unreachable.

## Strengths
- **Reliability**: Decouples application availability from individual provider uptime.
- **Cost Control**: Enables "cheapest-first" strategies with automatic escalation.
- **Performance**: Can route to the fastest available model based on real-time latency.
- **Resilience**: Protects against "Agentic Deadlocks" caused by model-specific failures.

## Limitations
- **Latency**: Each failure and subsequent retry adds round-trip time.
- **State Management**: Ensuring session context (chat history) is correctly passed to the fallback model, especially with differing context window sizes.
- **Inconsistent Outputs**: Different models may behave differently, potentially confusing downstream logic or multi-step reasoning chains.
- **Complex Observability**: Tracking fallback triggers requires sophisticated logging to identify the root cause of the failover.

## When to use it
- In production environments where high availability (99.9%+) is required.
- For mission-critical agents that must complete tasks even during provider outages.
- When working with providers that have strict rate limits or inconsistent performance.
- When implementing [Self-Healing Agent](../../knowledge_base/self-healing-agent-research.md) patterns.

## When not to use it
- Simple internal prototypes or research projects where occasional failure is acceptable.
- Applications with extremely tight latency requirements where the overhead of a proxy or a retry is too high.
- When the primary model is strictly required for its unique capabilities (e.g., specific vision or audio features).

## Getting started
1. **Identify Critical Paths**: Determine which LLM calls require 100% uptime.
2. **Select Fallback Targets**: Choose a secondary provider (e.g., switching from Anthropic to Google Vertex AI).
3. **Choose a Gateway**: Deploy a tool like [LiteLLM](../../services/litellm.md) or [Portkey](../../tools/providers/portkey.md) to manage the logic.
4. **Define Retry Policy**: Set specific HTTP error codes (429, 500, 503) that should trigger a fallback.
5. **Inject Reference Context**: Ensure the fallback model receives the same system instructions and conversation history.

## CLI examples
Using `litellm` CLI to start a proxy with a fallback configuration:

```bash
# Start litellm proxy with a config file containing fallbacks
litellm --config config.yaml

# Test the fallback by simulating a failure on the primary model
curl -X POST http://0.0.0.0:4000/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-5.5-preview",
       "messages": [{"role": "user", "content": "Hello"}]
     }'
```

Example `config.yaml` with ordered fallbacks:
```yaml
model_list:
  - model_name: gpt-5.5-preview
    litellm_params:
      model: openai/gpt-5.5-preview
      api_key: os.environ/OPENAI_API_KEY
  - model_name: claude-5-1-sonnet
    litellm_params:
      model: anthropic/claude-5-1-sonnet
      api_key: os.environ/ANTHROPIC_API_KEY

router_settings:
  fallback_policy:
    gpt-5.5-preview: ["claude-5-1-sonnet"]
```

## API examples
Example implementation using the [Vercel AI SDK](../../tools/providers/vercel-ai-gateway.md) or standard client patterns for graceful degradation and local backup:

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

async function generateWithFallback(prompt: string) {
  try {
    // Primary attempt with frontier model
    return await generateText({
      model: anthropic('claude-5-1-sonnet'),
      prompt: prompt,
    });
  } catch (error) {
    console.warn('Primary model failed, falling back to GPT-5.5...');
    try {
      // Fallback attempt
      return await generateText({
        model: openai('gpt-5-5-preview'),
        prompt: prompt,
      });
    } catch (innerError) {
      console.error('All SaaS providers down! Falling back to local Ollama Llama 4...');
      // Local recovery
      return await generateText({
        model: openai('ollama/llama4'),
        prompt: prompt,
      });
    }
  }
}
```

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — Universal proxy for LLM fallbacks.
- [OpenRouter](../../tools/ai_knowledge/openrouter.md) — Managed routing and failover service.
- [Claude Code Router](../../tools/development_ops/claude-code-router.md) — Specialized proxy for coding workflows.
- [Portkey](../../tools/providers/portkey.md) — Enterprise-grade AI gateway with fallback logic.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategies for selecting the right model.
- [Self-Healing Agent Research](../../knowledge_base/self-healing-agent-research.md) — Advanced patterns for autonomous remediation.
- [Temporal](../../tools/orchestration/temporal.md) — Durable execution for resilient agentic workflows.
- [Ollama](../../services/ollama.md) — Local inference engine for offline fallback.

## Sources / References
- [Anthropic: Implementing Fallbacks for Resilience](https://docs.anthropic.com/claude/docs/resilience-and-fallbacks)
- [LiteLLM Documentation: Fallbacks & Retries](https://docs.litellm.ai/docs/proxy/fallbacks)
- [Vercel AI SDK: Resilience and Failover](https://sdk.vercel.ai/docs/concepts/resilience)
- [OpenClaw Architectural Resilience Standards 2026](https://openclaw.io/standards/resilience)

## Contribution Metadata
- Last reviewed: 2026-07-24
- Confidence: high
