# Kimi CLI

## What it is
Kimi CLI is a command-line interface tool for interacting with Moonshot AI's Kimi models. It allows developers to access Kimi's large language model capabilities directly from their terminal.

## What problem it solves
It enables terminal-based AI assistance, allowing for quick queries, file-based processing, and integration into developer workflows without leaving the command line.

## Where it fits in the stack
**AI Assistants & Knowledge**. It is a local tool that acts as a bridge between the user's terminal and Moonshot AI's cloud-based models.

## Typical use cases
- Querying Kimi for coding assistance or general information from the terminal.
- Piping file contents to Kimi for analysis or summarization.
- Automating LLM-based tasks via shell scripts.

## Strengths
- Lightweight and easy to install.
- Supports long context (Moonshot AI is known for high context windows).
- Good performance for Chinese and English language tasks.

## Limitations
- Requires a Moonshot AI API key.
- Primarily focused on Moonshot's proprietary models.

## When to use it
- If you are already using Moonshot AI models and want a native CLI experience.
- When you need to process large amounts of text or code within the terminal using Kimi.

## When not to use it
- If you prefer a local-only model (consider [Ollama](../../services/ollama.md)).
- If you require tight IDE integration (consider [Cursor](../development_ops/cursor.md) or [Aider](../development_ops/aider.md)).

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free (CLI), API usage is paid per token.
- **Self-hostable**: No (Cloud-based models).

## Getting started

### Installation
Official Kimi CLI tools are often provided as community wrappers or via the Moonshot AI platform SDK.

```bash
# Example installation for a common community wrapper
pip install kimi-cli
```

### Configuration
Set your API key as an environment variable:
```bash
export MOONSHOT_API_KEY="your_api_key_here"
```

### Hello World
```bash
kimi "Explain the basics of quantum computing in one sentence."
```

## CLI examples
```bash
# Ask a question
kimi "How do I list files in a directory sorted by size?"

# Pipe a file for summarization
cat README.md | kimi "Summarize this file in 3 bullet points."

# Use a specific model if supported
kimi --model moonshot-v1-8k "Hello!"
```

## API examples
While the CLI is a wrapper, you can interact with the underlying API using standard OpenAI-compatible libraries.

### Python Example
```python
from openai import OpenAI

client = OpenAI(
    api_key="MOONSHOT_API_KEY",
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "user", "content": "Hello Kimi!"}
    ],
)

print(completion.choices[0].message.content)
```

## Related tools / concepts
- [Moonshot AI](../providers/moonshot.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Ollama](../../services/ollama.md)

## Sources / References
- [Moonshot AI Platform](https://platform.moonshot.cn/)
- [Kimi Code Subscription](https://www.kimi.com/code)

## Contribution Metadata
- Last reviewed: 2026-04-28
- Confidence: high
