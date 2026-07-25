# Jules Weekly Gap Analysis Prompt

## What it is
The "Jules Weekly Gap Analysis" is a structured LLM prompt and automated workflow pattern used to analyze failure patterns in [n8n](../../services/n8n.md) automation logs and propose concrete improvements to the repository's documentation or workflows. It leverages deep reasoning models to identify the underlying "why" behind recurring issues.

As of late August 2026, this prompt is the standard tool for the [Ralph-loop](../../tools/ai_knowledge/jules.md#orchestration-patterns-the-ralph-loop) to maintain system health and robustness across multi-agent environments.

## What problem it solves
Automation stacks often suffer from "silent decay" where small API changes, network timeouts, or unhandled data edge cases lead to recurring but non-critical failures. This prompt automates the root cause analysis and suggests specific fixes, ensuring the system remains resilient and well-documented without requiring constant manual monitoring.

## Where it fits in the stack
This prompt is part of the **Maintenance & Governance Layer**. It consumes data from the [n8n Log Aggregator](../../scripts/n8n_log_aggregator.py) and generates actionable PRs for the **DevOps** ([Jules](../../tools/ai_knowledge/jules.md)) layer.

## Typical use cases
- **Weekly Reliability Review**: Running the analysis every Sunday to identify top bottlenecks and regressions.
- **Post-Migration Audit**: Analyzing logs after a major service update (e.g., migrating to [Prowlarr](../../services/prowlarr.md)) to catch integration gaps.
- **Documentation Backfill**: Identifying when a "401 Unauthorized" or "404 Not Found" error indicates a gap in the setup instructions for a specific service.
- **Tool-Use Optimization**: Identifying nodes that could be replaced by **Model Context Protocol (MCP)** servers for better reliability.

## Strengths
- **Data-Driven**: Improvements are based on actual execution logs, not just theoretical gaps or anecdotal evidence.
- **Actionable Output**: Designed to be fed directly into an [Automation Improvement PR](../../.github/PULL_REQUEST_TEMPLATE/automation_improvement.md).
- **Proactive Maintenance**: Identifies patterns and trends before they become critical system-wide failures.
- **Reasoning-Aware**: Optimized for **Claude 5.1** and **GPT-5.5** to perform deep chain-of-thought root cause analysis.

## Limitations
- **Log Dependency**: Reliability is strictly dependent on the quality and verbosity of error messages provided by n8n nodes.
- **Volume Sensitivity**: Requires a representative sample of logs (ideally 24h to 168h) to distinguish between transient glitches and meaningful patterns.
- **Manual Verification**: AI-suggested workflow fixes still require human verification (HITL) before deployment in high-risk production environments.

## When to use it
- When you have more than 5 active n8n workflows and want to maintain a "High Confidence" stack.
- After integrating a new service, API, or hardware node to monitor for early "teething" problems.
- As a mandatory part of a regular maintenance sprint or "KnowledgeOps" audit.

## When not to use it
- For trivial stacks with only 1-2 simple workflows where manual monitoring is faster.
- If you don't have API access or the required permissions to export your n8n instance's execution logs.
- During an active "incident" (use real-time debugging tools instead).

## Getting started

### 1. Data Collection
Run the log aggregator script to gather execution data for the last week.
```bash
python3 scripts/n8n_log_aggregator.py --hours 168 > logs_summary.txt
```

### 2. Analysis
Feed the contents of `logs_summary.txt` into this prompt using a reasoning-capable model (e.g., **Claude 5.1**).

### 3. Implementation
Review the proposed fixes and execute them using the [Automation PR Template](../../.github/PULL_REQUEST_TEMPLATE/automation_improvement.md).

## CLI examples
The analysis process is managed via the command line and LLM interfaces.

```bash
# Aggregate logs for the last 24 hours
python3 scripts/n8n_log_aggregator.py --hours 24 --filter "status=error"

# Generate a report for a specific workflow ID
python3 scripts/n8n_log_aggregator.py --workflow-id "AbC123XyZ" > workflow_logs.txt

# Run a dry-run analysis using a local Llama 4 Maverick instance
ollama run llama-4-maverick "$(cat jules_prompt.txt) $(cat workflow_logs.txt)"
```

## API examples
The prompt uses a template structure designed for high-context windows.

### Prompt Template
```text
Role: Senior Automation Engineer (Jules)
Task: Analyze n8n failure patterns and propose improvements using deep reasoning.

Context:
- Current Date: Late August 2026
- Standards: High Confidence Documentation (13-section contract)
- Models: Claude 5.1 / GPT-5.5 / Llama 4 Maverick / Qwen 3.6

Data provided:
{{LOG_AGGREGATOR_OUTPUT}}

Analyze the top 3 failure patterns:
1. For each pattern, identify the likely root cause (API change, timeout, data validation error, credential expiry).
2. Use Chain-of-Thought reasoning to verify if the pattern is a regression or a new gap.
3. Propose a specific "Action A" (Do the work) or "Action C" (Decompose) for this repository.
4. If the fix involves documentation, specify which file in `docs/` needs updating and what content to add.
5. If the fix involves a workflow change, describe the node-level adjustment needed (e.g., switching to an MCP 3.1-based tool).

Response Format:
- **Pattern 1**: [Description]
  - **Root Cause**: [Analysis]
  - **Proposed Fix**: [Specific steps]
  - **Affected Files**: [File paths]
...
- **General Recommendation**: [One meta-improvement for the automation stack]
```

### Programmatic Integration with MCP 3.1
The following script demonstrates how an automated agent fetches these logs and issues an analysis payload via MCP 3.1:

```python
import json
import urllib.request

def run_mcp_gap_analysis(logs_data: str):
    url = "http://localhost:8000/tools/v1/jules-gap-analysis"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "claude-5.1",
        "parameters": {
            "temperature": 0.0,
            "logs_summary": logs_data
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    with urllib.request.urlopen(req) as res:
        response_data = json.loads(res.read().decode('utf-8'))
        print("Analysis completed successfully.")
        return response_data["analysis"]
```

## Related tools / concepts
- [n8n](../../services/n8n.md): The automation platform being monitored.
- [n8n Log Aggregator](../../scripts/n8n_log_aggregator.py): The primary data source for this prompt.
- [Automation PR Template](../../.github/PULL_REQUEST_TEMPLATE/automation_improvement.md): The output format for improvements.
- [KnowledgeOps](../../knowledge_base/patterns/knowledge-ops.md): The broader framework for repository-driven automation maintenance.
- [Error Handling Patterns](../../services/n8n.md#3-error-handling): The foundational n8n patterns this analysis helps enforce.
- [Jules](../../tools/ai_knowledge/jules.md): The AI agent persona executing the analysis.
- [Claude Code](../../tools/development_ops/claude-code.md): The environment where Jules executes these tasks.
- [MCP](../../tools/automation_orchestration/mcp.md): Used to extend n8n capabilities and improve reliability.
- [Claude 5.1](../../tools/providers/anthropic.md): The recommended model for running this complex analysis.

## Sources / references
- [n8n API Documentation - Execution Logs](https://docs.n8n.io/api/v1/executions/)
- [Jules Report Automation (Batch 42.4)](../../reports/task-decomposition-batch-42.md#sub-batch-424-jules-report-automation-high-effort)
- [Model Context Protocol (MCP) in n8n Workflows](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.mcp/)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
