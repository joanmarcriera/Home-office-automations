# AI Builder Index

## What it is
The AI Builder Index is the primary discovery portal for the automation and AI engineering stack documented in this repository. It serves as a high-signal directory that routes builders to the appropriate playbooks, tools, and architectural patterns based on their desired outcomes. As of January 2027, it is fully optimized for **FastMCP 3.1** and the **MCP Task Protocol Specification**, helping users navigate the complex ecosystem of frontier models including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro/Flash**, and **Gemma 3**.

## What problem it solves
The repository contains hundreds of specialized tools and integration patterns, which can cause decision paralysis and architectural fragmentation. The AI Builder Index solves "discovery friction" by organizing technical documentation into logical "outcome buckets." Instead of browsing a flat file list, builders start with a business or engineering goal (e.g., "Build a high-throughput RAG pipeline with local privacy guarantees") and immediately find the curated set of tools and standards required to implement it efficiently.

## Where it fits in the stack
**Knowledge Base / Navigation Layer**. It sits at the top of the documentation hierarchy, acting as the primary navigation bridge between the [Home Index](../../index.md) and the deep technical specifications in `docs/tools/`, `docs/services/`, `docs/knowledge_base/`, and `docs/playbooks/`. It defines the "Practical Defaults" for the entire KnowledgeOps architecture.

## Typical use cases
- **New User Onboarding**: Rapidly identifying the "Starter Stack" for home or enterprise automation.
- **Agentic Workflow Design**: Selecting the right framework (e.g., [LangGraph](../tools/frameworks/langgraph.md) or [OpenClaw](../tools/development_ops/openclaw.md)) and communication protocol (FastMCP 3.1) for autonomous agents.
- **Enterprise RAG Implementation**: Navigating high-signal retrieval engines, such as [LlamaIndex](llamaindex.md) and [Tavily](../tools/providers/tavily.md).
- **Rapid Prototyping**: Launching full-stack MVPs using the [Free AI Website Playbook](free_ai_website_playbook.md) with modern deployment hosts like [Vercel](../tools/development_ops/vercel.md) and [Cloudflare Pages](../tools/development_ops/cloudflare-pages.md).
- **Local AI Orchestration**: Setting up private, secure inference environments using [LocalAI](../tools/infrastructure/localai.md) and [Ollama](../services/ollama.md).

## Strengths
- **Outcome-Driven Navigation**: Focuses on "Jobs to be Done" rather than individual tool feature lists.
- **FastMCP 3.1 Alignment**: Explicitly highlights tools and architectures supporting current Model Context Protocol standards for agentic tool calling and streaming state management.
- **Visual Mapping**: Utilizes structured comparison matrices and grid cards for rapid mental model formation.
- **Opinionated Defaults**: Provides clear "Practical Defaults" to help builders ship faster with battle-tested tool combinations.

## Limitations
- **Manual Indexing**: Requires proactive updates as frontier models (e.g., new Gemini 4.0 or Gemma 3 variants) emerge.
- **Abstraction Layer**: Provides the roadmap but does not contain low-level code implementation details found in specific tool docs.
- **Path Dependency**: Highly optimized for the repository's core philosophy of structured, AI-assisted development and automation.

## When to use it
- When you are new to the repository and need a structured entry point.
- When starting a new project and deciding on an architecture (e.g., Agentic vs. Flow-based).
- When you need a high-level overview of how [Agentic Workflows](patterns/agentic-workflows.md) and [Infrastructure](../architecture/infrastructure.md) components integrate.

## When not to use it
- If you already know the specific tool you need (use the global search or category indices).
- When seeking low-level API reference documentation (go directly to the tool page in `docs/tools/`).
- For tracking daily repository changes (use the [AI Daily Digest](../../ai-daily-digest/index.md) instead).

## Getting started

To get the most out of the AI Builder Index, follow these steps:

1. **Identify your Goal**: Scan the "Start by outcome" table below.
2. **Follow the Path**: Click the link in the "Start here" column for your chosen goal.
3. **Adopt Defaults**: Reference the "Recommended entry paths" grid for quick architecture blueprints.

### Start by outcome

