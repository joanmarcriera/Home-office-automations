# Codestral

## What it is
Codestral is a generative AI model explicitly designed for code generation tasks by [Mistral AI](mistral.md). As of June 2026, it remains a frontier open-weight model (22B parameters) optimized for over 80 programming languages, featuring advanced Fill-In-the-Middle (FIM) capabilities and native integration with the [Model Context Protocol (MCP 3.0)](../../knowledge_base/mcp.md).

## What problem it solves
It provides a high-performance, specialized model for coding tasks that can be run locally or via API. It solves the "generalist fatigue" where broad LLMs may hallucinate syntax for niche languages or fail to maintain long-range architectural consistency in complex codebases.

## Where it fits in the stack
**Inference Provider / Specialized Model**. It serves as the primary intelligence layer for [Autonomous Coding Agents](../agents/README.md), IDE extensions, and automated CI/CD remediation pipelines.

## Typical use cases
- **Autonomous Coding**: Powering agents like [Cline](../agents/cline.md) or [Roo Code](../agents/roo-code.md) for multi-file refactoring.
- **Legacy Migration**: Porting COBOL or Fortran to modern Python/Rust environments with high fidelity.
- **Test-Driven Development**: Automatically generating comprehensive unit and integration test suites.
- **Real-time FIM**: Providing low-latency code completion in [Continue](../development_ops/continue_dev.md).

## Strengths
- **Multilingual Excellence**: Superior performance in 80+ languages, including niche systems languages.
- **Open Weights**: Enables private, on-premises deployment for sensitive enterprise IP.
- **FIM Native**: Optimized for "fill-in-the-middle" scenarios essential for IDE integrations.
- **Efficiency**: 22B parameter count allows for high-speed inference on consumer-grade hardware (24GB VRAM).

## Limitations
- **Narrow Focus**: Primary optimization is code; general reasoning is secondary.
- **Quantization Sensitivity**: Performance can degrade noticeably at 4-bit quantization compared to 8-bit or FP16.
- **Context Window**: While improved in 2026, it may still struggle with repository-scale context compared to 1M+ token models.

## When to use it
- When building specialized coding tools or agents that require high-density coding knowledge.
- When data privacy mandates local hosting of LLMs.
- When working with specialized languages where general-purpose models (e.g., GPT-4o) lack depth.

## When not to use it
- For general-purpose creative writing or non-technical roleplay.
- When a massive context window (e.g., [Gemini 3.5](../ai_knowledge/gemini.md)) is required to ingest an entire multi-GB repository.
- If you lack the VRAM for local execution and require the absolute lowest latency (consider [Claude 4.8 Haiku](../ai_knowledge/claude.md)).

## Getting started
Codestral is available via Mistral AI's **La Plateforme** or can be run locally using [Ollama](../../services/ollama.md).

1. **Local**: `ollama run codestral`
2. **API**: Obtain a key from [Mistral AI](https://console.mistral.ai/).
3. **IDE**: Install the [Continue](../development_ops/continue_dev.md) extension and select Codestral as the provider.

## CLI examples

### Using Ollama CLI
```bash
# Basic code generation
ollama run codestral "Write a Rust function for a thread-safe singleton"

# Using a prompt file
echo "Explain this regex: ^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$" > prompt.txt
ollama run codestral < prompt.txt
```

### Using Mistral CLI (June 2026)
```bash
mistral chat codestral-latest --message "Refactor this Python code for better performance: [attach file]"
```

## API examples

### Python SDK (FIM Example)
```python
from mistralai import Mistral
import os

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

# Fill-in-the-middle (FIM) completion
response = client.fim.complete(
    model="codestral-latest",
    prompt="def calculate_fibonacci(n):",
    suffix="return sequence"
)

print(response.choices[0].message.content)
```

### cURL request
```bash
curl https://api.mistral.ai/v1/fim/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -d '{
    "model": "codestral-latest",
    "prompt": "def sort_list(l):",
    "suffix": "return l"
  }'
```

## Related tools / concepts
- [Mistral AI](mistral.md)
- [Ollama](../../services/ollama.md)
- [vLLM](../infrastructure/vllm.md)
- [Cline](../agents/cline.md)
- [Roo Code](../agents/roo-code.md)
- [Continue](../development_ops/continue_dev.md)
- [Claude](../ai_knowledge/claude.md)
- [OpenAI](../ai_knowledge/openai.md)
- [Gemini](../ai_knowledge/gemini.md)

## Sources / References
- [Mistral AI Codestral Announcement](https://mistral.ai/news/codestral/)
- [Mistral Documentation - Codestral](https://docs.mistral.ai/models/codestral/)
- [Hugging Face - Codestral-22B-v0.1](https://huggingface.co/mistralai/Codestral-22B-v0.1)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
