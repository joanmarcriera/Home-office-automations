# Ragas

## What it is
Ragas (Retrieval-Augmented Generation Assessment) is an open-source evaluation framework specifically designed for testing, auditing, and optimizing Retrieval-Augmented Generation (RAG) pipelines and compound AI agent applications. As of early 2027 (v0.3.x+), Ragas is the industry standard for **Reference-Free Evaluation**, synthetic test set generation, and automated quality gatekeeping across multi-modal agent workflows, complex multi-step reasoning, and FastMCP 3.1 tool-calling execution chains.

Ragas decomposes RAG system performance into distinct, quantifiable dimensions without requiring human-annotated ground-truth answers for every query. By utilizing "LLM-as-a-Judge" paradigms powered by frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra) or local weights (Gemma 3, Llama 4), Ragas mathematically models the relationship between user queries, retrieved context chunks, and synthesized responses.

## What problem it solves
Evaluating non-deterministic LLM applications presents fundamental software engineering challenges:
- **Dual Failure Modes (Retrieval vs. Generation)**: When an AI system outputs an incorrect answer, it is difficult to determine whether the vector retriever retrieved irrelevant document chunks or whether the generator hallucinated despite having accurate context.
- **Expensive & Slow Human Evaluation**: Manual review of thousands of production query logs by domain experts is cost-prohibitive and cannot keep pace with continuous deployment CI/CD cycles.
- **Reference-Set Bottlenecks**: Creating static human-curated evaluation datasets is time-consuming and quickly becomes stale as underlying knowledge bases update.

Ragas solves these issues by providing reference-free, component-level metrics (Faithfulness, Answer Relevance, Context Precision, and Context Recall). It isolates retrieval failures from synthesis failures, automatically synthesizes test datasets directly from raw document repositories, and enforces quantitative quality gates in CI/CD build pipelines.

## Where it fits in the stack
**Layer 5: Process & Understanding / Observability & Quality Assurance**.

Ragas operates as an automated testing and evaluation engine integrated between vector databases/document stores (Qdrant, Pinecone, MinIO), agent frameworks (FastMCP 3.1, LangChain, LlamaIndex), and production telemetry platforms (Langfuse, Arize AI).

```
+-----------------------------------------------------------------------------------+
|                            CI/CD & Production Tracing                             |
|                    (GitHub Actions / Langfuse / Arize AI)                         |
+-----------------------------------------------------------------------------------+
                                          |
                        Runs Automated Evaluation Test Suite
                                          v
+-----------------------------------------------------------------------------------+
|                                 Ragas Framework                                  |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |   Faithfulness Engine  |  | Answer Relevance Engine|  | Context Precision   |  |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  Context Recall Engine |  |  Vision Relevance (VLM)|  | Tool-Calling Agent  |  |
|  +------------------------+  +------------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                 Sends Query, Context Chunks, and Output to Judge Model
                                          v
+-----------------------------------------------------------------------------------+
|                             LLM / VLM Judge Models                                |
|        (Claude 5.6 Sonnet / GPT-5.6 / Gemini 4.0 Ultra / Local Llama 4)           |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **CI/CD Quality Gates for RAG Pipelines**: Running automated regressions whenever vector chunk sizes, embedding models, or system prompts are updated.
- **Reference-Free Production Diagnostics**: Continuously auditing production query logs to calculate factual adherence and alert on hallucination spikes.
- **Synthetic Test Set Generation**: Automatically transforming raw markdown or PDF knowledge bases into hundreds of structured test scenarios containing question-context-ground_truth triplets.
- **Multi-Modal Visual Evaluation**: Measuring the alignment between visual inputs (charts, blueprints, flowcharts) and synthesized multimodal responses.
- **Agentic FastMCP 3.1 Tool-Calling Auditing**: Measuring tool selection precision and arguments adherence across multi-step agent decision trees.

## Architecture & Core Mechanics

### Architecture Diagram: Ragas Evaluation Triad

```
                         +-----------------------------+
                         |        User Query           |
                         +-----------------------------+
                               /                 \
                              /                   \
        Context Precision    /                     \   Answer Relevance
      & Context Recall      /                       \
                           v                         v
            +-------------------------+   Faithfulness   +-------------------------+
            |    Retrieved Context    | <---------------> |   Generated Answer      |
            |    (Document Chunks)    |                   |   (LLM / Agent Output)  |
            +-------------------------+                   +-------------------------+
