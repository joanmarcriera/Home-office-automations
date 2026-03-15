# Automated Contribution System (Google Jules)

This document describes how to set up and manage the automated contribution system using **Google Jules**.

## System Overview
The system allows the repository to self-improve through a staged automation pipeline:

1. scheduled workflows collect and summarize sources,
2. a bridge stages candidates into intake logs,
3. control issues are opened for Jules,
4. Jules opens PRs,
5. quality gates run,
6. passing changes merge directly or through the weekly automation rollup.

## Setup Instructions

### 1. Authorize the Jules GitHub App
- Visit [Jules Google](https://jules.google.com/) and sign in.
- Connect your GitHub account and authorize the Jules app for this repository.

### 2. Configure Issue-Based Triggering
- Jules natively supports triggering from issues with the label `jules`.
- Ensure the label `jules` (case-insensitive) is created in the repository.

### 3. Scheduled Tasks Configuration
The repository now uses multiple workflows rather than one watcher:

- `.github/workflows/daily-digest.yml` generates the daily digest content
- `.github/workflows/digest-to-intake.yml` stages qualifying sources into `docs/new-sources/`
- `.github/workflows/daily-jules-maintenance.yml` opens maintenance issues for Jules after intake staging
- `.github/workflows/daily-jules-knowledge.yml` opens knowledge-expansion issues
- `.github/workflows/process-jules-backlog.yml` opens backlog-processing control issues when queued Jules issues accumulate
- `.github/workflows/jules-auto-merge.yml` merges passing Jules PRs
- `.github/workflows/weekly-automation-rollup-merge.yml` merges the shared automation rollup PR

### 4. Issue Routing Logic
The repository also has an issue router:

- `.github/workflows/issue-automation-router.yml` labels ordinary issues for the correct automation lane
- default route is `jules`
- explicit autofix requests can be routed to the `autofix` lane instead

### 2. Manual Triggering
You can also manually trigger Jules by adding the `jules` label to any issue.

## Task Lifecycle
1.  **Discovery / staging**: digest and bridge workflows update repository-maintenance artifacts and intake logs.
2.  **Issue creation**: a control workflow opens a `jules` issue for the next unit of work.
3.  **Execution**: Jules analyzes the issue, makes changes, and opens a PR.
4.  **Validation**: docs, catalog, intake, link, and generated-content gates run on the PR.
5.  **Merge**: passing Jules PRs auto-merge; shared automation changes can accumulate on `automation/weekly-rollup` and merge through the weekly rollup workflow.
6.  **Next cycle**: `jules-pipeline-trigger.yml` triggers the next issue-creation cycle after a Jules PR merge.

## Best Practices for "Improvement" Issues
To help Jules improve the content effectively, use structured prompts in the issue description:
- **Refactoring**: "Refactor docs/tools/X to follow the new template. Ensure all links are updated."
- **Data Entry**: "Update data/all_tools.json with the latest version numbers for the tools in Intake & Storage."
- **Search & Research**: "Research Tool Y and create a documentation page in docs/tools/process_understanding/."

---

## Daily Maintenance Job

A scheduled GitHub Actions workflow (`.github/workflows/daily-jules-maintenance.yml`) opens maintenance issues twice a day. The morning run happens after the digest-to-intake bridge so intake rows are present before Jules starts the maintenance pass.

### What it does (in priority order)

The prompt instructs Jules to stop at the first step that produces meaningful work:

1. **Process the intake queue** — finds all `new` rows in daily logs under `docs/new-sources/YYYY-MM-DD.md` (indexed by `docs/new-sources.md`), deduplicates against existing pages, creates canonical docs using the correct template, updates `data/all_tools.json` and `mkdocs.yml` nav, and marks rows `integrated`
2. **Doc quality audit** (if queue is empty) — finds up to 3 tool docs missing required sections and adds placeholder content tagged `<!-- needs-content -->`
3. **Broken internal links** (if steps 1 & 2 found nothing) — scans `docs/` for dead internal links and fixes or removes them (up to 10 per run)

Daily intake files are validated by `scripts/validate_new_sources.py` and the `Intake Quality Gates` workflow.

Jules opens a PR after completing whichever step had work. If the work lands through the shared automation rollup branch, the weekly rollup merge workflow handles final integration.

## Working flow summary

```mermaid
flowchart LR
    A["Daily digest"] --> B["Digest-to-intake bridge"]
    B --> C["docs/new-sources/"]
    C --> D["Daily Jules Maintenance issue"]
    D --> E["Jules PR or automation rollup PR"]
    E --> F["Quality gates"]
    F --> G["Main branch or auto-merge queue"]
```

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
- [Digest to Intake Bridge Workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/digest-to-intake.yml)
- [Jules Auto-Merge Workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/jules-auto-merge.yml)
- [Weekly Automation Rollup Merge Workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/weekly-automation-rollup-merge.yml)

## Related

- [Home](../index.md)
- [Multi-Agent KnowledgeOps Governance](multi_agent_knowledgeops.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Contribution Metadata

- Last reviewed: 2026-03-15
- Confidence: high
