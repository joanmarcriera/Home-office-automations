# Together AI

## What it is
Together AI is an enterprise-grade cloud inference, fine-tuning, and dedicated GPU cluster platform optimized for open-source foundation models. As of early January 2027, it provides high-throughput, sub-100ms first-token latency API access to frontier open-weights model families (including Meta Llama 4 70B/405B, DeepSeek-V4, Qwen 3.6, Gemma 3, and specialized vision/code models). Powered by NVIDIA Rubin and Blackwell GPU clusters, NVLink interconnects, and custom FlashAttention-3/Liger execution kernels, Together AI serves as a primary cloud provider for sovereign, open-model AI infrastructure.

In modern agentic ecosystems, Together AI acts as a serverless tool-calling and reasoning backend. It natively supports **FastMCP 3.1 Task Protocol** execution, structured JSON mode output validation, and multi-tenant custom LoRA (Low-Rank Adaptation) adapter serving, allowing autonomous agents to execute complex tool pipelines without maintaining local high-VRAM hardware.

## What problem it solves
- **Infrastructure Capital Expenditure Overhead**: Self-hosting 70B+ or 400B+ parameter models locally requires hundreds of thousands of dollars in high-tier GPU clusters (e.g., NVIDIA H100/H200/B200 nodes), complex power/cooling infrastructure, and dedicated DevOps engineering. Together AI offers pay-per-token serverless endpoints with enterprise SLAs.
- **Agent Latency Bottlenecks**: Autonomous agents calling multi-step tool routines via Model Context Protocol (MCP) suffer performance degradation if inference engines stall. Together AI's optimized FlashAttention-3 kernels deliver high token generation rates (200+ tokens/sec) for real-time agentic reasoning.
- **Cold-Start Delays in Custom Model Adapters**: Deploying specialized domain models (e.g., medical extraction, code audit, legal compliance) typically requires provisioning separate GPU instances per fine-tune. Together AI's proprietary multi-tenant LoRA serving architecture allows hot-swapping thousands of custom adapters onto a single base model cluster with zero cold-start latency.
- **Lock-in to Closed Ecosystems**: Provides a high-performance alternative to proprietary closed-source APIs (like Claude 5.6 or GPT-5.6), allowing developers to retain model ownership, dataset sovereignty, and reproducible execution paths.
- **Dynamic Context Routing Bottlenecks**: Autonomous multi-agent pipelines require fluid shifts between high-throughput compact models for triage and deep-reasoning flagship models for synthesis; Together AI unifies this routing through an OpenAI-compliant gateway.

## Where it fits in the stack
**Providers & Inference Infrastructure Layer**. Together AI sits directly beneath orchestration frameworks (LangGraph, CrewAI, AutoGen) and automation engines ([n8n](../../services/n8n.md)). It connects structured agent requests with high-performance model execution nodes, serving outputs over standard OpenAI-compatible REST and SSE streaming endpoints.

```
+-----------------------------------------------------------------------------------+
|                        Orchestration & Agent Frameworks                           |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | FastMCP 3.1 Server |   |  LangGraph Agent Loop |   |  n8n Automation Engine |  |
|  | (Tool Orchestrator)|   | (Claude 5.6 / Qwen)   |   |   (JSON REST Workflows)|  |
|  +---------+----------+   +-----------+-----------+   +-----------+------------+  |
+------------|--------------------------|---------------------------|---------------+
             |                          |                           |
             +--------------------------+---------------------------+
                                        |
                                        v HTTP/HTTPS REST & SSE Stream (OpenAI API Compatible)
                                        |  - POST /v1/chat/completions
                                        |  - POST /v1/fine-tuning/jobs
                                        |  - POST /v1/embeddings
+---------------------------------------v-------------------------------------------+
|                           Together AI Platform Core                               |
|  +-----------------------------------------------------------------------------+  |
|  |                    Inference Router & Load Balancer                         |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Rate Limit & Token Usage |  | Hot-Swappable LoRA Adapter Registry    |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|  +-----------------------------------------------------------------------------+  |
|  |                  Distributed GPU Acceleration Infrastructure                |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   |  FlashAttention-3 / FP8 & FP4 Kernel Engines / Liger Kernels       |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   |  NVIDIA Rubin / Blackwell GPU Nodes connected via NVLink             |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **FastMCP 3.1 Agentic Reasoning Backend**: Serving ultra-low-latency Llama 4 70B and DeepSeek-V4 endpoints for continuous tool discovery, function calling, and structured output parsing.
- **Dynamic LoRA Adapter Multi-Tenancy**: Maintaining a single Together AI API endpoint while passing distinct `model` adapter strings (e.g., `accounts/org/models/code-audit-adapter`) per task or tenant.
- **Enterprise Dataset Fine-Tuning**: Ingesting synthetic or human-annotated JSONL datasets, initiating parallelized LoRA fine-tuning jobs, and instantly deploying resulting checkpoints to serverless endpoints.
- **Multi-Model Fallback & Routing**: Dynamically routing lightweight extraction queries to Llama 4 8B and complex architectural reasoning queries to DeepSeek-V4 or Llama 4 405B based on latency and cost parameters.
- **Continuous Batch Token Analysis**: Streaming logprob probabilities for token-level uncertainty estimation and calibration during autonomous code verification.

## Architecture & Serving Topology

Together AI's architecture decouples compute serving from model storage using custom tensor-parallel split execution and vLLM-derived memory management:

```
Client Request (OpenAI Format)
         |
         v
