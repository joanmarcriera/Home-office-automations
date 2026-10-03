# InternLM

## What it is
InternLM is an enterprise-grade, open-weight large language model series and AI provider suite developed by the Shanghai Artificial Intelligence Laboratory (Shanghai AI Lab) in collaboration with leading academic and industry partners. Culminating in the high-performance **InternLM2.5** family, **InternLM3**, and the ultra-large-scale **InternLM-Interns2-Preview-397B** Mixture-of-Experts (MoE) model, InternLM is engineered for extreme English-Chinese bilingual proficiency, advanced mathematical reasoning, multi-step agent tool calling, and long-context processing up to 1 million tokens. Operating natively alongside **FastMCP 3.1**, InternLM serves as a foundational open-weights reasoning provider for frontier agent architectures alongside models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Gemma 4**, and **Qwen 3.6 VL**.

## What problem it solves
Large-scale enterprise agent automation platforms and private homelab deployments require reasoning models that offer high mathematical and coding capabilities without commercial licensing restrictions or vendor lock-in. Proprietary cloud API services pose compliance and data-sovereignty risks while dense models can be prohibitively expensive to host locally. InternLM solves these challenges by providing open-weight dense and MoE architectures with Top-2 expert routing, enabling cost-effective memory activation during inference. Furthermore, its native localized Rotary Position Embedding (RoPE) mechanisms support up to 1M token context windows, allowing complete source code repositories or enterprise document silos to be processed without context truncation.

## Where it fits in the stack
**AI Model / Local LLM / Bilingual Provider Layer**. InternLM operates at the intelligence model layer. It can be hosted on local GPU clusters or cloud instances using high-throughput serving runtimes like [vLLM](../infrastructure/vllm.md), [LMDeploy](lmdeploy.md), or [SGLang](../infrastructure/sglang.md), managed via [Ollama](../../services/ollama.md), or connected to [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) tool servers using FastMCP 3.1.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Agent Application / Client API                        │
│                   (FastMCP 3.1 Orchestrator / LangChain / RAG)              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / OpenAI-Compatible REST API
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    High-Throughput Local Serving Engine                     │
│                  (vLLM / LMDeploy / SGLang / Ollama Port)                   │
└──────────────┬──────────────────────────────────────────────┬───────────────┘
               │                                              │
               │ Top-2 Expert Weight Activation               │ 1M Context Window (RoPE)
┌──────────────▼──────────────┐                ┌──────────────▼───────────────┐
│  Interns2-397B MoE Routing  │                │   InternLM2.5 / InternLM3    │
│  (Sparse Active Parameter)  │                │     (Dense 7B/20B Models)    │
└──────────────┬──────────────┘                └──────────────┬───────────────┘
               │                                              │
 ┌─────────────┴──────────────────────────────────────────────┴───────────────┐
 │                       Hardware Execution Acceleration                      │
 │                     (Multi-GPU CUDA / ROCm Tensor Parallel)                │
 └────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Bilingual Enterprise RAG**: Managing, indexing, and reasoning over dual English and Chinese technical documentation, legal archives, and financial reports.
- **Autonomous Multi-Step FastMCP 3.1 Tool Calling**: Functioning as the core reasoning engine for agent loops that require zero-shot JSON tool parsing and tool invocation over FastMCP 3.1 protocol interfaces.
- **Extreme Long-Context Code Analysis**: Reviewing full repository codebases (up to 1M tokens) for security audits, architectural refactoring, and bug detection.
- **Sovereign Math & Logic Pipelines**: Deploying private mathematical and legal parsing pipelines on local GPU infrastructure where data privacy is legally required.

## Strengths
- **Top-2 MoE Parameter Efficiency**: The 397B parameter MoE architecture dynamically routes tokens to active sub-networks, drastically lowering token generation latency and compute costs.
- **Proven Tool-Use & Function Calling**: Optimized instruction-tuning yields near-zero tool format syntax errors across complex nested FastMCP 3.1 schemas.
- **Native 1M Token Context Window**: Advanced RoPE scaling allows multi-document synthesis and repository-wide context reasoning.
- **Permissive Open Commercial Licensing**: Free for commercial and research applications, enabling full sovereign control over enterprise deployments.
- **Native FastMCP 3.1 Protocol Support**: Built-in support for structured JSON schemas and tool calling patterns.

## Limitations
- **Multi-GPU VRAM Requirements for MoE**: Serving the 397B MoE preview requires enterprise multi-GPU nodes (e.g., 8x H100 or 8x A100 80GB systems).
- **Quantization Tuning Complexity**: Finding optimal EXL2, AWQ, or GGUF quantization parameters for sparse MoE models requires specialized quantization setups.
- **Serving Engine Dependency**: Maximum token generation throughput relies on optimized runtimes like LMDeploy, vLLM, or SGLang.

