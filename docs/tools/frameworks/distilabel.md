# Distilabel

## What it is
Distilabel is an open-source framework designed for scalable and reliable synthetic data generation. It allows developers to build complex pipelines that leverage Large Language Models (LLMs) to generate, augment, and filter datasets for training and fine-tuning. By orchestrating interactions between multiple models and incorporating automated quality checks, distilabel helps create high-quality instruction, preference, and specialized datasets.

## What problem it solves
Creating high-quality datasets for LLM training is often the most significant bottleneck in AI development. Manual labeling is slow and expensive, while simple synthetic generation can lead to noisy or repetitive data. Distilabel addresses these challenges by:
- **Standardizing Pipeline Construction**: Providing a declarative way to define data generation and labeling steps.
- **Scaling Generation**: Natively supporting parallel execution and integration with various LLM providers (OpenAI, Anthropic, [vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)).
- **Ensuring Data Quality**: Built-in components for filtering, scoring, and verifying synthetic samples using "LLM-as-a-judge" patterns.

## Where it fits in the stack
Distilabel sits in the **Frameworks/Data-Generation** layer. It precedes the fine-tuning stage, acting as the engine that prepares the data subsequently used by tools like [Unsloth](../infrastructure/unsloth.md), [Axolotl](axolotl.md), or [LLaMA Factory](llama-factory.md).

## Typical use cases
- **Instruction Data Generation**: Generating thousands of varied prompts and responses from a few seed examples (Self-Instruct).
- **Preference Dataset Creation**: Generating multiple responses to the same prompt and using a stronger model to rank them for DPO or RLHF.
- **RAG Data Augmentation**: Generating synthetic questions and answers from a corpus of documents to train specialized embedding or retrieval models.
- **Domain Adaptation**: Creating niche datasets for specialized fields like coding, medicine, or law.

## Strengths
- **Provider Agnostic**: Seamlessly switch between local models ([Ollama](../../services/ollama.md)) and cloud APIs.
- **Reliable Pipeline Logic**: Handles retries, rate limiting, and caching out of the box.
- **Rich Component Library**: Includes pre-built tasks for common data generation patterns (e.g., UltraFeedback, Evol-Instruct).
- **Integration with Hugging Face**: Direct support for loading from and pushing to the Hugging Face Hub.

## Limitations
- **Cost Management**: Generating large datasets via cloud APIs can quickly become expensive if not monitored.
- **Model Bias**: Synthetic data inherits the biases and limitations of the generator models.
- **Complexity**: Designing effective "multi-step" pipelines requires a good understanding of prompt engineering and dataset theory.

## When to use it
- When you need to scale from hundreds to tens of thousands of high-quality training examples.
- When you want to implement automated "LLM-as-a-judge" workflows for data validation.
- When you need to generate preference data (pairs of good/bad responses) for alignment training.

## When not to use it
- If you only need a handful of examples that can be written manually.
- If you don't have access to sufficiently capable generator models (either local or via API).
- If your data needs are purely extractive and don't involve generative reasoning.

## Getting started

### Installation
```bash
pip install distilabel[vllm,openai]
```

### Hello-world Pipeline
A simple pipeline to evolve a dataset of instructions:

```python
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromHub
from distilabel.steps.tasks import EvolInstruction
from distilabel.llms import vLLM

with Pipeline(name="evol-instruct-pipeline") as pipeline:
    loader = LoadDataFromHub(repo_id="HuggingFaceH4/instruction-dataset")

    llm = vLLM(model="meta-llama/Meta-Llama-3-8B-Instruct")

    evolve = EvolInstruction(
        llm=llm,
        num_evolutions=2,
        store_evolutions=True,
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

## Sources / references
- [Distilabel Documentation](https://distilabel.argilla.io/)
- [Argilla (Maintainers of Distilabel)](https://argilla.io/)
- [Synthetic Data Generation for LLMs (Guide)](https://distilabel.argilla.io/latest/sections/getting_started/quickstart/)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
