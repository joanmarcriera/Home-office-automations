# System Prompts

## What it is
System prompts (also known as system messages or developer messages) are the foundational instructions provided to a Large Language Model (LLM) before a conversation begins. They define the model's persona, its capabilities, its behavioral constraints, and the tone it should adopt.

## What problem it solves
Raw LLMs are often overly generic or prone to irrelevant outputs. System prompts "steer" the model toward a specific goal, ensuring it follows technical protocols (like tool-calling), maintains a consistent persona, and adheres to safety and style guidelines without the user having to repeat instructions in every message.

## Where it fits in the stack
It belongs to the **Interface & Configuration Layer** of the AI stack. It is the primary mechanism for aligning a generic **Intelligence Layer** (the model) with a specific **Application Layer** (the task).

## Typical use cases
- **Persona Definition**: Instructing a model to act as a "Senior Python Engineer" or a "Helpful Home Assistant."
- **Tool Orchestration**: Providing the model with a list of available functions and the JSON schema required to call them.
- **Output Constraints**: Requiring all responses to be in valid Markdown, JSON, or a specific brevity level.
- **Chain-of-Thought Steering**: Encouraging the model to "think step-by-step" or "use a scratchpad" before providing a final answer.

## Strengths
- **Consistency**: Ensures the model's behavior remains stable across a multi-turn conversation.
- **Efficiency**: Reduces the need for long, repetitive user prompts (few-shot prompting).
- **Safety**: Hard-codes boundaries that prevent the model from generating restricted content.

## Limitations
- **Prompt Injection**: Sophisticated user prompts can sometimes "bypass" or "jailbreak" system instructions.
- **Instruction Fatigue**: Very long system prompts can lead to "forgetting" earlier instructions or reduced performance on the core task.
- **Model Sensitivity**: Different models respond differently to the same system prompt; what works for GPT-4o may fail for Claude 3.5 Sonnet.

## When to use it
- When building any production-grade AI application where consistent behavior is required.
- When providing the model with access to external tools and APIs via function calling.

## When not to use it
- For quick, throwaway chat sessions where the model's default "Helpful Assistant" persona is sufficient.
- If you are using a base model (non-instruct) that is not trained to follow system instructions.

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
- [Claude System Prompt](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude.ai-human-readable.md)

### GPT-5.5 Multi-Agent System Prompt
OpenAI's latest system prompt for GPT-5.5 includes specific instructions for coordinating with sub-agents and managing persistent memory across sessions.
- [GPT-5.5 System Prompt Analysis](https://openai.com/index/gpt-5-5-system-prompt-analysis)

### Model Context Protocol (MCP) Prompt Integration
Modern system prompts now include standardized blocks for MCP server discovery and tool use, allowing models to dynamically understand their available environment.
- [MCP Prompting Patterns](patterns/tool-calling-and-mcp.md)

## Related tools / concepts
- [Agent Protocols](agent_protocols.md)
- [Model Classes](model_classes.md)
- [Model Routing Guide](model_routing_guide.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Claude Code Router](../tools/development_ops/claude-code-router.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [Prompt Catalogue](../architecture/prompt-catalogue.md)

## Sources / References
- [System Prompts Leaks GitHub](https://github.com/asgeirtj/system_prompts_leaks/tree/main)
- [Claude System Prompt Leak](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude.ai-human-readable.md)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