## When to use it
- When building sovereign bilingual (English/Chinese) AI applications requiring high reasoning, math, and coding benchmarks.
- When deploying FastMCP 3.1 agent systems on private enterprise GPU hardware.
- When analyzing large document collections requiring up to 1 million tokens of context window.

## When not to use it
- On consumer hardware with severely limited VRAM (< 12GB) where smaller quantized models like Gemma 4 or Llama 4 fit better.
- For purely English-only lightweight edge scripts where small specialized models suffice.

## Getting started

To run InternLM locally using PyTorch and Hugging Face `transformers`:

1. **Install Prerequisites**:
   Ensure Python 3.10+, PyTorch 2.4+, and CUDA 12.1+ are installed:
   ```bash
   pip install transformers accelerate sentencepiece protobuf torch pydantic>=2.0.0
   ```

2. **Load Model via Python**:
   ```python
   import torch
   from transformers import AutoTokenizer, AutoModelForCausalLM

   model_id = "internlm/internlm2_5-7b-chat"
   tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
   model = AutoModelForCausalLM.from_pretrained(
       model_id,
       torch_dtype=torch.bfloat16,
       trust_remote_code=True,
       device_map="auto"
   ).eval()
   ```

3. **Generate Text Response**:
   ```python
   response, history = model.chat(tokenizer, "Explain FastMCP 3.1 protocol capabilities.", history=[])
   print(response)
   ```

## CLI examples

Serving InternLM using high-performance inference runtimes:

```bash
# Serve InternLM2.5 7B Chat via LMDeploy API Server on port 23333
pip install lmdeploy
lmdeploy serve api_server internlm/internlm2_5-7b-chat --server-port 23333 --tp 1

# Serve InternLM via vLLM with Tensor Parallelism across 2 GPUs
python3 -m vllm.entrypoints.openai.api_server \
    --model internlm/internlm2_5-7b-chat \
    --tensor-parallel-size 2 \
    --port 8000 \
    --trust-remote-code \
    --max-model-len 32768

# Test OpenAI-compatible endpoint with cURL
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "internlm/internlm2_5-7b-chat",
    "messages": [{"role": "user", "content": "Hello InternLM!"}]
  }'
```

## API examples

### Python: Querying Local InternLM Engine with Pydantic v2 Validation
Querying an InternLM instance served via vLLM using the OpenAI client and validating output structures via **Pydantic v2**:

```python
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
import openai

# 1. Define Pydantic v2 validation models
class InternLMToolCall(BaseModel):
    tool_name: str = Field(..., alias="toolName")
    parameters: Dict[str, Any] = Field(default_factory=dict)

class InternLMMessageOutput(BaseModel):
    role: str
    content: str
    tool_calls: Optional[List[InternLMToolCall]] = Field(None, alias="toolCalls")

class InternLMResponsePayload(BaseModel):
    model_identifier: str = Field(..., alias="modelIdentifier")
    message: InternLMMessageOutput
    is_mcp_compliant: bool = Field(default=True, alias="isMcpCompliant")
    token_usage: Dict[str, int] = Field(default_factory=dict, alias="tokenUsage")

    @field_validator("model_identifier")
    @classmethod
    def validate_model_name(cls, value: str) -> str:
        if "internlm" not in value.lower():
            raise ValueError(f"Expected InternLM model variant, received: {value}")
        return value

# 2. Query function
def query_internlm_agent(prompt: str) -> InternLMResponsePayload:
    client = openai.OpenAI(
        base_url="http://localhost:8000/v1",
        api_key=os.environ.get("OPENAI_API_KEY", "local-internlm-key")
    )

    response = client.chat.completions.create(
        model="internlm/internlm2_5-7b-chat",
        messages=[
            {"role": "system", "content": "You are a bilingual FastMCP 3.1 AI agent engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    choice = response.choices[0]
    raw_payload = {
        "modelIdentifier": response.model,
        "message": {
            "role": choice.message.role,
            "content": choice.message.content or "",
        },
        "isMcpCompliant": True,
        "tokenUsage": {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0
        }
    }

    validated = InternLMResponsePayload.model_validate(raw_payload)
    return validated

if __name__ == "__main__":
    try:
        res = query_internlm_agent("Demonstrate bilingual code refactoring with FastMCP 3.1.")
        print(f"Validated Response from [{res.model_identifier}]")
        print(f"Content: {res.message.content[:150]}...")
    except Exception as e:
        print(f"Query Error: {e}")
```

### FastMCP 3.1 Tool Server Binding for InternLM Agent
Setting up a FastMCP 3.1 tool server that InternLM can invoke during agent workflows:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp_server = FastMCP(
    name="InternLM-Bilingual-Tools",
    version="3.1.0"
)

class TranslationParams(BaseModel):
    text: str = Field(..., description="Source text to translate")
    source_lang: str = Field(default="zh", description="Source language code")
    target_lang: str = Field(default="en", description="Target language code")

