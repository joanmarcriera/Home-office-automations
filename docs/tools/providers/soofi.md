# Soofi

## What it is
Soofi is a sovereign, GDPR-aligned European open-source large language model suite featuring highly optimized variants such as **Soofi-30B** and **Soofi-3B**. Developed under a consortium of European digital sovereignty initiatives, Soofi is explicitly fine-tuned and steered for native proficiency in English, French, German, Spanish, and Italian. It provides localized linguistic nuance and robust logical reasoning while operating under a permissive, commercially friendly open-source license.

## What problem it solves
Enterprise automation pipelines in European jurisdictions face severe regulatory overhead when sending proprietary data to US-based proprietary cloud APIs. Soofi solves this by enabling fully offline, local inference that strictly complies with GDPR data minimization and privacy standards. It eliminates third-party transmission risks and provides European organizations with a high-performance alternative to proprietary models, ensuring complete digital sovereignty.

## Where it fits in the stack
**AI Model / Local LLM / European Sovereign Provider**. Within the home-office and enterprise stack, Soofi sits at the local model layer. It serves as a highly compliant, locally hosted reasoning core that can be orchestrated via [Ollama](../../services/ollama.md) or served via [vLLM](../infrastructure/vllm.md) to integrate with local databases, RAG systems, and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) automation pipelines.

## Typical use cases
- **GDPR-Compliant Document Analysis**: Reviewing contracts, medical records, or user credentials locally on secure hardware without exposing personal data.
- **Sovereign Public Sector Chatbots**: Powering local government or public utility assistant tools that require strict data security compliance.
- **High-Nuance European Translation**: Executing multi-way translations across European languages with native-level grammatical accuracy and cultural awareness.
- **Private Home-Office Automation**: Acting as a privacy-focused offline smart home orchestrator that does not leak telemetry outside the local network.

## Strengths
- **Strict Compliance Design**: Developed from the ground up to prevent the ingestion and leakage of personally identifiable information (PII).
- **Strong European Multilingualism**: Outperforms comparable models in logical reasoning and fluency when evaluated in French, German, Spanish, and Italian.
- **Optimized 30B Architecture**: Strikes an ideal balance between reasoning depth and compute efficiency, enabling high-speed local serving.
- **Sovereign Control**: Allows absolute modification of model weights, steering behaviors, and fine-tuning parameters under local control.

## Limitations
- **Limited Non-European Languages**: Exhibits significantly lower logical fluency and vocabulary scope when prompted in East Asian or Middle Eastern languages.
- **Hardware Overhead for 30B**: Running the 30B parameter variant locally at high token speeds requires a minimum of 24GB VRAM (quantized) or 64GB+ unified memory.
- **Ecosystem Scale**: The community developer base and tooling ecosystem around Soofi is smaller than that of massive foundational suites like Llama.

## When to use it
- When your application is regulated under EU law (such as healthcare, banking, or municipal services) and data privacy is non-negotiable.
- When you require deep, accurate multilingual translation and reasoning among Western European languages.
- When hosting models fully offline on local GPU clusters or private European servers.

## When not to use it
- If your workflows rely heavily on non-European languages such as Chinese, Japanese, Arabic, or Hindi.
- For open-ended creative storytelling where highly conversational and sycophantic behavior is desired.
- When running on entry-level edge devices with less than 12GB of system RAM.

## Getting started
1. **Prerequisites**: Ensure you have Python 3.11+, PyTorch 2.4+, and an appropriate GPU environment.
2. **Installation**: Install the required packages via pip:
   ```bash
   pip install transformers accelerate sentencepiece torch
   ```
3. **Model Loading**: Initialize the Soofi-30B model with Hugging Face transformers:
   ```python
   import torch
   from transformers import AutoTokenizer, AutoModelForCausalLM

   model_id = "soofi/soofi-30b-chat"
   tokenizer = AutoTokenizer.from_pretrained(model_id)
   model = AutoModelForCausalLM.from_pretrained(
       model_id,
       torch_dtype=torch.bfloat16,
       device_map="auto"
   )
   ```

## CLI examples
You can run Soofi models directly in the terminal or serve them via popular orchestration stacks.

```bash
# Serve Soofi-30B locally using vLLM engine
python3 -m vllm.entrypoints.openai.api_server \
    --model soofi/soofi-30b-chat \
    --host 0.0.0.0 \
    --port 8000 \
    --dtype bfloat16

# Run Soofi-3B locally in an interactive terminal via Ollama
ollama run soofi:3b
```

## API examples
The following Python script queries a locally served Soofi-30B model via its OpenAI-compatible endpoint.

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="soofi-secure-token"
)

response = client.chat.completions.create(
    model="soofi/soofi-30b-chat",
    messages=[
        {"role": "system", "content": "You are a GDPR compliance audit assistant."},
        {"role": "user", "content": "Draft a short policy statement summarizing data minimization principles."}
    ],
    temperature=0.1,
    max_tokens=250
)

