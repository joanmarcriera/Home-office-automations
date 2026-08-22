# Comet Opik

Comet Opik is an open-source platform designed for evaluating, testing, and monitoring LLM applications and autonomous multi-agent networks. In early 2027, Opik serves as a cornerstone of the "Evaluation-Driven Development" (EDD) workflow, providing software engineers with a highly performant, self-hostable alternative to proprietary observability suites for frontier models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro/Ultra**, **DeepSeek-V4**, and **Gemma 3**.

## What it is
Opik is a purpose-built LLM observability tool focusing on distributed tracing, automated prompt evaluation, and evaluation dataset management. It allows developers to capture the detailed semantic behavior of their agents, score outputs using specialized LLM-as-a-judge patterns, and manage production logging datasets for continuous iteration. It operates as an independent, lightweight, self-contained library for LLM-centric systems with full **FastMCP 3.1 Protocol** and OpenTelemetry integration.

## What problem it solves
Opik bridges the gap between a prompt working once in a sandbox playground and it working reliably and safely at scale in production. It provides the core tracing infrastructure to catch regressions, quantify performance improvements across model upgrades (e.g., transitioning from Claude 4.8 to Claude 5.1 or DeepSeek-V3 to V4), and debug nested agentic reasoning steps by visualizing the exact data flow between an agent and its tools via Agentic Session Orchestration.

## Where it fits in the stack
**Category**: Process & Understanding / Observability
Opik acts as the "Flight Recorder" for generative AI applications. It sits alongside agent runtimes (such as LangChain, AutoGen, or CrewAI) and publishes structured telemetry spans to either a local self-hosted instance or the Comet cloud, leveraging FastMCP 3.1 for low-latency tool discovery and high-throughput logging.

## Typical use cases
- **Unit Testing for Prompts**: Running "Golden Sets" of evaluation datasets through system prompts and scoring them automatically in CI pipelines.
- **Production Flight Recording**: Capturing every interaction with Claude 5.1, GPT-5.5, DeepSeek-V4, or Gemini 4.0 to identify failure modes and outlier inputs.
- **Experiment and Iteration Tracking**: Comparing multiple retrieval-augmented generation (RAG) strategies to determine which indexing method yields superior factual grounding.
- **Robustness Red-Teaming**: Managing datasets of adversarial prompts and evaluating model safety/toxicity compliance.

## Strengths
- **Fully Self-Hostable**: Can be run entirely on-premise or within private clouds via Docker/Kubernetes, ensuring 100% data privacy for enterprise workloads.
- **FastMCP 3.1 Protocol Support**: Dynamic tool registration and low-latency tracing optimized for autonomous agent workflows.
- **Pre-Built Scorers**: Out-of-the-box evaluators for common metrics such as answer relevance, faithfulness, factual correctness, hallucination, and toxicity.
- **Comet Ecosystem Syncing**: Seamless integration with Comet ML's traditional machine learning experiment tracker for a comprehensive AI lifecycle overview.
- **Standardized Task Protocol**: Adherence to the FastMCP 3.1 Task Protocol for automated benchmarking and execution.

## Limitations
- **Storage Management Overhead**: When self-hosting, the engineering team is fully responsible for configuring and scaling the underlying databases (PostgreSQL/ClickHouse) for high-frequency logs.
- **Sampling Overhead**: High-frequency real-time tracing of O5 reasoning series steps requires aggressive sampling configuration to limit ClickHouse storage growth.

## When to use it
- When you require a developer-centric, open-source LLM observability and tracing engine that can be run on local machines or private servers.
- When building multi-agent pipelines requiring high-fidelity nested execution visualization and debugging.
- When you want a single, unified workflow that handles both early developer experimentation and production monitoring.

## When not to use it
- For basic or small scale scripts where raw console print statements are sufficient for tracking model behavior.
- If you require a fully managed SaaS and do not want to use the Comet cloud platform or maintain self-hosted infrastructure.

## Getting started

Install the Opik SDK client and Pydantic v2:

```bash
pip install opik pydantic>=2.0.0
```

Configure your environment connection:

