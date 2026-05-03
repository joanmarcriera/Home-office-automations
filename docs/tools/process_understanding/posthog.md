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

### AI Trace Instrumentation
PostHog can be integrated into AI pipelines to track multi-step agent actions using their SDK's properties to link traces to specific user sessions.

## Related tools / concepts

- [Datadog](datadog.md)
- [Sentry](sentry.md)
- [Langfuse](langfuse.md)
- [AgentOps](agentops.md)
- [Logseq](../ai_knowledge/logseq.md)

## Sources / references
- [PostHog Website](https://posthog.com/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
