# Langfuse

## What it is
Langfuse is an open-source LLM engineering platform designed for tracing, observability, metrics, and evaluation. As of late October / November 2026, it serves as a central hub for teams to collaboratively debug, analyze, and iterate on their LLM applications (including those powered by **Claude 5.1**, **GPT-5.5**, **Gemini 4.0**, and **Llama 4 Maverick**) throughout the entire development lifecycle.

## What problem it solves
LLM applications involve complex, non-deterministic interactions that are difficult to monitor using traditional software tools. Langfuse solves these challenges by providing:
- **Trace Transparency**: Deep visibility into nested calls, including retrieval, tool usage, and embedding steps in complex **agentic workflows**.
- **Cost and Latency Management**: Precise tracking of token usage, model costs, and performance bottlenecks across diverse providers.
- **Quality Assurance**: Tools for measuring output quality via LLM-as-a-judge, user feedback, and manual labeling.
- **Prompt Fragmentation**: Centralized prompt management to decouple prompts from code and enable version control.
- **MCP Integration**: Enhanced support for monitoring **Model Context Protocol (MCP 3.1)** sessions and resource retrieval.

## Where it fits in the stack
Langfuse sits in the **Observability and Evaluation** layer of the AI stack. It integrates directly with LLM providers, frameworks (like LangChain and LlamaIndex), and gateways (like [LiteLLM](../../services/litellm.md)) to capture telemetry data. It often uses [ClickHouse](clickhouse.md) as a high-performance backend for analytical queries.

## Typical use cases
- **Debugging Agentic Workflows**: Visualizing multi-step agent loops and identifying where a "hallucination" or tool failure occurred.
- **Regression Testing**: Using datasets and experiments to ensure a new prompt version or model doesn't degrade performance.
- **Production Monitoring**: Tracking real-world usage, user feedback, and cost across different models and versions.
- **Prompt Engineering**: Collaboratively iterating on prompts in a UI-based playground and deploying them via API without redeploying code.
- **MCP Session Audit**: Tracing the lifecycle of MCP 3.1 connections and the context provided to models.

## Strengths
- **Open Source and Self-hostable**: Complete control over data and infrastructure, with a community-driven development model.
- **Minimal Performance Overhead**: Asynchronous SDKs designed to capture traces without blocking application logic.
- **Comprehensive Integration**: Native support for Python/JS SDKs, OpenTelemetry, and 50+ library/framework integrations.
- **API-First Architecture**: Easy to export data to blob storage or integrate with custom evaluation pipelines.

## Limitations
- **Hosting Complexity**: While self-hostable, managing the database (PostgreSQL), [ClickHouse](clickhouse.md) (for analytics), and Redis (for task queuing) requires operational effort.
- **Dashboard Latency**: For extremely high-volume applications, there can be a slight delay in analytics updates.
- **Learning Curve**: Mastering advanced features like multi-step experiments and custom scoring requires familiarity with the platform's core concepts.

## When to use it
- When building complex RAG systems or multi-agent workflows that require deep nested tracing.
- When you need to manage and version prompts independently of your application deployment cycle.
- When data privacy is a priority and you require a self-hosted observability solution.
- When you want to systematically evaluate LLM outputs using both automated and human-in-the-loop methods.

## When not to use it
- For extremely simple, single-prompt applications where basic logging suffices.
- If you prefer a fully managed, zero-config SaaS solution and do not mind data leaving your infrastructure (though Langfuse offers a Cloud version).
- If your application does not use LLMs (it is specialized for LLM telemetry).

## Getting started

### Installation
Install the Langfuse Python SDK:
```bash
pip install langfuse
```

### Basic Integration (OpenAI / GPT-5.5)
Langfuse provides a wrapper for the OpenAI SDK that automatically captures traces.

```python
import os
from langfuse.openai import openai

# Configure environment variables
# os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
# os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
# os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

# Standard OpenAI call, now automatically traced
response = openai.chat.completions.create(
  model="gpt-5.5-preview",
  messages=[{"role": "user", "content": "How does Langfuse help with AI observability?"}],
  name="obs-test-run" # Name the trace for easy filtering
)

print(response.choices[0].message.content)
```

## CLI examples

### Langfuse CLI Setup
The Langfuse CLI can be used for administrative tasks and CI/CD integrations:
```bash
npm install -g langfuse
```

### Health Check
Check the status of your Langfuse instance:
```bash
langfuse health
```

### Exporting Traces
Export traces for a specific period for offline analysis:
```bash
langfuse export --from 2026-10-01 --to 2026-11-01 --format csv > traces.csv
```

## API examples

### Python: Manual Tracing (with Async & Type Hints)
For non-standard integrations (e.g., custom **Llama 4 Maverick** local deployments), use the native SDK:

```python
import asyncio
from typing import Dict, Any
from langfuse import Langfuse

langfuse_client = Langfuse()

async def trace_translation_task(text: str, target_lang: str) -> Dict[str, Any]:
    trace = langfuse_client.trace(
        name="maverick-translation-task",
        input={"text": text, "target": target_lang}
    )

    span = trace.span(
        name="translate-to-german",
        input={"text": text}
    )

    try:
        # Simulate async LLM call logic
        await asyncio.sleep(0.1)
        translated_text = f"Hallo {text.split()[-1]}" if "world" in text.lower() else "Hallo Welt"
        span.end(output={"translated_text": translated_text})
        return {"status": "success", "result": translated_text}
    except Exception as e:
        span.end(level="ERROR", status_message=str(e))
        raise e
```

### JavaScript: Recording Feedback (with Type Definitions)
Record user feedback on an LLM output from a web interface:

```typescript
import { Langfuse } from "langfuse";

const langfuse = new Langfuse();

interface FeedbackPayload {
  traceId: string;
  score: number;
  comment?: string;
}

async function submitFeedback(payload: FeedbackPayload): Promise<void> {
  await langfuse.score({
    traceId: payload.traceId,
    name: "user-feedback",
    value: payload.score,
    comment: payload.comment
  });
}
```

## Related tools / concepts
- [AgentOps](agentops.md) - Specialized agent monitoring and session tracking.
- [Helicone](helicone.md) - Proxy-based LLM observability.
- [ClickHouse](clickhouse.md) - Analytical database often used as a backend for Langfuse.
- [Arize AI](arize-ai.md) - Enterprise-grade ML observability and evaluation.
- [W&B Weave](wandb-weave.md) - Lightweight tracing and versioning for AI developers.
- [Parea](parea.md) - AI engineering platform for testing and monitoring.
- [LiteLLM](../../services/litellm.md) - LLM gateway that can export traces to Langfuse.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Complex patterns that benefit from Langfuse tracing.
- [Model Routing](../../knowledge_base/model_routing_guide.md) - Decision logic that can be audited via Langfuse.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Protocol for connecting models to tools, traceable via Langfuse.

## Sources / references
- [Langfuse Official Documentation](https://langfuse.com/docs)
- [Langfuse GitHub Repository](https://github.com/langfuse/langfuse)
- [Langfuse SDK Reference](https://langfuse.com/docs/sdk/overview)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
