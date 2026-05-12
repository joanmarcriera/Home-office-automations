# PostHog

## What it is
An all-in-one product OS that includes product analytics, session replay, feature flags, and A/B testing.

## What problem it solves
It helps teams understand how users interact with their applications and allows for data-driven product decisions.

## Where it fits in the stack
**Category**: Process & Understanding / Product Analytics

## Typical use cases
- **Full-Funnel Analytics**: Tracking user behavior from the first click to the final AI-generated response.
- **A/B Testing AI Models**: Comparing the performance and user satisfaction of different LLMs using feature flags.
- **Session Replay**: Watching recordings of users interacting with AI agents to identify friction points.
- **Conversion Tracking**: Measuring how AI features impact key business metrics like signups or purchases.

## Strengths
- **All-in-One**: Combines analytics, session recording, and feature flagging in a single platform.
- **Extensible**: Supports "Apps" and integrations (like OpenRouter) to bring in data from external AI services.
- **HogQL**: Powerful, SQL-like query language for advanced data analysis.
- **Privacy Conscious**: Offers self-hosting options and SOC 2 compliance.

## Limitations
- **Generalist Focus**: While it has LLM features, it is not a dedicated AI-only observability tool (like LangSmith or LangFuse).
- **Complexity**: The sheer number of features can make the learning curve steeper for new users.

## When to use it
- When you want to see the "big picture" of how AI features affect your overall product metrics.
- For teams that need built-in A/B testing and feature flagging to roll out AI changes safely.
- When you want to link specific AI traces back to actual user session recordings.

## When not to use it
- If you only need deep, low-level AI engineering traces and don't care about broader product analytics.
- For extremely simple applications where a basic log aggregator (like Papertrail) would be enough.

## LLM Features
- **LLM Observability**: Track agent behavior and user feedback alongside traditional product metrics like conversion and retention.
- **Trace Management**: Capture and visualize LLM traces to debug agent decision-making.
- **OpenRouter Integration**: Native support for receiving event logs from OpenRouter sessions to monitor model performance and costs.

## Getting started

### Installation
```bash
pip install posthog
```

### Capturing LLM Events
```python
import posthog

posthog.project_api_key = '<ph_project_api_key>'
posthog.host = 'https://us.i.posthog.com'

posthog.capture('user_id', 'llm_interaction', {
    'model': 'gpt-4o',
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
Executes a HogQL (SQL) query against your PostHog data directly from the terminal:
```bash
posthog-cli query "SELECT event, count() FROM events GROUP BY event"
```

### posthog-cli capture
Sends a manual event to PostHog for testing purposes:
```bash
posthog-cli capture --distinct-id user_123 --event test_event --properties '{"source": "cli"}'
```

## API examples

### Python (AI Trace Instrumentation)
PostHog can be integrated into AI pipelines to track multi-step agent actions using their SDK's properties to link traces to specific user sessions.

```python
import posthog

# Link an AI trace to a user session
posthog.capture('user_123', 'ai_trace_step', {
    'trace_id': 'uuid-1234',
    'step_name': 'retrieval',
    'context_found': True
})
```

### Python (Feature Flag Evaluation)
```python
import posthog

posthog.project_api_key = '<ph_project_api_key>'

# Check if a new AI model feature flag is enabled for a user
if posthog.feature_enabled('use-new-llm-model', 'user_123'):
    # Logic for new model
    pass
else:
    # Logic for fallback model
    pass
```

## Related tools / concepts
- [Datadog](datadog.md)
- [Sentry](sentry.md)
- [Langfuse](langfuse.md)
- [AgentOps](agentops.md)
- [Arize AI](arize-ai.md)
- [Helicone](helicone.md)
- [Parea](parea.md)
- [Mixpanel](mixpanel.md)

## Sources / references
- [PostHog Website](https://posthog.com/)
- [PostHog CLI Documentation](https://posthog.com/docs/endpoints/cli)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
