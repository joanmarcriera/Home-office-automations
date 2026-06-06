# Codestral

## What it is
Codestral is an open-weight generative AI model explicitly designed for code generation tasks. Developed by [Mistral AI](mistral.md), it is a 22B parameter model optimized for over 80 programming languages, including Python, Java, C++, and JavaScript.

## What problem it solves
It provides a high-performance, specialized model for coding tasks that can be run locally or via API, offering an alternative to general-purpose LLMs that may lack deep proficiency in niche programming languages or complex code structures.

## Where it fits in the stack
**Inference Provider / Specialized Model**. It acts as a specialized backend for IDE extensions, autonomous coding agents, and CI/CD pipelines.

## Typical use cases
- **Code Completion**: Providing real-time FIM (Fill-In-the-Middle) suggestions in IDEs.
- **Test Generation**: Automatically writing unit tests and integration tests for existing codebases.
- **Code Translation**: Porting legacy code from one language (e.g., Fortran) to modern environments.
- **Autonomous Coding Agents**: Powering agents that can plan, execute, and debug code.

## Getting started
Codestral is available via Mistral AI's **La Plateforme** or can be run locally using [Ollama](../../services/ollama.md).

### Using Mistral SDK (Python)
```python
from mistralai import Mistral
import os

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

response = client.chat.complete(
    model="codestral-latest",
    messages=[
        {"role": "user", "content": "Write a Python function to calculate the Fibonacci sequence using recursion."}
    ]
)
print(response.choices[0].message.content)
```

### Local Execution (Ollama)
```bash
ollama run codestral
```

## Technical examples

### Fill-In-the-Middle (FIM)
Codestral supports FIM, allowing it to complete code based on both preceding and following context.

```python
# API example for FIM (using raw completion or specialized endpoint)
# Prefix: def fib(n):
# Suffix: return a
# Codestral completes the middle logic.
```

### Multilingual Code Generation
Codestral's strength lies in its ability to handle multiple languages simultaneously, such as writing a Python wrapper for a C++ library.

```python
# Example prompt: "Write a Python C-extension for the following C++ function..."
```

## Strengths
- **Performance**: High accuracy in code generation and debugging across 80+ languages.
- **Open Weights**: Can be self-hosted for maximum privacy and data security.
- **Specialization**: Better at complex coding tasks than many general-purpose models of similar size.
- **Efficiency**: 22B parameters offer a good balance between performance and hardware requirements.

## Limitations
- **Focus**: While it can handle general conversation, its primary optimization is for code.
- **Hardware**: Local hosting requires significant VRAM (ideally 24GB+ for 4-bit quantization).

## When to use it
- When building specialized coding tools or agents (e.g., [Cline](../agents/cline.md), [Roo Code](../agents/roo-code.md)).
- When you need high-quality code generation with the privacy of local hosting.
- When working with less common programming languages where general models fail.

## When not to use it
- For general creative writing or non-technical tasks.
- If you lack the hardware for local hosting and prefer the convenience of proprietary frontier models like Claude 3.5 Sonnet.

## Licensing and cost
- **Open Weights**: Released under the **Mistral AI Non-Commercial License** (MNCL) for research and non-commercial use. Commercial use requires a separate agreement or usage via Mistral's API.
- **API Cost**: Paid (Usage-based on Mistral AI La Plateforme).

## Related tools / concepts
- [Mistral AI](mistral.md)
- [Ollama](../../services/ollama.md)
- [vLLM](../infrastructure/vllm.md)
- [Cline](../agents/cline.md)
- [Roo Code](../agents/roo-code.md)
- [Continue](../development_ops/continue_dev.md)

## Sources / References
- [Mistral AI Codestral Announcement](https://mistral.ai/news/codestral/)
- [Mistral Documentation](https://docs.mistral.ai/models/codestral/)
- [Hugging Face - Codestral-22B-v0.1](https://huggingface.co/mistralai/Codestral-22B-v0.1)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
