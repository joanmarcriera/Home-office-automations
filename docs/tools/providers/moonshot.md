# Moonshot AI (Kimi)

## What it is
Moonshot AI (also known as Yuezhianmian) is a leading Chinese AI startup that developed the **Kimi** LLM family. As of late November/December 2026, their flagship proprietary API model is **Kimi K2.6**, featuring trillion-parameter reasoning and native support for 256K token context windows. In mid-July 2026, they also expanded their ecosystem with their first open-weights model, **Kimi K3**, a high-performance open-weight coding model designed for local deployment and specialized agentic coding workflows.

## What problem it solves
Enables the processing and analysis of massive documents, entire codebases, or long conversation histories. It serves as a high-performance alternative to Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.6 for long-context reasoning tasks, particularly in Chinese-language environments. In December 2026, it is frequently used with the **MCP 3.1 Task Protocol** for complex, multi-modal reasoning.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. Often used for "Chat with Document" applications, long-form content synthesis, and complex codebase navigation.

## Typical use cases
- **Large Document Analysis**: Summarizing and querying hundreds of pages of technical, legal, or medical text.
- **Codebase Navigation**: Providing context from an entire repository in a single prompt for better architectural understanding.
- **Intelligent Dialogue**: High-fidelity reasoning and visual reasoning (multimodal) in Chinese and English.
- **Automated Research**: Leveraging Kimi's long context for deep-dive literature reviews and data synthesis.
- **Local Coding and Codebase Interrogation**: Leveraging the open-weights **Kimi K3** model locally on developer hardware or private servers to securely analyze, generate, and refactor code without sending data over external APIs.

## Strengths
- **Native Long Context**: A pioneer in reliable 128k to 256k context windows, maintaining high retrieval accuracy (needle-in-a-haystack).
- **OpenAI Compatibility**: Kimi provides an OpenAI-compatible HTTP API, allowing developers to use the standard OpenAI SDKs by simply changing the `base_url`.
- **Trillion-Parameter Reasoning**: The proprietary K2.6 models offer state-of-the-art performance in complex logic and professional code generation.
- **Open-Weights Ecosystem (Kimi K3)**: The release of the Kimi K3 model brings powerful Chinese and English coding and reasoning capabilities to local consumer GPUs, eliminating API subscription constraints. Notably, Kimi K3 excels at complex one-shot generation and instruction compliance, with community benchmarks showing it frequently outperforming premier API models on high-fidelity single-turn coding queries.
- **Tool Calling**: Robust support for function calling and external tool integration, now optimized for **MCP 3.1 / FastMCP 3.1**.

## Limitations
- **Regional Optimization**: While globally accessible via API, the web interface and primary optimizations are centered on mainland China.
- **API Specifics**: Certain Kimi-specific extensions (like the `thinking` parameter) require `extra_body` configuration in standard SDKs.

## When to use it
- When your primary requirement is processing very large amounts of text (256k tokens) in a single context window with high reliability.
- For applications requiring high-fidelity Chinese language processing and reasoning.

## When not to use it
- If your workload requires fully local execution for strict offline air-gapped security.
- For purely image-generation-centric tasks (where specialized models might be preferred).

## Getting started
Moonshot AI provides an OpenAI-compatible API. Install the SDK:

```bash
pip install --upgrade 'openai>=1.0'
```

Initialize the client with the Moonshot base URL:

```python
from openai import OpenAI

client = OpenAI(
    api_key="$MOONSHOT_API_KEY",
    base_url="https://api.moonshot.ai/v1",
)
```

## CLI examples
```bash
# Test connection via curl
curl https://api.moonshot.ai/v1/models \
     -H "Authorization: Bearer $MOONSHOT_API_KEY"

# Chat via CLI using curl
curl https://api.moonshot.ai/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $MOONSHOT_API_KEY" \
     -d '{"model": "moonshot-v1-8k", "messages": [{"role": "user", "content": "Hi"}]}'
```

## API examples
Basic chat completion with strict **Pydantic v2** validation to verify and parse Kimi's output format:

```python
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
import os

# Define a strict schema for Kimi response parsing using Pydantic v2
class KimiResponseSchema(BaseModel):
    summary: str = Field(description="The generated summary of the document")
    raw_response: str = Field(description="The complete raw response content")
    confidence_score: float = Field(default=0.95, description="Self-reported generation confidence")

client = OpenAI(
    api_key=os.environ.get("MOONSHOT_API_KEY", "mock-key"),
    base_url="https://api.moonshot.ai/v1",
)

def fetch_kimi_summary() -> KimiResponseSchema:
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-256k",
            messages=[
                {"role": "system", "content": "You are Kimi, a helpful AI developed by Yuezhianmian/Moonshot."},
                {"role": "user", "content": "Summarize this long document."}
            ],
        )
        content = completion.choices[0].message.content or ""

        # Build structure for Pydantic v2 validation
        data = {
            "summary": content[:500],  # Example truncation/transformation
            "raw_response": content,
            "confidence_score": 0.98
        }

        # Strict schema validation using Pydantic v2
        return KimiResponseSchema.model_validate(data)
    except ValidationError as ve:
        print(f"Pydantic validation error: {ve}")
        raise
    except Exception as e:
        print(f"API call failed: {e}")
        raise
```

## Related tools / concepts
- [Dify](../ai_knowledge/dify.md)
- [LangChain](../ai_knowledge/langchain.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Perplexity](../providers/perplexity.md)
- [DeepSeek](deepseek.md)
- [MiniMax](minimax.md)
- [Kimi Code CLI](../ai_knowledge/kimi-cli.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://www.moonshot.cn/)
- [Kimi Open Platform](https://platform.kimi.ai/)
- [API Overview & Compatibility](https://platform.kimi.ai/docs/api/overview)
- [Quickstart Guide](https://platform.kimi.ai/docs/guide/start-using-kimi-api)
- [Simon Willison's Blog: Kimi K3 Announcement](https://simonwillison.net/2026/Jul/16/kimi-k3/#atom-entries)
- [Reddit r/LocalLLaMA: Kimi K3 ranks #1 on Afterquery SpreadsheetBench 2](https://www.reddit.com/r/LocalLLaMA/comments/1uzzecz/kimi_k3_ranks_1_on_afterquerys_spreadsheetbench_2/)
- [Reddit r/LocalLLaMA: All One-Shots from Kimi-K3 looks better than Opus 4.8](https://www.reddit.com/r/LocalLLaMA/comments/1vbf4bp/all_oneshots_from_kimik3_looks_better_than_opus48/)

## Contribution Metadata
- Last reviewed: 2026-12-21
- Confidence: high
