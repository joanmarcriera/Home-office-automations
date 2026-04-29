# Andrej Karpathy Skills

## What it is
A curated collection of skills and patterns inspired by Andrej Karpathy's approach to AI and software engineering, designed to help agents avoid basic pitfalls.

## What problem it solves
It codifies high-signal development habits and "instincts" into actionable patterns for AI agents.

## Where it fits in the stack
**Category**: AI & Knowledge / Best Practices

## Getting started

### Installation
Karpathy-inspired guidelines can be installed as a plugin for Claude Code:

```bash
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

Alternatively, you can manually add the `CLAUDE.md` to your project:

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

### Basic usage
Once installed, the guidelines are automatically applied by the AI agent during its thinking process. You can verify it's working by observing if the agent:
- Asks clarifying questions before implementation.
- Prefers simple, direct solutions over complex abstractions.
- Makes surgical changes to the code.

## CLI examples
The skills can be managed via the Claude Code CLI:

```bash
# List installed plugins
/plugin list

# Update the skill
/plugin update andrej-karpathy-skills
```

## Related tools / concepts

- [AI Templates](aitmpl.md)
- [AnythingLLM](anythingllm.md)
- [ChatGPT](chatgpt.md)
- [Claude](claude.md)
- [Claude Mythos](claude-mythos.md)

## Sources / references
- [Andrej Karpathy Skills (GitHub)](https://github.com/forrestchang/andrej-karpathy-skills)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high

- [Andrej Karpathy Skills (GitHub)](https://github.com/forrestchang/andrej-karpathy-skills)
