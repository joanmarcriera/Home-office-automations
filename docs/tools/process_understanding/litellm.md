# LiteLLM

## What it is
LiteLLM is a universal proxy for Large Language Models. It allows you to call 100+ LLM APIs using the standardized OpenAI format.

## What problem it solves
It solves the "API fragmentation" problem by providing a single interface for OpenAI, Anthropic, Gemini, Ollama, and more. It also handles retries, fallback logic, and budget tracking.

## Where it fits in the pipeline
**Reason / Proxy**

## Typical use cases (in this homelab / family automation context)
- **Model Switching**: Easily switching between a cheap local model (Ollama) and a powerful cloud model (GPT-4) based on task complexity.
- **Failover**: Automatically falling back to a local model if an API provider is down.
- **Cost Management**: Tracking spend across different AI-powered automations in the home.

## Integration points
- **AI Agents**: Serving as the backend for any agent framework that supports the OpenAI API format.
- **n8n / Dify**: Providing a single, stable endpoint for all LLM calls in complex workflows.
- **OpenHands**: Managing multiple model providers for a unified development experience.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Unmatched flexibility in model support.
- Very low overhead.
- Excellent for testing and rapid prototyping with different models.

## Limitations
- Requires careful configuration to manage all the different API keys.
- Adds a small layer of latency as a proxy.

## Alternatives / Related tools
- **One API**
- **Portkey**

## Links
- [Official Documentation](https://docs.litellm.ai/)
- [GitHub](https://github.com/BerriAI/litellm)
