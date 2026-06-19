# Ragas

## What it is
Ragas (Retrieval Augmented Generation Assessment) is an open-source framework for evaluating Retrieval Augmented Generation (RAG) pipelines. It provides a suite of metrics to measure the performance of different components of a RAG system without requiring extensive human-annotated datasets.

## What problem it solves
Evaluating RAG systems is notoriously difficult because both the retrieval (finding the right context) and the generation (writing the answer) can fail. Ragas provides automated, quantitative metrics to pinpoint whether a failure is due to poor retrieval, lack of factual consistency, or irrelevant generation. In 2026, it is the standard for **Reference-free Evaluation** of agentic RAG pipelines.

## Where it fits in the stack
**Category**: Process & Understanding / RAG Evaluation. It serves as the primary evaluation engine for verifying the accuracy and safety of LLM-driven knowledge retrieval.

## Typical use cases
- **RAG Pipeline Optimization**: Comparing different embedding models or retrieval strategies (e.g., hybrid search vs. semantic search).
- **Automated Testing**: Running evaluation suites as part of a CI/CD pipeline for AI applications.
- **Synthetic Dataset Generation**: Creating "ground truth" datasets from existing documents to bootstrap evaluation.
- **Multi-modal Evaluation**: Scoring RAG systems that retrieve and generate images, charts, and text.

## Strengths
- **Reference-Free Evaluation**: Can evaluate performance using only the generated answer and the retrieved context (no "gold" answers needed).
- **Component-Level Metrics**: Specific metrics for Faithfulness, Answer Relevance, Context Precision, and Context Recall.
- **LLM-as-a-Judge**: Leverages powerful LLMs like Claude 4.8 Opus to perform nuanced evaluations of complex text.
- **Framework Integration**: Easy to use with LangChain, LlamaIndex, and native MCP tools.
- **Multi-modal Scoring**: Support for scoring visual reasoning steps in complex chains.

## Limitations
- **LLM Cost**: Evaluation runs require many LLM calls, which can be expensive and slow for large datasets.
- **Judge Bias**: The accuracy of the evaluation depends on the quality of the "judge" model used (e.g., GPT-5.5 or Claude 4.8).

## When to use it
- To quantitatively evaluate a RAG system's faithfulness and relevance without manually writing ground-truth answers.
- During development to compare different retrieval strategies or model prompts.
- For continuous monitoring of production RAG pipelines via observability integrations.

## When not to use it
- If you have a very small dataset where manual human review is faster and more accurate.
- If you cannot afford the API costs or latency associated with using a powerful frontier LLM as a judge.

## Getting started

### Installation
```bash
pip install ragas
```

## CLI examples
```bash
# List available project templates
ragas quickstart

# Create a new RAG evaluation project from a template
ragas quickstart rag_eval

# Create project in a specific directory
ragas quickstart rag_eval --output-dir ./eval_project
```

## API examples

### Basic Evaluation (Python)
```python
from ragas import evaluate
from datasets import Dataset
import os

# Initialize your judge (Claude 4.8 Opus)
os.environ["ANTHROPIC_API_KEY"] = "your-key"

# Prepare your data
data_samples = {
    'question': ['When was the first AI conference?'],
    'answer': ['The Dartmouth workshop in 1956 is widely considered the first.'],
    'contexts' : [['The Dartmouth Summer Research Project on Artificial Intelligence was a 1956 summer workshop...']],
}
dataset = Dataset.from_dict(data_samples)

# Evaluate the dataset (returns a result object with scores)
result = evaluate(dataset)
print(result)
```

### Multi-modal Evaluation
```python
# Ragas 2026 supports multi-modal scoring
from ragas.metrics import vision_relevance

# Score a visual RAG step
score = vision_relevance.compute(
    image_path="retrieved_chart.png",
    question="What was the growth in Q3?",
    answer="The chart shows a 15% increase in Q3."
)
print(f"Vision Relevance: {score}")
```

## Backlog
- [x] Perform quarterly technical freshness audit (2026-06-19).
- [ ] Perform quarterly technical freshness audit.

## Related tools / concepts
- [LangSmith](../benchmarking/langsmith.md)
- [Arize AI](arize-ai.md)
- [W&B Weave](wandb-weave.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Langfuse](langfuse.md)
- [Claude 4.8 Opus](../providers/anthropic.md)
- [GPT-5.5](../providers/openai.md)

## Sources / references
- [Ragas Documentation](https://docs.ragas.io/)
- [Ragas GitHub Repository](https://github.com/explodinggradients/ragas)
- [Exploding Gradients Blog](https://explodinggradients.com/blog)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
