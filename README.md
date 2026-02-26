# Home-Office Automation & AI Hub

A comprehensive operating manual for a privacy-first, AI-powered home lab and family automation stack.

## 🚀 Start Here
- **New to the stack?** Read the [Maturity Ladder](#maturity-ladder) to understand the stages of implementation.
- **Want to automate emails to calendar?** Follow the [Email to Calendar Playbook](playbooks/email-to-calendar.md).
- **Need to digitize mail?** See the [Scan to Task Playbook](playbooks/scan-to-task.md).
- **How do agents communicate?** Read about [MCP & ACP](docs/knowledge_base/agent_protocols.md).
- **Understand the big picture?** View the [Component Map](docs/architecture/component_map.md) and [Automation Flows](docs/architecture/flows.md).

---

## 🪜 Maturity Ladder

| Level | Description | Core Tools |
| :--- | :--- | :--- |
| **Level 1: Manual** | Digital storage and basic sync. | [Nextcloud](docs/services/nextcloud.md), [Syncthing](docs/services/syncthing.md) |
| **Level 2: Organized** | Centralized documents and visual orchestration. | [Paperless-ngx](docs/services/paperless-ngx.md), [n8n](docs/services/n8n.md) |
| **Level 3: Augmented** | AI-assisted extraction, semantic search, and benchmarking. | [Paperless-AI](docs/services/paperless-ai.md), [Ollama](docs/services/ollama.md), [HLE](docs/tools/benchmarking/humanitys-last-exam.md) |
| **Level 4: Autonomous** | Agent-led refactoring, proactive task management, and performance optimization. | [Jules](docs/tools/ai_knowledge/jules.md), [OpenHands](docs/tools/development_ops/openhands.md), [Terminal-Bench](docs/tools/benchmarking/terminal-bench.md) |

---

## ⚖️ Decision Matrix

| Requirement | Preferred Tools | Why? |
| :--- | :--- | :--- |
| **100% Self-Hosted** | [Radicale](docs/services/radicale.md), [Vikunja](docs/services/vikunja.md), [Ollama](docs/services/ollama.md) | No external API dependencies. |
| **Highest Accuracy** | [ChatGPT](docs/tools/ai_knowledge/chatgpt.md), [Google Calendar](docs/tools/calendar_tasks/google_calendar.md) | State-of-the-art models and reliable SaaS. |
| **Developer Focus** | [Zed](docs/tools/development_ops/zed.md), [Cursor](docs/tools/development_ops/cursor.md), [Aider](docs/tools/development_ops/aider.md), [Junie CLI](docs/tools/development_ops/junie-cli.md) | High-performance editors and terminal agents. |
| **Low Resource** | [Homebox](docs/services/homebox.md), [Syncthing](docs/services/syncthing.md) | Efficient, specialized tools. |

---

## 📂 Repository Structure

-   [**Operational Playbooks**](playbooks/) - Step-by-step guides for common workflows.
-   [**Reference Implementations**](reference-implementations/) - Workflow exports, prompt templates, and config standards.
-   [**Tool Catalogue**](docs/tools/) - Detailed documentation for 90+ tools.
-   [**Architecture**](docs/architecture/) - High-level component maps and data flows.
-   [**Knowledge Base**](docs/knowledge_base/) - Deep dives into AI models and agent protocols.
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

## 🤝 Contributors

* **Antigravity** - Agentic AI Coding Assistant
