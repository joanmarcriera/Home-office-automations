# Mistral AI

## What it is
Mistral AI is a European AI company that develops both open-weight and commercial large language models, including the Mistral, Mixtral, and Codestral families. It has evolved from a model provider into a full agentic platform with native support for tool calling, persistent conversations, and standardized protocols.

## What problem it solves
Provides a high-performance, efficient alternative to American providers, offering some of the best-performing open-weight models for self-hosting and a robust API for agentic workflows.

## Where it fits in the stack
**LLM Provider** and **Agent Platform**. Offers both a hosted API (La Plateforme) and models that can be run locally via tools like Ollama or vLLM.

## Typical use cases
- **Agentic Workflows**: Building autonomous agents that use web search, code execution, and MCP tools.
- **Local Deployment**: Running Mixtral 8x7B or Mistral Nemo on-premises for privacy.
- **Code Assistance**: Using Codestral or Devstral for specialized programming tasks and coding agents.
- **Multimodal Applications**: Processing images and text together with Pixtral or Mistral Large 3.

## Getting started
Install the SDK:
```bash
pip install mistralai
```

Basic API call (Python):
```python
from mistralai import Mistral
import os

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)
print(chat_response.choices[0].message.content)
```

## Model Families
- **Mistral Large 3**: Flagship multimodal model with 256k context window and powerful agentic capabilities.
- **Ministral Family**: Compact models (3B, 8B, 14B) designed for edge devices and efficient local hosting.
- **Magistral**: Specialized reasoning models with transparent, verifiable thinking steps.
- **Codestral / Devstral**: Purpose-built models for code generation, FIM (Fill-In-the-Middle), and coding agents.
- **Pixtral**: Multimodal models capable of native vision and text processing.
- **Voxtral**: Specialized audio models for high-accuracy speech-to-text and transcription.

## Agentic Capabilities
Mistral provides a first-class Agents API that goes beyond simple completions:
- **Built-in Tools**: Native connectors for **Web Search**, **Code Interpreter**, and **Image Generation**.
- **Model Context Protocol (MCP)**: Native support in the Python SDK for connecting to any MCP server to extend agent capabilities.
- **Persistent Conversations**: Built-in state management for long-running agent interactions.
- **Agent Handoffs**: Orchestrate multi-agent workflows where agents can hand off tasks to specialized sub-agents.

## Strengths
- **Efficiency**: Known for "punching above their weight" in terms of parameter count vs performance.
- **Open Weights**: Many models are released under Apache 2.0 or Mistral Research License, allowing local hosting.
- **Native MCP Support**: Direct integration with the Model Context Protocol standard.
- **European Sovereignity**: High-performance AI hosted and developed in the EU.

## Limitations
- **API Maturity**: While rapidly catching up, some advanced features like complex model distillation are still evolving compared to OpenAI.
- **Safety Tuning**: Generally follows a more pragmatic approach to safety, which may require more specific guardrailing for certain enterprise use cases.

## When to use it
- When you want to avoid vendor lock-in with open-weight models.
- For building agents that need standardized tool access via MCP.
- For high-performance European-hosted AI requirements.
- For specialized coding tasks.

## When not to use it
- If your workflow is deeply coupled with proprietary OpenAI features like GPTs or specific Assistants API implementations that don't map to Mistral Agents.

## Licensing and cost
- **Free Tiers**:
    - **Free API Tier**: Available on **La Plateforme** for development, testing, and individual usage (subject to rate limits).
    - **Le Chat**: Free-to-use conversational interface at [chat.mistral.ai](https://chat.mistral.ai/).
- **Open Source**: Yes (Mistral 7B, Mixtral 8x7B/8x22B are Apache 2.0; others vary by model).
- **Commercial**: Paid API usage and enterprise licensing for self-deployment.

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [vLLM](../infrastructure/vllm.md)
- [Model Context Protocol (MCP)](../../knowledge_base/agent_protocols.md)
- [DeepSeek](../ai_knowledge/deepseek.md)

## Sources / References
- [Official Website](https://mistral.ai/)
- [Mistral Documentation](https://docs.mistral.ai/)
- [Mistral Models Overview](https://mistral.ai/models)
- [Mistral Agents Introduction](https://docs.mistral.ai/agents/introduction/)

## Contribution Metadata
- Last reviewed: 2026-03-03
- Confidence: high
