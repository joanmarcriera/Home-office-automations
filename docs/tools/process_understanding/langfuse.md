# Langfuse

## What it is
Langfuse is an open-source LLM engineering platform designed for tracing, observability, metrics, and evaluation. It provides a comprehensive suite of tools to help teams collaboratively debug, analyze, and iterate on their LLM applications throughout the entire development lifecycle.

## What problem it solves
LLM applications involve complex, non-deterministic interactions that are difficult to monitor using traditional software tools. Langfuse solves these challenges by providing:
- **Trace Transparency**: Deep visibility into nested calls, including retrieval, tool usage, and embedding steps.
- **Cost and Latency Management**: Precise tracking of token usage, model costs, and performance bottlenecks.
- **Quality Assurance**: Tools for measuring output quality via LLM-as-a-judge, user feedback, and manual labeling.
- **Prompt Fragmentation**: Centralized prompt management to decouple prompts from code and enable version control.

## Where it fits in the stack
Langfuse sits in the **Observability and Evaluation** layer of the AI stack. It integrates directly with LLM providers, frameworks (like LangChain and LlamaIndex), and gateways (like LiteLLM) to capture telemetry data.

## Typical use cases
- **Debugging Agentic Workflows**: Visualizing multi-step agent loops and identifying where a "hallucination" or tool failure occurred.
- **Regression Testing**: Using datasets and experiments to ensure a new prompt version or model doesn't degrade performance.
- **Production Monitoring**: Tracking real-world usage, user feedback, and cost across different models and versions.
- **Prompt Engineering**: Collaboratively iterating on prompts in a UI-based playground and deploying them via API without redeploying code.

## Strengths
- **Open Source and Self-hostable**: Complete control over data and infrastructure, with a community-driven development model.
- **Minimal Performance Overhead**: Asynchronous SDKs designed to capture traces without blocking application logic.
- **Comprehensive Integration**: Native support for Python/JS SDKs, OpenTelemetry, and 50+ library/framework integrations.
- **API-First Architecture**: Easy to export data to blob storage or integrate with custom evaluation pipelines.

## Limitations
- **Hosting Complexity**: While self-hostable, managing the database (PostgreSQL), ClickHouse (for analytics), and Redis (for task queuing) requires operational effort.
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
```bash
pip install langfuse
```

### Basic Integration (OpenAI)
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
  model="gpt-4o",
  messages=[{"role": "user", "content": "How does Langfuse help with AI observability?"}],
  name="obs-test-run" # Name the trace for easy filtering
)

print(response.choices[0].message.content)
```

### Manual Tracing
For non-standard integrations, use the native SDK to create traces and spans manually:

```python
from langfuse import Langfuse

langfuse = Langfuse()

trace = langfuse.trace(name = "translation-task")
span = trace.span(name = "translate-to-german", input = "Hello world")

# ... call your translation logic ...
span.end(output = "Hallo Welt")
```

## Related tools / concepts
- [AgentOps](agentops.md) - Specialized agent monitoring and session tracking.
- [Helicone](helicone.md) - Proxy-based observability for LLM requests.
- [Arize AI](arize-ai.md) - Enterprise-grade ML observability and evaluation.
- [W&B Weave](wandb-weave.md) - Lightweight tracing and versioning for AI developers.
- [Parea](parea.md) - AI engineering platform for testing and monitoring.
- [LiteLLM](../../services/litellm.md) - LLM gateway that can export traces to Langfuse.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Complex patterns that benefit from Langfuse tracing.
- [Model Routing](../../knowledge_base/model_routing_guide.md) - Decision logic that can be audited via Langfuse.

## Sources / references
- [Langfuse Official Documentation](https://langfuse.com/docs)
- [Langfuse GitHub Repository](https://github.com/langfuse/langfuse)
- [Langfuse SDK Reference](https://langfuse.com/docs/sdk/overview)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
