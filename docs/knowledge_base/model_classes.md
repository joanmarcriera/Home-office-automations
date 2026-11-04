# Classes of Large Language Models

## What it is
Large Language Models (LLMs) can be categorized into distinct architectural classes based on their underlying neural network topologies, training objectives, context window mechanisms, and specialized inference capabilities. This classification helps in selecting the right model for a specific task. As of early 2027, the taxonomy has consolidated around reasoning-native, Mixture-of-Experts (MoE) native, multimodal-unified, edge-native small models, and specialized embedding/reranker architectures.

Understanding LLM taxonomy allows software architects to optimize AI infrastructure across trade-offs between latency, token cost, reasoning depth, parameter count, memory footprint, and local execution requirements.

```mermaid
architecture-beta
    group user_layer(cloud, "Client & Request Layer")
    service request(internet, "User Prompt / FastMCP 3.1 Task") in user_layer

    group router_layer(server, "Model Routing & Taxonomy Gateway")
    service classifier(cpu, "Taxonomy Classifier") in router_layer
    service router(network, "Dynamic Model Router") in router_layer

    group model_classes(database, "Model Architectural Classes")
    service reasoning_class(brain, "Reasoning-Native (Claude 5.6 / GPT-5.6)") in model_classes
    service moe_class(disk, "MoE-Native (DeepSeek-V4 / Mixtral)") in model_classes
    service vision_class(camera, "Multimodal-Unified (Gemini 4.0 Pro)") in model_classes
    service edge_class(terminal, "Edge-Native SLM (Gemma 4 / Qwen 3.6-7B)") in model_classes

    request --> classifier: Parse Requirements (Latency, Vision, Reasoning)
    classifier --> router: Taxonomical Metadata Tag
    router --> reasoning_class: High-Depth Planning & Logic
    router --> moe_class: High-Throughput Token Generation
    router --> vision_class: Image / Video / Audio Ingestion
    router --> edge_class: Air-Gapped / Low-Latency Local Execution
```

## What problem it solves
The "one-size-fits-all" approach to LLM selection leads to severe cost inflation, latency bottlenecks, and context window exhaustion. Modern production AI architectures require matching specialized tasks to the appropriate model class:
- **Cost & Latency Optimization**: Deploying lightweight Small Language Models (SLMs) or Sparse MoEs for simple text extraction instead of expensive frontier reasoning models.
- **Reasoning Quality**: Routing multi-step planning, code execution, and formal logic to Reasoning-Native models with native chain-of-thought tokens.
- **Multimodal Context Ingestion**: Routing video, raw audio streams, and visual UI layouts to Multimodal-Unified architectures rather than using brittle OCR pipeline wrappers.
- **Air-Gapped & Local Compliance**: Running Edge-Native models directly on local hardware for data privacy.

## Where it fits in the stack
It belongs to the **Intelligence Layer** of the AI stack. It serves as the taxonomy for the [Model Routing Guide](model_routing_guide.md), helping orchestration layers, gateway proxies (like LiteLLM), and Model Context Protocol (FastMCP 3.1) servers choose the correct inference path.

```
+-----------------------------------------------------------------------+
|                    Application & Agent Layer                          |
|         (Superpowers, Claude Code, LlamaIndex Workflows)              |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                  Model Routing Gateway & Taxonomy                     |
|  +--------------------+ +--------------------+ +-------------------+  |
|  | Reasoning-Native   | | MoE-Native         | | Multimodal        |  |
|  | Deep Logic & Code  | | Sparse Routing     | | Video / Audio    |  |
|  +--------------------+ +--------------------+ +-------------------+  |
+-----------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+----------------------------------+       +----------------------------+
| Cloud Frontier Providers         |       | Edge / On-Device Runtimes  |
| (Anthropic, OpenAI, Google)      |       | (Ollama, vLLM, SGLang)     |
+----------------------------------+       +----------------------------+
```

## Taxonomy & Class Breakdown Matrix

