# LiteLLM

## What it is
LiteLLM is an open-source proxy server that allows you to call 100+ LLM APIs (OpenAI, Anthropic, VertexAI, Bedrock, Azure, etc.) using a unified OpenAI-compatible format.

## What problem it solves
It eliminates the complexity of managing different SDKs and authentication methods for multiple AI providers. It also provides features like load balancing, fallback strategies, and cost tracking.

## Where it fits in the stack
**Provider Routing / Abstraction Layer**. It sits between your agents and the various LLM providers, acting as a traffic controller.

## Architecture overview
```text
[ Agent (Aider/OpenHands) ] ----> [ LiteLLM Proxy ] ----> [ OpenAI ]
                                               | ----> [ Anthropic ]
                                               | ----> [ Local Ollama ]
```

## Typical workflows
- **Unified Interface**: Using one API key and one endpoint to access any model.
- **Failover**: Automatically switching to a secondary model (e.g., GPT-4o to Claude 3.5) if the primary one is down or rate-limited.
- **Cost Management**: Tracking spend across different departments or projects using virtual keys.
- **Load Balancing**: Distributing requests across multiple instances of the same model to increase throughput.

## Strengths
- **Protocol Standardization**: Everything speaks "OpenAI Chat Completions".
- **Massive Provider Support**: Works with almost every known LLM API.
- **Self-hostable**: Complete control over your routing infrastructure.
- **Detailed Logging**: Excellent for debugging agent-LLM interactions.

## Limitations
- **Operational Overhead**: Requires managing a proxy service.
- **Complexity**: Advanced configurations (fallbacks, load balancing) require careful setup.

## When to use it
- When using multiple LLM providers across different agents.
- When you need a centralized place to track AI costs and usage.
- For building resilient systems that can survive provider outages.

## When not to use it
- If you only ever use a single provider (e.g., only OpenAI).
- For very simple, low-volume projects where the proxy is overkill.

## Security considerations
- **Proxy Authentication**: Secure the LiteLLM proxy with master keys.
- **Secret Management**: LiteLLM stores your provider API keys; ensure its configuration/environment is protected.
- **Logging Privacy**: Be mindful of what is logged (prompts/responses) if they contain sensitive data.

## Links to related pages
- [OpenRouter](../tools/ai_knowledge/openrouter.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Anthropic](../tools/ai_knowledge/anthropic.md)
- [Local LLMs](../tools/ai_knowledge/local_llms.md)

## Sources / References

- [Reference](https://docs.litellm.ai/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
