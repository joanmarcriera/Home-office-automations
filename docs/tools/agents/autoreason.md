# AutoReason

## What it is
AutoReason (v2026.5.x+) is an autonomous reasoning framework by Nous Research designed to enable LLMs to perform complex, multi-step logical tasks with minimal human intervention. It implements advanced "Reasoning-as-a-Service" patterns, allowing models like Nous Hermes 3 (Llama 3.1 based) and [Gemma 3](../ai_knowledge/local_llms.md) to compete with proprietary reasoning models like the O4 series.

## What problem it solves
It addresses the limitations of standard chain-of-thought prompting by providing a structured environment for iterative reasoning, verification, and correction. It helps LLMs navigate large "search spaces" in complex logic, mathematics, or code problems where the first answer is rarely the correct one, effectively reducing hallucinations through automated self-critique.

## Where it fits in the stack
**Category**: Agent / Reasoning Engine. It operates as an orchestration layer above the raw inference API, wrapping model calls in a "Verify-and-Correct" loop that integrates with external verification tools (interpreters, checkers, MCP servers).

## Typical use cases
- **Complex Logical Puzzles**: Problems requiring backtracking and testing multiple conflicting hypotheses.
- **Mathematical Theorem Proving**: Structured steps with rigorous automated verification requirements.
- **Code Debugging**: Identifying root causes by iteratively testing assumptions against a live execution environment.
- **Deep Research**: Multi-hop reasoning tasks where the results of one step fundamentally redefine the search parameters for the next.
- **Synthetic Data Generation**: Creating high-quality reasoning traces for fine-tuning smaller models.

## Strengths
- **Self-Correction**: Significantly reduces hallucinations by requiring the model to "show its work" and then programmatically check it.
- **Open-Source**: Developed with a focus on open-weight model compatibility (Nous Hermes, Llama 3.1, DeepSeek, Gemma 3).
- **Structured Trace**: Provides a complete, auditable log of every reasoning step and correction.
- **Flexibility**: Can be integrated with any Python-based verification tool or MCP-enabled service.

## Limitations
- **High Token Consumption**: Iteration and verification loops can consume 5-10x more tokens than single-shot inference.
- **Inference Latency**: Not suitable for real-time human interaction; tasks often take seconds or minutes to converge.
- **Complexity**: Writing effective "verifiers" for new domains requires specialized prompt engineering and coding.

## When to use it
- **High-Stakes Logic**: When the cost of an incorrect logical step is high and multi-step verification is available.
- **Open-Weight Model Optimization**: When trying to achieve "reasoning" performance on par with proprietary models using local/open-weights.
- **Iterative Debugging**: For complex code issues where the agent must "test" a hypothesis and receive feedback from a runtime.
- **Non-Interactive Batch Tasks**: Ideal for "overnight" research or optimization tasks.

## When not to use it
- **Low-Latency Chat**: The iterative nature makes it too slow for standard conversational UI.
- **Simple Summarization**: For tasks that don't require logic (e.g., "summarize this email"), the overhead is unjustifiable.
- **Strict Budget Constraints**: High token usage makes it expensive for high-volume, low-value tasks.

## Getting started

### Installation
```bash
git clone https://github.com/NousResearch/autoreason.git
cd autoreason
pip install -r requirements.txt
```

### Basic Configuration
Configure the `config.yaml` to point to your preferred reasoning model (e.g., local Ollama instance or LiteLLM proxy).

## CLI examples

### Reasoning Task
```bash
# Run the main experiment runner for a reasoning task
python run_reasoning.py --task "Prove the square root of 2 is irrational"
```

### Code Debugging
```bash
# Run the code-specific debugger on a local directory
python run_code_debug.py --path ./src/buggy_project
```

### MCP Server
```bash
# Launch the reasoning-as-a-service MCP server
python -m autoreason.mcp_server --port 18795
```

## API examples

### Python (Reasoner)
```python
from autoreason import Reasoner

# Initialize with a high-reasoning model and a Python verifier
reasoner = Reasoner(
    model="nous-hermes-3-llama-3.1-70b",
    verifier="python_interpreter"
)

# Solve a complex causal reasoning task
result = reasoner.solve("Simulate the impact of a 2% interest rate hike on the housing market.")

# Access the final answer and the iterative reasoning trace
print(f"Final Answer: {result.final_answer}")
print(f"Total Iterations: {len(result.iterations)}")
```

### Async Usage
```python
# Async example for integration into larger agentic flows
async def run_reasoning():
    result = await reasoner.solve_async("Find the bug in this complex async loop.")
    return result.final_answer
```

## Related tools / concepts
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Agno](agno.md)
- [Letta](letta.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Software Factories](../../knowledge_base/patterns/software-factories.md)
- [Prompt Requests](../../knowledge_base/patterns/prompt_requests.md)
- [Jules](../ai_knowledge/jules.md)
- [Claude 4.8](../ai_knowledge/claude-4-8.md)
- [Gemma 3](../ai_knowledge/local_llms.md)

## Sources / references
- [NousResearch/autoreason GitHub](https://github.com/NousResearch/autoreason)
- [Nous Research Blog: Iterative Reasoning Patterns](https://nousresearch.com/blog/)

## Contribution Metadata
- Last reviewed: 2026-07-10
- Confidence: high
