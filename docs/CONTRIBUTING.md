# Contributing to the AI Hub

Thank you for your interest in improving the Home-Office Automation & AI Hub! We welcome contributions from both humans and AI agents.

## How You Can Help
- **Add New Tools**: Found a tool that fits the stack? Document it using our [standard template](/templates/tool_template/).
- **Refine Playbooks**: Improve our existing automation guides with more technical detail or new variants.
- **Update Services**: Ensure the documentation for self-hosted services remains accurate as versions change.
- **Improve Prompts**: Optimize our LLM prompt templates for better extraction and classification results.

## Automated Contributions via Google Jules
This repository uses **Google Jules**, an autonomous AI coding agent, to help with maintenance and feature development.

### Daily Ingestion Job
Jules runs a **scheduled daily job** that:

1. **Scans** high-signal sources (Hacker News, Reddit, arXiv, GitHub Trending, engineering blogs, etc.)
2. **Stages** qualifying items in daily logs under [`docs/new-sources/`](/new-sources/) with title, URL, tags, and status
3. **Integrates** staged items into canonical pages or creates new pages using the [tool template](/templates/tool_template/) or [article template](/templates/article_template/)
4. **Deduplicates** against existing content before adding anything

### Assigning a Task to Jules
You can request Jules to perform a task by:
1.  **Opening an Issue**: Describe the task clearly (e.g., "Add documentation for Tool X" or "Fix broken link in README").
2.  **Adding the Label**: Apply the label `jules` (case-insensitive) to the issue.
3.  **Review the Plan**: Jules will analyze the task and post a plan as a comment. Once you approve, Jules will get to work.
4.  **Review the PR**: Jules will open a Pull Request with its changes for your final review.

## Contribution Standards
- **Precise & Technical**: Avoid marketing language; focus on implementation details.
- **Cross-Link**: Always link to related tools, playbooks, or architectural docs.
- **One canonical page per tool/framework/provider**: All mentions elsewhere must link to the canonical page.
- **Use templates**: [Tool template](/templates/tool_template/) for tools/frameworks/providers. [Article template](/templates/article_template/) for papers and articles.
- **No stub pages**: Only create a page if you have enough information to fill the template meaningfully.
- **JSON Metadata**: If adding a tool, ensure you also update `data/all_tools.json`.

## Multi-Agent KnowledgeOps Contract (Mandatory)

For AI-authored documentation updates, this contract is required:

1. **Deduplicate first**: Search for existing tool/topic pages and aliases before creating new files.
2. **Keep canonical ownership**: Update the existing canonical page whenever possible.
3. **Use the right template and taxonomy**: Follow [tool template](/templates/tool_template/), [article template](/templates/article_template/), and [standards](/standards/).
4. **Add auditable metadata** on every AI-authored knowledge-page update:
   - `Last reviewed` in `YYYY-MM-DD`
   - `Confidence` as `high`, `medium`, or `low`
   - `Sources / References` with at least one URL
5. **Keep PR intent narrow**: Intake, curation, or audit work should be separate PRs whenever possible.

See [Multi-Agent KnowledgeOps Governance](/architecture/multi_agent_knowledgeops/) for the full operating model.

## AI PR Checklist

Before requesting review, AI-authored PRs must satisfy:

- [ ] Canonical page search completed (name + aliases)
- [ ] No duplicate canonical pages introduced
- [ ] Correct template and taxonomy used
- [ ] Required metadata added (`Last reviewed`, `Confidence`, `Sources / References`)
- [ ] At least one high-signal source URL included
- [ ] `data/all_tools.json` and `mkdocs.yml` updated when applicable

---
*Every contribution helps make this hub a better operating manual for everyone.*
