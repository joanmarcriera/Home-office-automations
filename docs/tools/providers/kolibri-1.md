# Kolibri-1

## What it is
Kolibri-1 is an open-weight mixture-of-experts (MoE) language model released by Aleph Alpha on 2026-10-03 under the Apache 2.0 licence. It has 78 billion total parameters with about 3.46 billion active per token, 50 layers with 384 experts per layer, FP8 weights with dynamically quantised activations, and a 1,048,576-token context window (262,144 tokens recommended for efficiency). It is designed for German and English and offers a reasoning mode with configurable effort.

## What problem it solves
It provides a European-origin, permissively licensed model with strong German/English coverage, long context, reasoning, retrieval-augmented generation, agentic tool calling and coding support, with low per-token compute thanks to sparse activation.

## Where it fits in the stack
**Provider / model weights.** A self-hostable foundation model that can be served behind an OpenAI-compatible inference engine and used by agents, RAG pipelines and coding tools.

## Typical use cases
- Bilingual (German/English) assistants and RAG.
- Agentic tool calling with an explicit reasoning mode.
- Long-context document analysis.
- Self-hosted inference where data must stay on premises.

## Strengths
- Apache 2.0 licence.
- Sparse MoE: about 3.46B active parameters of 78B total.
- Trained on 20T filtered tokens (62.5% English, 23.9% German, 13.6% code), knowledge cutoff 2026-06-18.
- Very long context window (1,048,576 tokens).

## Limitations
- Weights occupy roughly 78 GB; the model card lists a minimum of 2x A100 80GB GPUs or equivalent, which excludes typical homelab GPUs.
- Language focus is German and English; other languages are not documented as supported.
- Released days before this page was written; no independent benchmarks were reviewed.

## When to use it
- When you have data-centre-class GPUs and need an open German/English model with reasoning and tool calling.

## When not to use it
- On consumer or single small-GPU hardware.
- For workloads needing broad multilingual coverage beyond German and English.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0, open weights)
- **Cost**: Free weights; GPU hardware costs apply
- **Self-hostable**: Yes

## Related tools / concepts
- [Hugging Face](huggingface.md) - hosts the model card and weights.
- [Mistral AI](mistral.md) - another European open-weight model provider.
- [Providers overview](index.md)

## Sources / References
- [Aleph-Alpha/Kolibri-1 model card (Hugging Face)](https://huggingface.co/Aleph-Alpha/Kolibri-1)
- [r/LocalLLaMA announcement thread](https://www.reddit.com/r/LocalLLaMA/comments/1wwl7y6/alephalphakolibri1_hugging_face_78b_parameters/) (original intake source; not fetchable, not used for facts)

## Contribution Metadata
- Last reviewed: 2026-10-05
- Confidence: medium
