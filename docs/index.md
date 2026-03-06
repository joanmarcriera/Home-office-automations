---
hide:
  - navigation
  - toc
---

# Home-Office Automation & AI Hub

> Operational documentation for AI-enabled home-office automation, maintained by humans and agents with explicit quality gates.

## Start by Goal

<div class="grid cards" markdown>

-   **Implement a workflow**

    ---

    Go to [Playbooks](playbooks/index.md) for step-by-step execution guides.

-   **Evaluate or compare tools**

    ---

    Start in the [Tool Catalogue](tools/README.md), then use the [AI Tooling Landscape](knowledge_base/ai_tooling_landscape.md) for context.

-   **Understand architecture and system design**

    ---

    Use [Architecture](architecture/README.md) for component maps, flows, and governance.

-   **Contribute safely (human or agent)**

    ---

    Follow [Contributing](CONTRIBUTING.md), [Standards](standards.md), and the [Agent Rules](https://github.com/joanmarcriera/Home-office-automations/blob/main/AGENTS.md).

</div>

---

## Section Guide

| Section | What you will find | Entry page |
| :--- | :--- | :--- |
| **New Sources** | Intake queue process and dated discovery logs used by automation workflows. | [new-sources.md](new-sources.md) |
| **Playbooks** | Reusable execution guides for recurring operational workflows. | [playbooks/index.md](playbooks/index.md) |
| **Services** | Self-hosted service docs (deploy context, use cases, strengths/limits). | [services/README.md](services/README.md) |
| **Tool Catalogue** | Canonical docs for AI tools, frameworks, providers, agents, infra, benchmarking, and orchestration. | [tools/README.md](tools/README.md) |
| **Knowledge Base** | Concepts and patterns: protocols, RAG, model classes, security, and ecosystem landscape. | [knowledge_base/README.md](knowledge_base/README.md) |
| **Architecture** | Component map, data flows, infrastructure decisions, and multi-agent governance. | [architecture/README.md](architecture/README.md) |
| **Reference Implementations** | Concrete prompts, mapping rules, and workflow exports for direct reuse. | [reference-implementations/index.md](reference-implementations/index.md) |
| **Roadmap** | Planned improvements and known gaps. | [roadmap.md](roadmap.md) |
| **Standards** | Taxonomy, canonical-page rules, metadata requirements, and dedup policy. | [standards.md](standards.md) |

---

## How Repository Automation Works

```mermaid
flowchart LR
    A["Daily digest"] --> B["Intake logs"]
    B --> C["Jules maintenance issues"]
    C --> D["PRs with docs/catalog updates"]
    D --> E["Quality gates"]
    E --> F["Main branch"]
    F --> G["Weekly backlog/deepening loops"]
```

Supporting docs:

- [Automated Contributions](architecture/automated_contributions.md)
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md)
- [Contributing Guide](CONTRIBUTING.md)

---

## Maintenance Entry Points

- Human maintainers: [CONTRIBUTING.md](CONTRIBUTING.md)
- LLM agents: [AGENTS.md](https://github.com/joanmarcriera/Home-office-automations/blob/main/AGENTS.md)
- Agent task patterns: [skills.md](https://github.com/joanmarcriera/Home-office-automations/blob/main/skills.md)

<small>Use this page as the section index. Use section overview pages for detailed scope and conventions.</small>
