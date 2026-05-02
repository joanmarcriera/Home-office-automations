# Andrej Karpathy Skills

## What it is
A curated collection of skills and patterns inspired by Andrej Karpathy's approach to AI and software engineering, designed to help agents avoid basic pitfalls.

## What problem it solves
It codifies high-signal development habits and "instincts" into actionable patterns for AI agents.

## Where it fits in the stack
**Category**: AI & Knowledge / Best Practices

## Typical use cases
- **Agent Initialization**: Setting baseline "thinking" patterns for a new project.
- **Workflow Optimization**: Reducing agent hallucinations and "looping" by enforcing clarifying questions.
- **Code Review Standard**: Using the guidelines as a checklist for human or AI code reviews.

## Strengths
- **Low Overhead**: Simple Markdown-based guidelines that don't require complex infrastructure.
- **High Signal**: Focuses on the most common and damaging mistakes made by AI agents.
- **Developer-Centric**: Aligns AI behavior with senior-level software engineering best practices.

## Limitations
- **Opinionated**: Some patterns might conflict with specific project styles or requirements.
- **Manual Enforcement**: Outside of Claude Code, requires manual inclusion in system prompts or project context.

## When to use it
- When you find your AI agent is making "obvious" mistakes or over-complicating solutions.
- At the start of a new project to establish a high bar for code quality.

## When not to use it
- For highly experimental or "creative" coding where standard constraints might be too restrictive.
- In environments where a different, strict coding standard is already enforced.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: N/A (Documentation/Guidelines)

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

### Sample CLAUDE.md Snippet
```markdown
## Karpathy Instincts
- **Think Before Coding**: Surface tradeoffs. Ask when unclear.
- **Simplicity First**: Minimal code. No speculative features.
- **Surgical Changes**: Touch only what you must. Match existing style.
- **Goal-Driven Execution**: Define success criteria. Loop until verified.
```

### Basic usage
Once installed, the guidelines are automatically applied by the AI agent during its thinking process. You can verify it's working by observing if the agent:
- Asks clarifying questions before implementation.
- Prefers simple, direct solutions over complex abstractions.
- Makes surgical changes to the code.

## Thinking Pattern Example: Handling Ambiguity
When faced with a vague request like "Fix the auth," an agent using Karpathy/Pocock skills avoids jumping straight into code.

**Agent Thinking Process:**
1. **Initial Impulse**: Look for `auth.py` and start changing login logic.
2. **Skill Check (Simplicity/Surgical)**: Wait. "Fix the auth" is ambiguous. I need more context to be surgical and avoid over-engineering.
3. **Action**: Ask the user: "Could you specify if this is a bug with the current login flow, an integration issue with the new provider, or a request for a new feature like MFA?"
4. **Result**: User specifies it's a redirect loop after OAuth. Agent now knows exactly which file and function to target, minimizing code churn.

## Thinking Pattern Example: The "Zero-Draft" Pattern
Instead of writing 200 lines of complex boilerplate, the agent writes a "Zero-Draft" that proves the core logic works with minimum dependencies.

1. **Step 1**: Write a 10-line script that triggers the core API or logic.
2. **Step 2**: Verify the draft runs and returns the expected result.
3. **Step 3**: "Refactor" the proven logic into the production codebase surgically.

## CLI examples
The skills can be managed via the Claude Code CLI:

```bash
# List installed plugins
/plugin list

# Update the skill
/plugin update andrej-karpathy-skills
```

## Related tools / concepts

- [Surgical Changes](https://peerlist.io/xiji2646/articles/the-978kstar-file-that-makes-claude-code-stop-overengineerin)
- [Matt Pocock Skills](matt-pocock-skills.md)
- [Claude Code](../development_ops/claude-code.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)
- [Superpowers](../agents/superpowers.md)

## Sources / references
- [Andrej Karpathy Skills (GitHub)](https://github.com/forrestchang/andrej-karpathy-skills)
- [Andrej Karpathy's Recommendations for LLMs](https://karpathy.ai/llm.html)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
