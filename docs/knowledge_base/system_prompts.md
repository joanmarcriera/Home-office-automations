# System Prompts

## What are System Prompts
System prompts (also known as system messages or developer messages) are the foundational instructions provided to a Large Language Model (LLM) before a conversation begins. They define the model's persona, its capabilities, its behavioral constraints, and the tone it should adopt.

In frontier models (high engineering), these prompts are often complex, multi-layered instructions that guide the model through sophisticated reasoning paths, tool-calling protocols, and safety alignments.

## Why They Matter
- **Persona & Tone**: They establish how the model interacts (e.g., helpful assistant, technical expert, concise reporter).
- **Capability Disclosure**: They inform the model about the tools it has access to (e.g., Python execution, web search, specific APIs).
- **Constraint Enforcement**: They set hard boundaries on what the model can and cannot do (e.g., no medical advice, no sensitive data handling).
- **Instruction Following**: A well-engineered system prompt improves the reliability and quality of the model's output.

## High Engineering Examples
Studying the system prompts of frontier models like Claude, GPT-4, and Gemini provides deep insight into how these models are aligned and how they handle complex tasks.

### System Prompt Collections
A curated collection of extracted system prompts from popular chatbots and frontier models.
- [System Prompts Leaks (asgeirtj/system_prompts_leaks)](https://github.com/asgeirtj/system_prompts_leaks/tree/main)

### Claude System Prompt
Anthropic's system prompt for Claude is a prime example of "high engineering" prompt design, featuring detailed instructions for tool use and response formatting.
- [Claude System Prompt](https://asgeirtj.github.io/system_prompts_leaks/Anthropic/claude.html)

## Related tools / concepts
- [Agent Protocols](agent_protocols.md)
- [Model Classes](model_classes.md)
- [Claude Code Router](../tools/development_ops/claude-code-router.md)

## Sources / References
- [System Prompts Leaks GitHub](https://github.com/asgeirtj/system_prompts_leaks/tree/main)
- [Claude System Prompt Leak](https://asgeirtj.github.io/system_prompts_leaks/Anthropic/claude.html)

## Contribution Metadata
- Last reviewed: 2026-03-09
- Confidence: high
