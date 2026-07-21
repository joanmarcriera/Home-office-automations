# Gemma 4 31B AntiHal

## What it is
Gemma 4 31B AntiHal is an open-weights, instruction-tuned, multimodal large language model fine-tuned and steered by Specific Labs. Released in April 2026, it is based on Google DeepMind's stable **Gemma 4 31B IT** foundation. By leveraging native activation and representation steering, this specialized variant is explicitly engineered to suppress hallucinated outputs, refuse false premises, and confidently state its limitations, all while maintaining its general benchmark performance under a permissive Apache 2.0 license.

## What problem it solves
LLMs are notoriously prone to sycophancy (agreeing with incorrect premises to please the user) and hallucinations (asserting incorrect facts with high confidence). Gemma 4 31B AntiHal solves these issues by baking representation steering directly into the model's generation process. Instead of hallucinating details or complying with false assumptions, the model pushes back on false premises (e.g., correcting a historical prompt containing wrong dates or fake events) and declines to generate responses when it lacks high-confidence facts.

## Where it fits in the stack
**AI Model / Local LLM (Self-hosted)**. Sitting at the intelligence layer of the self-hosted developer stack, Gemma 4 31B AntiHal serves as a highly reliable, low-hallucination local reasoning engine. It operates securely on consumer workstations or local servers via [Ollama](../../services/ollama.md) or standard Transformers backends, and integrates smoothly with agentic and retrieval-augmented workflows using [Model Context Protocol (MCP) 3.0](../automation_orchestration/mcp.md).

## Typical use cases
- **Strict-Compliance Retrieval-Augmented Generation (RAG)**: Extracting information from sensitive local files where hallucinations can lead to financial or legal risks.
- **Truthfulness-Critical Agent Workflows**: Serving as an autonomous agent reasoning layer that refuses to proceed on invalid assumptions.
- **Local Coding Assistance**: Generating code with a reduced likelihood of hallucinating non-existent APIs, libraries, or functions.
- **Data Validation and Cleaning**: Checking logs and databases for errors, flagging false assumptions without sycophantically agreeing with the target records.

## Strengths
- **Baked-In Activation Steering**: Pushes back on incorrect premises and hallucinations dynamically without additional prompt engineering overhead.
- **Preserved Benchmark Performance**: Achieves its high truthfulness score without compromising its reasoning or logical capabilities on standard LLM benchmarks.
- **Runtime Toggle**: Includes a dynamic runtime switch (`model.set_antihal(False)`) to easily toggle the anti-hallucination layer off and revert to the base Gemma 4 model behavior.
- **Hybrid Attention Mechanism**: Interleaves local sliding-window attention and full global attention for optimal memory performance.
- **Proportional RoPE (p-RoPE)**: Natively supports long contexts up to 256K tokens.

## Limitations
- **Over-Questioning on Fringe Facts**: May occasionally refuse valid, highly complex or niche inputs if they resemble a false premise.
- **High VRAM/System Requirements**: With 30.7 billion parameters, running Gemma 4 31B locally requires significant hardware investment (minimum 24GB VRAM for quantized versions, or 64GB+ unified memory for Mac workstations).
- **Steering Overhead**: Although negligible, the steering calculations in custom model files can introduce a minor latency penalty over the bare-metal GPU base model.

## When to use it
- When accuracy and truthfulness are paramount, and you want to prevent the model from blindly agreeing with incorrect user assertions.
- When running localized, privacy-first agent loops that need to fail-fast on bad assumptions rather than hallucinate false success parameters.
- For local, offline deployment on high-end consumer hardware (such as an NVIDIA RTX 4090 or Apple Silicon Mac Studio).

## When not to use it
- For highly creative writing, roleplay, or speculative brainstorming where "hallucination" and unconstrained generation are desirable features.
- On highly resource-constrained devices with less than 24GB of memory; use smaller models like Gemma 3 8B instead.
- If you require the absolute ceiling of logical reasoning that only massive multi-hundred-billion parameter cloud frontier models can offer.

