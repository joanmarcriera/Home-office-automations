# Agent Skills Best Practices

## What it is

An agent **skill** is a self-contained, named behaviour module that an autonomous agent can discover, trigger, and execute. Skills define *what* to do (instructions), *when* to do it (triggers), *what tools* are available, and *what permissions* are required. Well-authored skills are the difference between a reliable agent workflow and a chaotic, unpredictable one.

This document covers skill authoring for the two main runtimes used in this stack:

- **Claude Code skills** (`.claude/skills/` directory, Markdown + YAML frontmatter)
- **OpenClaw skills** (`skills/` directory, YAML + optional Markdown instructions)

The principles apply equally to both.

## What problem it solves

Poorly authored skills:
- Trigger on the wrong input (false positives waste tokens and cause incorrect actions)
- Fail to trigger when needed (false negatives lose automation value)
- Bloat the context window with unnecessary preamble
- Produce inconsistent outputs because instructions are ambiguous
- Silently fail without surfacing the right error to the operator

Best-practice structure prevents all of these.

## Where it fits in the stack

**Pattern**. Governs prompt/skill engineering for all autonomous agent workflows. Applies at design time (when authoring skills) and at runtime (when the agent selects and executes them).

## Skill anatomy

### Claude Code skill (Markdown)

```markdown
---
name: commit
description: Create a git commit with a well-structured message. Trigger when the user
             says "commit", "save changes", "/commit", or asks to finalise staged changes.
             Do NOT trigger for general git questions or status checks.
---

# Commit Skill

## When to use
Invoke this skill when the user asks to commit staged changes. Do not invoke if
the user is asking about git status, history, or other operations.

## Steps
1. Run `git status` to confirm there are staged changes
2. Run `git diff --staged` to understand what is changing
3. Draft a commit message: imperative mood, 72-char subject, optional body
4. Run the commit with the drafted message
5. Confirm success with `git log -1 --oneline`

## Output
Respond with the one-line commit SHA and message. No preamble.
```

### OpenClaw skill (YAML)

```yaml
name: paperless-intake
version: 1.0.0
description: Extract key fields from a forwarded document and file it in Paperless-ngx
trigger:
  keywords: ["file this", "intake document", "add to paperless"]
  file_types: ["application/pdf", "image/jpeg", "image/png"]
permissions:
  channels: ["telegram:personal", "whatsapp:personal"]
  users: ["owner"]
tools:
  - paperless_api
  - ocr_extract
instructions: |
  You are a document intake assistant. When the user forwards a document:
  1. Extract: document type, date, correspondent, and any monetary amounts
  2. POST to Paperless-ngx with the correct tag based on document type
  3. Reply with: "Filed as [Type] from [Correspondent], [Date]. ID: [paperless_id]"
  Never ask follow-up questions. If fields are missing, use "unknown" and file anyway.
```

## Trigger design

The trigger is the most critical part of a skill. A bad trigger causes the skill to run when it should not (false positive) or miss runs when it should fire (false negative).

### Good trigger patterns

| Approach | When to use |
|---|---|
| **Explicit keywords** | User clearly uses a phrase that maps to one skill ("commit", "file this") |
| **Slash commands** | Deterministic invocation; user types `/commit`, `/deploy` |
| **Schedule (cron)** | Time-triggered tasks; no ambiguity |
| **File type + keyword** | Document intake; only fires when a PDF is forwarded |
| **Webhook event type** | GitHub PR opened, Paperless document added |

### Trigger anti-patterns

```markdown
# BAD — too broad; fires on any question
trigger:
  keywords: ["help", "what", "how"]

# BAD — description is the full instructions; agent reads too much to decide
description: |
  This skill handles all document management tasks including filing, searching,
  retrieving, updating, and deleting documents from Paperless-ngx ...

# GOOD — tight, discriminative description
description: >
  File a forwarded document into Paperless-ngx. Trigger ONLY when the user
  forwards a file and says "file this" or "intake". Do not trigger for searches.
```

**Rule**: The `description` field is the routing signal. It must be specific enough that another skill with similar semantics will NOT also fire.

