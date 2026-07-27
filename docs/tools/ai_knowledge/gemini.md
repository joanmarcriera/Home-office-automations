# Gemini

## What it is
Gemini is Google's most capable and general family of AI models, built to be natively multimodal from the ground up. By late July 2026, the series has matured into the **Gemini 3.5 and 3.6** families, representing Google's most advanced AI ecosystem. This includes the highly capable workhorse **Gemini 3.6 Flash**, the high-throughput speed champion **Gemini 3.5 Flash-Lite**, the secure specialized **Gemini 3.5 Flash Cyber** (deployed within the CodeMender code security agent), and the frontier-class **Gemini 3.5 Ultra** and **Gemini 3.5 Pro**.

## What problem it solves
Gemini solves the "Multimodal Gap" by processing text, code, audio, image, and video within a single native reasoning engine. It addresses the overhead, high costs, and latency of traditional LLM pipelines in agentic workflows by:
- **Reducing Output Token Verbosity**: Gemini 3.6 Flash consumes 17% fewer output tokens compared to Gemini 3.5 Flash on Artificial Analysis, and up to 65% on coding tasks like DeepSWE.
- **Extreme Speed/Throughput**: Gemini 3.5 Flash-Lite runs at 350 output tokens per second, making real-time high-volume processing highly viable.
- **Native Computer Use**: Simplifies automated desktop/browser interaction by exposing "computer use" as a native client-side tool.
- **Cybersecurity Vulnerability Mitigation**: Gemini 3.5 Flash Cyber addresses the slow turnaround of vulnerability patching by detecting, validating, and patching flaws in secure environments.

## Where it fits in the stack
**AI Model / Multimodal Foundation**. It serves as the primary intelligence layer for Google-integrated agentic workflows, available via Google AI Studio, Vertex AI, and Google Antigravity (AGY), often working in tandem with [Antigravity Agent](antigravity-agent.md).

## Typical use cases
- **Multi-Agent Orchestration**: Coordinating complex, multi-turn reasoning steps with 3.6 Flash serving as a master router and 3.5 Flash-Lite as subagents generating rapid concepts.
- **High-Throughput Ingestion**: Powering large-scale translation, receipt scanning, and product metadata extraction at minimal cost.
- **Autonomous Agentic Coding**: Running code migrations and complex refactoring with 3.6 Flash (MLE Bench rating: 63.9%, DeepSWE: 49%).
- **Interactive Visual Studios**: Building visual theme builders or mockups using real-time image understanding coupled with tldraw.
- **Automated Security Patching**: Deploying 3.5 Flash Cyber within CodeMender to automatically generate secure pull requests on compromised codebases.

## Strengths
- **Reduced Output Costs**: Gemini 3.6 Flash is priced cost-effectively at $1.50 per 1M input tokens and $7.50 per 1M output tokens.
- **Blazing Speed**: Gemini 3.5 Flash-Lite leads the industry with 350 output tokens/s.
- **Fine-grained Control**: 3.5 Flash-Lite allows developers to configure minimal, low, or high thinking levels depending on workload complexity.
- **Fewer Execution Loops**: Substantial reduction in unwanted code edits and infinite tool-calling loops.
- **Native Tool Integration**: Built-in native support for Computer Use and Code Execution.
- **Frontier Safety**: Shipped with advanced safeguards against Chemical, Biological, Radiological, and Nuclear (CBRN) risks, and robust resistance to adversarial jailbreaks.

## Limitations
- **Ecosystem Lock-in**: Deepest integration is limited to Google Cloud/Workspace and Google Antigravity platforms.
- **Restricted Access**: Gemini 3.5 Flash Cyber is restricted to governments and trusted partners in a limited pilot program.
- **Privacy**: Proprietary cloud processing is required for full multimodal, large-scale workflows (though small local tasks can offload to Gemma).

## When to use it
- When building production-scale autonomous agents requiring low-cost, low-latency execution (using 3.5 Flash-Lite and 3.6 Flash).
- When you need to process extremely long documents, multiple hours of video, or entire codebases in a single prompt.
- For tasks requiring robust, native client-side computer use capabilities.

## When not to use it
- If you require a fully local, air-gapped solution (use Gemma or Llama 3/4 via [Ollama](../../services/ollama.md) instead).
- If your workload does not benefit from multimodal inputs or token/caching optimization.

## Getting started
1. **API Key**: Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
2. **Install SDK**:
```bash
# Install the modern unified google-genai SDK
pip install google-genai
```
3. **Initialize Client**:
```python
from google import genai
client = genai.Client(api_key="YOUR_API_KEY")
```
4. **First Prompt**:
```python
response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents="What is the current state of agentic RAG?"
)
print(response.text)
```

## CLI examples
Using the [Gemini CLI](gemini-cli.md) for terminal-based interaction:

```bash
# Basic text generation using 3.6 Flash
gemini-cli --model gemini-3.6-flash "Summarize the latest trends in MCP 3.1"

# Multimodal input (sending a screenshot to Flash-Lite)
gemini-cli --model gemini-3.5-flash-lite --image screenshot.png "Explain this UI layout"

# Processing a video file
gemini-cli --model gemini-3.6-flash --video meeting_recording.mp4 "What were the action items?"
```

## API examples
### Advanced Multimodal Reasoning (Python - Unified SDK)
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

# Uploading a large file for context using the unified SDK
video_file = client.files.upload(file="large_codebase_walkthrough.mp4")

response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents=[
        video_file,
        "Based on this video, write a technical specification for the authentication module."
    ]
)

print(response.text)
```

### Configurable Thinking Levels (Python)
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

# Setting thinking levels for high-throughput subagent tasks with Gemini 3.5 Flash-Lite
config = types.GenerateContentConfig(
    thinking_level="high",  # Can be minimal, low, or high
    temperature=0.2
)

response = client.models.generate_content(
    model='gemini-3.5-flash-lite',
    contents="Synthesize e-commerce product features across 10,000 product rows.",
    config=config
)

print(response.text)
```

## Related tools / concepts
- [ChatGPT](chatgpt.md)
- [Claude](claude.md)
- [Ollama](../../services/ollama.md)
- [Google Search](google-search.md)
- [NotebookLM](notebooklm.md)
- [Gemini CLI](gemini-cli.md)
- [OpenAI](openai.md)
- [Mistral AI](../providers/mistral.md)
- [LangChain](langchain.md)
- [LlamaIndex](llamaindex.md)
- [Antigravity Agent](antigravity-agent.md)
- [Model Context Protocol (MCP) 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://deepmind.google/blog/introducing-gemini-36-flash-35-flash-lite-and-35-flash-cyber/)
- [Gemini API Release Notes (July 2026)](https://ai.google.dev/gemini-api/docs/changelog)
- [Google AI Studio](https://aistudio.google.com/)
- [Antigravity Agent Guide](https://ai.google.dev/gemini-api/docs/antigravity)
- [Managed Agents Overview](https://aistudio.google.com/managed-agents)

## Contribution Metadata
- Last reviewed: 2026-07-27
- Confidence: high