+----------------------------------+
| API Gateway & Auth Check         |
+----------------------------------+
         |
         v
+----------------------------------+      +----------------------------------+
| Base Model VRAM Allocation       |----->| Hot-Swappable LoRA Adapter Cache |
| (Llama 4 70B / FP8 Quantized)    |      | (Instantly loaded per request)   |
+----------------------------------+      +----------------------------------+
         |
         v
+----------------------------------+
| FlashAttention-3 Kernel Engine   |
+----------------------------------+
         |
         v
Streaming SSE Response Tokens -> Client
```

## Inference Provider Comparison Matrix

| Provider / Dimension | Together AI | Groq | Fireworks AI | DeepInfra | OpenRouter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | NVIDIA Rubin/Blackwell + NVLink | Custom LPUs (Deterministic) | Optimized CUDA Engines | Multi-Cloud GPU Nodes | Meta-Router Aggregator |
| **First-Token Latency** | Sub-100ms | Sub-30ms | Sub-100ms | 150-250ms | 200-400ms (Hops) |
| **Hot-Swappable LoRA** | Native multi-tenant adapters | Not supported | LoRA fine-tunes supported | Partial adapter support | Not supported |
| **Max Context Support** | Up to 128K–1M tokens | Up to 128K tokens | Up to 128K tokens | Up to 128K tokens | Model dependent |
| **FastMCP 3.1 Native** | Full structured JSON / Tooling | Tool calling API | Function calling | OpenAI compatible | Aggregated Tooling |
| **Dedicated Clusters** | Bare-metal GPU reservation | Enterprise cloud only | Dedicated deployments | Reserved instances | Routing only |

## Strengths
- **Sub-100ms First-Token Latency**: FlashAttention-3 optimizations and high-speed NVLink GPU interconnects ensure rapid agent response times.
- **Instant Hot-Swappable LoRA Adapters**: Deploy and serve custom LoRA weights on top of shared base model infrastructure without dedicated server deployment costs.
- **Full OpenAI API Compatibility**: Drops directly into existing agent codebases, Python `openai` SDKs, and MCP servers by updating the base URL to `https://api.together.xyz/v1`.
- **Comprehensive Open-Weights Catalog**: Immediate availability of flagship open models (Meta Llama 4, DeepSeek-V4, Qwen 3.6, Gemma 3) alongside vision and embedding models.
- **Enterprise SLA & Dedicated Clusters**: Provides isolated, single-tenant GPU clusters for privacy-sensitive enterprise environments with strict compliance controls.

## Limitations
- **External Network Dependency**: Requires active outbound Internet connectivity, making it unsuitable for fully air-gapped on-premises setups.
- **Serverless Token Rate Limits**: High-burst agent swarms can encounter rate limit throttles unless reserved compute or dedicated clusters are provisioned.
- **Rate Limit & Price Variance Across Models**: Enterprise billing requires tracking token usage across various base models and custom adapter tiers.
- **Multi-Region Routing Latency**: Geographically distant client workers may incur network transit latency without local reverse proxies.

## When to use it
- When you require production-grade, low-latency access to frontier open-weights models (Llama 4, DeepSeek-V4) without managing GPU hardware.
- When executing high-frequency agent tool calls via [FastMCP 3.1](../automation_orchestration/mcp.md) that require low-cost per-token pricing.
- When serving specialized, domain-tuned LoRA adapters dynamically across different workflow steps.
- When orchestrating hybrid fallback architectures that toggle between open-weights and proprietary models.

