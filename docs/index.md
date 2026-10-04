---
hide:
  - navigation
  - toc
---

# Home-Office Automation & AI Hub

> Operational documentation for AI-enabled home-office automation, maintained by humans and agents with explicit quality gates. Updated for early January 2027 SOTA standards (incorporating FastMCP 3.1, Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro, Llama 4, and Pydantic v2 validation).

## Start by Goal

<div class="grid cards" markdown>

-   **Implement a workflow**

    ---

    Go to [Playbooks](playbooks/index.md) for step-by-step execution guides.

-   **Evaluate or compare tools**

    ---

    Start in the [Tool Catalogue](tools/README.md), then use the [AI Tooling Landscape](knowledge_base/ai_tooling_landscape.md) for context.

-   **Build a website or app quickly**

    ---

    Start in the [AI Builder Index](knowledge_base/ai_builder_index.md), then use the [Free AI Website Playbook](knowledge_base/free_ai_website_playbook.md).

-   **Choose the right model**

    ---

    Start with the [Model Routing Guide](knowledge_base/model_routing_guide.md).

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
| **Reports** | Triage reports, execution logs, and backlog status. | [reports/index.md](reports/index.md) |
| **Roadmap** | Planned improvements and known gaps. | [roadmap](../roadmap.md) |
| **Standards** | Taxonomy, canonical-page rules, metadata requirements, and dedup policy. | [standards.md](standards.md) |

---

## How Repository Automation Works

```mermaid
flowchart LR
    A["Daily digest"] --> B["Digest-to-intake bridge"]
    B --> C["Intake logs"]
    C --> D["Jules maintenance issues"]
    D --> E["Jules PRs or weekly rollup PR"]
    E --> F["Quality gates"]
    F --> G["Main branch"]
    G --> H["Weekly backlog and deepening loops"]
```

Repository mapping:

- **Daily digest**: `.github/workflows/daily-digest.yml`
- **Digest-to-intake bridge**: `.github/workflows/digest-to-intake.yml`
- **Jules maintenance issues**: `.github/workflows/daily-jules-maintenance.yml`
- **Jules PRs / weekly rollup PR**: Jules bot PRs plus `automation/weekly-rollup`
- **Quality gates**: docs, catalog, intake, link, and generated-content workflows
- **Weekly backlog / deepening loops**: `.github/workflows/process-jules-backlog.yml`, `.github/workflows/daily-jules-knowledge.yml`, `.github/workflows/weekly-planner.yml`, `.github/workflows/weekly-automation-rollup-merge.yml`
- **Schedule**: `.github/workflows/odd-day-pipeline.yml` is the single scheduled entry point (00:30 UTC, odd days of the month only); it runs the lanes above as one chain, so even days have no scheduled jobs
- **Hygiene lanes** (first in the chain): `pr-hygiene.yml` closes orphaned bot PRs, `jules-issue-hygiene.yml` and `cleanup-automation-issues.yml` retire failed or superseded control issues, and `branch-cleanup.yml` reports (or, once enabled with the `BRANCH_CLEANUP_LIVE` repo variable, deletes up to 50 per run) branches that are fully merged or whose PR is closed — never `main`, `gh-pages`, `automation/*` or open-PR branches
- **Publishing**: `deploy-docs.yml` runs as the last lane, because merges made by the Actions token never trigger the push-based deploy
- **Dry run**: dispatching the pipeline with `dry_run: true` (and `weekly_lanes: all`) exercises every lane's real queries while writing nothing — no issues, PRs, pushes, branch deletions or deploys
- **Watchdog**: `automation-health.yml` follows every pipeline run (plus a slow dead-man schedule), reruns failed lanes once and keeps a single `automation-health` issue open while anything is red

Supporting docs:

- [Automated Contributions](architecture/automated_contributions.md)
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md)
- [Contributing Guide](CONTRIBUTING.md)

---

## Maintenance Entry Points

- Human maintainers: [CONTRIBUTING.md](CONTRIBUTING.md)
- LLM agents: [AGENTS.md](https://github.com/joanmarcriera/Home-office-automations/blob/main/AGENTS.md) (repo-root file on GitHub)
- Agent task patterns: [skills.md](https://github.com/joanmarcriera/Home-office-automations/blob/main/skills.md) (repo-root file on GitHub)

<small>Use this page as the section index. Use section overview pages for detailed scope and conventions.</small>

---

## Sources / References
- [Automated Contributions](architecture/automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](architecture/multi_agent_knowledgeops.md)
- [Contributing Guide](CONTRIBUTING.md)

---

## Contribution Metadata
- Last reviewed: 2026-10-04
- Confidence: high
