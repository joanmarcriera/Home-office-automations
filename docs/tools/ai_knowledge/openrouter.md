# OpenRouter

## What it is
OpenRouter is a unified interface (meta-provider) for LLMs, providing access to almost any model (OpenAI, Anthropic, Meta, DeepSeek, etc.) via a single OpenAI-compatible API.

## What problem it solves
Eliminates the need to manage multiple API keys and client libraries for different providers. It also provides access to models that might be otherwise hard to access in certain regions.

## Where it fits in the stack
**Provider / Router Layer**. It sits between the Agent and the actual LLM Providers.

## Architecture overview
Proxy service. Your agent sends requests to OpenRouter, which then routes them to the specified backend provider (e.g., Together AI, DeepInfra, Anthropic directly).

## Typical workflows
- **Model Switching**: Easily testing different models (e.g., switching from Claude 3.5 to GPT-4o) just by changing the model ID string.
- **Unified Billing**: Paying one provider for usage across many different model families.
- **Accessing Open Models**: Using Llama 3, Qwen, or Mistral models without self-hosting.

## Strengths
- **Simplicity**: One API key for everything.
- **Model Variety**: Access to both proprietary and open-source models.
- **Standardized API**: Uses the OpenAI chat completions format.
- **Competitive Pricing**: Often finds the cheapest provider for a given open model.

## Limitations
- **Additional Latency**: Adds a small proxy overhead.
- **Dependency**: If OpenRouter is down, access to all routed models is lost.
- **Privacy**: Adds another party (OpenRouter) into the data flow.

## When to use it
- During development and testing to quickly compare models.
- When you want to use many different models without setting up accounts with every provider.
- For hobbyist/homelab projects that benefit from unified billing.

## When not to use it
- For latency-critical production applications.
- When you have direct enterprise agreements/discounts with a specific provider (e.g. Azure OpenAI).

## Security considerations
- **Third-party Data Flow**: Your prompts pass through OpenRouter; ensure this is acceptable for your data sensitivity.
- **API Key Security**: Treat your OpenRouter key as a "master key" for all your AI services.

## Links to related pages
- [LiteLLM](../../services/litellm.md)
- [OpenAI](openai.md)
- [Anthropic](anthropic.md)
