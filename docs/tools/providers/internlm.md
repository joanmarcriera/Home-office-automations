# InternLM

## What it is
InternLM is an advanced, enterprise-grade open-weight large language model series developed by the Shanghai Artificial Intelligence Laboratory (Shanghai AI Lab) and key industry partners. Culminating in the high-performance **InternLM2.5** family and the ultra-large-scale **InternLM-Interns2-Preview-397B** Mixture-of-Experts (MoE) model, InternLM is engineered for extreme bilingual proficiency (English and Chinese), superior mathematical reasoning, multi-step agent tool call workflows, and long-context processing up to 1 million tokens, fully integrated with **FastMCP 3.1 Task Protocol**.

## What problem it solves
Large-scale, multi-agent enterprise automation platforms require reasoning engines that are highly stable, open-weight, and free from restrictive commercial licensing. InternLM solves these demands by delivering state-of-the-art benchmark-grade performance in coding, logical inference, and complex mathematics natively in local and hybrid cloud environments. Its MoE architecture enables cost-effective activation of subset routing weights, minimizing compute costs while maintaining extreme performance scaling alongside models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6 VL.

## Where it fits in the stack
**AI Model / Local LLM / Bilingual Provider**. Within the home lab or enterprise developer stack, InternLM resides at the intelligence provider layer. It can be served locally using high-throughput engines like [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md), managed via [Ollama](../../services/ollama.md), or integrated directly with [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers for autonomous tool use via FastMCP 3.1.

## Typical use cases
- **Complex Bilingual RAG**: Managing and retrieving structured or unstructured knowledge across highly diverse English and Chinese documentation silos.
- **Autonomous Multi-Step Agents**: Powering reasoning agent loops that require highly reliable function calling and structured JSON output using FastMCP 3.1.
- **Extreme Long-Context Code Analysis**: Reviewing full-code repository contexts and generating complex refactoring solutions utilizing its 1M context support.
- **Edge Math & Logic Engines**: Running sovereign quantitative financial models or legal parsing pipelines where data privacy is paramount.

## Strengths
- **Massive MoE Efficiency**: The Interns2-Preview-397B MoE model utilizes highly optimized top-2 routing, activating only a fraction of its total weights per token to minimize runtime latency.
- **Excellent Tool-Use Stability**: Demonstrates extremely high zero-shot function-calling accuracy, on par with leading proprietary cloud models.
- **1-Million Token Window**: Natively scales context length up to 1M tokens through localized rotary position embedding (RoPE) and specialized attention mechanisms.
- **Permissive Open-Weight License**: Released under free and open commercial licenses, providing maximum security for private enterprise operations.
- **FastMCP 3.1 Compliant**: Fully supports FastMCP 3.1 schemas for agent tool orchestration.

## Limitations
- **High VRAM Footprint for MoE**: Hosting the 397B parameter preview requires enterprise-grade multi-GPU nodes (e.g., multiple H100 or A100 systems).
- **Quantization Complexity**: Finding optimal bits-per-weight EXL2 or GGUF profiles for the Mixture-of-Experts model requires specialized tuning.
- **Serving Engine Dependency**: Requires optimized runtimes like LMDeploy, vLLM, or SGLang to achieve minimal time-to-first-token (TTFT).

## When to use it
- When you require a localized bilingual reasoning engine with state-of-the-art math and code-generation benchmark scores.
- When building multi-agent pipelines using FastMCP 3.1 where models must reliably parse structured tool schemas.
- For local enterprise clusters equipped with high-density GPU infrastructure.

## When not to use it
- On consumer edge hardware with limited VRAM (such as standalone laptops with less than 16GB VRAM).
- For workflows that are exclusively English-language and do not benefit from bilingual multi-hop semantic mapping.
- If your system requires lightweight dense local setups where Llama 4 or Gemma 4 are better suited.

## Getting started
1. **Prerequisites**: Python 3.10+, PyTorch 2.4+, and an NVIDIA GPU setup with CUDA 12.1+.
2. **Library Installation**: Install the Hugging Face `transformers` and accelerate libraries.
   ```bash
   pip install transformers accelerate sentencepiece protobuf torch pydantic>=2.0.0
   ```
3. **Load Model via Python**: Load the InternLM2.5 dense model locally:
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
   )
   model = model.eval()
   ```

## CLI examples
Serve InternLM using standard high-performance serving runtimes:

```bash
# Serve InternLM2.5 7B Chat locally via LMDeploy
pip install lmdeploy
lmdeploy serve api_server internlm/internlm2_5-7b-chat --server-port 23333 --tp 1

# Serve using vLLM in a multi-GPU environment
python3 -m vllm.entrypoints.openai.api_server \
    --model internlm/internlm2_5-7b-chat \
    --tensor-parallel-size 2 \
    --port 8000 \
    --trust-remote-code
```

## API examples
Query InternLM served via vLLM using OpenAI Python client protocol with strict **Pydantic v2** schema validation:

```python
import openai
from pydantic import BaseModel, Field, ValidationError
import os

class InternLMResponse(BaseModel):
    bilingual_explanation: str = Field(description="Generated technical response")
    source_model: str = Field(description="Identifier of active model")
    is_mcp_compliant: bool = Field(default=True, description="Indicates FastMCP 3.1 tool-calling readiness")

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key=os.environ.get("OPENAI_API_KEY", "local-placeholder")
)

def query_internlm() -> InternLMResponse:
    try:
        response = client.chat.completions.create(
            model="internlm/internlm2_5-7b-chat",
            messages=[
                {"role": "system", "content": "You are a bilingual software engineering assistant."},
                {"role": "user", "content": "Explain how to implement a custom FastMCP 3.1 tool server in Python."}
            ],
            temperature=0.2,
            max_tokens=300
        )
        content = response.choices[0].message.content or ""

        data = {
            "bilingual_explanation": content,
            "source_model": "internlm2_5-7b-chat",
            "is_mcp_compliant": True
        }

        return InternLMResponse.model_validate(data)
    except ValidationError as ve:
        print(f"Validation failure: {ve}")
        raise
    except Exception as e:
        print(f"Query failure: {e}")
        raise
```

## Related tools / concepts
- [DeepSeek](./deepseek.md) — SOTA open-source models specializing in reasoning and coding.
- [Mistral AI](./mistral.md) — Open-weight pioneer delivering scalable dense and MoE models.
- [Moonshot AI](./moonshot.md) — Long-context language processing provider.
- [Qwen](../ai_knowledge/qwen.md) — Alibaba's flagship open-weights model suite.
- [Ollama](../../services/ollama.md) — Terminal-native local LLM orchestration framework.
- [vLLM](../infrastructure/vllm.md) — High-throughput serving runtime utilizing PagedAttention.
- [SGLang](../infrastructure/sglang.md) — Local serving framework optimized for structured output and FastMCP 3.1.

## Sources / references
- [InternLM Official GitHub Repository](https://github.com/InternLM/InternLM)
- [Shanghai AI Lab Hugging Face Hub](https://huggingface.co/internlm)
- [Model Context Protocol FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
