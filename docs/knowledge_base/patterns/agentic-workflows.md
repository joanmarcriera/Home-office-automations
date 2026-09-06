# Agentic Workflows

## What it is
Agentic workflows are design patterns where Large Language Models (LLMs) are not just used for single-turn responses, but are part of a multi-step, iterative process where they can reason, use tools, and make decisions to achieve a goal. As of early January 2027, agentic workflows natively incorporate Model Context Protocol (FastMCP 3.1) Task Protocol primitives to support structured, secure tool usage.

## What problem it solves
It enables the automation of complex tasks that require more than a single LLM call, such as multi-step research, software development, or sophisticated data analysis, by allowing the model to "think" and act over several turns. It addresses the reliability gap in complex automation by introducing feedback loops and reflection.

## Where it fits in the stack
It is the **Orchestration and Reasoning Layer** of the AI stack. It sits above the **Intelligence Layer** (individual models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Qwen 3.6 VL, Gemma 4, DeepSeek-V4, and Llama 4) and integrates with the **Tool/Action Layer** (APIs and services via FastMCP 3.1) to complete end-to-end tasks.

## Typical use cases
- **Autonomous Coding Assistants**: Agents that can write, test, and debug code (e.g., [Claude Code](../../tools/development_ops/claude-code.md), [Aider](../../tools/development_ops/aider.md)).
- **Complex Research Tasks**: Agents that can search the web using [Tavily](../../tools/providers/tavily.md) or [Exa AI](../../tools/providers/exa_ai.md), synthesize information with [Claude 5.6](../../tools/ai_knowledge/claude.md), and write reports.
- **Personal Assistants**: Agents that can manage calendars and handle emails using [GPT-5.6](../../tools/ai_knowledge/openai.md) and [Llama 4](../../tools/ai_knowledge/meta_llama.md).
- **Self-Healing Infrastructure**: Agents that monitor system logs and autonomously remediate service failures via FastMCP 3.1 Task Protocol.

## Strengths
- **Handles Complexity**: Can solve problems that are too difficult for a single LLM prompt.
- **Greater Autonomy**: Reduces the need for constant human intervention in multi-step processes.
- **Improved Performance**: Iterative reasoning and reflection (self-correction) lead to higher-quality results.

## Limitations
- **Reliability Issues**: Agents can sometimes get stuck in reasoning loops or hallucinate intermediate states.
- **Cost and Latency**: Multi-turn workflows consume significantly more tokens and take longer to complete.
- **Security Risks**: Autonomous tool use requires robust trust boundaries and permission management.

## When to use it
- When a task requires multiple steps, tool use, or iterative refinement (e.g., "Plan-and-Execute" pattern).
- When you want to automate a complex process that previously required significant human oversight.

## When not to use it
- For simple, straightforward tasks where a single LLM call is sufficient.
- When high speed and low cost are the primary requirements.

## Getting started
To build an agentic workflow, select a framework like [LangGraph](../../tools/frameworks/langgraph.md) or [CrewAI](../../tools/frameworks/crewai.md) and define the agent's state, tools, and reasoning loop.

### Core Concepts
- **Planning**: The agent breaks down a complex goal into smaller, manageable steps.
- **Tool Use**: The agent can interact with external systems (APIs, databases, web browsers) via FastMCP 3.1 Task Protocol.
- **Reflection**: The agent evaluates its own performance or output and makes adjustments.
- **Multi-agent Collaboration**: Multiple specialized agents work together.

## CLI examples
```bash
# Example: Running an Aider session to refactor a local repository
aider --model claude-5-6-sonnet --auto-test

# Using the CrewAI CLI to kick off a multi-agent task
crewai run "Analyze the latest market trends for NVIDIA"
```

## API examples

### Programmatic State & Reflection Validation (Pydantic v2)
The following Python script implements a strict reflection loop validation schema in LangGraph style utilizing Pydantic v2:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class ReflectionState(BaseModel):
    draft: str = Field(..., min_length=10, description="The current generated draft text")
    critique: Optional[str] = Field(default=None, description="The critique from the reflection stage")
    iteration: int = Field(default=0, ge=0, le=5)
    is_satisfactory: bool = Field(default=False)

    @field_validator('iteration')
    @classmethod
    def max_iterations_check(cls, v: int) -> int:
        if v > 5:
            raise ValueError("Too many reflection iterations. Prevented potential reasoning loop.")
        return v

class AgentAction(BaseModel):
    action_type: str = Field(..., pattern="^(call_tool|generate_draft|reflect_critique|complete)$")
    parameters: dict

def generate(state: ReflectionState) -> ReflectionState:
    # Simulates calling Claude 5.6 / GPT-5.6 to draft content
    print(f"Generating draft (Iteration: {state.iteration + 1})...")
    state.draft = "Substantive early January 2027 AI documentation standards."
    state.iteration += 1
    return state

def reflect(state: ReflectionState) -> ReflectionState:
    # Simulates calling Gemini 4.0 Ultra to critique the draft
    print("Reflecting and critiquing...")
    state.critique = "The draft is highly technical but could use more Pydantic v2 schemas."
    state.is_satisfactory = True  # Mark satisfactory once criteria are met
    return state

# Validation & flow execution demonstration
if __name__ == "__main__":
    # Initialize state
    state_data = {
        "draft": "Initial empty draft of standards document.",
        "iteration": 0,
        "is_satisfactory": False
    }

    # 1. Validate initial state
    state = ReflectionState.model_validate(state_data)

    # 2. Transition through generator stage
    state = generate(state)

    # 3. Transition through reflection stage
    state = reflect(state)

    # 4. Strict final validation
    final_validated = ReflectionState.model_validate(state.model_dump())
    print(f"Loop Complete! Satisfactory: {final_validated.is_satisfactory} | Iterations: {final_validated.iteration}")
```

## Related tools / concepts
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)
- [Tool Calling & MCP](tool-calling-and-mcp.md)
- [CrewAI](../../tools/frameworks/crewai.md)
- [Home Admin Agent Architecture](../home-admin-agent-architecture.md)
- [Model Routing Guide](../model_routing_guide.md)
- [System Prompts](../system_prompts.md)
- [LangGraph](../../tools/frameworks/langgraph.md)
- [Multi-Agent Systems](../../tools/agents/multi-agent-systems.md)

## Sources / References
- [Anthropic: Agentic Workflows](https://www.anthropic.com/news/agentic-workflows)
- [Andrew Ng: Agentic Design Patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)
- [Microsoft: AutoGen Framework](https://microsoft.github.io/autogen/)
- [LangChain: LangGraph Documentation and FastMCP 3.1 Task Protocol Integration](https://langchain-ai.github.io/langgraph/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
