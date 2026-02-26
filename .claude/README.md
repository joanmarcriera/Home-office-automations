# .claude/ — Project Configuration for Claude Code

This directory is committed to the repo. It activates automatically when the project is opened in Claude Code.

```
.claude/
├── settings.json              # Hooks (see below)
├── settings.local.json        # Machine-specific permissions (gitignored)
├── agents/
│   └── playbook-reviewer.md   # Auto-invoked when editing docs/playbooks
└── skills/
    ├── new-tool-doc/           # /new-tool-doc <name> <category>
    └── knowledge-base-update/  # /knowledge-base-update
```

## Hooks

| Hook | When | What it does |
|---|---|---|
| mkdocs.yml validator | After any Edit/Write | Checks YAML syntax of mkdocs.yml |
| Workflow guard | Before any Edit/Write | Blocks `.github/workflows/` edits without confirmation |

## Full setup guide
See [docs/tools/development_ops/claude-code-setup.md](../docs/tools/development_ops/claude-code-setup.md) for the complete reproducible setup including plugins, MCP servers, and global skills.