| Model Class | Key Architectural Characteristics | Typical Latency / Cost | Target Frontier Examples (Early 2027) | Primary Strengths | Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Reasoning-Native** | Latent chain-of-thought, search-based inference scaling, deep planning. | High Latency / High Cost | [Claude 5.6](../tools/providers/anthropic.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [DeepSeek-V4](../tools/providers/deepseek.md) | Exceptional math, coding, tool-calling, and multi-hop agent logic. | Slower time-to-first-token (TTFT), higher cost per query. |
| **MoE-Native** | Sparse activation routing only a subset of total parameters per token. | Low Latency / Medium-Low Cost | DeepSeek-V4, Mixtral 8x22B, Qwen 3.6-MoE | High throughput, large context capacity, low serving cost. | Larger VRAM footprint for total model weights. |
| **Multimodal-Unified** | Native early-fusion audio/vision/text tokenization without adapter networks. | Medium Latency / Medium Cost | [Gemini 4.0 Pro/Flash](../tools/ai_knowledge/gemini.md), Qwen 3.6 VL | Direct processing of video streams, UI screenshots, and raw speech. | Complex deployment requirements for self-hosting. |
| **Edge-Native (SLM)** | 1B-9B parameters optimized for quantization, Apple Silicon, and edge GPUs. | Ultra-Low Latency / Zero API Cost | [Gemma 4](../tools/ai_knowledge/local_llms.md), Llama 4 8B, Qwen 3.6-7B | Air-gapped execution, zero token cost, sub-50ms latency. | Lower reasoning depth for complex multi-step problems. |
| **Embedding & Reranker** | Dense dual-encoder and cross-encoder vector projection spaces. | Micro Latency / Negligible Cost | BGE-M3, Cohere Rerank v3.5, Voyage-3 | Dense contextual retrieval, hybrid search relevance scoring. | Non-generative; restricted to similarity scoring and rank ordering. |

## Comparative Operational Metrics & Benchmark Matrix

The following table evaluates operational characteristics across the 5 primary model classes in enterprise production environments:

| Model Class | Avg Parameter Footprint | VRAM Footprint (FP16 / Int4) | Time-To-First-Token (p95) | Token Generation Throughput | Cost per 1M Input Tokens | Primary Production Failure Mode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reasoning-Native** | 70B - 200B+ Active | 160 GB / 48 GB | 1,200 - 3,500 ms | 45 - 85 tok/s | $3.00 - $25.00 | Thinking token timeout on complex reasoning branches |
| **MoE-Native** | 236B Total / 21B Active | 140 GB / 42 GB | 280 - 650 ms | 90 - 160 tok/s | $0.27 - $1.20 | VRAM thrashing when expert cache eviction occurs |
| **Multimodal-Unified** | 50B - 120B Multimodal | 110 GB / 36 GB | 450 - 950 ms | 70 - 110 tok/s | $0.15 - $2.50 | Context degradation on 60fps continuous video streams |
| **Edge-Native (SLM)** | 2B - 9B Dense | 16 GB / 5 GB | 35 - 90 ms | 120 - 220 tok/s | $0.00 (Self-hosted) | Instruction drift on prompts exceeding 16,000 tokens |
| **Embedding & Reranker**| 300M - 2B Projection | 4 GB / 1.5 GB | 15 - 40 ms | N/A (Batch Embed) | $0.02 - $0.10 | Truncation of documents exceeding token sequence caps |

## Typical use cases
- **Architecting Multi-Agent Workflows**: Routing primary planning to a Reasoning-Native model while delegating sub-task execution to fast MoE or Edge-Native models.
- **On-Device & Mobile AI Deployment**: Running Small Language Models (SLMs) like Gemma 4 or Qwen 3.6-7B on edge hardware for offline functionality.
- **RAG & Context Synthesis**: Using high-throughput MoE models for dense document ingestion alongside specialized embedding models.
- **Visual UI Verification**: Deploying Multimodal-Unified models for visual regression testing and UI accessibility audits in tools like [Superpowers](../tools/agents/superpowers.md).

## Strengths
- **Domain Specialization**: Up to 10x performance and cost optimization compared to generic monolithic deployments.
- **Compute Efficiency**: MoE and Edge architectures provide state-of-the-art accuracy with significantly reduced FLOPs per inference token.
- **Scalable Architecture**: Standardized taxonomy simplifies building dynamic fallback and load-balancing routers.
- **FastMCP 3.1 Task Protocol Compatibility**: Native alignment with FastMCP task routing for automatic sub-agent selection.

## Limitations
- **Rapid Model Evolution**: Model classes continuously overlap as frontier models integrate multimodal reasoning and MoE backbones.
- **Routing Overhead**: Managing multi-class routing logic increases engineering complexity in gateway services.
- **Fallback Drift**: Misconfigured routing fallbacks can unexpectedly redirect traffic to expensive reasoning models, causing API cost spikes.

## When to use it
- When designing multi-step AI pipelines requiring distinct trade-offs between speed, cost, and intelligence.
- When configuring gateway routing proxies (e.g., LiteLLM, OpenRouter) to balance budget constraints.
- When optimizing local/air-gapped systems on homelab hardware or edge GPUs.
- When building FastMCP 3.1 task protocol agents that delegate work to specialized sub-agents.

## When not to use it
- For simple, low-stakes chat prototypes where a single general-purpose API model is completely sufficient.
- When restricted to a single API provider with no model architectural variety.

## Getting started

1. **Identify the Task Requirements**: Is the task multi-step logical planning, structured data extraction, video parsing, or local text transformation?
2. **Select the Target Model Class**: Match the requirement to Reasoning-Native, MoE-Native, Multimodal-Unified, or Edge-Native.
3. **Configure Routing Metadata**: Tag your API requests or gateway routing rules with the required model class parameters.
4. **Consult the Routing Guide**: Review the [Model Routing Guide](model_routing_guide.md) for current recommended benchmarks and pricing tiers.

## FastMCP 3.1 Dynamic Model Classifier & Dispatcher

The following production implementation provides a FastMCP 3.1 server that parses task parameters using immutable Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) and dispatches inference requests to the optimal model class:

```python
"""
Model Class Dispatcher & Classifier - FastMCP 3.1 Implementation
Classifies user intent and task constraints to determine optimal inference architecture.
"""
import os
import sys
import logging
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("model-class-router")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("model-class-router", version="3.1.0")

class ModelCapabilities(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_context_window: int = Field(..., gt=0)
    supports_vision: bool = Field(default=False)
    supports_audio: bool = Field(default=False)
    supports_tool_calling: bool = Field(default=True)
    supports_latent_reasoning: bool = Field(default=False)

class ModelClassDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_id: str = Field(..., min_length=1)
    model_class: Literal["reasoning-native", "moe-native", "multimodal-unified", "edge-native-small", "embedding-rerank"]
    developer: str = Field(..., min_length=1)
    cost_per_million_input: float = Field(..., ge=0.0)
    capabilities: ModelCapabilities

    @field_validator("model_id")
    @classmethod
    def validate_model_id(cls, v: str) -> str:
        clean = v.strip().lower()
        if not clean:
            raise ValueError("model_id cannot be empty")
        return clean

class RoutingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_description: str = Field(..., min_length=5)
    require_vision: bool = Field(default=False)
    require_audio: bool = Field(default=False)
    require_deep_reasoning: bool = Field(default=False)
    air_gapped_only: bool = Field(default=False)
    max_acceptable_latency_ms: int = Field(default=5000, ge=10)

class RoutingDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    selected_model: ModelClassDefinition
    routing_reason: str
    estimated_cost_tier: str
    target_endpoint: str

# Catalog of Verified Production Models by Class (Early 2027)
MODEL_CATALOG: List[ModelClassDefinition] = [
    ModelClassDefinition(
        model_id="anthropic/claude-5.6-sonnet",
        model_class="reasoning-native",
        developer="Anthropic",
        cost_per_million_input=3.0,
        capabilities=ModelCapabilities(
            max_context_window=2000000,
            supports_vision=True,
            supports_audio=False,
            supports_tool_calling=True,
            supports_latent_reasoning=True
        )
    ),
    ModelClassDefinition(
        model_id="deepseek/deepseek-v4",
        model_class="moe-native",
        developer="DeepSeek",
        cost_per_million_input=0.27,
        capabilities=ModelCapabilities(
            max_context_window=128000,
            supports_vision=False,
            supports_audio=False,
            supports_tool_calling=True,
            supports_latent_reasoning=True
        )
    ),
    ModelClassDefinition(
        model_id="google/gemini-4.0-flash",
        model_class="multimodal-unified",
        developer="Google",
        cost_per_million_input=0.15,
        capabilities=ModelCapabilities(
            max_context_window=2000000,
            supports_vision=True,
            supports_audio=True,
            supports_tool_calling=True
        )
    ),
    ModelClassDefinition(
        model_id="google/gemma-4-8b-local",
        model_class="edge-native-small",
        developer="Google",
        cost_per_million_input=0.0,
        capabilities=ModelCapabilities(
            max_context_window=32000,
            supports_vision=False,
            supports_audio=False,
            supports_tool_calling=True
        )
    )
]

def calculate_optimal_route(req: RoutingRequest) -> RoutingDecision:
    if req.air_gapped_only:
        selected = next(m for m in MODEL_CATALOG if m.model_class == "edge-native-small")
        return RoutingDecision(
            selected_model=selected,
            routing_reason="Air-gapped security boundary requirement satisfied by local SLM.",
            estimated_cost_tier="FREE_LOCAL",
            target_endpoint="http://localhost:11434/api/generate"
        )
    if req.require_vision or req.require_audio:
        selected = next(m for m in MODEL_CATALOG if m.model_class == "multimodal-unified")
        return RoutingDecision(
            selected_model=selected,
            routing_reason="Direct audio/visual ingestion requires Multimodal-Unified architecture.",
            estimated_cost_tier="LOW_COST",
            target_endpoint="https://generativelanguage.googleapis.com/v1beta"
        )
    if req.require_deep_reasoning or "refactor" in req.task_description.lower() or "proof" in req.task_description.lower():
        selected = next(m for m in MODEL_CATALOG if m.model_class == "reasoning-native")
        return RoutingDecision(
            selected_model=selected,
            routing_reason="Task requires deep multi-step logic; selected Reasoning-Native frontier engine.",
            estimated_cost_tier="PREMIUM",
            target_endpoint="https://api.anthropic.com/v1/messages"
        )

    # High-throughput MoE fallback
    selected = next(m for m in MODEL_CATALOG if m.model_class == "moe-native")
    return RoutingDecision(
        selected_model=selected,
        routing_reason="Standard high-volume task; routed to cost-efficient MoE-Native cluster.",
        estimated_cost_tier="ULTRA_LOW_COST",
        target_endpoint="https://api.deepseek.com/v1"
    )

@mcp.tool(
    name="route_llm_task",
    description="Selects the optimal LLM class and model ID based on task constraints."
)
async def route_llm_task(params: RoutingRequest) -> Dict[str, Any]:
    decision = calculate_optimal_route(params)
    return decision.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Multi-Service Docker Compose Testbed Topology

The following Compose specification deploys a local testing sandbox with LiteLLM proxy, an edge Ollama instance, and the FastMCP 3.1 model class router:

```yaml
version: "3.8"

