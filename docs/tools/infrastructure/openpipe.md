# OpenPipe

## What it is
OpenPipe is a data-driven fine-tuning platform that allows developers to replace generic, expensive LLMs (like GPT-4) with smaller, faster, and cheaper specialized models. It works by capturing requests and completions from existing models and using them to train custom models.

## What problem it solves
It lowers the cost and latency of LLM applications without sacrificing quality by automating the process of distillation and fine-tuning. It simplifies the pipeline from data collection to model deployment.

## Where it fits in the stack
Infrastructure / Fine-tuning

## Typical use cases
- Distilling GPT-4 level performance into a specialized Mistral or Llama-based model.
- Reducing costs for high-volume LLM tasks like classification or extraction.
- Improving latency for real-time applications by using smaller models.
- "Golden Dataset" generation from production traffic.

## Technical Capabilities
- **Drop-in SDK**: Wraps the official OpenAI SDK, logging requests to OpenPipe with zero code changes to core logic.
- **Model Distillation**: Tools to compare "Teacher" (e.g., GPT-4o) vs. "Student" (e.g., Llama-3-8B) performance.
- **Data Pruning**: Automatically removes duplicate system prompts and redundant context to minimize training tokens.
- **OpenAI-Compatible Hosting**: Deploys fine-tuned models to an endpoint that responds to standard OpenAI API calls.

## Strengths
- Easy "drop-in" replacement for OpenAI's SDK.
- Automated data collection and curation for fine-tuning.
- Integrated evaluation to compare fine-tuned models against base models.
- Support for multiple base models (Mistral, Llama 3, etc.).

## Limitations
- Requires an initial "teacher" model to generate data.
- Performance depends on the quality and variety of captured data.
- Primarily focused on specialized tasks rather than general-purpose chat.

## When to use it
- When you have a stable production task and want to reduce costs or latency.
- When you want to own your weights but start with OpenAI-grade performance.

## When not to use it
- For highly exploratory tasks where the prompt is changing frequently.
- If you don't have enough volume to justify the fine-tuning effort or cost.

## Getting started

### Installation
```bash
pip install openpipe
```

### Minimal Example
```python
from openpipe import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count to three"}],
    openpipe={"tags": {"purpose": "testing"}}
)

print(completion.choices[0].message.content)
```

## CLI examples
```bash
# Log in to your OpenPipe account
openpipe login --api-key your_api_key_here

# Record a single request/response pair manually
openpipe record --prompt "Hello" --completion "Hi there!"

# List your fine-tuned models
openpipe models list
```

## API: Production Data Collection
The primary value of OpenPipe is capturing real-world "Teacher" model outputs to build a training set.

```python
import os
from openpipe import OpenAI

# OpenPipe is a drop-in replacement for the OpenAI SDK
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    openpipe={"api_key": os.environ.get("OPENPIPE_API_KEY")}
)

# Requests are automatically logged for fine-tuning
# You can tag requests to filter your dataset later in the dashboard
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Extract technical specs from this manual..."}],
    openpipe={
        "tags": {
            "pipeline": "manual-ingestion",
            "version": "v2.1",
            "is_production": "true"
        },
        "log_request": True # Explicitly ensure this request is logged
    }
)
```

## API: Switching to Fine-Tuned Model
Once a model is trained, switching is as simple as changing the `model` string.

```python
# Switch from GPT-4o to your fine-tuned model
# The interface remains identical
response = client.chat.completions.create(
    model="openpipe:my-fine-tuned-llama-model",
    messages=[{"role": "user", "content": "Extract technical specs..."}],
    # Tagging still works for monitoring the performance of the student model
    openpipe={"tags": {"model_type": "student"}}
)
```

## Licensing and cost
- **Open Source**: Yes (Client SDK and some components)
- **Cost**: Paid (Usage-based pricing for training and hosting)
- **Self-hostable**: Partial (SDK is open, training platform is managed)

## Related tools / concepts
- [Infrastructure](./index.md)
- [Mistral AI](../providers/mistral.md)
- [Together AI](../providers/together.md)
- [vLLM](vllm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [LangSmith](../benchmarking/langsmith.md)
- [Weights & Biases](../benchmarking/wandb.md)
- [Unstructured](../process_understanding/unstructured.md)
- [LlamaParse](../process_understanding/llamaparse.md)

## Sources / References
- [Official Website](https://openpipe.ai/)
- [GitHub](https://github.com/openpipe/openpipe)
- [Docs](https://docs.openpipe.ai/)
- [Weights & Biases](../process_understanding/wandb-weave.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
