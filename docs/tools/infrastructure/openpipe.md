# OpenPipe

## What it is
OpenPipe is a data-driven fine-tuning platform that allows developers to replace generic, expensive LLMs (like GPT-5.5 or Claude 4.8) with smaller, faster, and cheaper specialized models. It works by capturing requests and completions from existing models and using them to train custom models through automated distillation.

## What problem it solves
It lowers the cost and latency of LLM applications without sacrificing quality by automating the process of distillation and fine-tuning. It simplifies the pipeline from production data collection to model deployment, solving the "data fly-wheel" challenge for specialized AI tasks.

## Where it fits in the stack
**Infrastructure / Fine-tuning**. It sits between the production inference layer and the training pipeline, acting as both a data logger and a model provider.

## Typical use cases
- **Cost Reduction**: Distilling GPT-5.5 level performance into a specialized Llama-3-8B or Mistral model.
- **Latency Optimization**: Replacing heavy frontier models with 4-bit quantized local models for real-time extraction.
- **Dataset Generation**: Creating "Golden Datasets" from production traffic for RAG evaluation.
- **Quality Improvement**: Fine-tuning on specialized domains (legal, medical, or internal codebase) where general models underperform.

## Strengths
- **Drop-in SDK**: Wraps the official OpenAI/Anthropic SDKs with zero code changes to core application logic.
- **Automated Data Curation**: Advanced pruning algorithms remove duplicate system prompts and redundant context.
- **Integrated Evaluation**: Side-by-side comparison of "Teacher" vs. "Student" performance using standardized benchmarks.
- **Provider Agnostic**: Supports fine-tuning Llama, Mistral, and specialized open-weights models for deployment on [vLLM](vllm.md) or [Together AI](../providers/together.md).

## Limitations
- **Cold Start**: Requires an initial "Teacher" model to generate high-quality ground truth data.
- **Specialization vs. Generalization**: Fine-tuned models excel at specific tasks but lose general-purpose chat capabilities.
- **Token Volume**: Requires sufficient production volume (typically 1,000+ examples) to achieve significant performance gains over few-shot prompting.

## When to use it
- When you have a stable, high-volume production task (e.g., classification, extraction, or summarization).
- When you want to own your model weights while maintaining frontier-grade performance.
- When latency requirements necessitate moving from API-based models to local/edge inference.

## When not to use it
- For exploratory tasks where the prompt or schema changes daily.
- For extremely low-volume applications where the engineering overhead of fine-tuning exceeds the cost savings.
- If the task requires broad general knowledge or reasoning across multiple unrelated domains simultaneously.

## Getting started

### Installation
```bash
pip install openpipe
```

### Initial Configuration
Set your OpenPipe API key in your environment:
```bash
export OPENPIPE_API_KEY="op_..."
```

### Simple Implementation
```python
from openpipe import OpenAI

# OpenPipe wraps the standard OpenAI client
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Extract the invoice number: INV-2026-001"}],
    openpipe={"tags": {"purpose": "invoice-extraction"}}
)

print(completion.choices[0].message.content)
```

## CLI examples

### Authentication
```bash
openpipe login --api-key your_api_key_here
```

### Dataset Management
List your captured datasets and their current sample counts:
```bash
openpipe datasets list
```

### Model Status
Check the status of an ongoing fine-tuning job:
```bash
openpipe models status --job-id ft-12345
```

## API examples

### Capturing Production Data
OpenPipe captures "Teacher" completions automatically for future training.

```python
import os
from openpipe import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    openpipe={"api_key": os.environ.get("OPENPIPE_API_KEY")}
)

# This request is logged to OpenPipe with the associated tags
response = client.chat.completions.create(
    model="gpt-5.5-preview",
    messages=[{"role": "user", "content": "Summarize this ticket..."}],
    openpipe={
        "tags": {
            "department": "support",
            "priority": "high"
        },
        "log_request": True
    }
)
```

### Deploying the Student Model
Switching from the expensive teacher to the optimized student requires changing only the model identifier.

```python
# The student model is hosted on OpenPipe's optimized infrastructure
response = client.chat.completions.create(
    model="openpipe:support-summarizer-v1",
    messages=[{"role": "user", "content": "Summarize this ticket..."}]
)
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput inference for hosting OpenPipe-trained models.
- [Mistral AI](../providers/mistral.md) — Common base model for distillation.
- [Together AI](../providers/together.md) — Inference provider for fine-tuned open-weights models.
- [Weights & Biases](../process_understanding/wandb-weave.md) — Experiment tracking for model training.
- [Unstructured](../intake_storage/unstructured.md) — Pre-processing data for the distillation pipeline.
- [Llama Factory](../frameworks/llama-factory.md) — Alternative local fine-tuning framework.
- [LM Evaluation Harness](../benchmarking/lm-evaluation-harness.md) — Standardized testing for fine-tuned models.

## Sources / references
- [OpenPipe Official Website](https://openpipe.ai/)
- [OpenPipe Documentation](https://docs.openpipe.ai/)
- [OpenPipe GitHub Repository](https://github.com/openpipe/openpipe)
- [Model Distillation Research (2026)](https://arxiv.org/abs/distillation-trends-2026)
- [Llama Factory](../frameworks/llama-factory.md)
- [Unstructured](https://unstructured.io/)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