services:
  model-class-router:
    image: python:3.11-slim
    container_name: model-class-router
    restart: unless-stopped
    working_dir: /app
    volumes:
      - ./model_router.py:/app/model_router.py:ro
      - ./config:/app/config:ro
    environment:
      - MCP_PORT=8082
      - PYTHONUNBUFFERED=1
    command: >
      bash -c "pip install --no-cache-dir pydantic fastmcp httpx uvicorn &&
               python /app/model_router.py"
    ports:
      - "127.0.0.1:8082:8082"
    networks:
      - ai-router-net

  litellm-proxy:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm-routing-proxy
    restart: unless-stopped
    ports:
      - "127.0.0.1:4000:4000"
    volumes:
      - ./litellm-config.yaml:/app/config.yaml:ro
    environment:
      - DATABASE_URL=redis://redis-state:6379/0
      - STORE_MODEL_IN_DB=True
    networks:
      - ai-router-net

  ollama-edge:
    image: ollama/ollama:latest
    container_name: ollama-edge-slm
    restart: unless-stopped
    ports:
      - "127.0.0.1:11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    networks:
      - ai-router-net

  redis-state:
    image: redis:7.2-alpine
    container_name: router-redis-state
    restart: unless-stopped
    command: ["redis-server", "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru"]
    networks:
      - ai-router-net

networks:
  ai-router-net:
    driver: bridge

volumes:
  ollama_models:
```

## Systemd Service Unit Configuration

Deploy the model class router as a durable background daemon on local Linux workstations:

```ini
[Unit]
Description=Model Architectural Class Router FastMCP Daemon
After=network.target docker.service
Documentation=https://ai.riera.co.uk/knowledge_base/model_classes/

