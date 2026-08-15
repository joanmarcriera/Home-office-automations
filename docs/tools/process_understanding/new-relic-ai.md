# New Relic AI

## What it is
New Relic AI (part of the New Relic Intelligent Observability platform) is a specialized, enterprise-grade observability solution for monitoring large language model (LLM) applications and multi-agentic workflows. It provides "one-click" automated visibility into AI performance, security, and quality, seamlessly integrated with the broader New Relic Application Performance Monitoring (APM) ecosystem. It is a proprietary, usage-based SaaS offering that is not self-hostable.

## What problem it solves
It addresses the distinct challenges of production AI systems, including tracking non-deterministic model outputs, identifying token inefficiencies, detecting hallucinations or prompt injections, and managing spiraling LLM costs across highly distributed providers. By uniting system-level infrastructure telemetry with complex agent-level logic, New Relic AI gives developers complete visibility into system operations, especially as complexity grows with **Claude 5.1**, **GPT-5.5**, **Llama 4**, and **Gemini 4.0 Pro** deployments.

## Where it fits in the stack
**Observability / Eval**. It operates within the **Governance & Monitoring** layer of modern agentic frameworks, competing directly with enterprise platforms like [Datadog](datadog.md) and open-source or specialized alternatives such as [Grafana Cloud](grafana-cloud.md) and [Langfuse](langfuse.md).

## Typical use cases
- **LLM Performance Monitoring**: Real-time tracking of latency, response times, and token usage statistics across diverse model engines including **Claude 5.1**, **GPT-5.5**, and **Qwen 3.8**.
- **Quality and Bias Analysis**: Programmatically measuring output sentiment, quality, and semantic relevance using built-in or custom NLP evaluators.
- **Trace Visualization**: Visualizing full multi-turn agent execution runs, highlighting where slow tool calls, database fetches, or intermediate prompts introduce performance bottlenecks.
- **Cost Management**: Granular attribution of LLM spend on a per-user, per-organization, or per-agent-task basis to manage operational margins.

## Strengths
- **Low-Configuration Setup**: Automatic, zero-code instrumentation for major developer libraries including [LangChain](../ai_knowledge/langchain.md) and [LlamaIndex](../ai_knowledge/llamaindex.md).
- **Unified Telemetry**: Seamlessly correlates high-level AI application tracing with system-level infrastructure metrics (CPU, Memory, IO, Kubernetes health).
- **Security & PII Redaction**: Robust client-side filters and server-side rules to scrub sensitive personal data, API tokens, and credentials before persistent logging.
- **Native FastMCP 3.1 Support**: Features an official Model Context Protocol (FastMCP 3.1) server implementation enabling conversational AI assistants to query historical telemetry directly.

## Limitations
- **SaaS Vendor Lock-in**: Proprietary platform with significant egress and structural dependencies compared to pure OpenTelemetry frameworks.
- **Cost Scaling**: Volume-based and ingestion-heavy pricing requires defensive filtering to avoid surprise bills under heavy multi-agent production workloads.
- **Regional Disparities**: Select AI auditing and real-time security compliance tools may experience feature lag or restricted rollout in European and Asian regions.

