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
To run Jules in scheduled mode (e.g., several times each day to pick up new issues):
- **GitHub Action**: Create a workflow that uses a cron schedule.
- **CLI Interaction**: Use `jules-tools` (npm) in the action to list and assign tasks.

#### Example GitHub Action (`.github/workflows/scheduled-jules.yml`):
```yaml
name: Scheduled Jules Maintenance
on:
  schedule:
    - cron: '0 0,8,16 * * *' # Runs 3 times a day (00:00, 08:00, 16:00 UTC)
  workflow_dispatch:

jobs:
  run-jules:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Run Jules Tasks
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: |
          # Use GH CLI to find issues with label 'jules' and no assignee
          ISSUES=$(gh issue list --label "jules" --json number,title --jq '.[] | "\(.number): \(.title)"')

          if [ -z "$ISSUES" ]; then
            echo "No new Jules tasks found."
            exit 0
          fi

          echo "Processing issues: $ISSUES"
          # Automation logic to pipe to jules-tools would go here
```

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
