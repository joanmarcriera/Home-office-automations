# LastMile AI

LastMile AI is a specialized platform for the evaluation and reliability engineering of LLM-based applications. In the early 2027 AI stack, it is recognized for its "Evaluation as a Service" (EaaS) model, which provides high-fidelity, automated scoring for the reasoning outputs of frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Llama 4, Gemma 4, and Qwen 3.6 VL.

## What it is
LastMile AI is a comprehensive evaluation workspace that allows developers to design, run, and analyze complex AI test suites. Its primary innovation is the **AI Auto-Eval** framework, which uses specialized "judge" models to grade application outputs on criteria such as factuality, instruction adherence, and safety. By early 2027, it has fully integrated with the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**, enabling it to evaluate not just final outputs, but the high-speed, intermediate tool-use steps and task execution of autonomous agents using the **MCP 3.1 Task Protocol**.

## What problem it solves
It solves the "scalability bottleneck" of manual evaluation. As AI systems become more complex and autonomous, humans can no longer review every response for quality. LastMile AI provides a systematic, repeatable way to measure the impact of changes to prompts, RAG retrieval parameters, or model versions, ensuring that performance improvements in one area don't cause regressions in another.

## Architecture & System Flow

```
+-----------------------------------------------------------------------------------+
|                            AI Application / Agent System                          |
|             (RAG Pipeline / FastMCP 3.1 Agent / Prompt System Prompts)            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  Tool Executions & Prompts
+-----------------------------------------+-----------------------------------------+
|                                  LastMile AI Engine                               |
|                                                                                   |
|  +-----------------------------------+   +-------------------------------------+  |
|  |     RAG Faithfulness Evaluator    |   |     FastMCP Tool Trace Evaluator    |  |
|  |  - Groundedness Scoring           |   |  - Argument Correctness Check       |  |
|  |  - Context Recall Verification    |   |  - Execution Latency SLA Check      |  |
|  +-----------------+-----------------+   +------------------+------------------+  |
|                    |                                        |                     |
|                    +--------------------+-------------------+                     |
|                                         |                                         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  Grading & Telemetry Outputs
+-----------------------------------------------------------------------------------+
|                         CI/CD Quality Gate / Dashboard Report                     |
|              (Pydantic v2 Schema Validation, ClickHouse Telemetry, Reports)       |
+-----------------------------------------------------------------------------------+
```

### Async FastMCP Evaluation Sequence
The detailed runtime sequence between FastMCP 3.1 tool agents, the LastMile evaluation engine, and judge models during continuous quality gates:

```
+-------------------------------------------------------------------------------------------------------+
|                                  LASTMILE AI FASTMCP EVALUATION SEQUENCE                              |
+-------------------------------------------------------------------------------------------------------+
  FastMCP Agent Worker            LastMile AI Evaluator Core         Judge LLM Service         CI/CD Quality Gate
           |                                  |                              |                       |
           |--- 1. Post Tool Trace ---------->|                              |                       |
           |    (Prompt, Tool Calls, Output)  |--- 2. Parse Evaluation Suite |                       |
           |                                  |       & Metric Thresholds    |                       |
           |                                  |                              |                       |
           |                                  |--- 3. Prompt Grounding Check------------>|           |
           |                                  |<-- 4. Faithfulness Score (0.0-1.0) -------|           |
           |                                  |                              |                       |
           |                                  |--- 5. Tool Call Argument Audit --------->|           |
           |                                  |<-- 6. Correctness Evaluation ------------|           |
           |                                  |                              |                       |
           |                                  |--- 7. Generate Evaluation Summary Report ------------>|
           |                                  |       (Pass / Fail SLA Status)                       |
           |<-- 8. Return Eval ID & Metrics --|                                                      |
```

## Where it fits in the stack
**Category**: Process & Understanding / AI Evaluation.
LastMile AI fits into the **Validation and Testing** layer of the AI lifecycle. It typically sits between the development environment and the production deployment, serving as a quality gate in the CI/CD pipeline.

## Feature Comparison Matrix

| Feature / Dimension | LastMile AI | Ragas | Braintrust | LangSmith |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Evaluation-as-a-Service (EaaS) & Agent Traces | Open-Source RAG Metrics Library | Enterprise AI Eval & Observability | LangChain Ecosystem Observability |
| **FastMCP 3.1 Support**| Native FastMCP Tool Trace Evaluation | Custom Adapter Required | Custom Telemetry Hook | Custom Trace Adapter |
| **Deployment Model** | Managed Cloud & VPC | Self-Hosted Python Package | Managed Cloud & Enterprise VPC | Managed Cloud & Enterprise Self-Host |
| **CLI Capabilities** | Rich CLI for Local Execs & CI/CD | Python Library Scripting | Python / TS SDK Integrations | CLI & Web UI Tracing |
| **Auto-Eval Judges** | Pre-built Fine-Tuned Judge Models | LLM Prompt-Based Judges | Multi-Model Judge Suite | Custom LLM Prompt Judges |
| **Schema Enforcement** | Strict Pydantic v2 Contract Validation | Dataclass / Dictionary | Custom TypeScript / Py Schemas | LangChain Pydantic Integration |

