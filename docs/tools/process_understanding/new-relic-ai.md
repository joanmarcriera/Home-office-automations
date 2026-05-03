# New Relic AI

## What it is
New Relic AI (part of the New Relic Intelligent Observability platform) is a specialized observability solution for monitoring LLM-powered applications. It provides "one-click" visibility into AI performance and quality.

## What problem it solves
It addresses the unique challenges of AI monitoring, such as tracking non-deterministic outputs, monitoring "hallucinations," and managing LLM costs across multiple providers.

## Where it fits in the stack
**Observability / Eval**.

## Typical use cases
- **LLM Performance Monitoring**: Tracking response times and token usage across different models.
- **Quality Analysis**: Measuring output quality and relevance using built-in or custom evaluators.
- **Trace Visualization**: Seeing the full lifecycle of an AI request, from user input to multiple tool calls and final response.

## Strengths
- **Low Effort**: Easy integration with popular AI frameworks like LangChain and LlamaIndex.
- **Holistic View**: Connects AI metrics with the underlying infrastructure (CPU, Memory, Network).
- **Security & Privacy**: Features to redact PII from logs before they are stored.

## Limitations
- **Proprietary**: High level of vendor lock-in compared to OpenTelemetry-based solutions.
- **Cost**: Can become expensive as data volume and number of users increase.

## When to use it
- When you need a "batteries-included" observability solution for your AI stack.
- When you are already a New Relic customer and want to extend monitoring to LLMs.

## When not to use it
- If you have a strict preference for open-source observability tools.

## Licensing and cost
- **Open Source**: No (Proprietary).
- **Cost**: Paid (usage-based).
- **Self-hostable**: No.

## Getting started

### Installation
For Python applications, install the New Relic agent and the AI monitoring package:
```bash
pip install newrelic
```

### Example: Monitoring a LangChain Application
Initialize the agent at the very beginning of your application:
```python
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from langchain_openai import ChatOpenAI

# The New Relic agent automatically instruments supported libraries like LangChain
llm = ChatOpenAI(model_name="gpt-4o")
response = llm.invoke("What is the Model Context Protocol?")
```

### Viewing Results
Metrics such as token count, response time, and cost are automatically sent to the New Relic "AI Monitoring" dashboard, where you can view performance by model and individual request traces.

## Related tools / concepts
- [Datadog](datadog.md)
- [Grafana Cloud](grafana-cloud.md)
- [Langfuse](langfuse.md)
- [Arize Phoenix](arize-ai.md)
- [Parea](parea.md)

## Sources / References
- [New Relic AI Monitoring](https://newrelic.com/products/ai-monitoring)
- [New Relic Documentation](https://docs.newrelic.com/)
- [New Relic Python Agent AI Guide](https://docs.newrelic.com/docs/apm/agents/python-agent/getting-started/introduction-new-relic-python/)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
