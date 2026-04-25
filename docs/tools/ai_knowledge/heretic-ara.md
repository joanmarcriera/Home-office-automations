# Heretic / ARA

## What it is
Heretic is an experimental AI model project that implements the ARA (Ablative Refusal Alignment) decensoring method. It aims to provide high-performance models with minimal to no refusal behavior while maintaining reasoning capabilities.

## What problem it solves
It addresses the issue of "refusal alignment" in large language models, where models frequently refuse to answer harmless or contextually relevant queries due to over-zealous safety guardrails.

## Where it fits in the stack
**AI Assistants & Knowledge / Local Models**. It is typically used by researchers and enthusiasts who require uncensored or "abliterated" models for specific use cases.

## Typical use cases
- **Research and Analysis**: Exploring model behavior without safety-induced bias.
- **Creative Writing**: Generating content that might trigger standard safety filters but is legitimate in a creative context.
- **System Stress Testing**: Testing the limits of model reasoning when guardrails are removed.

## Strengths
- **Minimal Refusal**: High success rate in answering queries that standard models refuse.
- **Preserved Reasoning**: Aims to maintain the underlying logic and reasoning of the base model despite decensoring.
- **Local Execution**: Compatible with common local inference engines like llama.cpp and Ollama.

## Limitations
- **Experimental**: The ARA method is still in research and may introduce unpredictable behaviors.
- **Safety Risks**: Removal of guardrails means the model can generate harmful content if prompted; users must apply their own safety layers.

## When to use it
- When you encounter persistent refusals for legitimate tasks with standard aligned models.
- For local-first applications where you manage your own safety boundaries.

## When not to use it
- In production environments with untrusted users where safety guardrails are mandatory.
- If you require the most stable and predictable model behavior.

## Related tools / concepts
- [Qwen](qwen.md)
- [Local LLMs](local_llms.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [Ollama](../../services/ollama.md)

## Sources / References
- [Heretic has finally defeated GPT-OSS with a new decensoring method ARA](https://www.reddit.com/r/LocalLLaMA/comments/1rnic0a/heretic_has_finally_defeated_gptoss_with_a_new/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
