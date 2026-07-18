# OpenPipe

## What it is
OpenPipe is an enterprise-grade, data-driven fine-tuning and model distillation platform. As of July 2026, it is the standard for converting expensive, high-latency frontier model calls (like GPT-5.5 or Claude 4.8) into optimized, specialized, open-weights student models (such as Llama 4, Mistral, or Qwen 3.6). It integrates production data logging, automated dataset curation, supervised fine-tuning (SFT), and reinforcement learning for agents into a unified, developer-friendly workflow.

## What problem it solves
Frontier models are highly capable but introduce significant API costs, token overhead, and latency bottlenecks for repetitive or structured production tasks. OpenPipe solves these issues by automating the distillation pipeline. It continuously captures production input-output traces, intelligently filters and prunes the dataset, and trains smaller student models that match or exceed teacher performance on targeted tasks at a fraction of the cost. Additionally, it addresses agentic reasoning failure rates by offering native reinforcement learning workflows on multi-step tool-use trajectories.

## Where it fits in the stack
**Infrastructure / Fine-tuning**. It acts as an orchestrator and data logger sitting between the application client/gateway and frontier LLM providers. Once training is complete, OpenPipe serves the resulting model adapters or exports them to high-performance inference engines in the deployment layer.

## Typical use cases
- **Cost and Latency Distillation**: Replacing complex multi-shot prompts sent to expensive frontier APIs with a specialized, single-shot 8B or 14B model hosted locally or on optimized endpoints.
- **Agent Policy Optimization (ART & GRPO)**: Reinforcement learning via the open-source Agent Reinforcement Trainer (ART) library and Group Relative Policy Optimization (GRPO) to train agent models to use tools and reason with high reliability.
- **Production Data Collection & Pruning**: Capturing production traffic under real user distribution while removing redundant prompts, duplicates, and system overhead.
- **Structured Data Extraction**: Fine-tuning specialized models to produce highly complex JSON schemas consistently, eliminating structural formatting failures.

## Strengths
- **Drop-in SDK Integration**: Wraps standard OpenAI or Anthropic SDK clients with minimal changes to core application logic.
- **Automated Curation & Deduplication**: Employs context-aware pruning algorithms to extract high-value diversity and filter out low-utility logs.
- **Agentic Reinforcement Learning**: Built-in support for reinforcement learning on agentic execution, optimizing tool-calling and self-correction paths.
- **Native Evaluation Suites**: Provides side-by-side performance benchmarks (Teacher vs. Student) with automated test sets and blind evaluations.
- **Multi-Cloud Deployment**: Supports exporting fine-tuned weights directly or serving them on high-throughput, dedicated server fleets.

## Limitations
- **Cold Start Dependency**: Requires a working "Teacher" model configuration to generate high-quality initial data and ground-truth completions.
- **Narrow Specialization**: Fine-tuned student models are highly optimized for specific tasks and lose the general conversational and multi-domain reasoning capabilities of frontier models.
- **Hardware & Scale Requirements**: Achievable performance gains typically require a minimum volume of 1,000 to 5,000 distinct production traces before training becomes highly effective.

## When to use it
- When you have a stable, high-volume production task (e.g., classification, extraction, or specific structured generation).
- When you want to transition from commercial APIs to owned, open-weights models to ensure data privacy, security, and lower operating costs.
- When latency requirements necessitate moving to local, edge-based, or high-throughput specialized model endpoints.
- When optimizing multi-step agent actions where standard prompting fails to achieve >95% reliability.

## When not to use it
- For exploratory, rapidly evolving applications where prompts, system instructions, or output schemas change daily.
- For extremely low-volume tasks where the developer overhead of fine-tuning and evaluation outweighs potential cost savings.
- When a task inherently requires broad, multi-domain background knowledge or general-purpose, unstructured conversation.

## Getting started

### Installation
Install the official OpenPipe Python SDK via pip:
```bash
pip install openpipe
```

### Initial Configuration
Set your OpenPipe API key as an environment variable:
```bash
export OPENPIPE_API_KEY="op_test_key_abc123"
```

### Minimal SDK Wrapper
To begin capturing production logs automatically, wrap your standard OpenAI client initialization with the OpenPipe SDK.