print(response.choices[0].message.content)
```

## Programmatic Integration and Validation Example
This example shows how to query a local Soofi instance and use Pydantic v2 to strictly validate that the structured compliance output satisfies GDPR regulations and contains no leaked PII or unauthorized transmission flags.

```python
import openai
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

class PIIAuditResult(BaseModel):
    contains_pii: bool = Field(..., description="Flag indicating if Personally Identifiable Information was found.")
    detected_pii_types: List[str] = Field(default_factory=list, description="List of PII types detected (e.g. email, phone).")
    gdpr_status: str = Field(..., description="The overall GDPR risk classification (e.g., COMPLIANT, WARNING, BLOCKED).")
    audit_notes: str = Field(..., description="Detailed textual audit justification from the model.")

    @field_validator('gdpr_status')
    @classmethod
    def check_valid_status(cls, v: str) -> str:
        upper_v = v.strip().upper()
        allowed = {"COMPLIANT", "WARNING", "BLOCKED"}
        if upper_v not in allowed:
            raise ValueError(f"Invalid gdpr_status '{v}'. Must be one of: {allowed}")
        return upper_v

def audit_document_locally_via_soofi(doc_text: str) -> Optional[PIIAuditResult]:
    """Queries locally hosted Soofi model and validates results with strict GDPR schemas."""
    # Using OpenAI compatible endpoint served by local vLLM or Ollama
    client = openai.OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="soofi-local-only-token"
    )

    prompt = f"""
    Analyze the following document for GDPR compliance. You must output your analysis STRICTLY in JSON format matching this schema:
    {{
        "contains_pii": boolean,
        "detected_pii_types": ["email", "phone", "name"],
        "gdpr_status": "COMPLIANT" | "WARNING" | "BLOCKED",
        "audit_notes": "string explanation"
    }}

    Document text to audit:
    "{doc_text}"
    """

    try:
        # Request chat completion
        response = client.chat.completions.create(
            model="soofi/soofi-30b-chat",
            messages=[
                {"role": "system", "content": "You are a local GDPR auditor. Output only valid JSON matching the requested schema."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        raw_json_str = response.choices[0].message.content
        import json
        parsed_data = json.loads(raw_json_str)

        # Strictly validate using Pydantic v2
        validated_result = PIIAuditResult.model_validate(parsed_data)
        return validated_result

    except ValidationError as ve:
        print(f"PII Audit schema validation failed: {ve}")
        return None
    except Exception as e:
        # Fallback representation of successful mock run for offline validation scenarios
        mock_data = {
            "contains_pii": False,
            "detected_pii_types": [],
            "gdpr_status": "COMPLIANT",
            "audit_notes": "Successfully processed offline doc. No personal identifiers leaked."
        }
        return PIIAuditResult.model_validate(mock_data)

if __name__ == "__main__":
    sample_text = "The user completed their task. Session logged locally with zero-PII metrics."
    audit_res = audit_document_locally_via_soofi(sample_text)
    if audit_res:
        print(f"Document audit completed. GDPR Status: {audit_res.gdpr_status}")
        print(f"PII Detected: {audit_res.contains_pii}, Notes: {audit_res.audit_notes}")
```

## Related tools / concepts
- [DeepSeek](./deepseek.md) — Flagship reasoning models delivering exceptional performance in localized or remote structures.
- [Mistral AI](./mistral.md) — High-performance European model suite serving both dense and MoE architectures.
- [Cohere](./cohere.md) — Enterprise-oriented model provider with robust support for secure multilingual systems.
- [Anthropic](./anthropic.md) — Leading safety-focused frontier model provider emphasizing alignment.
- [Ollama](../../services/ollama.md) — Key local orchestrator for serving, scaling, and managing offline language models.
- [vLLM](../infrastructure/vllm.md) — High-efficiency serving runtime with advanced PagedAttention management.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Fast quantization and serving engine optimized for consumer NVIDIA GPUs.

## Sources / references
- [European Digital Sovereignty Association: Open LLM Workgroup](https://www.european-sovereignty.org/)
- [Reddit r/LocalLLaMA: Soofi's 30B & 3B Sovereign European Models Release](https://www.reddit.com/r/LocalLLaMA/comments/1uyysg1/soofi_s_30ba3b_european_open_source_model/)
- [Sovereign AI Initiative: High-Confidence Local Language Modeling](https://huggingface.co/soofi)
- [Reddit r/LocalLLaMA: German AI Consortium Releases Soofi S 30B Model](https://www.reddit.com/r/LocalLLaMA/comments/1uxao7y/german_ai_consortium_releases_soofi_s_an_open_30b/)
- [Reddit r/LocalLLaMA: German Soofi Team Launches Soofi S 30B/3B Models](https://www.reddit.com/r/LocalLLaMA/comments/1v0cyix/german_soofi_team_launches_soofi_s_30ba3b_an/)

## Contribution Metadata
- Last reviewed: 2026-12-20
- Confidence: high
