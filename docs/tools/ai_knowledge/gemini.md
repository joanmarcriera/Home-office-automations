# Gemini

## What it is
Gemini is Google's most capable and general family of AI models, built to be natively multimodal from the ground up. By late July 2026, the series has matured into the **Gemini 3.5** family, including **Gemini 3.5 Ultra**, **Gemini 3.5 Pro**, **Gemini 3.5 Flash**, and the speed-optimized **Gemini 3.1 Flash-Lite**.

## What problem it solves
Gemini provides a highly integrated AI experience across the Google ecosystem, solving the "Multimodal Gap" by processing text, code, audio, image, and video within a single native reasoning engine. Its massive context window (up to 2 million tokens) addresses the limitation of traditional RAG systems by allowing entire codebases or hours of video to be processed in-context, coupled with late July 2026 structured caching to minimize latency and token overhead.

## Where it fits in the stack
**AI Model / Multimodal Foundation**. It serves as the primary intelligence layer for Google-integrated agentic workflows, available via Google AI Studio, Vertex AI, and as the engine behind [Antigravity Agent](antigravity-agent.md).

## Typical use cases
- **Multimodal analysis**: Analyzing video, audio, and images natively (e.g., "Summarize the events in this security footage").
- **Large-scale codebase analysis**: Refactoring and documenting massive repositories using the 2M token context window.
- **Agentic Workflows**: Using Gemini 3.5 Flash for high-speed tool use and autonomous reasoning via the **Antigravity Agent** platform.
- **Production RAG**: High-efficiency retrieval augmented generation with Flash-tier models, utilizing native vector indexing.
- **Agentic Search**: Powering [Google Search](google-search.md) synthesis and multi-step research tasks.

## Strengths
- **Native Multimodality**: Built from the ground up to handle text, images, video, and audio simultaneously without separate encoders.
- **Industry-Leading Context Window**: 2M tokens standard across the 3.5 series, enabling "Long-Context as a Service".
- **Structured Caching**: (July 2026) Allows persistent in-memory caching of large context blocks (repos, manuals), reducing prompt cost by 90% and response latency for multi-turn runs.
- **Managed Agents**: Support for stateful, autonomous agents running in secure sandboxes (Antigravity).
- **Speed**: Gemini 3.5 Flash offers 4x output speed compared to previous generation Pro models while maintaining frontier-level intelligence.
- **MCP 3.1 Support**: Native integration with the Model Context Protocol (MCP 3.1) for seamless, secure tool calling.

## Limitations
- **Ecosystem Lock-in**: Deepest integration is limited to Google Cloud/Workspace services.
- **Privacy**: Proprietary models with data handling policies that may not suit local-first or highly regulated requirements.
- **Context Latency**: While throughput is high, very large context prompts (1M+ tokens) still incur significant time-to-first-token (TTFT) delays if not cached.

## When to use it
- When you need to process extremely long documents, multiple hours of video, or entire codebases in a single prompt.
- When building autonomous agents that require high-speed tool calling and native web browsing (via Antigravity).
- For native video-to-image or video-to-text generation tasks where alignment between frames is critical.

## When not to use it
- If you require a fully local, air-gapped solution (use Gemma or Llama 3/4 via [Ollama](../../services/ollama.md) instead).
- If your workload is primarily small-context, high-reasoning text where [Claude](claude.md) may have an edge in logical precision.

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
    model='gemini-3.5-flash',
    contents="What is the current state of agentic RAG?"
)
print(response.text)
```

## CLI examples
Using the [Gemini CLI](gemini-cli.md) for terminal-based interaction:

```bash
# Basic text generation
gemini-cli "Summarize the latest trends in MCP 3.1"

# Multimodal input (sending a screenshot)
gemini-cli --image screenshot.png "Explain this UI layout"

# Processing a video file
gemini-cli --video meeting_recording.mp4 "What were the action items?"
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
    model='gemini-3.5-pro',
    contents=[
        video_file,
        "Based on this video, write a technical specification for the authentication module."
    ]
)

print(response.text)
```

### Managed Agents (Antigravity Preview)
```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
# Utilizing the Antigravity agentic platform via unified client
response = client.models.generate_content(
    model='antigravity-preview',
    contents="Research the latest developments in Blackwell GPUs and write a 500-word report."
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

## Sources / References
- [Official Website](https://gemini.google.com/)
- [Gemini API Release Notes (July 2026)](https://ai.google.dev/gemini-api/docs/changelog)
- [Announcing Gemini 3.5](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-announcement/)
- [Google AI Studio](https://aistudio.google.com/)
- [Antigravity Agent Guide](https://ai.google.dev/gemini-api/docs/antigravity)
- [Managed Agents Overview](https://aistudio.google.com/managed-agents)

## Contribution Metadata
- Last reviewed: 2026-07-27
- Confidence: high