## Instructions design

### Lean instructions

Instructions should be step-by-step, deterministic, and minimal. Every extra word in the instruction costs context tokens at every invocation.

```markdown
# BAD — verbose, repeats context the model already has
## Instructions
You are a helpful assistant that will carefully and thoughtfully help the user
commit their changes to git. Git is a version control system. When you commit...
[200 more words of context]

# GOOD — direct, step-by-step, terminates with expected output
## Steps
1. `git status` — confirm staged changes exist; abort if none
2. `git diff --staged` — identify what changed
3. Draft: imperative subject (<72 chars) + optional body
4. `git commit -m "$(cat <<'EOF'\n{message}\nEOF)"`
5. Output: "{sha} {subject}"
```

### Progressive disclosure

Put the core steps in the skill itself. Reference external docs only for edge cases:

```markdown
## Steps
1. [core happy path — 3–6 steps]
2. [one sentence for each error case]

## Edge cases
See: ../../playbooks/dev-workflow-ai-assisted.md for conflict resolution
```

### Deterministic scripts over open-ended instructions

For predictable tasks, give the exact command to run rather than describing the goal:

```yaml
# BAD — model decides how to do it
instructions: "Push the changes to the remote repository"

# GOOD — exact command with escape hatches
instructions: |
  Run: git push -u origin HEAD
  If the push fails with "rejected":
    1. Run git fetch && git rebase origin/main
    2. Retry the push once
    3. If still failing, report the error and stop — do not force push
```

## Permission model

Always declare the minimum permissions a skill needs:

```yaml
permissions:
  channels: ["telegram:personal"]    # not ["*"]
  users: ["owner"]                   # not ["*"]
  tools:
    - paperless_api                  # only what is needed
    # NOT: shell_exec, file_system, http_any
```

For Claude Code skills, document any dangerous operations with a warning:

```markdown
!!! danger "Destructive operation"
    This skill can delete files. Always confirm with the user before running
    with `--confirm` flag omitted.
```

## Skill taxonomy for this stack

Organise skills into layers to avoid overlap and make discovery predictable:

| Layer | Examples | Notes |
|---|---|---|
| **Intake** | `paperless-intake`, `email-parse` | Receive and classify inputs |
| **Retrieve** | `vikunja-tasks`, `paperless-search` | Read from services |
| **Transform** | `summarise`, `extract-fields`, `translate` | Process content |
| **Write** | `create-task`, `file-document`, `send-message` | Mutate state |
| **Report** | `daily-digest`, `weekly-summary` | Aggregate and present |
| **Dev** | `commit`, `pr-review`, `deploy` | Software engineering actions |
| **Maintenance** | `knowledge-base-update`, `cleanup` | Repo/system maintenance |

## Validation loop

Before deploying a skill, run through this checklist:

### Design review
- [ ] Trigger description is specific enough to avoid false positives
- [ ] Trigger description is broad enough to catch all legitimate invocations
- [ ] Instructions are step-by-step, not open-ended goals
- [ ] Permissions are minimised to what is strictly needed
- [ ] Edge cases (missing inputs, API errors, ambiguous requests) are handled explicitly

### Execution review
- [ ] Invoke with an exact-match trigger phrase → skill fires correctly
- [ ] Invoke with a near-miss phrase that should NOT trigger → skill does not fire
- [ ] Run the skill on a test input → output matches expected format
- [ ] Introduce a simulated API error → skill handles it gracefully and reports the error

### Performance review
- [ ] Instruction length is under 300 tokens (measure with `tiktoken`)
- [ ] No redundant context that the model already knows from its system prompt
- [ ] Output format is consistent across 3+ separate test runs

## Common skill patterns

### Document intake skill

```yaml
name: document-intake
trigger:
  keywords: ["file this", "add to paperless", "intake"]
  file_types: ["application/pdf"]
instructions: |
  Extract: type, date (ISO-8601), correspondent, amount (or null).
  POST to POST /api/documents/ with tag derived from type.
  Reply: "Filed [type] from [correspondent] on [date]. ID: {id}"
  On API error: reply with the HTTP status and stop.
```