## Typical use cases
- **Golden Set Benchmarking**: Running every version of a system prompt against a curated set of "perfect" answers to measure accuracy.
- **RAG Quality Assessment**: Measuring the "grounding" of a response (does the answer only use the provided context?) and "retrieval relevance" using advanced judges.
- **Agentic Logic Validation**: Evaluating whether an agent selected the correct tool and used the correct arguments for a given task.
- **Red Teaming at Scale**: Automatically generating adversarial inputs to test the safety guardrails of a production model.
- **Model Comparison (e-vals)**: Running a head-to-head comparison between GPT-5.6, Claude 5.6, Llama 4, and [Gemma 4](../ai_knowledge/local_llms.md) on domain-specific data.
- **FastMCP Benchmarking**: Measuring the latency and reliability of tool-use sequences in ultra-low latency agentic sessions running FastMCP 3.1 servers.

## Strengths
- **Library of Evaluators**: Dozens of pre-built, science-backed evaluators for common metrics like NER, sentiment, faithfulness, and hallucination detection.
- **Developer-First CLI**: A powerful command-line interface that allows for running evaluations directly from local code or CI/CD pipelines.
- **Deep RAG Support**: Specialized tools for evaluating the entire RAG pipeline, from retrieval to synthesis.
- **Visualization Dashboard**: High-quality visual reports that highlight exactly where a model failed a specific evaluation.

## Limitations
- **Cost of Judges**: Running automated evaluations using frontier models (as judges) can incur significant token costs.
- **Complexity of Setup**: Defining robust "Golden Sets" and custom evaluators requires a structured approach to data engineering.

## Systemd Evaluator Daemon Configuration

To run LastMile evaluation workers continuously as background daemons in CI/CD self-hosted runner environments:

```ini
[Unit]
Description=LastMile AI FastMCP Evaluation Daemon
After=network.target
Documentation=https://docs.lastmileai.dev/

[Service]
Type=simple
User=lastmile
Group=lastmile
WorkingDirectory=/opt/lastmile-eval
ExecStart=/opt/lastmile-eval/venv/bin/python3 -m lastmile.eval_server
Restart=always
RestartSec=3s
Environment=PATH=/opt/lastmile-eval/venv/bin:/usr/local/bin:/usr/bin
Environment=LASTMILE_API_TOKEN=/etc/lastmile/token
Environment=EVAL_PORT=8095
Environment=PYTHONUNBUFFERED=1
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## When to use it
- When you are building production-ready RAG applications where accuracy and safety are non-negotiable.
- When you need to provide stakeholders with quantitative evidence of AI performance improvements.
- When you want to implement automated "judge" patterns without building your own evaluation infrastructure.

## When not to use it
- For early-stage "vibe check" prototyping where manual inspection of a few outputs is sufficient.
- If you are building a simple chatbot with no retrieval or complex logic that doesn't require rigorous testing.

## Getting started

Install the LastMile Python client:

```bash
pip install lastmile-ai pydantic fastmcp
```

Configure your API credentials:

```python
import os
os.environ["LASTMILE_API_TOKEN"] = "YOUR_TOKEN"
```

## CLI examples

### lastmile eval run
Executes a pre-defined evaluation suite and outputs results to the terminal:
```bash
lastmile eval run --suite "customer-support-golden-set" --model "gpt-5.6"
```

### lastmile dataset upload
Uploads a local dataset (CSV/JSONL) to be used for evaluations:
```bash
lastmile dataset upload ./data/test_cases.jsonl --name "mcp-tool-use-cases"
```

### lastmile login
Authenticates the CLI with your LastMile AI account:
```bash
lastmile login
```

## API examples

### FastMCP 3.1 Tool Evaluation Integration Pattern
Expose LastMile AI evaluation suite checks as an MCP tool for developer agents:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Dict, Any, List

mcp = FastMCP("lastmile-eval-mcp")

class EvalSuiteInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    suite_name: str = Field(..., description="Name of the LastMile golden evaluation suite")
    model_name: str = Field(..., description="Target model name evaluated")
    sample_limit: int = Field(default=10, ge=1, le=100)

    @field_validator("suite_name")
    @classmethod
    def validate_suite_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("suite_name cannot be empty")
        return v

class EvalSuiteOutput(BaseModel):
    model_config = ConfigDict(extra="ignore")

    suite_name: str
    pass_rate: float = Field(..., ge=0.0, le=1.0)
    faithfulness_score: float = Field(..., ge=0.0, le=1.0)
    status: str

@mcp.tool()
def run_lastmile_suite(input_data: EvalSuiteInput) -> EvalSuiteOutput:
    """Runs a LastMile AI evaluation suite against a target model output."""
    # Simulated connection to LastMile AI Evaluation API
    return EvalSuiteOutput(
        suite_name=input_data.suite_name,
        pass_rate=0.95,
        faithfulness_score=0.98,
        status="PASSED"
    )

if __name__ == "__main__":
    mcp.run()
```

### Python (Auto-Evaluating RAG Grounding and FastMCP 3.1 Tool Traces)
The following example demonstrates how to parse and strictly validate LastMile evaluation results using **Pydantic v2**:

```python
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ToolCallEvaluation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tool_name: str = Field(..., description="The name of the tool called by the agent.")
    arguments: Dict[str, Any] = Field(..., description="The parameters passed to the tool.")
    is_correct: bool = Field(..., description="Whether the tool selection and arguments were correct.")
    latency_ms: float = Field(..., ge=0.0, description="Execution latency of the tool call.")

class RAGEvalMetrics(BaseModel):
    model_config = ConfigDict(extra="ignore")

    faithfulness: float = Field(..., ge=0.0, le=1.0, description="Response is fully grounded in the context.")
    answer_relevance: float = Field(..., ge=0.0, le=1.0, description="The response directly answers the user prompt.")
    context_recall: float = Field(..., ge=0.0, le=1.0, description="The retrieved context contains the ground truth info.")

class LastMileEvalResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    eval_id: str = Field(..., description="Unique evaluation session ID.")
    target_model: str = Field(..., description="The frontier model evaluated (e.g., Claude 5.6, GPT-5.6).")
    prompt: str = Field(..., description="Input query submitted to the model.")
    response: str = Field(..., description="Output generated by the model.")
    metrics: RAGEvalMetrics = Field(..., description="RAG and alignment metrics.")
    tool_calls_trace: List[ToolCallEvaluation] = Field(default_factory=list, description="Trace of FastMCP 3.1 tool calls.")

    @field_validator("target_model")
    @classmethod
    def validate_target_model(cls, v: str) -> str:
        allowed = ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra", "Llama 4", "Gemma 4", "Qwen 3.6 VL"]
        if not any(model in v for model in allowed):
            raise ValueError(f"Target model must be an early 2027 frontier model: {allowed}")
        return v

raw_api_response = {
    "eval_id": "eval-99128-mcp",
    "target_model": "Claude 5.6",
    "prompt": "What are the specs of the 2027 Model X?",
    "response": "The 2027 Model X features a 120kWh battery and dual motors.",
    "metrics": {
        "faithfulness": 0.98,
        "answer_relevance": 1.0,
        "context_recall": 1.0
    },
    "tool_calls_trace": [
        {
            "tool_name": "fetch_car_specs",
            "arguments": {"model": "Model X", "year": 2027},
            "is_correct": True,
            "latency_ms": 145.2
        }
    ]
}

if __name__ == "__main__":
    try:
        eval_report = LastMileEvalResult.model_validate(raw_api_response)
        print(f"Successfully validated LastMile Eval ID: {eval_report.eval_id}")
        print(f"Target Model: {eval_report.target_model}")
        print(f"Faithfulness Score: {eval_report.metrics.faithfulness}")
        print(f"Tool Selection Correctness: {eval_report.tool_calls_trace[0].is_correct}")
    except Exception as e:
        print(f"Validation failed: {e}")
```

## Diagnostic Troubleshooting Matrix

| Symptom / Error | Potential Root Cause | Verification Command | Resolution Step |
| :--- | :--- | :--- | :--- |
| `HTTP 401 Invalid Token` | Missing or expired `LASTMILE_API_TOKEN` | `lastmile login --check` | Set `LASTMILE_API_TOKEN` environment variable or re-authenticate via CLI. |
| Low Faithfulness Score (<0.7) | RAG Context retrieval containing irrelevant chunks | `lastmile eval trace --eval-id <ID> --verbose` | Adjust chunk size, increase top-k vector retrieval, or refine query expansion prompts. |
| FastMCP Trace Eval Failure | Mismatch between expected tool argument types and trace | `python3 -c "import lastmile; print(lastmile.__version__)"` | Verify tool schema definition and update FastMCP tool parameters to conform to Pydantic models. |
| Judge LLM Timeout in CI/CD | High payload concurrency exceeding rate limits on Judge API | `systemctl status lastmile-eval.service` | Decrease worker batch concurrency or configure secondary fallback judge endpoints. |

## Related tools / concepts
- [Ragas](./ragas.md) — Open-source framework for RAG evaluation.
- [Promptfoo](../benchmarking/promptfoo.md) — CLI tool for testing prompts.
- [Braintrust](./braintrust.md) — Evaluation and observability platform.
- [Arize AI](./arize-ai.md) — Observability and MPM platform with Phoenix.
- [LangSmith](../benchmarking/langsmith.md) — Part of the LangChain ecosystem for evaluation.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for agent tool-use, which LastMile can evaluate.
- [Glaive](../ai_knowledge/glaive.md) — Synthetic data provider often used to generate evaluation sets.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) — Target for logic and tool-use evaluation.
- [Gemma 4](../ai_knowledge/local_llms.md) — Key target for local model evaluation and reliability engineering.
- [Comet Opik](./comet-opik.md) — Open-source evaluation platform with deep integration for agentic logic.

## Sources / references
- [LastMile AI Official Website](https://lastmileai.dev/)
- [LastMile AI Documentation](https://docs.lastmileai.dev/)
- [AI Evaluation Best Practices (2027)](https://lastmileai.dev/blog/eval-as-a-service-2027)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