## When not to use it
- If your workload must run entirely air-gapped on local home-lab hardware (use [vLLM](../infrastructure/vllm.md) or [Ollama](../../services/ollama.md)).
- If your application is exclusively locked into proprietary closed models like Claude 5.6 or GPT-5.6.
- When zero cloud egress is mandated by statutory data air-gap policies.

## Getting started

### Installation
Install the official Together Python client SDK and FastMCP:

```bash
pip install together pydantic>=2.0 fastmcp httpx
```

### Basic Chat Completion Example

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

response = client.chat.completions.create(
    model="meta-llama/Llama-4-70b-instruct",
    messages=[
        {"role": "system", "content": "You are a senior systems architect specializing in FastMCP 3.1 tool integration."},
        {"role": "user", "content": "Explain how LoRA adapters improve inference efficiency for agent swarms."}
    ],
    temperature=0.2,
    max_tokens=1024,
)

print(response.choices[0].message.content)
```

## CLI examples

```bash
# Set environment API key
export TOGETHER_API_KEY="your_api_key_here"

# List available serverless models in catalog
together models list

# Stream chat response from command line using Meta Llama 4
together chat "meta-llama/Llama-4-70b-instruct" --prompt "Draft a FastMCP 3.1 tool schema in Python."

# Submit fine-tuning job using a remote JSONL dataset
together fine-tuning create \
  --training-file "file-2027-01-07-dataset-id" \
  --model "meta-llama/Llama-4-8b" \
  --n-epochs 3 \
  --learning-rate 1e-4

# Retrieve status of an active fine-tuning job
together fine-tuning retrieve "ft-job-20270107-001"
```

## API examples

### FastMCP 3.1 Server Using Together AI for Structured Agent Reasoning

This production implementation demonstrates a FastMCP 3.1 tool server using Together AI's OpenAI-compatible API to perform structured tool reasoning with strict Pydantic v2 input validation:

```python
import os
import json
import time
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from together import Together

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Together-AI-Reasoning-Gateway", version="3.1.0")

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# --- Pydantic v2 Schemas ---

class FastMCPToolRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model_name: str = Field(
        default="meta-llama/Llama-4-70b-instruct",
        description="Target Together AI model (e.g., meta-llama/Llama-4-70b-instruct or deepseek-ai/DeepSeek-V4)"
    )
    user_prompt: str = Field(..., min_length=1, max_length=10000, description="Task prompt for model evaluation")
    system_instructions: Optional[str] = Field(
        default="You are an expert system reasoning engine. Return structured JSON responses.",
        description="System role behavior prompt"
    )
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Sampling temperature")

class StructuredAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model_used: str = Field(..., description="Together AI model identifier")
    reasoning_summary: str = Field(..., description="Brief step-by-step reasoning summary")
    action_type: str = Field(..., description="Action category (e.g. EXECUTE_TOOL, REQUEST_INFO, COMPLETE)")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Structured parameters for downstream tool execution")
    latency_ms: float = Field(..., ge=0.0, description="Inference turnaround duration in milliseconds")

class LoRAInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    base_model: str = Field("meta-llama/Llama-4-70b-instruct", description="Base model identifier")
    adapter_id: str = Field(..., description="Custom LoRA fine-tune adapter identifier")
    prompt: str = Field(..., min_length=1, description="Domain prompt for adapted model")
    max_tokens: int = Field(512, ge=1, le=4096)

# --- Helper Functions ---

def get_together_client() -> Together:
    if not TOGETHER_API_KEY:
        raise ValueError("TOGETHER_API_KEY environment variable is missing.")
    return Together(api_key=TOGETHER_API_KEY)

# --- FastMCP 3.1 Tool Definitions ---

