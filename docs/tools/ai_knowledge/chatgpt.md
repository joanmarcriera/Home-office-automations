# ChatGPT

## What it is
ChatGPT is an AI-powered chatbot developed by OpenAI. It uses large language models to provide human-like responses to various prompts and questions.

## What problem it solves
Provides a general-purpose conversational AI interface for brainstorming, drafting text, answering questions, and completing a wide range of language tasks without requiring technical setup.

## Where it fits in the stack
AI & Knowledge — used as a cloud-based conversational assistant alongside local LLM options.

## Typical use cases
- Drafting and editing text, emails, and documentation.
- Answering research questions and summarizing information.
- **Excel Data Integration**: Direct data processing and financial integrations within Excel (launched 2026-03-06).
- **Advanced Education**: New ways to learn math and science with interactive step-by-step guidance (launched 2026-03-11).
- Exploring Custom GPTs for repository-specific or domain-specific knowledge.

## Strengths
- Broad general knowledge and strong reasoning capabilities
- Easy to use with no local infrastructure required
- Extensible through Custom GPTs and plugin ecosystem

## Limitations
- Requires an internet connection and sends data to OpenAI servers
- Not privacy-first; unsuitable for sensitive or private data without additional safeguards
- Usage beyond the free tier requires a paid subscription or API credits

## When to use it
- When you need quick, high-quality text generation or brainstorming and privacy is not a concern
- When local LLM infrastructure is unavailable or insufficient for the task

## When not to use it
- When working with sensitive or private data that should not leave the local network
- When deterministic, reproducible outputs are required

## Licensing and cost
- **Open Source**: No (Proprietary).
- **Cost**: Free tier available; "Plus" subscription for priority access and GPT-4o; usage-based API.
- **Self-hostable**: No.

## Getting started

### Web Interface
1. Visit [chatgpt.com](https://chatgpt.com/).
2. Log in with an OpenAI, Google, or Microsoft account.
3. Type a message in the chat bar to begin.

### OpenAI API
For programmatic access to ChatGPT models (gpt-4o, gpt-4-turbo, etc.):
1. Create an account at [platform.openai.com](https://platform.openai.com/).
2. Add credits to your billing account.
3. Create an API key.
4. Install the library: `pip install openai`.

## CLI examples

### Official OpenAI CLI
OpenAI provides a CLI tool as part of the `openai` Python package:

```bash
# Set your API key
export OPENAI_API_KEY='your-api-key'

# Simple chat completion from terminal
openai api chat_completions.create -m gpt-4o -g user "What is the capital of France?"

# List available models
openai api models.list
```

### Unofficial CLI (using `shell-gpt`)
A popular way to use ChatGPT for terminal automation:

```bash
# Install Shell GPT
pip install shell-gpt

# Use it as a filter (REPL style)
ls | sgpt "summarize these files"

# Request a shell command (Dangerous, use with caution)
sgpt --shell "find all python files larger than 1MB"
```

## API examples

### Python (OpenAI SDK)
Standard synchronous request for a chat completion:

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a one-sentence summary of the Pydantic v2 changes."}
    ]
)

print(response.choices[0].message.content)
```

### JSON Mode
Ensuring the model returns a valid JSON object for automation:

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
        {"role": "user", "content": "List the top 3 cities in Japan by population as JSON."}
    ]
)

print(response.choices[0].message.content)
```

## Related tools / concepts
- [Claude](claude.md) — The leading reasoning competitor from Anthropic.
- [Gemini](gemini.md) — Google's multimodal AI integration.
- [Perplexity](perplexity.md) — AI-native search focused on citations.
- [OpenAI](../providers/openai.md) — Detailed overview of the provider ecosystem.
- [DeepSeek R1](deepseek-r1.md) — An open-weight reasoning alternative.
- [Everything Claude Code](everything-claude-code.md) — For comparison with Anthropic's agentic tools.
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) — Official technical docs.
- [Local LLMs](local_llms.md) — Privacy-focused alternatives.

## Sources / references
- [Official Website](https://chatgpt.com/)
- [ChatGPT for Excel](https://openai.com/index/chatgpt-for-excel)
- [New ways to learn math and science in ChatGPT](https://openai.com/index/new-ways-to-learn-math-and-science-in-chatgpt)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
