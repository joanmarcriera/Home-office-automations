# Home-Office Automation & AI Hub

A comprehensive operating manual for a privacy-first, AI-powered home lab and family automation stack.

## 🚀 Start Here
- **New to the stack?** Read the [Maturity Ladder](#maturity-ladder) to understand the stages of implementation.
- **Want to automate emails to calendar?** Follow the [Email to Calendar Playbook](playbooks/email-to-calendar.md).
- **Need to digitize mail?** See the [Scan to Task Playbook](playbooks/scan-to-task.md).
- **How do agents communicate?** Read about [MCP & ACP](./knowledge_base/agent_protocols.md).
- **Understand the big picture?** View the [Component Map](./architecture/component_map.md) and [Automation Flows](./architecture/flows.md).

---

## 🪜 Maturity Ladder

| Level | Description | Core Tools |
| :--- | :--- | :--- |
| **Level 1: Manual** | Digital storage and basic sync. | [Nextcloud](./services/nextcloud.md), [Syncthing](./services/syncthing.md) |
| **Level 2: Organized** | Centralized documents and visual orchestration. | [Paperless-ngx](./services/paperless-ngx.md), [n8n](./services/n8n.md) |
| **Level 3: Augmented** | AI-assisted extraction, semantic search, and benchmarking. | [Paperless-AI](./services/paperless-ai.md), [Ollama](./services/ollama.md), [HLE](./tools/benchmarking/humanitys-last-exam.md) |
| **Level 4: Autonomous** | Agent-led refactoring, proactive task management, and performance optimization. | [Jules](./tools/ai_knowledge/jules.md), [OpenHands](./tools/development_ops/openhands.md), [Terminal-Bench](./tools/benchmarking/terminal-bench.md) |

---

## ⚖️ Decision Matrix

| Requirement | Preferred Tools | Why? |
| :--- | :--- | :--- |
| **100% Self-Hosted** | [Radicale](./services/radicale.md), [Vikunja](./services/vikunja.md), [Ollama](./services/ollama.md) | No external API dependencies. |
| **Highest Accuracy** | [ChatGPT](./tools/ai_knowledge/chatgpt.md), [Google Calendar](./tools/calendar_tasks/google_calendar.md) | State-of-the-art models and reliable SaaS. |
| **Developer Focus** | [Zed](./tools/development_ops/zed.md), [Cursor](./tools/development_ops/cursor.md), [Aider](./tools/development_ops/aider.md), [Junie CLI](./tools/development_ops/junie-cli.md) | High-performance editors and terminal agents. |
| **Low Resource** | [Homebox](./services/homebox.md), [Syncthing](./services/syncthing.md) | Efficient, specialized tools. |

---

## 📂 Repository Structure

-   [**Operational Playbooks**](playbooks/index.md) - Step-by-step guides for common workflows.
-   [**Reference Implementations**](reference-implementations/index.md) - Workflow exports, prompt templates, and config standards.
-   [**Tool Catalogue**](tools/README.md) - Detailed documentation for 90+ tools.
-   [**Architecture**](architecture/README.md) - High-level component maps and data flows.
-   [**Knowledge Base**](knowledge_base/README.md) - Deep dives into AI models and agent protocols.
-   [**Standards & Conventions**](standards.md) - Naming and data contract specifications.
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