## Getting started
1. **Prerequisites**: Ensure you have Python 3.10+ and a GPU with at least 24GB VRAM.
2. **Installation**: Install the required `transformers` library.
   ```bash
   pip install transformers accelerate sentencepiece
   ```
3. **Download Model**: Load the model from Hugging Face:
   ```python
   from transformers import AutoModelForImageTextToText, AutoTokenizer
   model = AutoModelForImageTextToText.from_pretrained(
       "Specific-Labs/Gemma-4-31B-AntiHal",
       trust_remote_code=True,
       device_map="auto"
   )
   ```
4. **Dynamic Control**: You can dynamically toggle the anti-hallucination feature using the built-in function:
   ```python
   # Disable steering to match standard Gemma 4 IT behavior
   model.set_antihal(False)
   # Re-enable anti-hallucination steering
   model.set_antihal(True)
   ```

## CLI examples
You can interact with Gemma 4 31B AntiHal via Hugging Face's command-line tools or through custom CLI scripts.

```bash
# Download and cache the model from Hugging Face
huggingface-cli download Specific-Labs/Gemma-4-31B-AntiHal

# Run a localized python-wrapped prompt to test premise rejection
python3 -c "
from transformers import AutoModelForImageTextToText, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('Specific-Labs/Gemma-4-31B-AntiHal')
model = AutoModelForImageTextToText.from_pretrained('Specific-Labs/Gemma-4-31B-AntiHal', trust_remote_code=True, device_map='auto')
inputs = tokenizer('Why did Leonardo da Vinci build the first iPhone in 1503?', return_tensors='pt').to('cuda')
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
"
```

## API examples
The following Python script demonstrates how to load, prompt, and dynamically toggle the anti-hallucination steering layer of the model.

```python
import torch
from transformers import AutoModelForImageTextToText, AutoTokenizer

model_id = "Specific-Labs/Gemma-4-31B-AntiHal"

# Load tokenizer and multimodal model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(
    model_id,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16
)

prompt = "Can you help me diagnose a bug with my Windows 98 installation of Docker Desktop?"

# 1. Prompt with AntiHal steered layer ACTIVE (default)
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=150)
print("--- Steered Output (Expected refusal/correction) ---")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# 2. Dynamically toggle AntiHal steering OFF to get the raw Gemma 4 behavior
model.set_antihal(False)
with torch.no_grad():
    raw_outputs = model.generate(**inputs, max_new_tokens=150)
print("\n--- Raw Gemma 4 Output (Expected compliant hallucination) ---")
print(tokenizer.decode(raw_outputs[0], skip_special_tokens=True))
```

## Related tools / concepts
- [J-Wash](./j-wash.md) — Open-source alignment and steering framework utilizing emergent reasoning and representations.
- [Local LLMs](./local_llms.md) — Self-hosting and executing large models on local hardware configurations.
- [Google Gemini](./google-gemini.md) — Google's primary cloud-based multimodal reasoning engine ecosystem.
- [Gemini](./gemini.md) — Standard multimodal family from Google DeepMind.
- [Ollama](../../services/ollama.md) — The industry-standard tool for managing and running local models on consumer devices.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard protocol for giving local models tool-calling capabilities.
- [ExLlamaV2](../infrastructure/exllamav2.md) — A high-performance inference engine optimized for extreme local speeds using EXL2 quantization.
- [vLLM](../infrastructure/vllm.md) — High-throughput and memory-efficient LLM serving engine.

## Sources / references
- [Specific Labs: Gemma-4-31B-AntiHal Model Repository on Hugging Face](https://huggingface.co/Specific-Labs/Gemma-4-31B-AntiHal)
- [Reddit r/LocalLLaMA: Gemma-4-31B-AntiHal Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1uwhwt8/gemma431bantihal_gemma_steered_to_push_back_on/)
- [Google DeepMind Gemma Model Card](https://huggingface.co/google/gemma-4-31B)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