@mcp_server.tool(name="translate_technical_doc", description="Translates technical documentation between Chinese and English")
def translate_technical_doc(params: TranslationParams) -> dict:
    return {
        "status": "success",
        "translated_text": f"[Translated to {params.target_lang}]: {params.text}",
        "fastmcp_version": "3.1.0"
    }

if __name__ == "__main__":
    mcp_server.run(transport="sse", port=8002)
```

## Comparative Matrix: InternLM vs Alternative Open-Weight LLM Families

| Capability / Feature | InternLM2.5 / Interns2-397B | DeepSeek-V4 / R1 | Qwen 3.6 VL / Dense | Llama 4 Suite |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Bilingual Math, Code & MoE | Mathematical Reasoning | Vision-Language & Multimodal | General Open-Weight SOTA |
| **MoE Routing Architecture**| Top-2 Expert Active Weights | DeepSeek MoE Routing | Dense & MoE Variants | Dense & MoE Variants |
| **Max Context Window** | 1,000,000 Tokens (Native RoPE)| 128,000 Tokens | 128,000 Tokens | 128,000 Tokens |
| **Bilingual Proficiency** | SOTA English & Chinese | High English & Chinese | High English & Chinese | Primary English |
| **FastMCP 3.1 Support** | First-Class Integration | Native Function Calling | Native Function Calling | Function Calling Adapters |
| **Serving Engines** | LMDeploy, vLLM, SGLang | SGLang, vLLM, Ollama | vLLM, Ollama | vLLM, Ollama, Llama.cpp |

## Production Deployment & Optimization Checklist

1. **Tensor Parallelism & GPU Allocation**:
   - For InternLM2.5-20B, configure `--tensor-parallel-size 2` across 2 GPUs to distribute VRAM load evenly.
   - For Interns2-397B MoE, deploy across an 8-GPU node with FP8 quantization enabled (`--quantization fp8`).

2. **KV Cache PagedAttention Tuning**:
   - In vLLM / SGLang, set `--gpu-memory-utilization 0.92` to maximize KV cache allocation for 32k+ token contexts.

3. **FastMCP 3.1 Tool Schema Validation**:
   - Ensure the system prompt includes strict JSON-schema formatting guidelines when binding tools to prevent tool argument formatting drifts.

4. **Monitoring & Latency Tracking**:
   - Monitor Time-To-First-Token (TTFT) and Inter-Token-Latency (ITL) using Prometheus metrics endpoints exposed by LMDeploy/vLLM on `/metrics`.

## Step-by-Step Troubleshooting Guide

### Issue 1: "Trust Remote Code safety error when loading InternLM in Hugging Face"
- **Root Cause**: InternLM uses custom architecture code hosted in its Hugging Face repository, requiring explicit user authorization.
- **Resolution**:
  1. Pass `trust_remote_code=True` in both `AutoTokenizer.from_pretrained()` and `AutoModelForCausalLM.from_pretrained()`.
  2. For CLI runtimes, add `--trust-remote-code` flag in vLLM or LMDeploy execution commands.

### Issue 2: "CUDA Out of Memory (OOM) during 1M long context processing"
- **Root Cause**: KV cache size scales linearly with context length, exhausting GPU VRAM.
- **Resolution**:
  1. Enable FlashAttention-2 (`--enable-prefix-caching` and `--max-model-len 32768` if full 1M is unneeded).
  2. Use FP8 or INT4 KV cache quantization in vLLM (`--kv-cache-dtype fp8`).

### Issue 3: "Model outputs unformatted raw text instead of FastMCP tool call JSON"
- **Root Cause**: System prompt template did not apply the exact ChatML / InternLM function calling prompt format.
- **Resolution**:
  1. Ensure tokenizer chat template is used: `tokenizer.apply_chat_template(messages, tokenize=False)`.
  2. Enforce structured JSON output sampling using SGLang or vLLM guided decoding parameters (`guided_json`).

## Related tools / concepts
- [DeepSeek](./deepseek.md) — Open-source reasoning model family.
- [Mistral AI](./mistral.md) — Pioneer in open-weight MoE models.
- [Moonshot AI](./moonshot.md) — Long-context language processing provider.
- [Qwen](../ai_knowledge/qwen.md) — Flagship open-weights model suite from Alibaba.
- [Ollama](../../services/ollama.md) — Local LLM orchestration binary.
- [vLLM](../infrastructure/vllm.md) — High-throughput serving engine utilizing PagedAttention.
- [SGLang](../infrastructure/sglang.md) — High-performance structured execution engine for FastMCP 3.1.

## Sources / references
- [InternLM Official GitHub Repository](https://github.com/InternLM/InternLM)
- [Shanghai AI Lab Hugging Face Hub](https://huggingface.co/internlm)
- [LMDeploy High-Performance Inference Engine](https://github.com/InternLM/lmdeploy)
- [Model Context Protocol FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
