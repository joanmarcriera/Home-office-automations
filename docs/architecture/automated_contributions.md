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