## When to use it
- When you require a robust, enterprise-supported, out-of-the-box observability setup for complex multi-agent setups.
- When your engineering organization is already standardized on New Relic for traditional APM and wants to consolidate AI telemetry.
- When you want to leverage official [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers for live-debugging systems via terminal interfaces.

## When not to use it
- If your stack mandates fully open-source, local-first, or self-hosted telemetry tools (e.g., [Prometheus](../../reference-implementations/k8s-infrastructure/monitoring/prometheus-grafana-values.yaml) and [Grafana Cloud](grafana-cloud.md)).
- For localized prototype environments or tiny test scripts where lighter tools like [Arize Phoenix](arize-ai.md) or [Parea](parea.md) are sufficient.

## Getting started

### Installation
For Python application monitoring, install the latest New Relic agent package along with Pydantic v2:

```bash
pip install newrelic pydantic
```

### Basic Configuration
Set your license and configuration options using environment variables before running your main entrypoint:

```bash
# Set necessary environment variables
export NEW_RELIC_LICENSE_KEY="your_secure_license_key"
export NEW_RELIC_APP_NAME="Agent-Factory-Observability"
export NEW_RELIC_HOST="collector.newrelic.com"
```

### Model Context Protocol (FastMCP 3.1) Integration
New Relic's FastMCP server can be added directly to your standard `mcp-config.json` configuration block to expose logs to frontier agent engines:

```json
{
  "mcpServers": {
    "new-relic-mcp": {
      "command": "uvx",
      "args": ["mcp-newrelic"],
      "env": {
        "NEW_RELIC_API_KEY": "NRAK-XXXXXXXXXXXXXXXXXXXXX",
        "NEW_RELIC_ACCOUNT_ID": "1234567",
        "NEW_RELIC_REGION": "US",
        "MCP_PROTOCOL_VERSION": "3.1"
      }
    }
  }
}
```

## CLI examples

### Recording a Deployment
Record deployments to correlate performance shifts with specific model prompt adjustments:

```bash
newrelic-admin record-deploy \
  --user="ci-cd-pipeline" \
  --revision="release-v2.6.1-gpt5.5" \
  --description="Upgraded agent backbone to GPT-5.5 and added FastMCP 3.1 tools" \
  "Agent-Factory-Observability"
```

### Validating Configuration
Validate your local `.ini` configuration and test credentials directly:

```bash
newrelic-admin validate-config newrelic.ini
```

### Checking Agent Connection Status
Query connection state and local environment specifications:

```bash
newrelic-admin server-config
```

## API examples

### Monitoring a LangChain Application
The New Relic agent automatically intercepts calls to LangChain and extracts system and LLM metadata when initialized at the application root:

```python
import newrelic.agent
newrelic.agent.initialize()

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, ConfigDict


class AgentConfig(BaseModel):
    """Pydantic v2 validation schema for agent execution settings."""
    model_config = ConfigDict(str_strip_whitespace=True)

    model_name: str = Field(default="gpt-5.5", description="Target LLM model name.")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)


def run_monitored_langchain_agent(config: AgentConfig, user_prompt: str) -> str:
    # LLM metrics for GPT-5.5, Claude 5.1, and Llama 4 are captured autonomously by New Relic APM
    llm = ChatOpenAI(model_name=config.model_name, temperature=config.temperature)
    response = llm.invoke(user_prompt)
    return response.content


if __name__ == "__main__":
    cfg = AgentConfig(model_name="gpt-5.5", temperature=0.2)
    prompt = "Summarize late August 2026 SOTA changes in Model Context Protocol v3.1."
    print(f"Executing monitored LangChain call with model: {cfg.model_name}")
```

### Querying Metrics via NRQL
Use Python to execute custom New Relic Query Language (NRQL) requests to audit model performance programmatically:

```python
import requests
from pydantic import BaseModel, Field, ConfigDict


class NRQLQueryConfig(BaseModel):
    """Pydantic v2 schema for validating New Relic query parameters."""
    model_config = ConfigDict(str_strip_whitespace=True)

    account_id: str = Field(..., pattern=r"^\d+$", description="Numeric New Relic account ID.")
    api_key: str = Field(..., min_length=10, description="NRAK Query API key.")
    query: str = Field(..., min_length=10, description="NRQL query string.")


def query_telemetry_metrics(config: NRQLQueryConfig) -> dict:
    url = f"https://insights-api.newrelic.com/v1/accounts/{config.account_id}/query"
    headers = {
        "X-Query-Key": config.api_key,
        "Accept": "application/json"
    }
    params = {"nrql": config.query}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


if __name__ == "__main__":
    cfg = NRQLQueryConfig(
        account_id="1234567",
        api_key="NRAK-YYYYYYYYYYYYYYYYYYYYYY",
        query="SELECT average(llm.response.time) FROM Transaction WHERE appName = 'Agent-Factory-Observability' SINCE 1 week ago"
    )
    print(f"NRQL query configured for account: {cfg.account_id}")
```

## Related tools / concepts
- [Datadog](datadog.md) — Main enterprise SaaS monitoring alternative.
- [Grafana Cloud](grafana-cloud.md) — Open-source-friendly cloud metrics and logging.
- [Langfuse](langfuse.md) — Open-source LLM engineering and tracing platform.
- [Arize Phoenix](arize-ai.md) — Localized agent evaluation and tracking.
- [Parea](parea.md) — LLM evaluation and testing tool.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for model-tool interaction.
- [LangChain](../ai_knowledge/langchain.md) — Mainstream orchestration library.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Data-connective LLM framework.
- [Prometheus](../../reference-implementations/k8s-infrastructure/monitoring/prometheus-grafana-values.yaml) — Self-hosted time-series metrics.

## Sources / references
- [New Relic AI Monitoring Official Site](https://newrelic.com/products/ai-monitoring)
- [New Relic MCP Server Guide](https://docs.newrelic.com/docs/apis/mcp-server/)
- [Monitoring Llama 4 and Claude 5.1 with New Relic](https://docs.newrelic.com/docs/observability/ai-monitoring/llama-4-guide/)
- [New Relic Python Agent AI Guide](https://docs.newrelic.com/docs/apm/agents/python-agent/getting-started/introduction-new-relic-python/)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
