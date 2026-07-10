# PostHog

## What it is
An all-in-one product OS that includes product analytics, session replay, feature flags, and A/B testing. In July 2026, it serves as a critical observability hub for [Gemma 3](../ai_knowledge/local_llms.md) and other frontier models, providing a comprehensive suite for monitoring user behavior and system performance in real-time.

## What problem it solves
It helps teams understand how users interact with their applications and allows for data-driven product decisions. For AI teams, it provides visibility into how LLM responses affect user conversion and retention, with deep integration for [MCP 3.0](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) based tool-calling traces.

## Where it fits in the stack
**Category**: [Process & Understanding](index.md) / Product Analytics. It serves as the primary observability layer for user-facing applications and agentic workflows, sitting alongside [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) components.

## Typical use cases
- **Full-Funnel Analytics**: Tracking user behavior from the first click to the final AI-generated response.
- **A/B Testing AI Models**: Comparing the performance and user satisfaction of different LLMs (e.g., [Gemma 3](../ai_knowledge/local_llms.md) vs Claude 4.8) using feature flags.
- **Session Replay**: Watching recordings of users interacting with AI agents to identify friction points and hallucination impacts.
- **Conversion Tracking**: Measuring how AI features impact key business metrics like signups or purchases.

## Strengths
- **All-in-One**: Combines analytics, session recording, and feature flagging in a single platform.
- **AI Observability Dashboard**: Specialized views for cost, latency, and error rates across different LLM providers via MCP 3.0.
- **Integrated Session Recordings**: Visualize UI changes triggered by LLM responses directly in the trace timeline.
- **HogQL**: Powerful, SQL-like query language for advanced data analysis and custom dashboarding.

## Limitations
- **Indexing Latency**: In high-volume environments, there can be a slight delay before traces appear in the dashboard.
- **Complexity**: The sheer number of features can make the learning curve steeper for new users compared to point solutions.

## When to use it
- When you want to see the "big picture" of how AI features affect your overall product metrics.
- For teams that need built-in A/B testing and feature flagging to roll out AI changes safely.
- When you want to link specific AI traces back to actual user session recordings.

## When not to use it
- If you only need deep, low-level AI engineering traces and don't care about broader product analytics.
- For extremely simple applications where a basic log aggregator would be enough.

## Getting started

### Installation
```bash
pip install posthog
```

### Basic Capture
```python
import posthog

posthog.project_api_key = '<ph_project_api_key>'
posthog.host = 'https://us.i.posthog.com'

posthog.capture('user_id', 'llm_interaction', {
    'model': 'gemma-3-27b',
    'prompt_tokens': 150,
    'completion_tokens': 200,
    'total_cost': 0.005,
    'user_feedback': 'helpful'
})
```

## CLI examples

### posthog-cli login
Authenticates the CLI with your PostHog instance:
```bash
posthog-cli login
```

### posthog-cli query
Executes a HogQL (SQL) query against your PostHog data:
```bash
posthog-cli query "SELECT event, count() FROM events GROUP BY event"
```

### posthog-cli capture
Sends a manual event for testing:
```bash
posthog-cli capture --distinct-id user_123 --event test_event --properties '{"source": "cli"}'
```

## API examples

### Python (AI Trace Instrumentation)
PostHog supports a structured trace API for LLM monitoring (v2026.7+):

```python
import posthog

# Capture a full LLM generation trace with MCP context
posthog.capture('user_123', '$ai_generation', {
    '$ai_model': 'gemma-3-27b',
    '$ai_provider': 'ollama',
    '$ai_input_tokens': 150,
    '$ai_output_tokens': 200,
    '$ai_latency': 1.2,
    '$ai_cost': 0.0,
    '$ai_trace_id': 'trace-uuid-456',
    '$ai_input': 'Summarize the latest sales data.',
    '$ai_output': 'Summary: Sales are up 20%...',
    '$mcp_protocol_version': '3.0'
})
```

### JavaScript (Feature Flag Evaluation)
```javascript
import posthog from 'posthog-js'

posthog.init('<ph_project_api_key>', { api_host: 'https://us.i.posthog.com' })

// Check if a new AI model feature flag is enabled
if (posthog.isFeatureEnabled('use-gemma-3-model')) {
    // Use Gemma 3
} else {
    // Use fallback model
}
```

## Related tools / concepts
- [Datadog](datadog.md)
- [Sentry](sentry.md)
- [Langfuse](langfuse.md)
- [AgentOps](agentops.md)
- [Arize AI](arize-ai.md)
- [Helicone](helicone.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Local LLMs (Gemma 3)](../ai_knowledge/local_llms.md)
- [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md)

## Sources / References
- [PostHog Website](https://posthog.com/)
- [PostHog AI Observability Documentation](https://posthog.com/docs/ai-analytics)
- [PostHog CLI Repository](https://github.com/PostHog/posthog-cli)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
