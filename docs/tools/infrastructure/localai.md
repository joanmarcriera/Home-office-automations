# LocalAI

## What it is
LocalAI is a self-hosted, OpenAI-compatible inference platform for running local models without depending on proprietary cloud APIs.

## What problem it solves
It gives teams a local or self-hosted way to serve models behind a familiar API surface, which reduces vendor dependence and can lower marginal cost for internal workloads.

## Where it fits in the stack
**Infrastructure / Local Inference Platform**. It is part of the serving layer for teams that want private or self-hosted model access.

## Typical use cases
- Self-hosted internal AI APIs
- Replacing cloud APIs for low-risk internal workloads
- Running local models behind an OpenAI-compatible interface

## Strengths
- OpenAI-compatible surface for easier app integration
- Strong fit for privacy-sensitive internal tooling
- Useful bridge between local models and existing app stacks

## Limitations
- Model quality still depends on the local models you choose
- Running local inference well still requires ops and hardware discipline

## When to use it
- When data locality, cost control, or self-hosting matters
- When you want one local API surface for multiple internal tools

## When not to use it
- When you need frontier-model quality above all else
- When your team is not ready to own inference infrastructure

## Example company use cases
- **Internal helpdesk assistant**: answer policy or ops questions without sending data to external providers.
- **Drafting and classification**: handle low-risk summarization, tagging, and document enrichment locally.
- **Prototype lab**: give teams a local API for experiments before deciding what should stay local vs move to cloud models.

## Selection comments
- Use **LocalAI** when control and self-hosting matter more than absolute model quality.
- Use **Ollama** when you want simpler single-host local inference and desktop/server ergonomics.
- Use **llmfit** before committing, to verify which models actually fit your hardware envelope.

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](../ai_knowledge/lm-studio.md)
- [llmfit](../development_ops/llmfit.md)

## Sources / References
- [Official Website](https://localai.io/)
- [GitHub Repository](https://github.com/mudler/LocalAI)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
