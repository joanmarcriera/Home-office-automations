# Gemini

## What it is
Gemini is Google's most capable and general family of AI models, built to be natively multimodal from the ground up. As of June 2026, the series includes the frontier-tier **Gemini 3.5 Flash** and **Gemini 3.1 Pro**, alongside the speed-optimized **Gemini 3.1 Flash-Lite**.

## What problem it solves
Gemini provides a highly integrated AI experience across the Google ecosystem. It excels at processing and reasoning across different types of information, including text, code, audio, image, and video. Its massive context window (up to 2 million tokens) enables unique use cases like analyzing hours of video or massive codebases.

## Where it fits in the stack
AI Model and Multimodal Assistant. Available via Gemini (web/app), Google AI Studio, and Google Cloud Vertex AI.

## Typical use cases
- **Multimodal analysis**: Analyzing video, audio, and images natively (e.g., "Summarize the events in this security footage").
- **Large-scale codebase analysis**: Refactoring and documenting massive repositories using the 2M token context window.
- **Agentic Workflows**: Using Gemini 3.5 Flash for high-speed tool use and autonomous reasoning via the **Antigravity Agent** platform.
- **Production RAG**: High-efficiency retrieval augmented generation with Flash-tier models.

## Strengths
- **Native Multimodality**: Built from the ground up to handle text, images, video, and audio simultaneously.
- **Industry-Leading Context Window**: 1M+ tokens standard across the Pro and Flash 3.x series.
- **Managed Agents**: (New for 2026) Support for stateful, autonomous agents running in secure sandboxes.
- **Speed**: Gemini 3.5 Flash offers 4x output speed compared to previous generation Pro models while maintaining frontier-level intelligence.

## Limitations
- **Consistency**: Performance can vary between different model tiers (Flash vs. Pro).
- **Privacy**: Proprietary models with specific data handling policies that may not suit all enterprise or local-first use cases.
- **Closed Ecosystem**: Integration is deepest within Google services.

## When to use it
- When you need to process extremely long documents or multiple hours of video.
- When building autonomous agents that require high-speed tool calling (MCP support).
- For native video-to-image or video-to-text generation tasks.

## When not to use it
- If you require a fully local, air-gapped solution (use Gemma or Llama 3 via Ollama instead).
- If your workload is primarily small-context, high-reasoning text where Claude 3.5 Sonnet may have an edge.

## Getting started

### Python API Example (Gemini 3.5 Flash)
Google's Generative AI SDK (v0.8.x+) supports the latest Gemini 3.5 features, including managed agents and advanced multimodal inputs.

```python
import google.generativeai as genai
import os

# Configure the SDK
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the model (using the May 2026 GA version)
model = genai.GenerativeModel('gemini-3.5-flash')

# Generate content with massive context
response = model.generate_content("Analyze this 1,000-page technical specification and find all security vulnerabilities.")

print(response.text)

# Multimodal Video Example
# video_file = genai.upload_file(path="tutorial_video.mp4")
# response = model.generate_content([video_file, "Summarize the key steps in this tutorial."])
# print(response.text)
```

## Managed Agents & Antigravity (2026)
Google's **Managed Agents** platform (released May 2026) allows developers to deploy autonomous agents like the **Antigravity Agent**. These agents:
- Run in secure, isolated Google-hosted Linux sandboxes.
- Can plan, reason, execute code, and browse the web autonomously.
- Are orchestrated via the Gemini API using the `antigravity-preview` model ID.

## Licensing and cost
- **Open Source**: No (Proprietary).
- **Cost**: Free tier available in Google AI Studio; Pay-as-you-go for Gemini API and Vertex AI.
- **Self-hostable**: No.

## Related tools / concepts
- [ChatGPT](chatgpt.md)
- [Claude](claude.md)
- [Ollama](../../services/ollama.md) (for running Gemma)
- [Google Search](google-search.md)
- [NotebookLM](notebooklm.md)
- [Gemini for macOS](gemini-macos.md)
- [Gemini CLI](gemini-cli.md)
- [OpenAI](openai.md)
- [Mistral AI](../providers/mistral.md)
- [LangChain](../frameworks/langchain.md)
- [LlamaIndex](../frameworks/llamaindex.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)
- [Antigravity Agent](antigravity-agent.md)
- [Managed Agents Overview](managed-agents.md)

## Sources / References
- [Official Website](https://gemini.google.com/)
- [Gemini API Release Notes (May 2026)](https://ai.google.dev/gemini-api/docs/changelog)
- [Announcing Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-flash-announcement/)
- [Google AI Studio](https://aistudio.google.com/)
- [Antigravity Agent Guide](https://ai.google.dev/gemini-api/docs/antigravity)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