| Goal | Start here | Then go to | Best for |
| :--- | :--- | :--- | :--- |
| Build a website or app for free | [Free AI Website Playbook](free_ai_website_playbook.md) | [Vercel](../tools/development_ops/vercel.md), [GitHub Pages](../tools/development_ops/github-pages.md), [Supabase](../tools/infrastructure/supabase.md) | Founders, consultants, indie developers |
| Set up an AI-driven company | [AI Company Starter Stack](ai_company_starter_stack.md) | [n8n](../services/n8n.md), [mem0](../tools/agents/mem0.md), [Vault](../tools/automation_orchestration/hashicorp-vault.md) | Teams building high-leverage workflows |
| Choose an agent stack | [Agent Framework Learning Map](agent_framework_learning_map.md) | [LangGraph](../tools/frameworks/langgraph.md), [OpenClaw](../tools/development_ops/openclaw.md) | Engineers building agentic state machines |
| Research markets & leads | [AI Company Starter Stack](ai_company_starter_stack.md) | [Tavily](../tools/providers/tavily.md), [Browser Use](../tools/automation_orchestration/browser-use.md) | Sales, growth, and market intelligence |
| Run private / local AI | [AI Company Starter Stack](ai_company_starter_stack.md) | [LocalAI](../tools/infrastructure/localai.md), [Ollama](../services/ollama.md), [Gemma 3](local_llms.md) | Privacy-sensitive and enterprise teams |

### Recommended entry paths

<div class="grid cards" markdown>

-   **Build Websites**
    ---
    Start with [Free AI Website Playbook](free_ai_website_playbook.md). Deploy static or dynamic sites using [GitHub Pages](../tools/development_ops/github-pages.md) or [Vercel](../tools/development_ops/vercel.md).

-   **Ship AI Products**
    ---
    Start with [AI Tooling Landscape](ai_tooling_landscape.md). Navigate frontier providers like Claude 5.1 and GPT-5.5 with [Agentic Workflows](patterns/agentic-workflows.md).

-   **Run Operations**
    ---
    Start with [AI Company Starter Stack](ai_company_starter_stack.md). Orchestrate background jobs with [n8n](../services/n8n.md) and secure credentials via [Vault](../tools/automation_orchestration/hashicorp-vault.md).

-   **Private / Local AI**
    ---
    Start with [LocalAI](../tools/infrastructure/localai.md) and [llmfit](../tools/development_ops/llmfit.md) for secure, on-premise inference with Gemma 3 and Qwen 3.8.

</div>

## CLI examples
The AI Builder Index is a documentation portal and does not have a direct CLI. However, you can query and index the knowledge base programmatically:

```bash
# Search for specific outcomes within the knowledge base
grep -r "Build a website" docs/knowledge_base/

# Extract all tool references from the AI Builder Index
python3 -c "
import re
with open('docs/knowledge_base/ai_builder_index.md') as f:
    links = re.findall(r'\[(.*?)\]\((.*?)\)', f.read())
for text, url in links:
    print(f'{text} -> {url}')
"
```

## API examples
For programmatic integration within agentic tool chains (e.g., FastMCP 3.1 servers querying documentation), use Pydantic v2 schemas to validate index entries:

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class IndexOutcomeEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    goal: str = Field(description="Target business or engineering outcome")
    start_here_path: str = Field(description="Primary playbook or guide URL")
    next_steps: List[str] = Field(default_factory=list, description="Recommended downstream tools")
    target_persona: str = Field(description="Primary beneficiary persona")

class AIBuilderIndexSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    version: str = Field(default="2027.1")
    protocol_support: str = Field(default="FastMCP 3.1")
    outcomes: List[IndexOutcomeEntry]

# Example initialization
index_data = AIBuilderIndexSchema(
    outcomes=[
        IndexOutcomeEntry(
            goal="Build a website or app for free",
            start_here_path="free_ai_website_playbook.md",
            next_steps=["docs/tools/development_ops/vercel.md", "docs/tools/infrastructure/supabase.md"],
            target_persona="Founders and indie developers"
        )
    ]
)
print(index_data.model_dump_json(indent=2))
```

## Related tools / concepts
- [Free AI Website Playbook](free_ai_website_playbook.md) — Step-by-step launch guide.
- [AI Company Starter Stack](ai_company_starter_stack.md) — Operational blueprint for modern AI startups.
- [AI Tooling Landscape](ai_tooling_landscape.md) — The broader ecosystem map.
- [Agent Framework Learning Map](agent_framework_learning_map.md) — Comparing agent frameworks like LangGraph and OpenClaw.
- [Agentic Workflows](patterns/agentic-workflows.md) — Designing multi-step reasoning tasks.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — FastMCP 3.1 standards.
- [Home Index](../../index.md) — Root of the documentation tree.
- [Infrastructure](../architecture/infrastructure.md) — The hardware and software foundation.

## Sources / references
- [KnowledgeOps Documentation Standards](../../standards-and-conventions.md)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/docs/concepts/tasks)
- [Awesome Claude AI Curated List](https://awesomeclaude.ai/)
- [Gemma 3 Technical Report](https://storage.googleapis.com/deepmind-media/gemma/gemma-3-report.pdf)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