[Service]
Type=simple
User=jules
WorkingDirectory=/home/jules/workspace
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/local/bin/python3 /home/jules/self_created_tools/model_class_router.py
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536
CapabilityBoundingSet=
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Manage and monitor the router unit:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now model-class-router.service
sudo systemctl status model-class-router.service
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Resolution Procedure |
| :--- | :--- | :--- |
| **Unexpected High Billing Spikes** | Simple classification tasks routed to Reasoning-Native models due to ambiguous intent tags. | Tighten prompt classification regex and enforce MoE/SLM defaults for tasks lacking explicit reasoning tags. |
| **Air-Gap Compliance Breach** | Client requested local execution but router fallback redirected to cloud API endpoints. | Hard-code air-gapped security guardrails in the router logic to throw immediate HTTP 403 errors rather than failing over to external APIs. |
| **Multimodal Schema Rejection** | Video or multi-frame payload passed to text-only MoE model. | Inspect MIME type headers at gateway ingest and dynamically steer payloads to Multimodal-Unified classes. |
| **VRAM OOM on Local SLM** | Loading unquantized 70B models on edge hardware without sufficient unified memory. | Enforce automatic 4-bit (GGUF Q4_K_M) quantization loading parameters via Ollama or vLLM flags. |
| **Thinking Token Generation Runaway** | Reasoning models entering recursive reasoning loops on open-ended creative prompts. | Set strict `max_thinking_tokens` caps (e.g., 4,096 tokens) in API request parameters. |
| **LiteLLM Routing Deadlock** | Downstream model backend health checks failing due to expired API credentials. | Implement health probes and active gateway failover to secondary cloud providers. |
| **FastMCP Connection Timeout** | Router daemon blocked on synchronous HTTP calls during heavy query volume. | Refactor client invocations to asynchronous HTTP (`httpx.AsyncClient`) with connection pooling. |
| **Token Truncation in RAG** | Exceeding dense embedding chunk limits (e.g. >512 tokens). | Implement sentence-window recursive splitting prior to dispatching to embedding models. |

## CLI examples

```bash
# Query local Edge-Native SLM model details via Ollama
ollama show gemma4:8b-instruct

# Filter available models on OpenRouter by architecture and modality using curl and jq
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | select(.id | contains("deepseek")) | {id, context_length, pricing}'

# Inspect local vLLM serving parameters for an MoE model
python3 -m vllm.entrypoints.openai.api_server --model deepseek-ai/DeepSeek-V4 --tensor-parallel-size 4
```

## API examples

### Dynamic Model Gateway Routing with FastMCP 3.1 & Pydantic v2
Below is a complete Python verification script demonstrating taxonomical model classification and Pydantic v2 validation:

```python
import json
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class VerificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_description: str = Field(..., min_length=5)
    require_vision: bool = Field(default=False)
    require_deep_reasoning: bool = Field(default=False)

class VerificationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    target_class: str
    target_model: str
    action_plan: str

def verify_routing(req: VerificationRequest) -> VerificationResponse:
    if req.require_vision:
        return VerificationResponse(
            target_class="multimodal-unified",
            target_model="google/gemini-4.0-flash",
            action_plan="Process visual frames and extract structured schema"
        )
    if req.require_deep_reasoning:
        return VerificationResponse(
            target_class="reasoning-native",
            target_model="anthropic/claude-5.6-sonnet",
            action_plan="Generate formal proof and perform step-by-step logic verification"
        )
    return VerificationResponse(
        target_class="moe-native",
        target_model="deepseek/deepseek-v4",
        action_plan="Execute high-throughput batch text completion"
    )

if __name__ == "__main__":
    req = VerificationRequest(
        task_description="Analyze high-resolution architectural schematics",
        require_vision=True,
        require_deep_reasoning=True
    )
    result = verify_routing(req)
    print("Class Route Verification Dump:\n", json.dumps(result.model_dump(), indent=2))
```

## Related tools / concepts
- [Model Routing Guide](model_routing_guide.md)
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [Gemini](../tools/ai_knowledge/gemini.md)
- [Qwen](../tools/ai_knowledge/qwen.md)
- [DeepSeek](../tools/providers/deepseek.md)
- [Local LLMs & Gemma 4](../tools/ai_knowledge/local_llms.md)
- [API Pricing & Free Tiers](api_pricing_free_tiers.md)
- [Model Context Protocol (FastMCP 3.1)](../tools/automation_orchestration/mcp.md)

## Sources / references
- [Model Context Protocol Task Protocol Specs (MCP 3.1, July 2026)](https://modelcontextprotocol.org/docs/protocols/3.1/task)
- [OpenRouter Model Catalog & Taxonomy](https://openrouter.ai/models)
- [Anthropic Claude 5.6 Architecture Whitepaper](https://www.anthropic.com/news)
- [DeepSeek-V4 Technical Report](https://github.com/deepseek-ai)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