@mcp.tool(
    name="together_reasoning_agent",
    description="Invokes Together AI high-throughput models to evaluate agent reasoning and emit structured action payloads."
)
def run_reasoning_step(request: FastMCPToolRequest) -> StructuredAgentOutput:
    """Sends prompt to Together AI and parses structured JSON reasoning output into a validated Pydantic model."""
    start_time = time.perf_counter()
    client = get_together_client()

    messages = [
        {"role": "system", "content": request.system_instructions},
        {"role": "user", "content": request.user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=request.model_name,
            messages=messages,
            temperature=request.temperature,
            max_tokens=2048,
            response_format={"type": "json_object"}
        )

        raw_content = response.choices[0].message.content
        parsed_json = json.loads(raw_content)
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        return StructuredAgentOutput(
            model_used=request.model_name,
            reasoning_summary=parsed_json.get("reasoning_summary", "Completed successfully."),
            action_type=parsed_json.get("action_type", "COMPLETE"),
            payload=parsed_json.get("payload", {}),
            latency_ms=round(duration_ms, 2)
        )
    except (ValidationError, json.JSONDecodeError) as err:
        raise RuntimeError(f"Failed to parse or validate Together AI model output: {err}")
    except Exception as exc:
        raise RuntimeError(f"Together AI API request failed: {exc}")

@mcp.tool(
    name="together_lora_inference",
    description="Routes specialized prompts through a dynamically attached LoRA adapter checkpoint."
)
def run_lora_inference(request: LoRAInferenceRequest) -> Dict[str, Any]:
    """Invokes Together AI multi-tenant LoRA serving engine without dedicated cluster spin-up."""
    client = get_together_client()
    try:
        response = client.chat.completions.create(
            model=f"{request.base_model}:{request.adapter_id}",
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens
        )
        return {
            "model": request.base_model,
            "adapter": request.adapter_id,
            "output": response.choices[0].message.content,
            "tokens_generated": response.usage.completion_tokens
        }
    except Exception as e:
        return {"error": f"LoRA invocation failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
```

## Deployment & Containerization

### Docker Compose Architecture
Deploy a resilient FastMCP router container connected to Together AI:

```yaml
version: "3.8"

services:
  together-ai-gateway:
    image: python:3.12-slim
    container_name: together-ai-gateway
    restart: unless-stopped
    ports:
      - "8430:8430"
    environment:
      - TOGETHER_API_KEY=${TOGETHER_API_KEY}
      - PYTHONUNBUFFERED=1
      - PORT=8430
    volumes:
      - ./gateway:/app
    working_dir: /app
    command: >
      bash -c "pip install together fastmcp pydantic &&
               python /app/server.py"
```

### Systemd Service Daemon (`/etc/systemd/system/together-gateway.service`)
Configure a dedicated background service to keep the Together AI agent gateway operational:

```ini
[Unit]
Description=Together AI FastMCP 3.1 Gateway Daemon
After=network.target

[Service]
Type=simple
User=togetherops
Group=togetherops
WorkingDirectory=/opt/together-gateway
EnvironmentFile=/etc/default/together-gateway
ExecStart=/usr/local/bin/python3 /opt/together-gateway/server.py
Restart=always
RestartSec=5s

# Hardening
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause Analysis | Diagnostic Step | Mitigation / Resolution Strategy |
| :--- | :--- | :--- | :--- |
| `429 Rate Limit Exceeded` | Surpassed requests per minute (RPM) or tokens per minute (TPM) limit | Check account dashboard rate usage metrics | Implement token bucket client-side throttling or reserve dedicated GPU endpoints |
| `AdapterNotFound` (LoRA) | Specified custom LoRA adapter checkpoint ID does not exist or has expired | Query `/v1/fine-tuning/jobs` for checkpoint status | Verify adapter string format: `<account>/<model>:<adapter-id>` |
| `JSONDecodeError` on Schema | Output model failed to return valid JSON format despite `response_format` | Inspect raw model candidate output string | Re-enforce system prompt instruction: "Return ONLY valid JSON matching schema" |
| `SSE Stream Interrupted` | Client socket closed prematurely or gateway timeout occurred | Inspect HTTP client timeout configuration | Set keep-alive ping headers and increase read timeout to >= 120s |
| High First-Token Latency | Heavy cold routing or cross-region network transit latency | Probe latency using `curl -w "%{time_starttransfer}\n"` | Switch to nearest Together AI region endpoint or use smaller parameter variant |
| `AuthenticationError (401)` | Expired, revoked, or missing `TOGETHER_API_KEY` token | Verify env variable: `echo $TOGETHER_API_KEY` | Reissue token in Together developer portal and reload systemd service |

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md): Multi-model API routing hub across cloud model providers.
- [Groq](groq.md): LPU-based ultra-fast inference provider.
- [Fireworks AI](fireworks.md): High-throughput open-model serving and fine-tuning platform.
- [vLLM](../infrastructure/vllm.md): Sovereign self-hosted inference engine.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Open protocol for agent tool and prompt integration.
- [Hugging Face](huggingface.md): Open-source model hub and dataset repository.

## Sources / references
- [Together AI Official Website](https://www.together.ai/)
- [Together AI Developer Documentation](https://docs.together.ai/)
- [Together AI Serverless Model Catalog](https://www.together.ai/models)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
