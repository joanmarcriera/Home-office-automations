# Contributing to the AI Hub

Thank you for your interest in improving the Home-Office Automation & AI Hub! We welcome contributions from both humans and AI agents.

## LLM Agent Quick Start

Before changing files, read these in order:

1. [AGENTS.md](https://github.com/joanmarcriera/Home-office-automations/blob/main/AGENTS.md) — repository operating contract, checklists, and quality bar
2. [skills.md](https://github.com/joanmarcriera/Home-office-automations/blob/main/skills.md) — reusable task patterns for intake, docs updates, workflow edits, and branch hygiene
3. [Standards](standards.md) — taxonomy and canonical-page rules

Use this sequence for most tasks:

1. Find canonical page or confirm it does not exist.
2. Make scoped edits for one intent only.
3. Run relevant validation scripts.
4. Open/merge PR only after required checks pass.

## How You Can Help
- **Add New Tools**: Found a tool that fits the stack? Document it using our [standard template](templates/tool_template.md).
- **Refine Playbooks**: Improve our existing automation guides with more technical detail or new variants.
- **Update Services**: Ensure the documentation for self-hosted services remains accurate as versions change.
- **Improve Prompts**: Optimize our LLM prompt templates for better extraction and classification results.

## Automated Contributions: The Ralph-loop

This repository implements the **Ralph-loop**, a systematic directive for AI agents (primarily **Google Jules**) to close issues by performing one of three actions:

a) **Do the work**: Implement the requested feature, fix the bug, or perform the documentation update.
b) **Add links**: Find the appropriate canonical location for provided external links.
c) **Decompose**: Divide complex tasks into smaller, trackable issues with extracted context.

### Daily Ingestion & Maintenance Lanes
Automation is split into specialized lanes to maintain the "High Confidence" standard:

1. **Daily Digest**: Scans and summarizes external sources (GitHub, Reddit, News).
2. **Intake Bridge**: Stages qualifying items in [`docs/new-sources/`](new-sources.md).
3. **Maintenance Run**: Automates routine audits, broken link fixes, and catalog syncs.
4. **Knowledge Deepening**: Targets "Shallow" or "Stale" documents for technical expansion.
5. **Quality Gates**: Mandatory execution of `audit_docs_quality.py` and `check_docs_contract.py`.

### Assigning a Task to Jules
You can request Jules to perform a task by:
1.  **Opening an Issue**: Describe the task clearly (e.g., "Add documentation for Tool X" or "Fix broken link in README").
2.  **Adding the Label**: Apply the label `jules` (case-insensitive) to the issue.
3.  **Review the Plan**: Jules will analyze the task and post a plan as a comment. Once you approve, Jules will get to work.
4.  **Review the PR**: Jules will open a Pull Request with its changes. Depending on the automation lane and repository policy, it may auto-merge after required checks pass.

## Contribution Standards
- **Precise & Technical**: Avoid marketing language; focus on implementation details.
- **Cross-Link**: Always link to related tools, playbooks, or architectural docs.
- **One canonical page per tool/framework/provider**: All mentions elsewhere must link to the canonical page.
- **Use templates**: [Tool template](templates/tool_template.md) for tools/frameworks/providers. [Article template](templates/article_template.md) for papers and articles.
- **No stub pages**: Only create a page if you have enough information to fill the template meaningfully.
- **JSON Metadata**: If adding a tool, ensure you also update `data/all_tools.json`.

## Multi-Agent KnowledgeOps Contract (Mandatory)

For AI-authored documentation updates, this contract is required:

1. **Deduplicate first**: Search for existing tool/topic pages and aliases before creating new files.
2. **Keep canonical ownership**: Update the existing canonical page whenever possible.
3. **Use the right template and taxonomy**: Follow [tool template](templates/tool_template.md), [article template](templates/article_template.md), and [standards](standards.md).
4. **Add auditable metadata** on every AI-authored knowledge-page update:
   - `Last reviewed` in `YYYY-MM-DD`
   - `Confidence` as `high`, `medium`, or `low`
   - `Sources / References` with at least one URL
5. **Keep PR intent narrow**: Intake, curation, or audit work should be separate PRs whenever possible.

See [Multi-Agent KnowledgeOps Governance](architecture/multi_agent_knowledgeops.md) for the full operating model.

## AI PR Checklist

Before requesting review, AI-authored PRs must satisfy:

- [ ] Canonical page search completed (name + aliases)
- [ ] No duplicate canonical pages introduced
- [ ] Correct template and taxonomy used
- [ ] Required metadata added (`Last reviewed`, `Confidence`, `Sources / References`)
- [ ] At least one high-signal source URL included
- [ ] `data/all_tools.json` and `mkdocs.yml` updated when applicable
- [ ] `audit_docs_quality.py` and `check_docs_contract.py` pass with 100% compliance

---
*Every contribution helps make this hub a better operating manual for everyone.*

## Sources / References
- [Automated Contributions](architecture/automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](architecture/multi_agent_knowledgeops.md)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Ralph-loop Execution Reports](reports/)

## Related
- [Home](index.md)
- [Automated Contributions](architecture/automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](architecture/multi_agent_knowledgeops.md)
- [Jules Agent](tools/ai_knowledge/jules.md)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
