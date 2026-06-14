# Distilabel

## What it is
Distilabel is an open-source framework designed for scalable and reliable synthetic data generation and AI feedback. As of June 2026, it is the industry standard for creating high-quality datasets for fine-tuning frontier models like `claude-4-8-opus-20260528` and GPT-5.5. It allows developers to build complex pipelines that leverage Large Language Models (LLMs) to generate, augment, and filter datasets, incorporating "LLM-as-a-judge" patterns to ensure data quality.

## What problem it solves
Creating high-quality datasets for LLM training remains a significant bottleneck. Manual labeling is slow and expensive, while naive synthetic generation often produces noisy or repetitive data. Distilabel addresses these challenges by:
- **Standardizing Pipeline Construction**: Providing a declarative way to define data generation and labeling steps.
- **Scaling Generation**: Natively supporting parallel execution and integration with various LLM providers (Anthropic, OpenAI, [vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)).
- **Ensuring Data Quality**: Built-in components for filtering, scoring, and verifying synthetic samples using advanced reasoning models.
- **Reducing Alignment Costs**: Streamlining the creation of preference datasets for DPO and RLHF workflows.

## Where it fits in the stack
Distilabel sits in the **Frameworks/Data-Generation** layer. It is the primary engine for data preparation that precedes the fine-tuning stage, serving as the "upstream" source for tools like [Unsloth](../infrastructure/unsloth.md), [Axolotl](axolotl.md), or [LLaMA Factory](llama-factory.md).

## Typical use cases
- **Instruction Data Generation**: Generating thousands of varied prompts and responses from a few seed examples (Self-Instruct).
- **Preference Dataset Creation**: Generating multiple responses to the same prompt and using a stronger model like Claude 4.8 to rank them.
- **RAG Data Augmentation**: Generating synthetic questions and answers from a corpus of documents to train specialized embedding or retrieval models.
- **Domain Adaptation**: Creating niche datasets for specialized fields like coding, medicine, or law where public data is scarce.
- **Synthetic Agentic Data**: Generating multi-step tool-use trajectories for agent training.

## Strengths
- **Provider Agnostic**: Seamlessly switch between local models ([Ollama](../../services/ollama.md)) and cloud APIs (Anthropic, OpenAI).
- **Reliable Pipeline Logic**: Handles retries, rate limiting, and caching out of the box.
- **Rich Component Library**: Includes pre-built tasks for common patterns (e.g., UltraFeedback, Evol-Instruct, DEITA).
- **Integration with Hugging Face**: Direct support for loading from and pushing to the Hugging Face Hub.
- **Scalability**: Designed to handle millions of samples via distributed processing.

## Limitations
- **Cost Management**: Generating large datasets via frontier APIs (e.g., GPT-5.5) can be extremely expensive.
- **Model Bias**: Synthetic data inherits the biases and reasoning patterns of the generator models.
- **Pipeline Complexity**: Designing effective "multi-step" pipelines requires deep expertise in prompt engineering and dataset theory.

## When to use it
- When you need to scale from hundreds to tens of thousands of high-quality training examples.
- When you want to implement automated "LLM-as-a-judge" workflows for data validation.
- When you need to generate preference data (pairs of good/bad responses) for alignment training.
- When you want to leverage frontier models like Claude 4.8 to improve the quality of data for smaller, specialized models.

## When not to use it
- If you only need a handful of examples that can be written manually.
- If you don't have access to sufficiently capable generator models (either local or via API).
- If your data needs are purely extractive and don't involve generative reasoning.

## Getting started

### Installation
```bash
pip install distilabel[vllm,anthropic,openai]
```

### Hello-world
A minimal script to generate a response using a pipeline:

```python
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromHub
from distilabel.llms import AnthropicLLM

with Pipeline(name="hello-world") as pipeline:
    loader = LoadDataFromHub(repo_id="instruction-dataset")
    llm = AnthropicLLM(model="claude-4-8-opus-20260528")
    # ... define steps ...
```

## CLI examples
Distilabel provides a CLI for managing and running pipelines.

```bash
# Run a pipeline from a configuration file
distilabel pipeline run --config pipeline.yaml

# List all available local pipelines
distilabel pipeline list

# Check the version and environment info
distilabel --version
```

## API examples

### Generating Evol-Instructions
Using Claude 4.8 to evolve a dataset of instructions for increased complexity.

```python
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromHub
from distilabel.steps.tasks import EvolInstruction
from distilabel.llms import AnthropicLLM

with Pipeline(name="evol-instruct-pipeline") as pipeline:
    loader = LoadDataFromHub(repo_id="HuggingFaceH4/instruction-dataset")
    llm = AnthropicLLM(model="claude-4-8-opus-20260528")

    evolve = EvolInstruction(
        llm=llm,
        num_evolutions=2,
    )

    loader >> evolve

if __name__ == "__main__":
    pipeline.run()
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The primary beneficiary of distilabel output.
- [Unsloth](../infrastructure/unsloth.md) — For training on the generated data.
- [axolotl](axolotl.md) — For training on the generated data.
- [vLLM](../infrastructure/vllm.md) — Often used as the high-speed generation backend for distilabel.
- [Ollama](../../services/ollama.md) — Can be used for local, private data generation.
- [glaive](../ai_knowledge/glaive.md) — A platform for generating synthetic agentic data.
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/index) — The ecosystem where distilabel data is typically shared.
- [Instructor](instructor.md) — For structured data extraction which can be used within distilabel tasks.

## Sources / references
- [Distilabel Documentation](https://distilabel.argilla.io/)
- [Argilla GitHub Repository](https://github.com/argilla-io/distilabel)
- [Synthetic Data Generation for LLMs (Guide)](https://distilabel.argilla.io/latest/sections/getting_started/quickstart/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
