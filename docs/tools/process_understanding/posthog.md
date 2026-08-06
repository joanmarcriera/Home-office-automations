# PostHog

## What it is
PostHog is an all-in-one product OS that includes product analytics, session replay, feature flags, and A/B testing. As of late December 2026, it serves as a critical observability hub for [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5, and other frontier models, providing a comprehensive suite for monitoring user behavior, feature flag rolls, and model performance in real-time.

## What problem it solves
It helps product and engineering teams understand how users interact with their applications and allows for data-driven product decisions. For AI teams, it provides visibility into how LLM responses affect user conversion and retention, with deep integration for [MCP 3.1](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) and FastMCP 3.1 based tool-calling traces.

## Where it fits in the stack
**Category**: [Process & Understanding](index.md) / Product Analytics. It serves as the primary observability layer for user-facing applications and agentic workflows, sitting alongside [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) components.

## Typical use cases
- **Full-Funnel Analytics**: Tracking user behavior from the first click to the final AI-generated response.
- **A/B Testing AI Models**: Comparing the performance and user satisfaction of different LLMs (e.g., [Gemma 3](../ai_knowledge/local_llms.md) vs Claude 5.1) using feature flags.
- **Session Replay**: Watching recordings of users interacting with AI agents to identify friction points and hallucination impacts.
- **Conversion Tracking**: Measuring how AI features impact key business metrics like signups or purchases.

## Strengths
- **All-in-One**: Combines analytics, session recording, and feature flagging in a single platform.
- **AI Observability Dashboard**: Specialized views for cost, latency, and error rates across different LLM providers via FastMCP 3.1.
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
- If you only need deep, low-level AI engineering traces and don't care about broader product analytics (consider [Langfuse](langfuse.md)).
- For extremely simple applications where a basic log aggregator would be enough.

## Getting started

### Installation
```bash
pip install posthog pydantic>=2.0
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

### Python (AI Trace Instrumentation & Schema Validation)
This script demonstrates how to format and validate AI traces, model metadata, and custom telemetry data using strict Pydantic v2 before capturing them inside PostHog.

```python
from typing import Dict, Literal, Optional
from pydantic import BaseModel, Field
import posthog

# 1. Define Pydantic v2 schemas for tracing metadata
class LLMTraceTelemetry(BaseModel):
    ai_model: str = Field(..., description="E.g., gemma-3-27b, claude-5.1")
    ai_provider: Literal["openai", "anthropic", "ollama", "openrouter"]
    input_tokens: int = Field(..., ge=0)
    output_tokens: int = Field(..., ge=0)
    latency_seconds: float = Field(..., gt=0.0)
    cost: float = Field(0.0, ge=0.0)
    trace_id: str = Field(..., min_length=8)
    mcp_protocol_version: str = Field("3.1", pattern="^3\\.[0-1]$")

class UserAIInteraction(BaseModel):
    user_id: str = Field(..., min_length=3)
    event_name: str = Field("$ai_generation", min_length=1)
    telemetry: LLMTraceTelemetry
    user_feedback: Optional[Literal["helpful", "unhelpful"]] = None

# 2. Capture function with validated payload
def capture_validated_ai_trace(interaction: UserAIInteraction):
    # Initialize PostHog
    posthog.project_api_key = "ph_mock_key"
    posthog.host = "https://us.i.posthog.com"

    # Pack parameters conforming to PostHog's custom AI traces schema (v2026.12+)
    properties = {
        "$ai_model": interaction.telemetry.ai_model,
        "$ai_provider": interaction.telemetry.ai_provider,
        "$ai_input_tokens": interaction.telemetry.input_tokens,
        "$ai_output_tokens": interaction.telemetry.output_tokens,
        "$ai_latency": interaction.telemetry.latency_seconds,
        "$ai_cost": interaction.telemetry.cost,
        "$ai_trace_id": interaction.telemetry.trace_id,
        "$mcp_protocol_version": interaction.telemetry.mcp_protocol_version,
    }

    if interaction.user_feedback:
        properties["user_feedback"] = interaction.user_feedback

    posthog.capture(
        distinct_id=interaction.user_id,
        event=interaction.event_name,
        properties=properties
    )

if __name__ == "__main__":
    try:
        # Create a validated interaction object
        interaction_data = UserAIInteraction(
            user_id="user_987",
            telemetry=LLMTraceTelemetry(
                ai_model="claude-5.1-sonnet",
                ai_provider="anthropic",
                input_tokens=250,
                output_tokens=480,
                latency_seconds=1.85,
                cost=0.0072,
                trace_id="tx-992384-abc"
            ),
            user_feedback="helpful"
        )

        capture_validated_ai_trace(interaction_data)
        print("Successfully captured validated PostHog AI trace.")
    except Exception as e:
        print(f"Failed schema validation: {e}")
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
- Last reviewed: 2026-12-06
- Confidence: high
