# Claude Code — Project Setup Guide

## What it is
A reproducible configuration guide for the Claude Code CLI setup used in this repo, covering installed plugins, global skills, MCP servers, and project-level automation.

## What problem it solves
Claude Code's power in this repo comes from project-specific hooks, agents, and skills that need to be configured. This guide lets anyone who clones the repo reproduce the full setup from scratch.

## Where it fits in the stack
**Category**: Development & Ops / Tooling Configuration

---

## Prerequisites
- Claude Code CLI installed: `npm install -g @anthropic/claude-code`
- Anthropic API key configured
- `uv` installed (for Ollama skill scripts): `pip install uv`

---

## 1. Plugins (global, install once)

Run these once on any machine:

```bash
claude plugin install claude-code-setup@claude-plugins-official
claude plugin install claude-md-management@claude-plugins-official
claude plugin install code-simplifier@claude-plugins-official
claude plugin install commit-commands@claude-plugins-official
claude plugin install feature-dev@claude-plugins-official
claude plugin install github@claude-plugins-official
claude plugin install playwright@claude-plugins-official
claude plugin install security-guidance@claude-plugins-official
claude plugin install slack@claude-plugins-official
claude plugin install huggingface-skills@claude-plugins-official
claude plugin install qodo-skills@claude-plugins-official
```

---

## 2. MCP Servers (global, install once)

```bash
# Live documentation lookup for any library used in playbooks/docs
claude mcp add context7 -- npx -y @upstash/context7-mcp

# GitHub — create/close issues, trigger workflows, read PR state
claude mcp add github -- npx @anthropic-ai/mcp-server-github
```

---

## 3. Global Skills (live at `~/.claude/skills/`)

These Ollama utility skills are stored globally and work across all projects.

| Skill | Invocation | Purpose |
|---|---|---|
| `ollama-status` | `/ollama-status` | Check health and model count on both Ollama servers |
| `ollama-models` | `/ollama-models <task>` | Get model recommendation for a task type |
| `ollama-generate` | `/ollama-generate <prompt>` | Generate text using a local Ollama model |
| `ollama-process` | `/ollama-process` | Batch-process items through Ollama |

**Servers configured:**
- TrueNAS: `http://192.168.0.5:30068` (GPU-accelerated, 18+ models)
- MacBook M4: `http://localhost:11434`

To install these skills on a new machine, copy `~/.claude/skills/ollama-*/` from an existing setup.

---

## 4. Project-Level Configuration (`.claude/`)

Committed to this repo — automatically active when you open the project in Claude Code.

### Hooks (`settings.json`)

| Hook | Trigger | Behavior |
|---|---|---|
| mkdocs.yml validator | PostToolUse on any Edit/Write | Validates YAML syntax of `mkdocs.yml` immediately after editing |
| Workflow guard | PreToolUse on any Edit/Write | Blocks edits to `.github/workflows/` — requires explicit user confirmation |

### Subagent (`agents/playbook-reviewer.md`)

Invoked automatically when adding or editing playbooks and tool docs. Checks:
- All 10 required sections are present
- File is in the correct taxonomy directory
- Internal links resolve to real files
- No duplicate tool pages exist elsewhere

### Skills

| Skill | Invocation | Purpose |
|---|---|---|
| `new-tool-doc` | `/new-tool-doc <name> <category>` | Scaffold a new tool page from the standard template; dedup-checks first; updates mkdocs.yml nav and category index |
| `knowledge-base-update` | `/knowledge-base-update` | Process `docs/new-sources.md` intake queue: classify, create/update canonical pages, mark done |

---

## Related tools / concepts
- [Claude Code](./claude-code.md)
- [Agent Protocols (MCP & ACP)](../../knowledge_base/agent_protocols.md)
- [Standards & Conventions](../../standards.md)

## Sources / references
- [Claude Code documentation](https://docs.anthropic.com/claude-code)
- [MCP specification](https://modelcontextprotocol.io)
