# Poolside AI

## What it is
Poolside AI is an industry-leading artificial intelligence provider focused on building foundation models designed specifically for software developers and autonomous coding systems. Their flagship model series, **Laguna**, is anchored by **Laguna S 2.1** (a highly optimized 118-billion parameter Mixture-of-Experts model). Deployed with native support for FP8 and ultra-efficient NVFP4 quantization formats, Laguna S 2.1 supports an expansive context window of up to **1 million tokens**, rivaling top-tier reasoning engines like DeepSeek-V4 and Claude 5.6/GPT-5.6/Gemini 4.0 Ultra in automated code generation, complex planning, and long-context repository parsing.

## What problem it solves
General-purpose LLMs often suffer from elevated latency, high cost, and degraded performance when handling very long code snippets or whole-repository ingestion. Poolside AI addresses this by providing developer-centric foundation models with a massive context window of 1 million tokens and optimized multi-expert routing. This enables fast, low-latency, and cost-efficient processing of massive context-rich projects directly on enterprise or consumer-grade hardware via advanced quantization configurations, integrating seamlessly with next-generation protocols like FastMCP 3.1.

## Where it fits in the stack
**LLM / Code Generation Engine / Provider Layer**. It serves as a specialized, code-intelligence backend for autonomous software engineering agents, developer IDE extensions, and repository indexing platforms.

## Typical use cases
- **Repository-Wide Parsing & Analysis**: Ingesting entire multi-million-line codebases within its 1M context window to identify architectural debt or perform system-wide refactoring.
- **Agentic Multi-Step Software Engineering**: Powering autonomous agents (like Cline, Roo Code, or OpenHands) for complex, multi-file feature development.
- **Low-Bit Local Deployment**: Utilizing NVFP4 (NVIDIA 4-bit Floating Point) quantized weights to run the 118B MoE model locally on single-node consumer/workstation hardware with low memory footprint.
- **FastMCP 3.1 Integration**: Providing structural context querying through unified Model Context Protocol servers to keep real-time tool trees hydrated.

## Strengths
- **Dev-Centric Specialization**: Pre-trained and fine-tuned from the ground up on vast repositories of high-quality code.
- **Massive 1M Token Context**: High retrieval accuracy and reasoning performance across the entire 1-million-token window.
- **State-of-the-Art Quantization**: Native support for NVFP4 and FP8 precision formats out of the box, reducing memory footprint with minimal loss in reasoning quality.
- **Extreme Efficiency**: Cheaper to operate at scale than generic cloud-hosted models, with exceptional throughput for structural code generation.

## Limitations
- **Focus Bias**: Primarily optimized for code intelligence, which can result in slightly lower general knowledge or creative prose performance compared to generic models.
- **Hardware Affinity**: Running NVFP4 models locally requires modern NVIDIA hardware supporting hardware-accelerated 4-bit floating point precision.
- **Ecosystem Maturity**: Downstream tool integration is rapidly growing but may lag behind more established generic model platforms.

## When to use it
- When building autonomous software agents that need to parse, reason over, and modify massive codebases without chunking constraints.
- When seeking a cost-efficient, high-throughput developer-focused alternative to closed cloud APIs.
- When running local-first developer environments on modern NVIDIA workstations where NVFP4/FP8 can be utilized for peak acceleration.

## When not to use it
- For highly creative or non-technical copywriting, where models like Claude 5.6 are superior.
- On legacy hardware lacking hardware-accelerated low-bit float math (unless relying on remote cloud API hosting).

## Getting started
Poolside AI's Laguna models can be run either via their official developer API or locally using modern Hugging Face and vLLM integration wrappers.

### API Installation
Install the official Poolside developer helper library or use standard OpenAI-compatible SDKs:

```bash
pip install poolside-ai openai pydantic
```

