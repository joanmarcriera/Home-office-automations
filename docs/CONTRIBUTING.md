# Contributing to the AI Hub

Thank you for your interest in improving the Home-Office Automation & AI Hub! We welcome contributions from both humans and AI agents.

## How You Can Help
- **Add New Tools**: Found a tool that fits the stack? Document it using our [standard template](templates/tool_template.md).
- **Refine Playbooks**: Improve our existing automation guides with more technical detail or new variants.
- **Update Services**: Ensure the documentation for self-hosted services remains accurate as versions change.
- **Improve Prompts**: Optimize our LLM prompt templates for better extraction and classification results.

## Automated Contributions via Google Jules
This repository uses **Google Jules**, an autonomous AI coding agent, to help with maintenance and feature development.

### Assigning a Task to Jules
You can request Jules to perform a task by:
1.  **Opening an Issue**: Describe the task clearly (e.g., "Add documentation for Tool X" or "Fix broken link in README").
2.  **Adding the Label**: Apply the label `jules` (case-insensitive) to the issue.
3.  **Review the Plan**: Jules will analyze the task and post a plan as a comment. Once you approve, Jules will get to work.
4.  **Review the PR**: Jules will open a Pull Request with its changes for your final review.

## Contribution Standards
- **Precise & Technical**: Avoid marketing language; focus on implementation details.
- **Cross-Link**: Always link to related tools, playbooks, or architectural docs.
- **JSON Metadata**: If adding a tool, ensure you also update `data/all_tools.json`.

---
*Every contribution helps make this hub a better operating manual for everyone.*
