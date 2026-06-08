# AI Signal Sources

## What it is
AI Signal Sources is a curated directory of high-signal information streams focused on model updates, tooling direction, safety changes, and practical engineering patterns. It serves as the authoritative intake list for the repository's intelligence-gathering activities.

## What problem it solves
The AI landscape moves at an overwhelming pace, making it difficult to distinguish between marketing hype and substantive technical advancement. This document filters the noise, identifying the specific sources that provide actionable technical signal for homelab automation and agentic engineering.

## Where it fits in the stack
It belongs in the **Knowledge Management / Intelligence** layer. It acts as the intake strategy for staying informed about changes in the underlying AI technologies (providers, frameworks, and tools) that power the homelab.

## Typical use cases
- **Alpha-Seeking**: Tracking new model releases and API capabilities from frontier providers (OpenAI, Anthropic, Google).
- **Pattern Recognition**: Discovering practical agent engineering patterns and "vibe-coding" results from independent researchers.
- **Security Hardening**: Monitoring security research for emerging threats like prompt injection or supply chain attacks in LLM systems.
- **Maintenance Planning**: Informing the next "Ralph loop" or repository maintenance cycle with current industry standards.

## Strengths
- **High Signal-to-Noise Ratio**: Curated specifically for technical depth and engineering relevance.
- **Primary Source Focus**: Emphasizes direct research and engineering blogs over secondary reporting or aggregators.
- **Actionable Cadence**: Provides a structured rhythm for staying updated without being overwhelmed.

## Limitations
- **Maintenance Overhead**: Requires periodic auditing to remove sources that pivot toward marketing content or become inactive.
- **Subjective Curation**: Reflects the specific technical standards and architectural preferences of this repository.
- **Temporal Lag**: Even high-signal blogs can lag behind real-time social media leaks (though they offer better depth).

## When to use it
- When planning the next batch of documentation deepening or tool integration.
- When researching a new model's performance characteristics or safety guardrails.
- When setting up automated intelligence gathering (e.g., RSS to Telegram pipelines).

## When not to use it
- For general AI news, gossip, or speculative financial analysis.
- As a primary learning resource for foundational concepts (use the [AI Reading List](ai_reading_list.md) instead).

## Getting started

### Subscription Workflow
The most effective way to "consume" these signals is via RSS or Atom feeds.
1. Install an RSS reader or set up an n8n workflow to monitor these URLs.
2. Filter for keywords relevant to your current project (e.g., "MCP", "WebRTC", "Agentic").
3. Use a "Read Later" tool like [Linkwarden](../services/linkwarden.md) to archive high-value posts.

### Suggested Operating Cadence
- **Daily**: Skim company release feeds (OpenAI, Anthropic) for model/API/policy updates.
- **Weekly**: Review independent analysis (Simon Willison, Interconnects) for implementation implications.
- **Monthly**: Refresh canonical docs and [Tool Access Matrix](ai_tool_access_matrix.md) based on what changed materially.

## Company Engineering and Research Blogs

| Source | Focus | URL |
| :--- | :--- | :--- |
| OpenAI Research | Research papers, evaluations, model internals, safety work | https://openai.com/research/ |
| OpenAI Product/Company Updates | Product releases and major platform changes | https://openai.com/index/ |
| Anthropic News | Claude releases, safety policy, and partner integrations | https://www.anthropic.com/news |
| Mistral News | Model launches, API capabilities, and research notes | https://mistral.ai/news |
| Google DeepMind | Research milestones and applied AI updates | https://blog.google/technology/google-deepmind/ |
| Meta AI Blog | Research publications and open model announcements | https://ai.meta.com/blog/ |
| Microsoft Research Blog | Applied and foundational AI research updates | https://www.microsoft.com/en-us/research/blog/ |
| NVIDIA Technical Blog | AI infrastructure, inference, and performance engineering | https://developer.nvidia.com/blog/ |
| Hugging Face Blog | Open-source ecosystem updates, tutorials, and model tooling | https://huggingface.co/blog |
| Cohere Blog | Enterprise AI engineering and model/product updates | https://cohere.com/blog |