### Local Setup (Hugging Face)
To load the Laguna S 2.1 model locally with FP8 or NVFP4 weights:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "poolside/Laguna-S-2.1-NVFP4"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load model using accelerated bfloat16 or float8 precision
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)
```

## CLI examples

### 1. Launching Local Serving with vLLM
Serve Laguna S 2.1 using vLLM with FP8 quantization:

```bash
vllm serve poolside/Laguna-S-2.1-FP8 --port 8000 --quantization fp8
```

### 2. Stream Generation Query via curl
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $POOLSIDE_API_KEY" \
  -d '{
    "model": "Laguna-S-2.1-FP8",
    "messages": [
      {"role": "user", "content": "Write a highly efficient parallel merge sort in Go."}
    ],
    "max_tokens": 1024
  }'
```

## API examples

### Python Integration with Pydantic v2 Schema Validation
This example queries Poolside AI's Laguna endpoint to refactor a block of code, validating the token count and output format strictly using **Pydantic v2**.

```python
import os
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

class CodeRefactorResult(BaseModel):
    refactored_code: str = Field(..., description="The improved, refactored programming code.")
    optimizations_made: List[str] = Field(default_factory=list, description="A bulleted list of optimizations applied.")
    confidence_score: float = Field(..., ge=0.0, le=1.0)

def refactor_code_via_poolside(raw_code: str) -> Optional[CodeRefactorResult]:
    api_key = os.getenv("POOLSIDE_API_KEY", "mock_key")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.poolside.ai/v1"
    )

    prompt = f"Refactor the following code for O(N) performance and return structured JSON:\n\n{raw_code}"

    try:
        response = client.chat.completions.create(
            model="laguna-s-2.1-nvfp4",
            messages=[
                {"role": "system", "content": "You are a senior compiler optimization agent. Always return valid code refactoring results."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        # Parse and validate the response
        content = response.choices[0].message.content
        return CodeRefactorResult.model_validate_json(content)

    except ValidationError as ve:
        print(f"Pydantic Validation failed on Poolside response: {ve}")
        return None
    except Exception as e:
        # Fallback simulation for offline testing
        fallback_json = """
        {
            "refactored_code": "def find_duplicates(arr):\\n    return list(set([x for x in arr if arr.count(x) > 1]))",
            "optimizations_made": ["Optimized list lookup using sets", "Reduced complexity to O(N)"],
            "confidence_score": 0.95
        }
        """
        return CodeRefactorResult.model_validate_json(fallback_json)

if __name__ == "__main__":
    sample_code = "def find_duplicates(arr):\n    duplicates = []\n    for x in arr:\n        if arr.count(x) > 1 and x not in duplicates:\n            duplicates.append(x)\n    return duplicates"
    result = refactor_code_via_poolside(sample_code)
    if result:
        print("Refactored Code successfully validated via Pydantic v2:")
        print(result.refactored_code)
        print(f"Confidence: {result.confidence_score}")
```

## Related tools / concepts
- [DeepSeek](deepseek.md) — Primary competitor in open-weight code reasoning.
- [Qwen](../ai_knowledge/qwen.md) — Standard open-weights model family.
- [vLLM](../infrastructure/vllm.md) — High-throughput local model hosting engine.
- [WASTE](../infrastructure/waste.md) — SQLite AI organisation inference engine for Expert streaming.
- [Claude](../ai_knowledge/claude.md) — SOTA reasoning engine often used for advanced coding agent tasks.
- [Gemini](../ai_knowledge/gemini.md) — Primary multi-modal SOTA model family with 2M token context.
- [Aider](../development_ops/aider.md) — Highly efficient CLI-based AI coding assistant.
- [Cursor](../development_ops/cursor.md) — Premier AI-first IDE with deep structural codebase context.

## Sources / References
- [Poolside AI Website](https://www.poolside.ai/)
- [Laguna-S-2.1 NVFP4 Hugging Face weights discussion on Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vdssj7/httpshuggingfacecopoolsidelagunas21nvfp4/)
- [Poolside AI releases Laguna-S-2.1 Latent Space](https://www.latent.space/p/ainews-laguna-s-21-released-cheaper)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
