# Mistral AI

## What it is
Mistral AI is a European AI company that develops both open-weight and commercial large language models, including the **Mistral 7B**, **Mixtral 8x7B**, **Mixtral 8x22B**, and the **Codestral** families.

## What problem it solves
Provides a high-performance, efficient alternative to American providers, offering some of the best-performing open-weight models for self-hosting and private deployment.

## Where it fits in the stack
**LLM Provider**. Offers both a hosted API (La Plateforme) and models that can be run locally via tools like Ollama or vLLM.

## Typical use cases
- **Local Deployment**: Running Mixtral 8x7B or Mistral Nemo on-premises for maximum data privacy.
- **Code Assistance**: Using Codestral for specialized programming tasks and FIM (Fill-In-the-Middle) operations.
- **Efficient Inference**: Using small but capable models (Ministral) for high-volume, low-cost tasks.

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

## Strengths
- **Efficiency**: Known for "punching above their weight" in terms of parameter count vs performance (e.g., Mixtral's Sparse MoE architecture).
- **Open Weights**: Many flagship models are released under Apache 2.0 or Mistral Research License, allowing local hosting.
- **Codestral**: Highly capable model specifically for code generation and professional software development.
- **Pricing Tiers**: Extremely competitive pricing through **La Plateforme**, ranging from the ultra-cheap **Ministral** and **Mistral Small** to the flagship **Mistral Large**.

## Limitations
- **API Maturity**: While improving rapidly, the API featureset (e.g., complex tool use, Assistants-style abstractions) has historically trailed OpenAI.
- **Safety Tuning**: Generally less "preachy" than US counterparts, which may require more careful prompting for specific alignment needs.

## When to use it
- When you want to avoid vendor lock-in by using open-weight models.
- For high-performance, European-hosted AI services that comply with GDPR.
- For specialized coding tasks where Codestral excels.

## When not to use it
- If you require deeply integrated multi-modal native support (e.g., vision/audio/image gen) in a single unified API.
- If your workflow is already heavily reliant on OpenAI-specific features like GPTs.

## Licensing and cost
- **Open Source**: Yes (Mistral 7B, Mixtral 8x7B/8x22B are Apache 2.0; others vary).
- **Cost**: Free (Self-hosted) / Paid (API).
- **Self-hostable**: Yes.

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [vLLM](../infrastructure/vllm.md)
- [DeepSeek](../ai_knowledge/deepseek.md)

## Sources / References
- [Official Website](https://mistral.ai/)
- [Mistral Documentation](https://docs.mistral.ai/)
- [Mistral News](https://mistral.ai/news)

## Contribution Metadata
- Last reviewed: 2026-03-02
- Confidence: high