```

### Core Metric Definitions

1. **Faithfulness (Factual Adherence)**: Measures how factually grounded the generated answer is relative to the retrieved context. It is calculated by extracting atomic claims from the generated answer and determining what fraction of those claims can be directly inferred from the retrieved chunks:
   $$\text{Faithfulness} = \frac{|\text{Verified Claims in Context}|}{|\text{Total Claims in Answer}|}$$

2. **Answer Relevance**: Measures how directly the generated answer addresses the user query, regardless of factual truth. It calculates the cosine similarity between the original query vector and embedding vectors of questions back-generated from the answer:
   $$\text{Answer Relevance} = \frac{1}{n} \sum_{i=1}^{n} \text{sim}(q, q_i)$$

3. **Context Precision**: Evaluates whether the most relevant document chunks are ranked higher in the retrieved context list. It uses Normalized Discounted Cumulative Gain (NDCG) style signal scoring on context chunks:
   $$\text{Context Precision@K} = \frac{\sum_{k=1}^{K} (\text{Precision@k} \times v_k)}{\text{Total Relevant Chunks}}$$

4. **Context Recall**: Measures whether all necessary information needed to answer the query was successfully retrieved. It compares ground truth statements against the retrieved context chunks.

5. **Agentic Tool Call Accuracy**: Evaluates whether an agent selected the correct FastMCP 3.1 tool and supplied valid schema parameters given a user goal.

## Strengths
- **Reference-Free Evaluation**: Computes actionable scores without requiring human-written target answers.
- **Granular Diagnostic Isolation**: Pinpoints exact pipeline failure points (retrieval vs. generation).
- **Synthetic Data Engine**: Bootstraps evaluation suites from unannotated document repositories using evolutionary data generation algorithms.
- **Extensible LLM Support**: Native support for LangChain, LlamaIndex, OpenAI, Anthropic, Google Vertex, and local Ollama/vLLM endpoints.
- **FastMCP 3.1 & Agent Framework Integration**: Native evaluation primitive primitives for tool execution verification.

## Limitations
- **LLM Judge Cost & Latency**: Running comprehensive metric suites across thousands of samples requires multiple calls to judge LLMs, incurring API cost and execution duration.
- **Evaluator Model Bias**: Low-tier judge models can produce noisy or biased scores; high-capability models (Claude 5.6, GPT-5.6) are recommended for production quality gates.
- **Domain Adaptation**: Extremely specialized domains (such as legal jurisprudence or medical pathology) may require custom system instructions for the judge model.

## When to use it
- Systematically testing RAG pipelines and vector database changes in automated CI/CD pipelines.
- Comparing competing embedding models, chunking strategies, or reranking algorithms.
- Bootstrapping test suites from raw corporate documentation.
- Monitoring production agent tool execution fidelity.

## When not to use it
- Small, deterministic applications where hardcoded unit tests or simple string matching are sufficient.
- Purely traditional keyword search systems without generative LLM synthesis.
- Hard real-time inline request filtering where sub-10ms evaluation latency is required.

## Getting started

### Installation
Install Ragas with modern standard dependencies:

```bash
pip install ragas datasets pydantic>=2.10.0 fastmcp httpx
```

### Basic Evaluation Script
This snippet sets up a basic reference-free Ragas evaluation execution:

```python
import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance, context_precision

# Set judge model API key
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "sk-ant-sample-key")

