# Jules Weekly Gap Analysis Prompt

## What it is
The "Jules Weekly Gap Analysis" is a structured LLM prompt used to analyze failure patterns in [n8n](../../services/n8n.md) automation logs and propose concrete improvements to the repository's documentation or workflows.

## What problem it solves
Automation stacks often suffer from "silent decay" where small API changes or unhandled edge cases lead to recurring failures. This prompt automates the root cause analysis and suggests specific fixes, ensuring the system remains resilient and well-documented.

## Where it fits in the stack
This prompt is part of the **Maintenance & Governance** layer. It consumes data from the [n8n Log Aggregator](../../scripts/n8n_log_aggregator.py) and generates actionable PRs for the **DevOps** ([Jules](../../tools/ai_knowledge/jules.md)) layer.

## Typical use cases
- **Weekly Reliability Review**: Running the analysis every Sunday to identify top bottlenecks.
- **Post-Migration Audit**: Analyzing logs after a major service update (e.g., migrating to [Prowlarr](../../services/prowlarr.md)) to catch integration gaps.
- **Documentation Backfill**: Automatically identifying when a "401 Unauthorized" or "404 Not Found" error indicates a gap in the setup instructions for a service.
- **Tool-Use Optimization**: Identifying nodes that could be replaced by [MCP](../../tools/automation_orchestration/mcp.md) servers for better reliability.

## Strengths
- **Data-Driven**: Improvements are based on actual execution logs, not just theoretical gaps.
- **Actionable**: Output is designed to be fed directly into an [Automation Improvement PR](../../.github/PULL_REQUEST_TEMPLATE/automation_improvement.md).
- **Proactive**: Identifies patterns before they become critical failures.
- **Reasoning-Aware**: Optimized for [Claude 4.8](../../tools/providers/anthropic.md) and [GPT-5.5](../../tools/ai_knowledge/openai.md) to perform deep root cause analysis.

## Limitations
- **Log Dependency**: Relies on the quality of error messages provided by n8n nodes.
- **Volume Sensitivity**: Requires a representative sample of logs (ideally 24h-168h) to identify meaningful patterns.
- **Manual Verification**: AI-suggested workflow fixes still require human verification before deployment in high-risk environments.

## When to use it
- When you have more than 5 active n8n workflows and want to maintain a "High Confidence" stack.
- After integrating a new service or API to monitor for "teething" problems.
- As part of a regular maintenance sprint ([Ralph-loop](../../tools/ai_knowledge/jules.md#orchestration-patterns-the-ralph-loop)).

## When not to use it
- For trivial stacks with only 1-2 simple workflows.
- If you don't have API access to your n8n instance's execution logs.

## Related tools / concepts
- [n8n](../../services/n8n.md): The automation platform being monitored.
- [n8n Log Aggregator](../../scripts/n8n_log_aggregator.py): The data source for this prompt.
- [Automation PR Template](../../.github/PULL_REQUEST_TEMPLATE/automation_improvement.md): The output format for improvements.
- [KnowledgeOps](../../knowledge_base/patterns/knowledge-ops.md): The broader framework for repository-driven automation maintenance.
- [Error Handling Patterns](../../services/n8n.md#3-error-handling): The foundational n8n patterns this analysis helps enforce.
- [Jules](../../tools/ai_knowledge/jules.md): The AI agent persona executing the analysis.
- [Claude Code](../../tools/development_ops/claude-code.md): The environment where Jules executes these tasks.
- [MCP](../../tools/automation_orchestration/mcp.md): Used to extend n8n capabilities.
- [Claude 4.8](../../tools/providers/anthropic.md): The recommended model for running this analysis.

## Prompt Template
```text
Role: Senior Automation Engineer (Jules)
Task: Analyze n8n failure patterns and propose improvements using deep reasoning.

Context:
- Current Date: June 2026
- Standards: High Confidence Documentation (10+ headers, 7+ links)
- Models: Claude 4.8 / GPT-5.5 / Llama 4 Maverick

Data provided:
{{LOG_AGGREGATOR_OUTPUT}}

Analyze the top 3 failure patterns:
1. For each pattern, identify the likely root cause (API change, timeout, data validation error, credential expiry).
2. Use Chain-of-Thought reasoning to verify if the pattern is a regression or a new gap.
3. Propose a specific "Action A" (Do the work) or "Action C" (Decompose) for this repository.
4. If the fix involves documentation, specify which file in `docs/` needs updating and what content to add.
5. If the fix involves a workflow change, describe the node-level adjustment needed (e.g., switching to an MCP-based tool).

Response Format:
- **Pattern 1**: [Description]
  - **Root Cause**: [Analysis]
  - **Proposed Fix**: [Specific steps]
  - **Affected Files**: [File paths]
- **Pattern 2**: ...
...
- **General Recommendation**: [One meta-improvement for the automation stack]
```

## How to use
1. Run `python3 scripts/n8n_log_aggregator.py --hours 168 > logs_summary.txt`.
2. Feed the contents of `logs_summary.txt` into this prompt using a reasoning-capable model (e.g., Claude 4.8 Opus).
3. Execute the proposed PRs using the [Automation PR Template](../../.github/PULL_REQUEST_TEMPLATE/automation_improvement.md).

## Sources / References
- [n8n API Documentation](https://docs.n8n.io/api/)
- [Jules Report Automation (Batch 42.4)](../../reports/task-decomposition-batch-42.md#sub-batch-424-jules-report-automation-high-effort)
- [Prometheus n8n Exporter Patterns](../../services/n8n.md#2-slo-dashboard-prometheusgrafana)
- [Model Context Protocol (MCP) in n8n](../../services/n8n.md#mcp-integration)

---
## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
