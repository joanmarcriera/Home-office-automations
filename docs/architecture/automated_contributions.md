# Automated Contribution System (Google Jules)

This document describes how to set up and manage the automated contribution system using **Google Jules**.

## System Overview
The system allows the repository to self-improve by assigning tasks to the Jules coding agent via GitHub issues. A scheduled automation ensures that Jules periodically checks for new tasks and executes them.

## Setup Instructions

### 1. Authorize the Jules GitHub App
- Visit [Jules Google](https://jules.google.com/) and sign in.
- Connect your GitHub account and authorize the Jules app for this repository.

### 2. Configure Issue-Based Triggering
- Jules natively supports triggering from issues with the label `jules`.
- Ensure the label `jules` (case-insensitive) is created in the repository.

### 3. Scheduled Tasks Configuration
The repository utilizes an autonomous watcher (`.github/workflows/scheduled-jules.yml`) that runs periodically to find new tasks.

### 1. Issue Watcher Logic
The watcher searches for any open issues mentioning "jules" that do not yet have the `jules` label.
- **Labeling**: It automatically adds the `jules` label to trigger the agent.
- **Default Intent**: If no specific action verbs (e.g., "refactor", "fix", "add") are found in the issue, it assumes the issue provides new information to be organized. In this case, it adds a guiding comment for Jules.

### 2. Manual Triggering
You can also manually trigger Jules by adding the `jules` label to any issue.

## Task Lifecycle
1.  **Discovery**: Human or script adds `jules` label to an issue.
2.  **Planning**: Jules analyzes the issue and codebase context, then posts a Markdown plan.
3.  **Approval**: A maintainer approves the plan via a comment.
4.  **Execution**: Jules clones the repo in a secure VM, applies changes, and runs tests.
5.  **Submission**: Jules opens a Pull Request for review.

## Best Practices for "Improvement" Issues
To help Jules improve the content effectively, use structured prompts in the issue description:
- **Refactoring**: "Refactor docs/tools/X to follow the new template. Ensure all links are updated."
- **Data Entry**: "Update data/all_tools.json with the latest version numbers for the tools in Intake & Storage."
- **Search & Research**: "Research Tool Y and create a documentation page in docs/tools/process_understanding/."

---

## Daily Maintenance Job

A scheduled GitHub Actions workflow (`.github/workflows/daily-jules-maintenance.yml`) opens one maintenance issue per day at **07:00 UTC** and immediately applies the `jules` label. Jules picks it up automatically.

### What it does (in priority order)

The prompt instructs Jules to stop at the first step that produces meaningful work:

1. **Process the intake queue** — finds all `new` rows in daily logs under `docs/new-sources/YYYY-MM-DD.md` (indexed by `docs/new-sources.md`), deduplicates against existing pages, creates canonical docs using the correct template, updates `data/all_tools.json` and `mkdocs.yml` nav, and marks rows `integrated`
2. **Doc quality audit** (if queue is empty) — finds up to 3 tool docs missing required sections and adds placeholder content tagged `<!-- needs-content -->`
3. **Broken internal links** (if steps 1 & 2 found nothing) — scans `docs/` for dead internal links and fixes or removes them (up to 10 per run)

Daily intake files are validated by `scripts/validate_new_sources.py` and the `Intake Quality Gates` workflow.

Jules opens a PR titled `chore: daily maintenance YYYY-MM-DD` after completing whichever step had work.

### Free tier cost
~30 seconds per run × 30 days = **~15 minutes/month** of GitHub Actions time.

### How to pause it
- **One day**: Close the issue Jules created — it won't reopen until the next day's cron
- **Indefinitely**: Disable the workflow in GitHub → Actions → Daily Jules Maintenance → Disable workflow

### Reviewing Jules' PRs
The first time Jules runs, review the PR carefully to confirm it follows the templates and taxonomy. Jules self-corrects based on feedback left in PR comments.

## Sources / References

- [Jules](https://jules.google/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Daily Jules Maintenance Workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/daily-jules-maintenance.yml)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: high
