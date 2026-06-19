# Contributing to the AI Hub

Thank you for your interest in improving the Home-Office Automation & AI Hub! We welcome contributions from both humans and AI agents. In 2026, this repository operates as a semi-autonomous knowledge graph managed by the Ralph-loop.

## LLM Agent Quick Start

Before changing files, agents must read these in order to maintain the "High Confidence" standard:

1. [AGENTS.md](../AGENTS.md) — Repository operating contract, checklists, and quality bar.
2. [skills.md](../skills.md) — Reusable task patterns for intake, docs updates, and branch hygiene.
3. [Standards](standards.md) — Taxonomy and canonical-page rules.

**The Golden Sequence:**
1. **Search**: Find the canonical page or confirm it does not exist using name and aliases.
2. **Scope**: Make scoped edits for one intent only (e.g., technical audit OR metadata update).
3. **Validate**: Run `audit_docs_quality.py` and `check_docs_contract.py`.
4. **Submit**: Open PR only after all automated quality gates pass.

## How You Can Help
- **Add New Tools**: Document new tools in the AI/Automation stack using the [standard template](templates/tool_template.md).
- **Refine Playbooks**: Improve existing guides with June 2026 technical context (e.g., Claude 4.8 / GPT-5.5 patterns).
- **Update Services**: Ensure self-hosted service documentation reflects current stable versions and MCP 3.0 integrations.
- **Audit Freshness**: Help us move "Stale" or "Shallow" documents to the "High Confidence" (13-section) standard.

## Automated Contributions: The Ralph-loop

This repository implements the **Ralph-loop**, a systematic directive for AI agents (primarily **Google Jules**) to close issues by performing one of three actions:

a) **Do the work**: Implement the requested feature, technical audit, or bug fix.
b) **Add links**: Find the appropriate canonical location for provided external links.
c) **Decompose**: Divide complex tasks into smaller, trackable issues with extracted context.

### Daily Ingestion & Maintenance Lanes
Automation is split into specialized lanes to maintain the "High Confidence" standard:
1. **Daily Digest**: Scans and summarizes external sources (GitHub, Reddit, News).
2. **Intake Bridge**: Stages qualifying items in [`docs/new-sources/`](new-sources.md).
3. **Maintenance Run**: Automates routine audits, broken link fixes, and catalog syncs.
4. **Knowledge Deepening**: Targets docs for 13-section technical expansion.
5. **Quality Gates**: Mandatory execution of `audit_docs_quality.py` and `check_docs_contract.py`.

## Multi-Agent KnowledgeOps Contract (Mandatory)

For AI-authored documentation updates, this contract is non-negotiable:

1. **Deduplicate first**: Search for existing tool/topic pages and aliases before creating new files.
2. **Keep canonical ownership**: Update the existing canonical page whenever possible.
3. **Use the right template and taxonomy**: Follow [tool template](templates/tool_template.md) and [standards](standards.md).
4. **Add auditable metadata** on every update:
   - `Last reviewed` in `YYYY-MM-DD`
   - `Confidence` as `high`, `medium`, or `low`
   - `Sources / References` with at least one high-signal URL.
5. **Keep PR intent narrow**: Audit work and feature work should be in separate PRs.

## AI PR Checklist

Before requesting review, AI-authored PRs must satisfy:

- [ ] Canonical page search completed (name + aliases)
- [ ] No duplicate canonical pages introduced
- [ ] Correct template and taxonomy used
- [ ] Required metadata added (`Last reviewed`, `Confidence`, `Sources / References`)
- [ ] At least one high-signal source URL included
- [ ] `data/all_tools.json` and `mkdocs.yml` updated when applicable
- [ ] `audit_docs_quality.py` and `check_docs_contract.py` pass with 100% compliance

## Related tools / concepts
- [Home](index.md)
- [Automated Contributions](architecture/automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](architecture/multi_agent_knowledgeops.md)
- [Jules Agent](tools/ai_knowledge/jules.md)
- [Standards and Conventions](standards.md)
- [Tool Template](templates/tool_template.md)
- [Article Template](templates/article_template.md)

## Sources / references
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Ralph-loop Execution Reports](reports/)
- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
