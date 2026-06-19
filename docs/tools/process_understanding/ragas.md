# Ragas

## What it is
Ragas (Retrieval Augmented Generation Assessment) is an open-source framework for evaluating Retrieval Augmented Generation (RAG) pipelines. It provides a suite of metrics to measure the performance of different components of a RAG system without requiring extensive human-annotated datasets.

## What problem it solves
Evaluating RAG systems is notoriously difficult because both the retrieval (finding the right context) and the generation (writing the answer) can fail. Ragas provides automated, quantitative metrics to pinpoint whether a failure is due to poor retrieval, lack of factual consistency, or irrelevant generation. In June 2026, it is the standard for reference-free evaluation of agentic RAG pipelines using Claude 4.8 Opus as a judge.

## Where it fits in the stack
**Category**: Process & Understanding / RAG Evaluation. It serves as the primary "Evaluation Plane" for agentic workflows.

## Typical use cases
- **RAG Pipeline Optimization**: Comparing different embedding models or retrieval strategies (e.g., hybrid search vs. semantic search).
- **Automated Testing**: Running evaluation suites as part of a CI/CD pipeline for AI applications.
- **Synthetic Dataset Generation**: Creating "ground truth" datasets from existing documents to bootstrap evaluation.
- **Agentic Reasoning Evaluation**: Scoring the multi-step reasoning traces of autonomous agents.

## Strengths
- **Reference-Free Evaluation**: Can evaluate performance using only the generated answer and the retrieved context (no "gold" answers needed).
- **Component-Level Metrics**: Specific metrics for Faithfulness, Answer Relevance, Context Precision, and Context Recall.
- **LLM-as-a-Judge**: Leverages powerful LLMs like Claude 4.8 Opus to perform nuanced evaluations of complex text.
- **Multi-Modal Support**: 2026 updates include native scoring for multi-modal RAG (images, charts, and tables) via [Docling](docling.md).
- **Framework Integration**: Easy to use with LangChain and LlamaIndex.

## Limitations
- **LLM Cost**: Evaluation runs require many LLM calls, which can be expensive and slow for large datasets.
- **Judge Bias**: The accuracy of the evaluation depends on the quality of the "judge" model used.

## When to use it
- To quantitatively evaluate a RAG system's faithfulness and relevance without manually writing ground-truth answers.
- During development to compare different retrieval strategies or model prompts.
- For reference-free evaluation of agentic reasoning steps.

## When not to use it
- If you have a very small dataset where manual human review is faster and more accurate.
- If you cannot afford the API costs or latency associated with using a powerful LLM as a judge.

## Getting started

### Installation
```bash
pip install ragas[all] # Includes multi-modal support
```

## CLI examples
```bash
# List available project templates
ragas quickstart

# Create a new RAG evaluation project from a template
ragas quickstart rag_eval

# Run evaluation on a local JSONL file
ragas evaluate --dataset my_data.jsonl --metrics faithfulness,relevance
```

## API examples

### Basic Evaluation (Faithfulness)
```python
from ragas import evaluate
from datasets import Dataset
from ragas.metrics import faithfulness

# Prepare your data
data_samples = {
    'question': ['When was the first AI conference?'],
    'answer': ['The Dartmouth workshop in 1956 is widely considered the first.'],
    'contexts' : [['The Dartmouth Summer Research Project on Artificial Intelligence was a 1956 summer workshop...']],
}
dataset = Dataset.from_dict(data_samples)

# Evaluate using Claude 4.8 Opus as the judge
result = evaluate(dataset, metrics=[faithfulness])
print(f"Faithfulness Score: {result['faithfulness']}")
```

### Multi-modal Evaluation
```python
from ragas.metrics import multi_modal_relevance

# Example for evaluating image-based retrieval
# (Requires Ragas v1.2+ and Docling-processed contexts)
result = evaluate(mm_dataset, metrics=[multi_modal_relevance])
```

## Related tools / concepts
- [LangSmith](../benchmarking/langsmith.md)
- [Arize AI](arize-ai.md) — For production-level observability.
- [W&B Weave](wandb-weave.md) — For tracing and visualizing evaluation runs.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — For building the RAG pipelines evaluated by Ragas.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Langfuse](langfuse.md)
- [Docling](docling.md) — For multi-modal document ingestion.
- [AgentOps](agentops.md) — For session-level audit trails.

## Sources / references
- [Ragas Documentation](https://docs.ragas.io/)
- [Ragas GitHub Repository](https://github.com/explodinggradients/ragas)
- [Evaluation-Driven Development (EDD)](https://www.comet.com/site/blog/evaluation-driven-development/)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