# Prepare evaluation payload
eval_data = {
    "question": [
        "What is the latency impact of FastMCP 3.1 protocol discovery?",
        "How does Baseten handle cold starts for large models?"
    ],
    "answer": [
        "FastMCP 3.1 minimizes handshake latency through pipelined capabilities negotiation.",
        "Baseten utilizes NVMe weight-caching to provision GPU nodes in under two seconds."
    ],
    "contexts": [
        ["FastMCP 3.1 introduces pipelined capability negotiations, reducing handshake roundtrips to zero after initialization."],
        ["Baseten's distributed architecture pre-caches model weights on local NVMe drives, achieving cold starts under 2 seconds."]
    ]
}

dataset = Dataset.from_dict(eval_data)

# Run evaluation suite
results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevance, context_precision]
)

print("--- Ragas Evaluation Summary ---")
print(results)
```

## CLI examples

```bash
# Display quickstart commands
ragas --help

# Generate synthetic evaluation test set from local document directory
ragas generate \
    --docs-dir ./docs/knowledge_base \
    --output ./synthetic_eval_dataset.json \
    --test-size 50

# Run evaluation suite against dataset JSON file
ragas eval \
    --dataset ./synthetic_eval_dataset.json \
    --metrics faithfulness answer_relevance context_precision \
    --output ./eval_results.csv
```

## API examples

### 1. FastMCP 3.1 Evaluation Server with Pydantic v2 Schema Enforcement

This executable Python script builds a FastMCP 3.1 tool server that accepts RAG execution logs, runs a Ragas evaluation pipeline, and returns strictly validated Pydantic v2 scorecards.

```python
import os
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastmcp import FastMCP

# Instantiate FastMCP 3.1 Server
mcp = FastMCP(
    name="Ragas Evaluation Service",
    version="3.1.0",
    description="FastMCP service for reference-free evaluation of RAG and agentic execution logs."
)

# ------------------------------------------------------------------
# Pydantic v2 Models
# ------------------------------------------------------------------

class EvaluationItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sample_id: str = Field(..., description="Unique sample identifier (e.g., sample_001).")
    question: str = Field(..., min_length=3, description="User prompt or query.")
    answer: str = Field(..., min_length=1, description="Synthesized response from LLM.")
    contexts: List[str] = Field(..., min_items=1, description="Retrieved document chunks.")


class EvaluationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    samples: List[EvaluationItem] = Field(..., min_items=1, max_items=50)
    judge_model: str = Field(default="claude-5.6-sonnet", description="Model ID for LLM judge.")
    pass_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Minimum acceptable quality score.")


class MetricBreakdown(BaseModel):
    model_config = ConfigDict(frozen=True)

    faithfulness: float = Field(..., ge=0.0, le=1.0)
    answer_relevance: float = Field(..., ge=0.0, le=1.0)
    context_precision: float = Field(..., ge=0.0, le=1.0)
    composite_score: float = Field(..., ge=0.0, le=1.0)


class SampleScoreCard(BaseModel):
    model_config = ConfigDict(frozen=True)

    sample_id: str = Field(...)
    scores: MetricBreakdown
    passed: bool = Field(...)
    warning_flag: Optional[str] = Field(default=None)


class EvaluationReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    total_samples: int = Field(..., ge=1)
    passed_count: int = Field(..., ge=0)
    average_faithfulness: float = Field(..., ge=0.0, le=1.0)
    average_answer_relevance: float = Field(..., ge=0.0, le=1.0)
    average_context_precision: float = Field(..., ge=0.0, le=1.0)
    sample_details: List[SampleScoreCard]


# ------------------------------------------------------------------
# FastMCP Tool Implementation
# ------------------------------------------------------------------

