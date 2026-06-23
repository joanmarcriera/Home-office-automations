# Google One Plans Comparison (June 2026)

This document provides a comprehensive comparison of Google One subscription plans, focusing on the distinction between standard storage-centric plans and the **AI Plus**, **AI Pro**, and **AI Ultra** tiers as of June 2026.

## What it is
Google One is a subscription service that provides expanded cloud storage across Google Drive, Gmail, and Google Photos. In June 2026, it is defined as a tiered AI-enablement platform, offering direct access to the **Gemini 3.5** family of models and autonomous agent capabilities like **Gemini Spark**.

## What problem it solves
It addresses the growing need for unified digital storage while solving the "AI action gap" by bundling frontier intelligence (Gemini 3.5 Pro/Ultra) and autonomous agents into a consumer-friendly monthly subscription. It eliminates the need for separate subscriptions for storage, video generation, and agentic development platforms.

## Where it fits in the stack
Google One sits at the **Subscription & Access Layer** of the personal AI stack. It serves as the gateway to the [Google Gemini](../tools/providers/google-gemini.md) ecosystem, providing the storage backbone for [NotebookLM](../tools/ai_knowledge/notebooklm.md) and the compute credits for [Google Antigravity](../tools/agents/agno.md) agentic workflows.

## Typical use cases
- **Personal Data Archiving**: High-capacity storage (up to 20TB) for massive datasets and 8K video libraries.
- **Agentic Productivity**: Using **Gemini Spark** to autonomously take action across Workspace (scheduling, drafting, data cleanup).
- **Autonomous Development**: Leveraging **Gemini 3.5 Ultra** in **Google Antigravity** for whole-repository reasoning and automated deployment.
- **Multimodal Creation**: Generating 10-second 4K video clips via **Gemini Omni** with conversational editing.

## Strengths
- **Intelligence + Action**: Gemini 3.5 Pro/Ultra are optimized for agentic benchmarks (Terminal-Bench, MCP Atlas).
- **Omni Integration**: "Any input to any output" capability including video generation and conversational editing.
- **Developer Synergy**: AI Ultra subscribers get YouTube Premium, 20TB storage, and priority access to Antigravity agents.
- **Large Context**: Ultra members enjoy a **10M token context window**, enabling native reasoning over entire codebases.

## Limitations
- **Ecosystem Gravity**: Deepest benefits (Daily Brief, Spark) require full integration with Google Workspace and Android/Chrome.
- **Privacy Trade-offs**: Agentic actions (Spark) require pervasive access to personal data to be effective.
- **Regional Availability**: Some advanced Antigravity features may be subject to regional compute capacity.

## When to use it
- When your primary productivity and data storage are already centered in the Google ecosystem.
- When you require a cost-effective way to access frontier AI models like Gemini 3.5 Pro.
- When you need a shared family storage solution that also provides AI benefits to all members.

## When not to use it
- If you have strict data sovereignty requirements that forbid cloud-based AI processing.
- If you primarily use the Apple (iCloud/Apple Intelligence) or Microsoft (365/Copilot) ecosystems.
- If you only need storage and have no interest in AI-enhanced productivity tools (use standard plans).

## Plan Overview & Pricing (June 2026)

| Feature | Basic | Standard | AI Plus | AI Pro | AI Ultra |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Monthly Price** | $1.99 | $2.99 | $19.99 | $29.99 | $99.99 |
| **Storage** | 100 GB | 200 GB | 2 TB | 2 TB | 20 TB |
| **Primary Model** | Gemini (Free) | Gemini (Free) | Gemini 3.1 Pro | Gemini 3.5 Pro | Gemini 3.5 Ultra |
| **Workspace AI** | No | No | Yes | Yes + Spark | Yes + Spark |
| **Omni (Video)** | No | No | Trial | Omni Flash | Omni Flash (High) |
| **Antigravity** | No | No | No | Standard Access | Priority Access |
| **Context Window** | 32k | 32k | 1M | 2M | 10M |
| **YouTube Prem.** | No | No | No | No | Yes |
| **Sharing** | Up to 5 people | Up to 5 people | Up to 5 people | Up to 5 people | Up to 5 people |

## Detailed AI & Agent Feature Matrix

| Capability | AI Plus | AI Pro | AI Ultra |
| :--- | :--- | :--- | :--- |
| **Gemini App** | Gemini 3.1 Pro | 3.5 Pro (Default) | 3.5 Ultra (5x limits) |
| **Gemini Spark** | No | 24/7 Agent (Standard) | 24/7 Agent (High-Priority) |
| **Daily Brief** | Basic | Advanced (Full Sync) | Advanced (Full Sync) |
| **Gemini Omni** | Limited | 10s Video + Edit | 10s Video (High Concurrency) |
| **Google Antigravity** | No | Standard Tier | Priority (Agent Platform) |
| **Jules (Coding Agent)** | Standard | High-Intensity | Elite (Unlimited Concurrency) |
| **NotebookLM** | 50 sources | 300 sources | 500 sources |
| **Cloud Credits** | $0 | $10 / month | $50 / month |

## Key June 2026 Innovations

### Gemini 3.5 Ultra
The flagship model, combining frontier intelligence with agentic action. It features a **10M token context window** for Ultra members:
- **Terminal-Bench 2.1**: 82.4%
- **MCP Atlas**: 89.1%
Ideal for "long-horizon" agentic tasks where reasoning across entire repositories is required.

### Gemini Spark
A 24/7 personal AI agent that autonomously takes action. It can:
- Reschedule meetings based on conflicting priorities across JMAP/Graph APIs.
- File expense reports from scanned receipts in Google Photos.
- Draft complex replies in Gmail by referencing documents in Drive and local files via MCP.

### Gemini Omni
A leap forward in world understanding, allowing users to generate any output from any input.
- **Conversational Video Editing**: Change characters or lighting in a generated 10s clip via chat.
- **Multimodal Search**: Search through your own video library using natural language.

### Google Antigravity
An agent-first development platform. AI Ultra members receive priority access to build and deploy custom agents within secure, Google-hosted environments using the **Managed Agents API**.

## Getting started
To upgrade or compare plans, visit the [Google One website](https://one.google.com/about). Most AI features are immediately accessible via the Gemini app or Workspace once the subscription is active.

## CLI examples
Subscribers can use the `gcloud` CLI to manage their AI resources:

```bash
# Check your current AI usage and limits
gcloud alpha one ai-usage describe

# List your active Gemini Spark missions
gcloud alpha one spark missions list
```

## API examples
Developers on the AI Ultra plan can use the Managed Agents API:

```python
import google_antigravity

# Create a custom agent with Ultra-priority access
agent = google_antigravity.Agent(
    name="LogAuditBot",
    tier="ultra",
    capabilities=["mcp_read", "workspace_write"]
)
agent.deploy()
```

## Related tools / concepts
- [Gemini 3.5 Pro/Ultra](../tools/providers/google-gemini.md): The core engines.
- [Google Antigravity](../tools/agents/agno.md): The agent-first dev platform.
- [Jules](../tools/ai_knowledge/jules.md): Autonomous software engineering agent.
- [NotebookLM](../tools/ai_knowledge/notebooklm.md): Source-heavy analysis.
- [Model Routing Guide](model_routing_guide.md): Guidance on model selection.

## Sources / references
- [Innovations from Google I/O 26 (Google Cloud Blog)](https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud)
- [Everything new in our Google AI subscriptions (Google One Blog)](https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/)
- [100 things we announced at I/O 2026 (Google Blog)](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