### Scheduled digest skill

```yaml
name: morning-brief
trigger:
  schedule: "0 7 * * 1-5"  # weekdays 07:00
instructions: |
  1. GET /api/tasks?status=open from Vikunja → list today's tasks
  2. GET today's weather from wttr.in/London?format=3
  3. Respond with: "**Today**: {weather}\n**Tasks ({n})**: {bullet_list}"
  Under 100 words. No preamble.
```

### Code review skill (Claude Code)

```markdown
---
name: review-pr
description: Review a pull request for correctness, style, and potential regressions.
             Trigger when user says "review this PR", "review PR #N", or "/review-pr".
---
## Steps
1. `gh pr diff {number}` — fetch the diff
2. Identify: logic errors, missing tests, style violations, security issues
3. Output structured review: **Summary** (2 sentences) + **Issues** (bulleted, max 5)
4. For each issue: file:line, severity (critical/warning/info), brief explanation
```

## Skill versioning and maintenance

```yaml
# Include version and last-updated in all skills
name: daily-digest
version: 2.1.0
last_updated: "2026-03-21"
changelog:
  "2.1.0": "Added weather to morning brief"
  "2.0.0": "Migrated from Notion to Vikunja for task retrieval"
  "1.0.0": "Initial version"
```

Review skills when:
- The tool they invoke changes its API
- The model runtime changes (new models may handle instructions differently)
- You observe consistent false positives or false negatives
- The task requirements change

## Comparing skill systems

| Runtime | Skill format | Trigger types | Tool binding |
|---|---|---|---|
| **Claude Code** | Markdown + YAML frontmatter | Keywords, slash commands | Any tool available in session |
| **OpenClaw** | YAML + Markdown instructions | Keywords, schedule, webhooks, file types | Declared tool list |
| **Anthropic Agent SDK** | Python + `@skill` decorator | Programmatic | Function calls |
| **n8n** | Visual node workflow | Webhooks, schedules, events | n8n node library |

## Strengths

- Clear trigger guidance prevents the most common failure mode (wrong skill fires)
- Step-by-step instructions eliminate ambiguity in execution
- Minimised permissions reduce blast radius of agent errors
- Versioning enables safe iteration without breaking existing automation

## Limitations

- Strict conventions add overhead for very simple, one-off tasks
- Skill behaviour depends on the underlying model; a skill tested on Claude 3.5 may perform differently on Qwen 2.5
- Trigger keyword lists need maintenance as vocabulary drifts
- Complex branching logic is better expressed as code than as skill instructions

## When to use it

- When building a growing library of reusable skills across one or more agent runtimes
- When skill false-positives or context bloat are recurring problems
- When multiple people (or agents) will be writing and sharing skills
- When automation reliability is more important than development speed

## When not to use it

- For one-off tasks that will never be reused
- When no autonomous skill routing is in use (pure API calls don't need skills)
- When the task logic is inherently complex enough to require code, not instructions

## Related tools / concepts

- [OpenClaw](../../tools/development_ops/openclaw.md) — primary skill runtime for messaging-channel agents
- [Anthropic Agent Skills](../../tools/agents/anthropic-agent-skills.md) — Anthropic's skill SDK
- [Claude Skills Ecosystem](../../tools/agents/claude-skills-ecosystem.md) — Claude Code skill environment
- [Claude Code Setup](../../tools/development_ops/claude-code-setup.md) — configuring skills in Claude Code
- [OpenClaw Workflow Prompts](openclaw-workflow-prompts.md) — curated prompt library for OpenClaw
- [Patterns Index](index.md) — other patterns in this knowledge base

## Sources / References

- [Claude Code Skills Documentation](https://docs.anthropic.com/claude-code/skills)
- [OpenClaw Skills Guide](https://github.com/openclaw/openclaw/wiki/Skills)
- [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)
- [Prompt Engineering Guide — few-shot and chain-of-thought](https://www.promptingguide.ai/)

## Contribution Metadata

- Last reviewed: 2026-03-21
- Confidence: high
