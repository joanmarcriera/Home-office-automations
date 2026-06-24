# Classes of Large Language Models

## What it is
Large Language Models (LLMs) can be categorized into several classes based on their architecture, training objectives, and specialized capabilities. This classification helps in selecting the right tool for a specific task.

## What problem it solves
The "one-size-fits-all" approach to LLMs is increasingly inefficient. Understanding model classes allows developers to optimize for cost, latency, and reasoning depth by matching the model's specialized architecture (e.g., MoE for efficiency, reasoning-native for logic) to the problem at hand.

## Where it fits in the stack
It belongs to the **Intelligence Layer** of the AI stack. It serves as the taxonomy for the [Model Routing Guide](model_routing_guide.md), helping orchestration layers choose the correct inference path.

## Typical use cases
- **Architecting Agentic Workflows**: Choosing a "Reasoning" model for planning and a "Chat" model for user interaction.
- **On-Device Deployment**: Selecting "Small Language Models" (SLMs) for local execution on edge hardware.
- **RAG Systems**: Using specialized "Embedding Models" for vectorization and "Long-Context Models" for large document analysis.

## Strengths
- **Specialization**: Allows for 10x performance improvements in niche domains (like coding or vision).
- **Efficiency**: MoE and SLM architectures provide high performance with significantly lower compute requirements.
- **Scalability**: Proper classification enables multi-model routing pipelines that scale better than monolithic systems.

## Limitations
- **Rapid Evolution**: Model classes overlap as frontier models become increasingly multimodal and reasoning-capable.
- **Complexity**: Managing multiple specialized models increases the engineering overhead of the routing layer.

## When to use it
- When designing a multi-step AI pipeline that requires different types of reasoning.
- When optimizing for specific constraints like local execution, low cost, or extreme context length.

## When not to use it
- For very simple, low-stakes chat applications where a single general-purpose model is sufficient.
- If your infrastructure only supports a single API provider with limited model variety.

## Getting started
To select the correct model class for your project:
1. **Identify the Primary Task**: Is it coding, reasoning, summarization, or image generation?
2. **Evaluate Constraints**: Do you need low latency (mini models) or high reasoning depth (frontier models)?
3. **Check Data Modality**: Do you need multimodal support (Vision-Language Models)?
4. **Consult the Routing Guide**: Use the [Model Routing Guide](model_routing_guide.md) to find the best current model for that class.

## CLI examples
You can identify model classes using various CLI interfaces to local and hosted providers.

```bash
# Identify model details in Ollama
ollama show llama4-maverick

# List available model classes in OpenRouter
curl https://openrouter.ai/api/v1/models | jq '.data[] | {id, architecture}'
```

## API examples
When using APIs, you can filter for specific model classes or architectures.

### Filtering by Architecture (Pseudo-code)
```python
import openrouter_api

# Request models with 'moe' architecture for cost-efficiency
efficient_models = openrouter_api.get_models(architecture="moe")
for model in efficient_models:
    print(f"Model: {model.name}, Price: {model.price_per_token}")
```

### Selecting a Reasoning Model
```python
import litellm

# Explicitly route to a reasoning-native model
response = litellm.completion(
    model="openai/o4-preview",
    messages=[{"role": "user", "content": "Solve this complex logic puzzle: ..."}]
)
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
- [MCP 3.0 Standard](../tools/automation_orchestration/mcp.md)

## Sources / References
- [Current Large Audio Language Models largely transcribe rather than listen](https://arxiv.org/abs/2510.10444)
- [The First Fully General Computer Action Model](https://si.inc/posts/fdm1)
- [Learnings from 4 months of Image-Video VAE experiments](https://www.linum.ai/field-notes/vae-reconstruction-vs-generation)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
