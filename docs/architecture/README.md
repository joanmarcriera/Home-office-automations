# Architecture & Flows

High-level design of the AI Hub: how components connect, how data flows between them, and how the repository maintains itself over time.

## Contents

| Document | What it covers |
| :--- | :--- |
| [Component Map](component_map.md) | Full inventory of services and their relationships — the definitive "what talks to what" map |
| [Automation Flows](flows.md) | Detailed sequence and data-flow diagrams for key automation workflows |
| [Infrastructure](infrastructure.md) | Hardware topology, network layout, and resource allocation decisions |
| [SSH Execution Patterns](ssh_execution_patterns.md) | Secure orchestration of remote commands across TrueNAS, Pi, and MacBook |
| [MCP Patterns](../knowledge_base/patterns/tool-calling-and-mcp.md) | Architecture for tool-calling via the Model Context Protocol |
| [Automated Contributions](automated_contributions.md) | How Google Jules, digest workflows, and quality gates keep the repo self-improving |
| [Multi-Agent KnowledgeOps](multi_agent_knowledgeops.md) | Governance contract, role model, and CI gates for scalable multi-agent documentation growth |
| [Prompt Catalogue](prompt-catalogue.md) | Reference library of production prompts used across automation workflows |
| [Text-to-SQL Architecture](data-copilot-text-to-sql.md) | Layered multi-agent pipeline for natural language data querying |

---

## System at a Glance

```mermaid
flowchart TD
    subgraph Ingest
        A[Daily Digest] --> B[Intake Bridge]
        B --> C[docs/new-sources/]
    end
    subgraph Ralph-loop
        C --> D[Jules Issue]
        D --> E[Jules Execution\n(a) Work (b) Link (c) Decompose]
        E --> F[Jules PR]
    end
    subgraph Quality Gates
        F --> G[Audit Docs Quality]
        G --> H[Check Docs Contract]
        H --> I[Check Catalog Consistency]
        I --> J[Main Branch]
    end
    subgraph Deployment
        J --> K[MkDocs Build]
        K --> L[GitHub Pages]
    end
```

---

## Related

- [Home](../index.md)
- [Contributing](../CONTRIBUTING.md)
- [Standards](../standards.md)
- [Ralph-loop Execution Reports](reports/)

## Sources / References
- [Automated Contributions](automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](multi_agent_knowledgeops.md)
- [GitHub Actions Documentation](https://docs.github.com/actions)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
