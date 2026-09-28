# Classes of Large Language Models

## What it is
Large Language Models (LLMs) can be categorized into distinct architectural classes based on their underlying neural network topologies, training objectives, context window mechanisms, and specialized inference capabilities. This classification helps in selecting the right model for a specific task. As of early 2027, the taxonomy has consolidated around reasoning-native, Mixture-of-Experts (MoE) native, multimodal-unified, and edge-native small models.

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
Below is a complete Python implementation demonstrating a taxonomical model classifier, Pydantic v2 validation, and a FastMCP 3.1 routing gateway endpoint.

```python
import json
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("model-class-router", version="3.1.0")

class ModelCapabilities(BaseModel):
    max_context_window: int = Field(..., gt=0)
    supports_vision: bool = Field(default=False)
    supports_audio: bool = Field(default=False)
    supports_tool_calling: bool = Field(default=True)
    supports_latent_reasoning: bool = Field(default=False)

class ModelClassDefinition(BaseModel):
    model_id: str = Field(..., min_length=1)
    model_class: Literal["reasoning-native", "moe-native", "multimodal-unified", "edge-native-small"]
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
    task_description: str = Field(..., min_length=5)
    require_vision: bool = Field(default=False)
    require_deep_reasoning: bool = Field(default=False)
    air_gapped_only: bool = Field(default=False)
    max_acceptable_latency_ms: int = Field(default=5000, ge=10)

class RoutingDecision(BaseModel):
    selected_model: ModelClassDefinition
    routing_reason: str
    estimated_cost_tier: str

# Catalog of Early 2027 Models by Class
MODEL_CATALOG: List[ModelClassDefinition] = [
    ModelClassDefinition(
        model_id="anthropic/claude-5.6-sonnet",
        model_class="reasoning-native",
        developer="Anthropic",
        cost_per_million_input=3.0,
        capabilities=ModelCapabilities(
            max_context_window=1000000,
            supports_vision=True,
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
            supports_tool_calling=True
        )
    )
]

def route_request(req: RoutingRequest) -> RoutingDecision:
    if req.air_gapped_only:
        selected = next(m for m in MODEL_CATALOG if m.model_class == "edge-native-small")
        return RoutingDecision(
            selected_model=selected,
            routing_reason="Air-gapped constraint satisfied by local SLM.",
            estimated_cost_tier="FREE_LOCAL"
        )
    if req.require_vision:
        selected = next(m for m in MODEL_CATALOG if m.model_class == "multimodal-unified")
        return RoutingDecision(
            selected_model=selected,
            routing_reason="Vision capability required; selected Multimodal-Unified model.",
            estimated_cost_tier="LOW_COST"
        )
    if req.require_deep_reasoning:
        selected = next(m for m in MODEL_CATALOG if m.model_class == "reasoning-native")
        return RoutingDecision(
            selected_model=selected,
            routing_reason="Deep latent reasoning required; selected Reasoning-Native frontier model.",
            estimated_cost_tier="PREMIUM"
        )

    # Default to high-throughput MoE
    selected = next(m for m in MODEL_CATALOG if m.model_class == "moe-native")
    return RoutingDecision(
        selected_model=selected,
        routing_reason="Standard task routing to high-throughput MoE-Native model.",
        estimated_cost_tier="ULTRA_LOW_COST"
    )

@mcp.tool(
    name="route_llm_task",
    description="Selects the optimal LLM class and model ID based on task constraints."
)
async def route_llm_task(params: RoutingRequest) -> Dict[str, Any]:
    decision = route_request(params)
    return decision.model_dump()

if __name__ == "__main__":
    test_req = RoutingRequest(
        task_description="Analyze multi-page architectural blueprint diagram and output security issues.",
        require_vision=True,
        require_deep_reasoning=True
    )
    res = route_request(test_req)
    print("Routing Result (Validated Pydantic v2 Dump):")
    print(json.dumps(res.model_dump(), indent=2))
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
