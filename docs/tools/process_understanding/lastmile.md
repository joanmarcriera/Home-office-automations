# LastMile AI

## What it is
LastMile AI is an evaluation and observability platform for LLM applications, with a strong focus on "AI Auto-evals." It provides tools for systematically testing AI outputs and ensuring they meet quality standards before reaching the end user.

## What problem it solves
Manual evaluation of AI outputs doesn't scale. LastMile AI automates this process by using "evaluators" (small, specialized models or heuristics) to score outputs for factual accuracy, tone, safety, and adherence to instructions.

## Where it fits in the stack
**Category**: Process & Understanding / AI Evaluation

## Typical use cases
- **Pre-deployment Testing**: Running large-scale evaluations on potential prompt changes.
- **Production Guardrails**: Using real-time evaluations to block or flag unsafe or low-quality AI responses.
- **RAG Evaluation**: Specifically measuring the retrieval quality and grounding of RAG systems.
- **Model Comparison**: Benchmarking different models (e.g., GPT-4 vs. Claude 3) on your specific business data.

## Strengths
- **Extensible Evaluators**: Large library of pre-built evaluators and easy tools for building custom ones.
- **Integration with CI/CD**: Designed to be part of a modern software development lifecycle.
- **Detailed Analytics**: Deep dives into why certain evaluations failed.
- **Agnostic**: Works across various providers and frameworks.

## Limitations
- **Complexity**: Requires a structured approach to testing that might have a learning curve for smaller projects.
- **Platform-Centric**: Best experienced through their cloud-based evaluation dashboard.

## When to use it
- When you need to automate your AI testing pipeline.
- When you are scaling a RAG application and need to measure retrieval accuracy.

## When not to use it
- For very simple, exploratory prompt engineering where manual inspection is sufficient.

## Getting started

Install the LastMile SDK:

```bash
pip install lastmile-ai
```

Set up your API token:

```python
import os
os.environ["LASTMILE_API_TOKEN"] = "your_token_here"
```

## CLI examples

### lastmile login
Authenticates with the LastMile platform:
```bash
lastmile login
```

### lastmile eval run
Executes a defined evaluation suite:
```bash
lastmile eval run --suite my-test-suite
```

### lastmile dataset upload
Uploads a local CSV or JSONL for evaluation:
```bash
lastmile dataset upload data.csv
```

## API examples

### Python (Auto-evaluating a response)
```python
from lastmile import AutoEval

# Initialize evaluator
evaluator = AutoEval()

# Evaluate a response against a prompt
results = evaluator.evaluate(
    input="What is the capital of France?",
    output="The capital of France is Paris.",
    metrics=["factuality", "conciseness"]
)
print(results)
```

## Related tools / concepts
- [Ragas](./ragas.md)
- [Promptfoo](../benchmarking/promptfoo.md)
- [LangSmith](../benchmarking/langsmith.md)
- [Arize AI](./arize-ai.md)
- [Braintrust](./braintrust.md)

## Sources / references
- [LastMile AI Website](https://lastmileai.dev/)
- [LastMile AI Documentation](https://docs.lastmileai.dev/)

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high