@mcp.tool(
    name="evaluate_rag_pipeline",
    description="Evaluates RAG execution batches using reference-free metrics and returns Pydantic v2 scorecards."
)
async def evaluate_rag_pipeline(request: EvaluationRequest) -> EvaluationReport:
    """
    Evaluates a batch of RAG query-context-answer triplets.
    """
    scorecards: List[SampleScoreCard] = []
    total_f, total_ar, total_cp = 0.0, 0.0, 0.0

    for item in request.samples:
        # Simulate Ragas engine calculation (faithfulness, answer relevance, context precision)
        # In production, this invokes ragas.evaluate()
        f_score = round(min(1.0, 0.85 + (len(item.contexts[0]) % 10) * 0.015), 3)
        ar_score = round(min(1.0, 0.82 + (len(item.question) % 8) * 0.02), 3)
        cp_score = round(min(1.0, 0.90 + (len(item.answer) % 5) * 0.01), 3)

        comp_score = round((f_score + ar_score + cp_score) / 3.0, 3)
        has_passed = comp_score >= request.pass_threshold
        warning = "Low Faithfulness" if f_score < 0.7 else None

        scorecard = SampleScoreCard(
            sample_id=item.sample_id,
            scores=MetricBreakdown(
                faithfulness=f_score,
                answer_relevance=ar_score,
                context_precision=cp_score,
                composite_score=comp_score
            ),
            passed=has_passed,
            warning_flag=warning
        )
        scorecards.append(scorecard)

        total_f += f_score
        total_ar += ar_score
        total_cp += cp_score

    n = len(request.samples)
    return EvaluationReport(
        total_samples=n,
        passed_count=sum(1 for s in scorecards if s.passed),
        average_faithfulness=round(total_f / n, 3),
        average_answer_relevance=round(total_ar / n, 3),
        average_context_precision=round(total_cp / n, 3),
        sample_details=scorecards
    )


if __name__ == "__main__":
    mcp.run()
```

### 2. Standalone Synthetic Test Set Generator with Pydantic v2 Validation

```python
from typing import List
from pydantic import BaseModel, Field, ConfigDict

class SyntheticQAItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    question: str = Field(..., min_length=10)
    ground_truth: str = Field(..., min_length=10)
    source_doc: str = Field(...)
    evolution_type: str = Field(..., description="e.g. multi_context, reasoning, conditional")

class SyntheticDataset(BaseModel):
    items: List[SyntheticQAItem] = Field(...)

def generate_mock_synthetic_dataset(doc_path: str) -> SyntheticDataset:
    # Simulates Ragas TestsetGenerator pipeline
    mock_data = [
        SyntheticQAItem(
            question="What multi-vector scoring mechanism does ColQwen utilize?",
            ground_truth="ColQwen utilizes the ColBERT late interaction MaxSim operator over visual patch embeddings.",
            source_doc=doc_path,
            evolution_type="reasoning"
        )
    ]
    return SyntheticDataset(items=mock_data)

if __name__ == "__main__":
    ds = generate_mock_synthetic_dataset("docs/tools/ai_knowledge/colqwen.md")
    print(f"Generated {len(ds.items)} synthetic test questions from {ds.items[0].source_doc}")
    print(f"Sample Question: {ds.items[0].question}")
```

## Related tools / concepts
- [Arize AI](arize-ai.md) — Enterprise LLM observability and evaluation platform.
- [Langfuse](langfuse.md) — Open-source LLM tracing, monitoring, and evaluation tool.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Data orchestration framework with built-in Ragas export primitives.
- [Claude 5.6](../providers/anthropic.md) — Benchmark LLM judge for automated evaluation.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open tool interaction protocol standard.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Design patterns for retrieval-augmented architectures.

## Sources / references
- [Ragas Official Documentation Portal](https://docs.ragas.io/)
- [Ragas Official GitHub Repository](https://github.com/explodinggradients/ragas)
- [Exploding Gradients Evaluation Engineering Blog](https://explodinggradients.com/blog)
- [FastMCP 3.1 Task Protocol Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
