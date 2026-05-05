# PostHog

## What it is
An all-in-one product OS that includes product analytics, session replay, feature flags, and A/B testing.

## What problem it solves
It helps teams understand how users interact with their applications and allows for data-driven product decisions.

## Where it fits in the stack
**Category**: Process & Understanding / Product Analytics

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

## Sources / references
- [PostHog Website](https://posthog.com/)
- [PostHog CLI Documentation](https://posthog.com/docs/endpoints/cli)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
