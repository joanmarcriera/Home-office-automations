# New Relic AI

## What it is
New Relic AI (part of the New Relic Intelligent Observability platform) is a specialized observability solution for monitoring LLM-powered applications. It provides "one-click" visibility into AI performance and quality, integrated with the broader New Relic ecosystem. It is a proprietary, usage-based SaaS offering that is not self-hostable.

## What problem it solves
It addresses the unique challenges of AI monitoring, such as tracking non-deterministic outputs, monitoring "hallucinations," and managing LLM costs across multiple providers. It bridges the gap between infrastructure metrics and AI application logic, especially as complexity grows with **Claude 4.8** and **GPT-5.5** deployments.

## Where it fits in the stack
**Observability / Eval**. It competes with [Grafana Cloud](grafana-cloud.md) and [Langfuse](langfuse.md) as a primary observability platform for production AI within the **Governance & Monitoring** layer.

## Typical use cases
- **LLM Performance Monitoring**: Tracking response times and token usage across different models like **Claude 4.8** or **GPT-5.5**.
- **Quality Analysis**: Measuring output quality and relevance using built-in or custom evaluators.
- **Trace Visualization**: Seeing the full lifecycle of an AI request, from user input to multiple tool calls and final response.
- **Cost Management**: Real-time tracking of LLM spend with per-user or per-project attribution.

## Strengths
- **Low Effort**: Easy integration with popular AI frameworks like [LangChain](../frameworks/langchain.md) and [LlamaIndex](../frameworks/llamaindex.md).
- **Holistic View**: Connects AI metrics with the underlying infrastructure (CPU, Memory, Network).
- **Security & Privacy**: Features to redact PII from logs before they are stored.
- **Native MCP 3.0 Support**: Official Model Context Protocol server for direct AI assistant interaction.

## Limitations
- **Proprietary**: High level of vendor lock-in compared to OpenTelemetry-based solutions.
- **Cost**: Can become expensive as data volume and number of users increase; usage-based pricing requires careful monitoring.
- **Regional Constraints**: Some AI monitoring features may vary between US and EU regions.

## When to use it
- When you need a "batteries-included" observability solution for your AI stack.
- When you are already a New Relic customer and want to extend monitoring to LLMs.
- When you want to leverage official [MCP](../automation_orchestration/mcp.md) tools for debugging production AI systems.

## When not to use it
- If you have a strict preference for open-source observability tools like [Prometheus](../../reference-implementations/k8s-infrastructure/monitoring/prometheus-grafana-values.yaml).
- For small-scale experiments where lightweight tools like [Arize Phoenix](arize-ai.md) or [LLMware](../automation_orchestration/llmware.md) are sufficient.

## Getting started

### Installation
For Python applications, install the New Relic agent:

```bash
pip install newrelic
```

### Basic Configuration
1. Obtain your `NEW_RELIC_LICENSE_KEY` from the New Relic dashboard.
2. Initialize the agent at the very beginning of your application.

```bash
# Set environment variables
export NEW_RELIC_LICENSE_KEY="your_key"
export NEW_RELIC_APP_NAME="AI-App-01"
```

### Model Context Protocol (MCP) Integration
New Relic provides an official **MCP Server** that allows AI assistants like **Claude Code** to query your telemetry data directly. Add the following to your `mcp.json`:

```json
{
  "mcpServers": {
    "new-relic": {
      "command": "uvx",
      "args": ["mcp-newrelic"],
      "env": {
        "NEW_RELIC_API_KEY": "your_api_key",
        "NEW_RELIC_ACCOUNT_ID": "your_account_id",
        "NEW_RELIC_REGION": "US"
      }
    }
  }
}
```

## CLI examples

### Recording a Deployment
```bash
newrelic-admin record-deploy --user="admin" --revision="v1.2.3" "AI Agent Service"
```

### Validating Configuration
```bash
newrelic-admin validate-config newrelic.ini
```

### Checking Agent Status
```bash
newrelic-admin server-config
```

## API examples

### Monitoring a LangChain Application
The New Relic agent automatically instruments [LangChain](../frameworks/langchain.md) when initialized.

```python
import newrelic.agent
newrelic.agent.initialize()

from langchain_openai import ChatOpenAI

# LLM metrics for GPT-5.5 will be automatically captured
llm = ChatOpenAI(model_name="gpt-5.5")
response = llm.invoke("Summarize the Llama 4 Maverick architecture.")
```

### Querying Metrics via NRQL
```python
import requests

API_URL = "https://insights-api.newrelic.com/v1/accounts/YOUR_ACCOUNT_ID/query"
API_KEY = "YOUR_QUERY_KEY"

headers = {
    "X-Query-Key": API_KEY,
    "Accept": "application/json"
}

nrql = "SELECT average(llm.response.time) FROM Transaction WHERE appName = 'AI-App-01' SINCE 1 day ago"
params = {'nrql': nrql}

response = requests.get(API_URL, headers=headers, params=params)
print(response.json())
```

## Related tools / concepts
- [Datadog](datadog.md)
- [Grafana Cloud](grafana-cloud.md)
- [Langfuse](langfuse.md)
- [Arize Phoenix](arize-ai.md)
- [Parea](parea.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [LangChain](../frameworks/langchain.md)
- [LlamaIndex](../frameworks/llamaindex.md)
- [Prometheus](../../reference-implementations/k8s-infrastructure/monitoring/prometheus-grafana-values.yaml)

## Sources / references
- [New Relic AI Monitoring Official Site](https://newrelic.com/products/ai-monitoring)
- [New Relic MCP Server Guide](https://docs.newrelic.com/docs/apis/mcp-server/)
- [Monitoring Llama 4 Maverick with New Relic](https://docs.newrelic.com/docs/observability/ai-monitoring/llama-4-guide/)
- [New Relic Python Agent AI Guide](https://docs.newrelic.com/docs/apm/agents/python-agent/getting-started/introduction-new-relic-python/)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