```python
from openpipe import OpenAI

# The OpenPipe SDK intercepts standard OpenAI calls
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5.5-preview",
    messages=[{"role": "user", "content": "Extract SKU: Item-99X-Red"}],
    openpipe={"tags": {"pipeline": "extraction-v1"}}
)

print(completion.choices[0].message.content)
```

## CLI examples

### Authentication
Authenticate your local CLI environment with your platform credentials:
```bash
openpipe login --api-key op_live_prod_key_789xyz
```

### Dataset Operations
List captured dataset groups and view sample counts:
```bash
openpipe datasets list
```

Download a specific dataset slice for offline inspection or local training:
```bash
openpipe datasets download --id ds_987abc --output-dir ./data/
```

### Fine-Tuning Jobs
Monitor the status and progress of an active training run:
```bash
openpipe jobs status --job-id ft-job-456
```

## API examples

### Capturing Production Traces for Distillation
This example demonstrates logging standard API calls to OpenPipe with custom metadata tags to facilitate downstream dataset curation.

```python
import os
from openpipe import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    openpipe={"api_key": os.environ.get("OPENPIPE_API_KEY")}
)

# Call the frontier teacher model; OpenPipe automatically logs this request-response pair
response = client.chat.completions.create(
    model="gpt-5.5-preview",
    messages=[
        {"role": "system", "content": "You are a precise JSON medical transcriptionist."},
        {"role": "user", "content": "Patient reports mild chest tightness after exercise."}
    ],
    openpipe={
        "tags": {
            "department": "cardiology",
            "environment": "production",
            "doctor_id": "doc_90210"
        },
        "log_request": True
    }
)
```

### Deploying and Call the Distilled Student Model
Once the student model is trained and active, replace the teacher's model identifier with your distilled OpenPipe model path.

```python
import os
from openpipe import OpenAI

client = OpenAI()

# Call your highly optimized, distilled model served on OpenPipe
response = client.chat.completions.create(
    model="openpipe:medical-transcriber-llama4-8b-v1",
    messages=[
        {"role": "system", "content": "You are a precise JSON medical transcriptionist."},
        {"role": "user", "content": "Patient reports mild chest tightness after exercise."}
    ]
)

print(response.choices[0].message.content)
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput engine for hosting exported OpenPipe model weights.
- [Unsloth](unsloth.md) — Extremely fast local fine-tuning engine optimized for single-node GPUs.
- [Mistral AI](../providers/mistral.md) — Common open-weights base model family for high-quality distillation.
- [Together AI](../providers/together.md) — Managed cloud provider frequently used for serving OpenPipe models.
- [Anthropic](../providers/anthropic.md) — Maker of Claude models often leveraged as teachers for training datasets.
- [Weights & Biases](../process_understanding/wandb-weave.md) — SOTA experiment and evaluation tracking tool for machine learning.
- [Unstructured](../intake_storage/unstructured.md) — Document pre-processing library to ingestion-ready formats for training pipelines.
- [Llama Factory](../frameworks/llama-factory.md) — Comprehensive framework for visual and CLI-based local model tuning.
- [Axolotl](../frameworks/axolotl.md) — YAML-driven multi-GPU fine-tuning framework for advanced open models.
- [Distilabel](../frameworks/distilabel.md) — Pipeline framework for generating high-quality synthetic instruction and preference datasets.
- [LM Evaluation Harness](../benchmarking/lm-evaluation-harness.md) — Industry-standard benchmark runner for evaluating distilled models.

## Sources / references
- [OpenPipe Official Website](https://openpipe.ai/)
- [OpenPipe Documentation](https://docs.openpipe.ai/)
- [OpenPipe GitHub Repository](https://github.com/openpipe/openpipe)
- [Agent Reinforcement Trainer (ART) GitHub](https://github.com/openpipe/art)
- [Braintrust: Best LLM Fine-Tuning Platforms in 2026](https://www.braintrust.dev/articles/best-llm-fine-tuning-platforms-2026)
- [Llama Factory Documentation](https://llamafactory.readthedocs.io/)
- [Unstructured.io](https://unstructured.io/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