## Independent Technical Blogs (High-Signal)

| Author | Why follow | URL |
| :--- | :--- | :--- |
| Simon Willison | Fast, practical analysis of LLM tooling and agent workflows | https://simonwillison.net/ |
| Lilian Weng (Lil'Log) | Deep technical explainers on modern model behavior and methods | https://lilianweng.github.io/ |
| Chip Huyen | Strong coverage of production AI/ML systems design tradeoffs | https://huyenchip.com/ |
| Sebastian Raschka | Reproducible, code-first breakdowns of current LLM research | https://sebastianraschka.com/blog/ |
| Nathan Lambert (Interconnects) | Clear frontier-model research commentary from a practitioner lens | https://www.interconnects.ai/ |
| Latent Space | Engineering-focused interviews and implementation patterns | https://www.latent.space/ |
| Daniel Saewitz | High-signal analysis of commercial OSS and AI strategy | https://saewitz.com/ |

## Prompt Engineering & System Prompts

| Source | Focus | URL |
| :--- | :--- | :--- |
| System Prompts Leaks | Extracted system prompts from frontier models (Claude, GPT, Gemini) | https://github.com/asgeirtj/system_prompts_leaks/ |
| Dmitri Sotnikov (Yogthos) | Deep dives into managing AI complexity and Clojure patterns | https://yogthos.net/ |
| Tyler Rockwood | Applied LLM security analysis with practical trust-boundary experiments | https://rockwotj.com/blog/ |

## Curation Rules

- Prefer primary sources over reposts.
- Track only sources with clear technical signal.
- Remove sources that become mostly marketing content.

## Related tools / concepts
- [AI Tool Access Matrix](ai_tool_access_matrix.md) — For tracking the state of model capabilities across providers.
- [AI Reading List](ai_reading_list.md) — For foundational research and long-form education.
- [Agent Protocols](agent_protocols.md) — For the standards that enable the tools discussed in these blogs.
- [System Prompts](system_prompts.md) — For tracking the "instructions" behind the models.
- [Linkwarden](../services/linkwarden.md) — For archiving high-signal articles found in these sources.
- [n8n](../services/n8n.md) — For automating the ingestion and filtering of these signal sources.
- [Ollama](../services/ollama.md) — For testing the local models often announced in these blogs.
- [SearXNG](../services/searXNG.md) — For private search to discover new signal sources.

## Sources / References

- [OpenAI Research](https://openai.com/research/)
- [OpenAI Index](https://openai.com/index/)
- [Anthropic News](https://www.anthropic.com/news)
- [Mistral News](https://mistral.ai/news)
- [Google DeepMind on Google Blog](https://blog.google/technology/google-deepmind/)
- [Meta AI Blog](https://ai.meta.com/blog/)
- [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/)
- [NVIDIA Developer Blog](https://developer.nvidia.com/blog/)
- [Hugging Face Blog](https://huggingface.co/blog)
- [Cohere Blog](https://cohere.com/blog)
- [Simon Willison's Weblog](https://simonwillison.net/)
- [Lil'Log](https://lilianweng.github.io/)
- [Chip Huyen](https://huyenchip.com/)
- [Sebastian Raschka Blog](https://sebastianraschka.com/blog/)
- [Interconnects](https://www.interconnects.ai/welcome)
- [Latent Space](https://www.latent.space/)
- [Daniel Saewitz's Blog](https://saewitz.com/)
- [Dmitri Sotnikov's Blog (yogthos.net)](https://yogthos.net/)
- [Tyler Rockwood's Blog](https://rockwotj.com/blog/)
- [System Prompts Leaks GitHub](https://github.com/asgeirtj/system_prompts_leaks/tree/main)
- [The AI Agent Tools Landscape: 120+ Tools Mapped [2026]](https://stackone.com/blog/ai-agent-tools-landscape-2026/)
- [Claude 4.7 Performance Analysis on Maverick Hardware](https://www.anthropic.com/news/claude-4-7-maverick) (Standard for June 2026)
- [GPT-5.5 Multi-Agent System Scaling](https://openai.com/index/gpt-5-5-multi-agent-scaling) (Standard for June 2026)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
