# LastMile AI

LastMile AI is a specialized platform for the evaluation and reliability engineering of LLM-based applications. In early January 2027, it is recognized for its "Evaluation as a Service" (EaaS) model, which provides high-fidelity, automated scoring for the reasoning outputs of SOTA frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, and Qwen 3.6 VL.

## What it is
LastMile AI is a comprehensive evaluation workspace that allows developers to design, run, and analyze complex AI test suites. Its primary innovation is the **AI Auto-Eval** framework, which uses specialized "judge" models to grade application outputs on criteria such as factuality, instruction adherence, and safety. By early 2027, it has fully integrated with the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**, enabling it to evaluate not just final outputs, but the high-speed, intermediate tool-use steps and task execution of autonomous agents using the **MCP 3.1 Task Protocol**.

## What problem it solves
It solves the "scalability bottleneck" of manual evaluation. As AI systems become more complex and autonomous, humans can no longer review every response for quality. LastMile AI provides a systematic, repeatable way to measure the impact of changes to prompts, RAG retrieval parameters, or model versions, ensuring that performance improvements in one area don't cause regressions in another.

## Where it fits in the stack
**Category**: Process & Understanding / AI Evaluation
LastMile AI fits into the **Validation and Testing** layer of the AI lifecycle. It typically sits between the development environment and the production deployment, serving as a quality gate in the CI/CD pipeline.

## Typical use cases
- **Golden Set Benchmarking**: Running every version of a system prompt against a curated set of "perfect" answers to measure accuracy.
- **RAG Quality Assessment**: Measuring the "grounding" of a response (does the answer only use the provided context?) and "retrieval relevance" using advanced judges.
- **Agentic Logic Validation**: Evaluating whether an agent selected the correct tool and used the correct arguments for a given task.
- **Red Teaming at Scale**: Automatically generating adversarial inputs to test the safety guardrails of a production model.
- **Model Comparison (e-vals)**: Running a head-to-head comparison between GPT-5.6, Claude 5.6, Gemini 4.0 Ultra, and [Gemma 4](../ai_knowledge/local_llms.md) on domain-specific data.
- **FastMCP Benchmarking**: Measuring the latency and reliability of tool-use sequences in ultra-low latency agentic sessions running FastMCP 3.1 servers.

## Strengths
- **Library of Evaluators**: Dozens of pre-built, science-backed evaluators for common metrics like NER, sentiment, faithfulness, and hallucination detection.
- **Developer-First CLI**: A powerful command-line interface that allows for running evaluations directly from local code or CI/CD pipelines.
- **Deep RAG Support**: Specialized tools for evaluating the entire RAG pipeline, from retrieval to synthesis.
- **Visualization Dashboard**: High-quality visual reports that highlight exactly where a model failed a specific evaluation.

## Limitations
- **Cost of Judges**: Running automated evaluations using frontier models (as judges) can incur significant token costs.
- **Complexity of Setup**: Defining robust "Golden Sets" and custom evaluators requires a structured approach to data engineering.

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
pip install lastmile-ai pydantic
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

### Python (Auto-Evaluating RAG Grounding and FastMCP 3.1 Tool Traces)
The following example demonstrates how to parse and strictly validate LastMile evaluation results using **Pydantic v2**:

```python
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define strict Pydantic v2 schemas for the evaluation payload
class ToolCallEvaluation(BaseModel):
    tool_name: str = Field(..., description="The name of the tool called by the agent.")
    arguments: Dict[str, Any] = Field(..., description="The parameters passed to the tool.")
    is_correct: bool = Field(..., description="Whether the tool selection and arguments were correct.")
    latency_ms: float = Field(..., description="Execution latency of the tool call.")

class RAGEvalMetrics(BaseModel):
    faithfulness: float = Field(..., ge=0.0, le=1.0, description="Response is fully grounded in the context.")
    answer_relevance: float = Field(..., ge=0.0, le=1.0, description="The response directly answers the user prompt.")
    context_recall: float = Field(..., ge=0.0, le=1.0, description="The retrieved context contains the ground truth info.")

class LastMileEvalResult(BaseModel):
    eval_id: str = Field(..., description="Unique evaluation session ID.")
    target_model: str = Field(..., description="The SOTA frontier model evaluated (e.g., Claude 5.6, GPT-5.6).")
    prompt: str = Field(..., description="Input query submitted to the model.")
    response: str = Field(..., description="Output generated by the model.")
    metrics: RAGEvalMetrics = Field(..., description="RAG and alignment metrics.")
    tool_calls_trace: List[ToolCallEvaluation] = Field(default_factory=list, description="Trace of FastMCP 3.1 tool calls.")

    @field_validator("target_model")
    @classmethod
    def validate_target_model(cls, v: str) -> str:
        allowed = ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra", "Llama 4", "Gemma 4", "Qwen 3.6 VL"]
        if not any(model in v for model in allowed):
            raise ValueError(f"Target model must be a SOTA early 2027 frontier model: {allowed}")
        return v

# 2. Example simulation of LastMile AutoEval API response with FastMCP 3.1 tracing
raw_api_response = {
    "eval_id": "eval-99128-mcp",
    "target_model": "Claude 5.6",
    "prompt": "What are the specs of the 2026 Model X?",
    "response": "The 2026 Model X features a 120kWh battery and dual motors.",
    "metrics": {
        "faithfulness": 0.98,
        "answer_relevance": 1.0,
        "context_recall": 1.0
    },
    "tool_calls_trace": [
        {
            "tool_name": "fetch_car_specs",
            "arguments": {"model": "Model X", "year": 2026},
            "is_correct": True,
            "latency_ms": 145.2
        }
    ]
}

# 3. Perform strict validation
try:
    eval_report = LastMileEvalResult(**raw_api_response)
    print(f"Successfully validated LastMile Eval ID: {eval_report.eval_id}")
    print(f"Target Model: {eval_report.target_model}")
    print(f"Faithfulness Score: {eval_report.metrics.faithfulness}")
    print(f"Tool Selection Correctness: {eval_report.tool_calls_trace[0].is_correct}")
except Exception as e:
    print(f"Validation failed: {e}")
```

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
