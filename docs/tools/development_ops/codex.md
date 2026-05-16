# OpenAI Codex (and Evolution to GPT-4o/O1/O3)

## What it is
OpenAI's coding-specialized model line (Codex) and its successors. While the specific "Codex" models (like `code-davinci-002`) are largely deprecated, their capabilities have been integrated and surpassed by newer frontier models like GPT-4o, O1, and O3. In current routing terms, this is the lane to use when the task is strongly code-centric.

## What problem it solves
Provides a specialized language model and tooling surface for code generation, editing, and implementation-oriented coding assistance. It reduces the cognitive load of syntax, boilerplate, and routine implementation tasks.

## Where it fits in the stack
**Development & Ops**. Functions as the underlying model powering several AI coding assistants, including [GitHub Copilot](github-copilot-cli.md), [Cursor](cursor.md), and [Aider](aider.md).

## Typical use cases
- Powering code completion tools in the IDE.
- Generating code from natural language descriptions or design specs.
- Translating between programming languages (e.g., Python to Rust).
- Editing, refactoring, or optimizing an existing codebase.
- Writing unit tests and implementation scaffolds.
- Debugging and explaining complex code blocks.

## Evolution of OpenAI Coding Models
1. **Codex (2021)**: The original specialized coding model.
2. **GPT-4 (2023)**: Integrated coding expertise with broad reasoning.
3. **GPT-4o (2024)**: Faster, multimodal, and highly efficient for real-time IDE completions.
4. **O1/O3 (2024-2025)**: Reasoning-heavy models designed for complex software engineering and logical problem solving.

## API Usage Example (Chat Completion)
Most modern coding tasks use the standard Chat Completions API with a coding-specific system prompt.

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are an expert software engineer. Provide only high-quality, commented code."},
    {"role": "user", "content": "Write a Python script to perform a BFS on a graph."}
  ]
)

print(response.choices[0].message.content)
```

## Strengths
- Unmatched code-specialized behavior in frontier models.
- Deep understanding of modern libraries, frameworks, and patterns.
- Strong fit for code generation, refactors, and test-writing loops.
- Excellent performance in [SWE-bench](../benchmarking/swe-bench.md) and other coding benchmarks.

## Limitations
- Proprietary; no self-hosted option.
- API costs can scale quickly for large codebase indexing.
- Knowledge cutoff may affect very recent library updates.
- Best used as a specialized lane, not a universal default for all reasoning tasks.

## When to use it
- When using GitHub Copilot or other tools built on OpenAI's coding models.
- When evaluating code-specialized models against general-purpose LLMs.
- When the task is code-centric enough to justify a specialized coding lane.
- For complex refactors that require a high degree of logical reasoning (O1/O3).

## When not to use it
- When you need a self-hosted or open-source code model.
- When the task is not primarily code-related.
- When you require a model with an absolute up-to-the-minute knowledge base of very niche new libraries.

## Model routing

Use `gpt-4o` or `o1-preview` when:
- The task is mostly code and requires high precision.
- You want source-editing behavior.
- You are building inside an IDE, CLI, or code agent flow.

Do not use it when:
- The task is mainly broad research without implementation.
- You need a local/offline model for privacy reasons.
- You actually need the broader deliberate reasoning of GPT-5.4/O3 for non-code planning.

Best pairings:
- Default coding lane: [Anthropic Sonnet](../providers/anthropic.md) (highly competitive with GPT-4o for code).
- Central policy: [Model Routing Guide](../../knowledge_base/model_routing_guide.md).
- Local fallback: [Llama 3](../ai_knowledge/llama-3.md) (fine-tuned for code).

## Implementation Example: CLI Integration
Many developers use these models via CLI tools for rapid prototyping.

```bash
# Example using a tool like Aider
aider --model gpt-4o

# Example using OpenAI CLI directly
openai api chat.completions.create -m gpt-4o -g user "Implement a thread-safe singleton in Java"
```

## Related tools / concepts
- [GitHub Copilot](github-copilot-cli.md)
- [Cursor](cursor.md)
- [Aider](aider.md)
- [OpenAI](../ai_knowledge/openai.md)
- [Anthropic](../providers/anthropic.md)
- [SWE-bench](../benchmarking/swe-bench.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Sources / references
- [OpenAI Models Overview](https://platform.openai.com/docs/models)
- [OpenAI Codex (Legacy)](https://openai.com/blog/openai-codex)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
