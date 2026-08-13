# System Prompts

## What it is
System prompts (also known as system messages or developer messages) are the foundational instructions provided to a Large Language Model (LLM) before a conversation begins. They define the model's persona, its capabilities, its behavioral constraints, and the tone it should adopt.

## What problem it solves
Raw LLMs are often overly generic or prone to irrelevant outputs. System prompts "steer" the model toward a specific goal, ensuring it follows technical protocols (like tool-calling), maintains a consistent persona, and adheres to safety and style guidelines without the user having to repeat instructions in every message, fully leveraging late December 2026 SOTA reasoning engines such as Claude 5.1, GPT-5.5, Gemini 4.0 Pro/Flash, Llama 4, Gemma 3, Qwen 3.6, and FastMCP 3.1.

## Where it fits in the stack
It belongs to the **Interface & Configuration Layer** of the AI stack. It is the primary mechanism for aligning a generic **Intelligence Layer** (the model) with a specific **Application Layer** (the task).

## Typical use cases
- **Persona Definition**: Instructing a model to act as a "Senior Python Engineer" or a "Helpful Home Assistant."
- **Tool Orchestration**: Providing the model with a list of available functions and the JSON schema required to call them under modern standards.
- **Output Constraints**: Requiring all responses to be in valid Markdown, JSON, or a specific brevity level.
- **Chain-of-Thought Steering**: Encouraging the model to "think step-by-step" or "use a scratchpad" before providing a final answer.

## Strengths
- **Consistency**: Ensures the model's behavior remains stable across a multi-turn conversation.
- **Efficiency**: Reduces the need for long, repetitive user prompts (few-shot prompting).
- **Safety**: Hard-codes boundaries that prevent the model from generating restricted content.
- **MCP 3.1 Task Protocol Compliance**: Enables system prompts to explicitly define Task Protocol behaviors for autonomous state synchronization.

## Limitations
- **Prompt Injection**: Sophisticated user prompts can sometimes "bypass" or "jailbreak" system instructions.
- **Instruction Fatigue**: Very long system prompts can lead to "forgetting" earlier instructions or reduced performance on the core task.
- **Model Sensitivity**: Different models respond differently to the same system prompt; what works for GPT-5.5 may fail for Claude 5.1 or Qwen 3.6.

## When to use it
- When building any production-grade AI application where consistent behavior is required.
- When providing the model with access to external tools and APIs via function calling.

## When not to use it
- For quick, throwaway chat sessions where the model's default "Helpful Assistant" persona is sufficient.
- If you are using a base model (non-instruct) that is not trained to follow system instructions.

## Getting started
To begin engineering system prompts:
1. **Define the Role**: Clearly state who the model is (e.g., "You are an expert at YAML configuration").
2. **Set the Objective**: Explain the primary goal of the interaction.
3. **Establish Constraints**: List negative constraints (e.g., "Do not use external libraries").
4. **Format Requirements**: Specify the desired output structure (e.g., "Always return a valid JSON object").
5. **Test with Different Models**: Verify behavior across Claude 5.1, GPT-5.5, and Llama 4.

## CLI examples
While system prompts are typically passed via API, you can test them using various CLI tools.

```bash
# Testing a system prompt with Ollama (Llama 4)
ollama run llama4 "You are a concise technical writer. Explain MCP 3.1."

# Testing with the OpenAI CLI (GPT-5.5)
openai chat create --model gpt-5.5 --message system "Act as a Python security auditor." --message user "Analyze this script: ..."
```

## API examples
Most modern APIs use a list of message objects where the first message is often the system prompt.

### OpenAI / LiteLLM Pattern (GPT-5.5)
```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-5.5",
    messages=[
        {"role": "system", "content": "You are a senior DevOps engineer specializing in K3s and MCP 3.1."},
        {"role": "user", "content": "How do I secure my node?"}
    ]
)
```

### Anthropic Pattern (Claude 5.1)
Anthropic treats the system prompt as a separate top-level parameter. Below is an example that integrates MCP 3.1 / FastMCP 3.1 Task Protocol with strict Pydantic v2 validation for structured system prompts and behavioral constraints.

```python
import anthropic
from pydantic import BaseModel, Field
from typing import List, Optional
from mcp import Client, TaskProtocol

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-5-1-sonnet-20260731",
    system="You are a helpful assistant that always responds in Haiku.",
    messages=[
        {"role": "user", "content": "Tell me about MCP 3.1."}
    ]
)

# Incorporating Task Protocol with system prompts context
mcp_client = Client()
task_proto = TaskProtocol(mcp_client)

async def trigger_agent_task():
    task = await task_proto.create_task(
        name="Structured Prompt Execution",
        instruction="Deploy an agent using Claude 5.1 to auto-correct prompt injection patterns."
    )
    print(f"Task launched: {task.id}")

# Robust Pydantic v2 model to validate system prompt design and constraints
class PromptConstraint(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=5)
    criticality: str = Field(pattern="^(high|medium|low)$")

class SystemPromptTemplate(BaseModel):
    persona: str = Field(min_length=10)
    instructions: List[str] = Field(min_length=1)
    constraints: List[PromptConstraint]
    mcp_features_enabled: bool = True

# Verification logic of secure prompt configurations
raw_prompt_config = {
    "persona": "Senior DevOps Engineer specializing in secure K3s deployments",
    "instructions": [
        "Enforce strict mutual TLS configurations across all node templates.",
        "Always output clean, copy-pasteable YAML manifest files."
    ],
    "constraints": [
        {"name": "NoExternalLibraries", "description": "Do not import or suggest third-party Python packages", "criticality": "high"},
        {"name": "NoUnsecureSecrets", "description": "Never include hardcoded API keys, private keys, or credentials", "criticality": "high"}
    ]
}
validated_prompt = SystemPromptTemplate.model_validate(raw_prompt_config)
print(f"Validated system prompt configuration for persona: {validated_prompt.persona}")
```

## Related tools / concepts
- [Agent Protocols](agent_protocols.md)
- [Model Classes](model_classes.md)
- [Model Routing Guide](model_routing_guide.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Claude Code Router](../tools/development_ops/claude-code-router.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [Prompt Catalogue](../architecture/prompt-catalogue.md)
- [MCP Prompting Patterns](patterns/tool-calling-and-mcp.md)

## Sources / References
- [System Prompts Leaks GitHub](https://github.com/asgeirtj/system_prompts_leaks/tree/main)
- [Claude System Prompt Leak](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude.ai-human-readable.md)
- [GPT-5.5 System Prompt Analysis](https://openai.com/index/gpt-5-5-system-prompt-analysis)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
