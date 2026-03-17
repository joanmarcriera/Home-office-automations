# llmfit

## What it is
llmfit is a hardware-to-model fit utility that helps you determine which models and providers are realistic for your machine.

## What problem it solves
It prevents wasted time trying to run models that do not fit your hardware or performance requirements.

## Where it fits in the stack
**Development & Ops / Model Selection Utility**. It is a planning tool for local AI deployment decisions.

## Typical use cases
- Choosing models for local inference
- Comparing what can run on different hardware profiles
- Deciding whether to use LocalAI, Ollama, or a cloud provider

## Strengths
- Fast hardware reality check
- Useful before investing in local inference setup

## Limitations
- It helps with feasibility, not workload design
- It does not choose the right workflow architecture for you

## When to use it
- Before standing up local model infrastructure

## When not to use it
- When you already know you will use hosted frontier APIs

## Related tools / concepts

- [Ollama](../../services/ollama.md)
- [LM Studio](../ai_knowledge/lm-studio.md)
- [LocalAI](../infrastructure/localai.md)

## Sources / References
- [GitHub Repository](https://github.com/AlexsJones/llmfit)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