```bash
opik configure
```

## CLI examples

### opik harbor run
Executes an evaluation benchmark suite against an active agent using the FastMCP 3.1 Task Protocol:
```bash
opik harbor run -d reasoning-bench -a my-gemma-agent
```

### opik configure
Initializes the SDK defaults, API keys, and server project mappings:
```bash
opik configure --api-key YOUR_COMET_OPIK_API_KEY --project support-agent-evaluation
```

### docker-compose up
Starts the local Opik server, including database storage containers:
```bash
docker-compose -f opik-docker-compose.yml up -d
```

## API examples

### Python (Evaluation Scoring with Pydantic v2 & FastMCP 3.1)
This example shows how to track and score model responses programmatically using Opik while enforcing strict type validation through Pydantic v2:

```python
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError
from opik import track

# Define structured telemetry and evaluation schemas using Pydantic v2
class EvaluationResult(BaseModel):
    test_case_id: str = Field(..., description="The ID of the tested evaluation case.")
    prompt_version: str = Field(..., description="Commit hash or version identifier of the prompt.")
    faithfulness_score: float = Field(..., ge=0.0, le=1.0, description="Evaluated factual grounding score.")
    model_name: str = Field(default="claude-5.1-sonnet", description="Model evaluated.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata matching FastMCP 3.1 context.")

class AgentSpan(BaseModel):
    span_id: str = Field(..., description="Unique trace identifier.")
    tool_calls: List[str] = Field(default_factory=list, description="List of tool names invoked.")
    status: str = Field(default="success")

# Use track decorator to instrument traces programmatically
@track
def execute_agent_tool(tool_name: str, args: Dict[str, Any]) -> str:
    # Simulates a FastMCP 3.1 tool call
    print(f"Executing tool {tool_name} with arguments: {args}")
    return f"Result of {tool_name}"

@track
async def run_evaluated_agent(task_query: str, eval_config: Dict[str, Any]) -> str:
    # Auto-validate incoming configuration utilizing Pydantic v2 model_validate
    validated_eval = EvaluationResult.model_validate(eval_config)

    # Nested trace spans are automatically handled by Opik's @track decorator
    search_output = execute_agent_tool(
        tool_name="web_search",
        args={"query": task_query, "mcp_version": "3.1"}
    )

    response = f"Answer to query: {search_output}"
    print(f"Agent finished evaluating. Model: {validated_eval.model_name}")
    return response

# Execution Simulation
mock_eval_config = {
    "test_case_id": "tc_0182_grounding",
    "prompt_version": "v5.1.2-beta",
    "faithfulness_score": 0.98,
    "model_name": "claude-5.1-sonnet",
    "metadata": {
        "fastmcp_active": True,
        "environment": "ci-pipeline"
    }
}

asyncio.run(run_evaluated_agent("What are the core updates in FastMCP 3.1?", mock_eval_config))
```

## Related tools / concepts
- [Arize AI](./arize-ai.md) — Enterprise-grade model performance management (MPM) and Arize Phoenix.
- [Braintrust](./braintrust.md) — Evaluation-driven LLM developer platform and trace logs.
- [Langfuse](./langfuse.md) — Open-source LLM analytics and tracing framework.
- [LangSmith](../benchmarking/langsmith.md) — Industry-standard evaluation framework for LangChain-built systems.
- [PostHog](./posthog.md) — General product analytics platform containing specialized LLM tracing tools.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Universal protocol for agent capabilities (FastMCP 3.1).
- [LiteLLM](../../services/litellm.md) — Unified inference gateway often providing Opik's stream logging.
- [ClickHouse](./clickhouse.md) — High-throughput relational database used to store local Opik traces.

## Sources / references
- [Comet Opik Official Documentation Portal](https://www.comet.com/docs/opik/)
- [Comet Opik Official GitHub Repository](https://github.com/comet-ml/opik)
- [Open-Source LLM Observability & Testing Best Practices](https://www.comet.com/site/blog/opik-open-source-llm-observability/)
- [FastMCP 3.1 Specification & Task Guidelines](https://modelcontextprotocol.io/specification)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
