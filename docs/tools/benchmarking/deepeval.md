# DeepEval

## What it is
DeepEval is an open-source LLM evaluation and unit testing framework developed by Confident AI. Designed to mirror unit testing practices in software engineering (such as Pytest), DeepEval enables developers to benchmark LLM outputs, prompt templates, RAG pipelines, and agentic workflows against continuous integration (CI/CD) pipelines using SOTA evaluation metrics.

## What problem it solves
Evaluating LLM-generated responses, RAG retrieval accuracy, and agent tool execution manually or through ad-hoc inspection is prone to bias, inconsistency, and regression failures as system prompts evolve. DeepEval provides standardized, deterministic, and LLM-as-a-judge metric suites (e.g., G-Eval, hallucination, answer relevancy, contextual precision, toxicity, and tool correctness) with full CI/CD regression testing support.

## Where it fits in the stack
**Evaluation & Benchmarking Layer**. It operates alongside evaluation frameworks and observability platforms (such as [Promptfoo](promptfoo.md), [Ragas](../process_understanding/ragas.md), [LangSmith](langsmith.md), and [Opik](../process_understanding/comet-opik.md)), validating prompt quality, RAG contexts, and agent tool execution before or during continuous deployment.

## Typical use cases
- **RAG Pipeline Benchmarking**: Quantifying faithulness, context recall, and contextual relevancy for vector database retrieval (e.g., [Chroma](../infrastructure/chroma.md), [Qdrant](../infrastructure/qdrant.md)).
- **Agent Tool Calling Verification**: Testing whether agent decisions match expected FastMCP 3.1 tool call sequences and parameter schemas.
- **CI/CD Regression Suite**: Running automated LLM evaluation unit tests on GitHub Actions prior to deploying new system prompts or model configurations.
- **G-Eval Custom Metric Scoring**: Defining criteria-based evaluation metrics using frontier reasoning models like Claude 5.1, GPT-5.5, or Gemini 4.0 Pro.

## Strengths
- **Pytest Native**: Seamlessly integrates into existing Python testing infrastructure using familiar `assert_test` paradigms.
- **Comprehensive Built-in Metrics**: Includes out-of-the-box metrics for RAG (faithfulness, answer relevancy, contextual precision), safety (toxicity, bias), and tool calling accuracy.
- **Synthesizer Dataset Generation**: Automatically generates synthetic QA evaluation datasets from raw enterprise documents.
- **Confident AI Cloud & Local Support**: Supports both completely local open-source testing runs and enterprise cloud reporting dashboards.
- **FastMCP 3.1 Schema Integration**: Supports structured JSON schema evaluation for FastMCP tool execution outputs.

## Limitations
- **Evaluation Model API Costs**: Utilizing SOTA LLM-as-a-judge metrics (like G-Eval) with frontier models incur LLM API token expenses during CI runs.
- **Non-Deterministic Scores**: Because LLM-as-a-judge evaluation relies on reasoning models, metric scores can exhibit slight variance across test executions.

## When to use it
- When you need a Pythonic, Pytest-integrated evaluation framework for RAG or agentic LLM applications.
- When establishing automated regression testing pipelines in GitHub Actions or GitLab CI.
- When generating synthetic test datasets to benchmark system prompt updates across frontier models (Claude 5.1, GPT-5.5, DeepSeek-V4).

## When not to use it
- For real-time low-latency production response guardrails (use latency-optimized runtime guardrails instead).
- For non-Python ecosystems requiring zero-dependency standalone CLI binaries (consider [Promptfoo](promptfoo.md)).

## Getting started

Install DeepEval via pip:

```bash
pip install deepeval pydantic
```

Set up your evaluation model credentials (e.g., OpenAI API Key):

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

## CLI examples

### 1. Run DeepEval Pytest Suite
```bash
# Execute all test cases in the test suite
deepeval test run test_rag_pipeline.py
```

### 2. Login and Sync with Confident AI Platform
```bash
# Authenticate CLI to upload evaluation results to dashboard
deepeval login --api-key YOUR_CONFIDENT_AI_API_KEY
```

## API examples

### Python: Unit Testing a RAG Context with Answer Relevancy and Faithfulness Metrics (Pydantic v2 Verified)
```python
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from pydantic import BaseModel, Field

# Schema for structured assessment report
class EvalReport(BaseModel):
    test_passed: bool
    relevancy_score: float = Field(..., description="Answer relevancy score between 0 and 1")
    faithfulness_score: float = Field(..., description="Faithfulness score between 0 and 1")

def test_rag_retrieval_quality():
    # Define test case containing input prompt, actual output, and retrieved contexts
    input_prompt = "What is the primary vector database used for local storage in our agent architecture?"
    actual_output = "The primary vector database used for local storage in our agent architecture is Chroma."
    retrieved_context = [
        "Chroma (also referred to as ChromaDB) is an open-source, lightweight vector database used for local storage in agent architectures."
    ]

    test_case = LLMTestCase(
        input=input_prompt,
        actual_output=actual_output,
        retrieval_context=retrieved_context
    )

    # Initialize evaluation metrics with minimum passing thresholds
    relevancy_metric = AnswerRelevancyMetric(threshold=0.8, model="gpt-5.5")
    faithfulness_metric = FaithfulnessMetric(threshold=0.8, model="gpt-5.5")

    # Assert test case passes metric thresholds
    assert_test(test_case, [relevancy_metric, faithfulness_metric])

if __name__ == "__main__":
    print("Executing DeepEval evaluation test...")
    test_rag_retrieval_quality()
    print("DeepEval test completed successfully.")
```

## Related tools / concepts
- [Promptfoo](promptfoo.md) — Multi-model evaluation and red-teaming tool.
- [Ragas](../process_understanding/ragas.md) — Framework for evaluating RAG pipelines.
- [LangSmith](langsmith.md) — Observability and evaluation platform by LangChain.
- [Opik](../process_understanding/comet-opik.md) — Open-source LLM evaluation and monitoring framework.
- [SWE-bench](swe-bench.md) — Benchmark for software engineering capabilities.

## Sources / references
- [DeepEval GitHub Repository](https://github.com/confident-ai/deepeval)
- [DeepEval Official Documentation](https://docs.confident-ai.com/)
- [Confident AI Platform](https://www.confident-ai.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
