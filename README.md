# Home-Office Automation & AI Hub

A comprehensive operating manual for a privacy-first, AI-powered home lab and family automation stack.

## 🚀 Start Here
- **New to the stack?** Read the [Maturity Ladder](#maturity-ladder) to understand the stages of implementation.
- **Want to automate emails to calendar?** Follow the [Email to Calendar Playbook](playbooks/email-to-calendar.md).
- **Need to digitize mail?** See the [Scan to Task Playbook](playbooks/scan-to-task.md).
- **Understand the big picture?** View the [Component Map](docs/architecture/component_map.md) and [Automation Flows](docs/architecture/flows.md).

---

## 🪜 Maturity Ladder

| Level | Description | Core Tools |
| :--- | :--- | :--- |
| **Level 1: Manual** | Digital storage and basic sync. | [Nextcloud](docs/tools/intake_storage/nextcloud.md), [Syncthing](docs/tools/intake_storage/syncthing.md) |
| **Level 2: Organized** | Centralized documents and visual orchestration. | [Paperless-ngx](docs/tools/intake_storage/paperless-ngx.md), [n8n](docs/tools/automation_orchestration/n8n.md) |
| **Level 3: Augmented** | AI-assisted extraction and semantic search. | [Paperless-AI](docs/tools/process_understanding/paperless-ai.md), [Ollama](docs/tools/process_understanding/ollama.md) |
| **Level 4: Autonomous** | Agent-led refactoring and proactive task management. | [Jules](docs/tools/ai_knowledge/jules.md), [OpenHands](docs/tools/development_ops/openhands.md) |

---

## ⚖️ Decision Matrix

| Requirement | Preferred Tools | Why? |
| :--- | :--- | :--- |
| **100% Self-Hosted** | Radicale, Vikunja, Ollama | No external API dependencies. |
| **Highest Accuracy** | ChatGPT, Google Calendar | State-of-the-art models and reliable SaaS. |
| **Developer Focus** | Cursor, Aider, OpenHands | Tight integration with Git and codebases. |
| **Low Resource** | Homebox, Syncthing | Efficient, specialized tools. |

---

## 📂 Repository Structure

-   [**Operational Playbooks**](playbooks/) - Step-by-step guides for common workflows.
-   [**Reference Implementations**](reference-implementations/) - Workflow exports, prompt templates, and config standards.
-   [**Tool Catalogue**](docs/tools/) - Detailed documentation for 35+ tools.
-   [**Architecture**](docs/architecture/) - High-level component maps and data flows.
-   [**Standards & Conventions**](standards-and-conventions.md) - Naming and data contract specifications.
-   [**Roadmap**](roadmap.md) - Future improvements and known gaps.

---

## 🛠️ Hub Utility Tool
Quickly explore the stack from your terminal:
```bash
# List all tools
python3 scripts/compare_agents.py list

# View documentation for a specific tool
python3 scripts/compare_agents.py doc paperless-ngx
```

---
*Organized for a high-performance, private homelab environment as of 2025.*
