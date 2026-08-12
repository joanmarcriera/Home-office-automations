# Classes of Large Language Models

## What it is
Large Language Models (LLMs) can be categorized into several classes based on their architecture, training objectives, and specialized capabilities. This classification helps in selecting the right tool for a specific task. As of August 2026, the taxonomy has consolidated around reasoning-native, MoE-native, multimodal-unified, and edge-native small models.

## What problem it solves
The "one-size-fits-all" approach to LLMs is increasingly inefficient. Understanding model classes allows developers to optimize for cost, latency, and reasoning depth by matching the model's specialized architecture (e.g., Mixture-of-Experts for cost-efficiency, reasoning-native for multi-step planning, or edge-native for air-gapped systems) to the problem at hand.

## Where it fits in the stack
It belongs to the **Intelligence Layer** of the AI stack. It serves as the taxonomy for the [Model Routing Guide](model_routing_guide.md), helping orchestration layers and Model Context Protocol (MCP 3.1) servers choose the correct inference path.

## Typical use cases
- **Architecting Agentic Workflows**: Choosing a "Reasoning-Native" model (such as Claude 5.1 or GPT-5.5) for planning and a fast "Mini" model for text transformation.
- **On-Device Deployment**: Selecting "Small Language Models" (SLMs) like Gemma 3 or Qwen 3.6-7B for local execution on edge hardware.
- **RAG Systems**: Using specialized "Embedding Models" for vectorization and "Long-Context Models" for large document analysis.
- **Unified Multimodal Tasks**: Deploying Gemini 3.5 Ultra/Pro for unified video, audio, and text reasoning tasks.

## Strengths
- **Specialization**: Allows for 10x performance improvements in niche domains (like coding or vision).
- **Efficiency**: MoE and SLM architectures provide high performance with significantly lower compute requirements.
- **Scalability**: Proper classification enables multi-model routing pipelines that scale better than monolithic systems.
- **Task Protocol Integration**: Out-of-the-box support for MCP 3.1 task states.

## Limitations
- **Rapid Evolution**: Model classes overlap as frontier models become increasingly multimodal and reasoning-capable.
- **Complexity**: Managing multiple specialized models increases the engineering overhead of the routing layer.
- **Sub-optimal Defaults**: Fallback behaviors in routing libraries can lead to unexpected cost spikes.

## When to use it
- When designing a multi-step AI pipeline that requires different types of reasoning.
- When optimizing for specific constraints like local execution, low cost, or extreme context length.
- When configuring MCP 3.1 task protocol agents to dynamically choose sub-agents.

## When not to use it
- For very simple, low-stakes chat applications where a single general-purpose model is sufficient.
- If your infrastructure only supports a single API provider with limited model variety.

## Getting started
To select the correct model class for your project:
1. **Identify the Primary Task**: Is it coding, multi-step planning, summarization, or audio-video parsing?
2. **Evaluate Constraints**: Do you need sub-50ms latency (mini models) or high reasoning depth (frontier models)?
3. **Check Data Modality**: Do you need multimodal support (Vision-Language Models)?
4. **Consult the Routing Guide**: Use the [Model Routing Guide](model_routing_guide.md) to find the best current model for that class.

## CLI examples
You can identify model classes and retrieve characteristics using various CLI interfaces.

```bash
# Identify local model characteristics via Ollama
ollama show gemma3:9b-instruct

# Search for available model classes in OpenRouter using curl and jq
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | {id, architecture, context_length}'
```

## API examples
When using APIs, you can filter for specific model classes or architectures.

### Filtering by Architecture
```python
import requests

def get_efficient_moe_models():
    # Fetch models and filter for Mixture of Experts (MoE)
    response = requests.get("https://openrouter.ai/api/v1/models")
    if response.status_code == 200:
        models = response.json().get("data", [])
        moe_models = [m for m in models if "moe" in m.get("architecture", {}).get("modality", "").lower()]
        return moe_models
    return []

print(get_efficient_moe_models()[:3])
```

### Selecting a Reasoning Model with System Prompting
```python
import litellm

# Route to an August 2026 reasoning-native model with thinking capabilities
response = litellm.completion(
    model="openai/gpt-5.5-reasoning",
    messages=[
        {"role": "system", "content": "You are a specialized mathematical planner."},
        {"role": "user", "content": "Solve this multi-step logic puzzle."}
    ],
    temperature=0.0
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [Model Routing Guide](model_routing_guide.md)
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [Gemini](../tools/ai_knowledge/gemini.md)
- [Qwen](../tools/ai_knowledge/qwen.md)
- [DeepSeek](../tools/providers/deepseek.md)
- [Mistral](../tools/providers/mistral.md)
- [Llama 4](../tools/ai_knowledge/local_llms.md)
- [API Pricing & Free Tiers](api_pricing_free_tiers.md)
- [MCP 3.1 Standard](../tools/automation_orchestration/mcp.md)

## Sources / References
- [Current Large Audio Language Models largely transcribe rather than listen](https://arxiv.org/abs/2510.10444)
- [The First Fully General Computer Action Model](https://si.inc/posts/fdm1)
- [Learnings from 4 months of Image-Video VAE experiments](https://www.linum.ai/field-notes/vae-reconstruction-vs-generation)
- [Model Context Protocol Task Protocol Specs (MCP 3.1, July 2026)](https://modelcontextprotocol.org/docs/protocols/3.1/task)

## Contribution Metadata
- Last reviewed: 2026-08-01
- Confidence: high
