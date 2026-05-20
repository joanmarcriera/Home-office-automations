# Hugging Face

## What it is
Hugging Face is the central hub for the machine learning community, providing a platform where users can share, discover, and collaborate on models, datasets, and ML applications. It is often referred to as the "GitHub of AI."

## What problem it solves
It simplifies the process of finding, downloading, and deploying state-of-the-art machine learning models. It provides standardized libraries (like Transformers, Diffusers, and Datasets) that allow developers to work with models from many different providers using a unified API.

## Where it fits in the stack
**Provider and Model Hub**. It serves as the primary source for models used by [Ollama](../../services/ollama.md), [LiteLLM](../../services/litellm.md), and many other local AI tools.

## Typical use cases
- **Model Discovery**: Finding the latest open-source LLMs (e.g., Llama, Qwen, Mistral).
- **Application Development**: Using the `transformers` library to integrate AI into Python applications.
- **Data Management**: Hosting and versioning large-scale datasets for training and evaluation.
- **Collaboration**: Hosting private models and datasets for team collaboration.
- **Rapid Prototyping**: Running quick experiments using Hugging Face Spaces.

## Getting started

### Installation

Install the core libraries for model interaction and hub management:

```bash
# Install transformers and huggingface_hub
pip install transformers huggingface_hub

# Install additional libraries for specific model types (optional)
pip install diffusers datasets
```

### Hello-world task

Authenticate with the hub and download a model's configuration:

```bash
# Login via CLI (requires an Access Token from huggingface.co/settings/tokens)
huggingface-cli login

# Download a model to the local cache
huggingface-cli download meta-llama/Llama-3.2-1B-Instruct
```

## CLI Reference

The `huggingface-cli` tool provides several commands for managing models and datasets:

### `huggingface-cli login`
Authenticates your local environment with your Hugging Face account using a User Access Token.

### `huggingface-cli download`
Downloads a model or dataset repository from the hub.

```bash
# Download a specific file from a repository
huggingface-cli download TheBloke/Llama-2-7B-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

### `huggingface-cli scan-cache`
Scans and lists the models currently stored in your local cache, helping manage disk space.

## Python API Examples

### Loading a Model and Tokenizer
Using the `transformers` library to load and run a model:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

inputs = tokenizer("The capital of France is", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0]))
```

### Managing the Hub Programmatically
Using `huggingface_hub` to interact with the repository structure:

```python
from huggingface_hub import HfApi

api = HfApi()

# List files in a model repository
files = api.list_repo_files(repo_id="meta-llama/Llama-3.2-1B-Instruct")
print(files)

# Upload a file to a repository
api.upload_file(
    path_or_fileobj="my_config.json",
    path_in_repo="configs/my_config.json",
    repo_id="username/my-cool-model",
    repo_type="model"
)
```

## Strengths
- **Massive Ecosystem**: The largest collection of open-source models and datasets in the world.
- **Interoperability**: Standardized formats (Safetensors, GGUF) and libraries make it easy to switch between models.
- **Community-Driven**: Rapid integration of new research and models.
- **Free Tier**: Extensive free access to models and hosting for public projects.

## Limitations
- **Complexity**: The sheer volume of models can be overwhelming for beginners.
- **Hardware Requirements**: While the hub is free, running the models locally requires significant GPU resources.
- **Model Quality**: Since anyone can upload models, quality and documentation vary significantly.

## When to use it
- When you need to find the latest open-source models for local deployment.
- When you want to use industry-standard libraries for ML development.
- When you need a place to share your own ML work with the community.

## When not to use it
- If you only need a simple, managed API (like OpenAI) and don't want to manage models yourself.
- If you are working in an environment with extremely strict data privacy requirements that forbid connecting to external hubs (though private/on-prem options exist).

## Licensing and cost
- **Open Source**: Yes (the libraries and many models).
- **Cost**: Free for public models/spaces; paid for private hosting and dedicated compute (Inference Endpoints).
- **Self-hostable**: No (the hub itself is a hosted service), but models downloaded from it are self-hostable.

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LiteLLM](../../services/litellm.md)
- [Local LLMs](../ai_knowledge/local_llms.md)
- [vLLM](../infrastructure/vllm.md)
- [Unsloth](../frameworks/unsloth.md)
- [LLaMA-Factory](../frameworks/llama-factory.md)
- [OpenCompass](../benchmarking/opencompass.md)

## Sources / References
- [Official Website](https://huggingface.co/)
- [Hugging Face Storage Buckets](https://thenewstack.io/hugging-face-now-offers-storage-buckets/)
- [Introducing Storage Buckets on the Hugging Face Hub](https://huggingface.co/blog/storage-buckets)
- [Hugging Face Documentation](https://huggingface.co/docs)
- [Hugging Face GitHub](https://github.com/huggingface)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
