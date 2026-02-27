---
hide:
  - navigation
  - toc
---

# Home-Office Automation & AI Hub

> A self-updating knowledge base for AI tools, local LLMs, and privacy-first home automation — maintained by humans and agents working together.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Get Started**

    ---

    New here? Explore the [AI Tooling Landscape](knowledge_base/ai_tooling_landscape.md) to see how it all fits together, or follow the [Maturity Ladder](#maturity-ladder).

-   :material-tools:{ .lg .middle } **126 Tools & Services**

    ---

    Browse the [Tool Catalogue](tools/README.md) covering AI coding agents, LLM providers, benchmarks, orchestration platforms, and 47 self-hosted services.

-   :material-book-open-variant:{ .lg .middle } **Knowledge Base**

    ---

    Deep dives into [agent protocols](knowledge_base/agent_protocols.md), [model classes](knowledge_base/model_classes.md), [design patterns](knowledge_base/patterns/index.md), and [security](knowledge_base/llm_security_privacy.md).

-   :material-robot:{ .lg .middle } **Self-Improving**

    ---

    This repo grows autonomously. A [daily AI digest](new-sources.md) discovers tools, [Jules](tools/ai_knowledge/jules.md) writes docs, and a [weekly planner](architecture/multi_agent_knowledgeops.md) deepens coverage — all via GitHub Actions.

</div>

---

## :ladder: Maturity Ladder

Your journey from manual file storage to fully autonomous home-lab operations:

=== "Level 1 — Manual"

    Digital storage and basic sync. You have files in the cloud and can access them from anywhere.

    **Core tools**: [Nextcloud](services/nextcloud.md) · [Syncthing](services/syncthing.md)

=== "Level 2 — Organized"

    Centralized documents with visual orchestration. Paper goes in, structured data comes out.

    **Core tools**: [Paperless-ngx](services/paperless-ngx.md) · [n8n](services/n8n.md) · [Vikunja](services/vikunja.md)

=== "Level 3 — Augmented"

    AI-assisted extraction, semantic search, and local model benchmarking.

    **Core tools**: [Paperless-AI](services/paperless-ai.md) · [Ollama](services/ollama.md) · [Open WebUI](services/open-webui.md) · [SearXNG](services/searXNG.md)

=== "Level 4 — Autonomous"

    Agents run daily, write documentation, triage issues, and self-improve the knowledge base.

    **Core tools**: [Jules](tools/ai_knowledge/jules.md) · [Claude Code](tools/development_ops/claude-code.md) · [OpenHands](tools/development_ops/openhands.md) · [Dify](tools/ai_knowledge/dify.md)

---

## :compass: Quick Decision Matrix

| I need … | Reach for … |
| :--- | :--- |
| **100 % self-hosted AI** | [Ollama](services/ollama.md) + [Open WebUI](services/open-webui.md) + [LiteLLM](services/litellm.md) |
| **Best coding agent** | [Claude Code](tools/development_ops/claude-code.md) · [Cursor](tools/development_ops/cursor.md) · [Aider](tools/development_ops/aider.md) |
| **Workflow automation** | [n8n](services/n8n.md) · [Make](tools/automation_orchestration/make.md) · [Zapier](tools/automation_orchestration/zapier.md) |
| **Document intelligence** | [Paperless-ngx](services/paperless-ngx.md) + [Tika](services/tika.md) + [OCRmyPDF](tools/process_understanding/ocrmypdf.md) |
| **Web scraping / RAG** | [Crawl4AI](tools/process_understanding/crawl4ai.md) · [Firecrawl](tools/process_understanding/firecrawl.md) · [RAGFlow](tools/process_understanding/ragflow.md) |
| **LLM benchmarking** | [SWE-bench](tools/benchmarking/swe-bench.md) · [HLE](tools/benchmarking/humanitys-last-exam.md) · [Chatbot Arena](tools/benchmarking/chatbot-arena.md) |

---

## :bar_chart: Coverage at a Glance

| Category | Docs | | Category | Docs |
| :--- | ---: | --- | :--- | ---: |
| **Development & Ops** | 29 | | **Benchmarking** | 14 |
| **AI & Knowledge** | 18 | | **Automation & Orchestration** | 8 |
| **Self-hosted Services** | 47 | | **Process & Understanding** | 5 |
| **Infrastructure** | 2 | | **Frameworks** | 1 |

!!! tip "Growing daily"
    The automated pipeline discovers new tools every day. Categories with fewer than 8 docs are automatically targeted for expansion by the weekly planner.

---

## :books: Explore

<div class="grid cards" markdown>

-   **[Playbooks](playbooks/index.md)**

    Step-by-step guides: [email → calendar](playbooks/email-to-calendar.md), [scan → task](playbooks/scan-to-task.md), [dev workflow](playbooks/dev-workflow-ai-assisted.md), and more.

-   **[Architecture](architecture/README.md)**

    [Component map](architecture/component_map.md), [data flows](architecture/flows.md), [infrastructure](architecture/infrastructure.md), and the [multi-agent ops](architecture/multi_agent_knowledgeops.md) design.

-   **[Reference Implementations](reference-implementations/index.md)**

    n8n workflow exports, LLM prompt templates, calendar mapping rules, and Paperless tag taxonomies.

-   **[Standards](standards.md)**

    Taxonomy, naming conventions, doc templates, and the deduplication contract that keeps this repo consistent.

</div>

---

## :gear: How the Automation Works

```mermaid
flowchart LR
    A["Daily AI Digest<br/><small>00:00 & 12:00 UTC</small>"] -->|discovers| B["Digest → Intake Bridge<br/><small>01:00 & 13:00 UTC</small>"]
    B -->|new rows| C["docs/new-sources/"]
    C -->|processes| D["Jules Maintenance<br/><small>07:00 & 19:00 UTC</small>"]
    D -->|creates| E["Tool Docs + PRs"]
    F["Weekly Planner<br/><small>Mon & Thu 02:00</small>"] -->|deepening issues| D
    E -->|metrics| F
```

All automation runs on **GitHub Actions** using free-tier OpenRouter models and Google Jules. No human intervention required — just merge the PRs.

[:octicons-mark-github-16: View the pipeline](architecture/multi_agent_knowledgeops.md){ .md-button }
[:material-new-box: Latest discoveries](new-sources.md){ .md-button .md-button--primary }

---

<small>Privacy-first · Self-hosted · Agent-maintained · Updated daily · [Contribute](CONTRIBUTING.md) · [Roadmap](roadmap.md)</small>
