# Automated Contribution System (Google Jules)

The Automated Contribution System is a staged automation pipeline that enables the repository to self-improve. As of July 21, 2026, it has been fully integrated with **MCP 3.0** and **Gemma 3**, allowing for autonomous knowledge expansion and technical freshness audits with high precision.

## What it is
The Automated Contribution System is a staged automation pipeline that enables the repository to self-improve. It uses **Google Jules** as the core agent to analyze issues, perform research, update documentation, and submit pull requests. The system is designed to handle routine maintenance, knowledge expansion, and data synchronization tasks with minimal human intervention.

## What problem it solves
Maintaining a large knowledge base of rapidly evolving AI tools and services is manually intensive. This system automates the collection of new sources, the auditing of documentation quality, the fixing of broken links, and the integration of new information into the canonical repository structure. It ensures the repository stays up-to-date while maintaining high standards for documentation quality.

## Where it fits in the stack
It is a **Meta-Automation Service** that sits on top of the repository's content. It leverages GitHub Actions for scheduling and orchestration, Google Jules for intelligent execution, and a suite of validation scripts (KnowledgeOps) to ensure all changes comply with repository standards. It is the primary engine for the "Ralph-loop" maintenance cycle.

## Typical use cases
- **Intake Processing**: Automatically creating documentation pages from new source logs.
- **Documentation Deepening**: Identifying shallow pages and adding missing technical details or examples using **Gemma 3**.
- **Link Maintenance**: Auditing and fixing broken internal or external markdown links.
- **Data Synchronization**: Keeping `data/all_tools.json` and navigation in `mkdocs.yml` in sync with the filesystem.

## Strengths
- **Consistency**: Ensures all documentation follows the same mandatory structure and metadata requirements.
- **Efficiency**: Processes high volumes of routine updates faster than human contributors.
- **Traceability**: Every automated change is backed by an issue and a PR, with full quality gate logs.
- **MCP 3.0 Native**: Leverages the latest Model Context Protocol for tool-calling and resource access.

## Limitations
- **Reasoning Depth**: While excellent for structured tasks, it may struggle with complex architectural decisions requiring deep human-centric context.
- **Review Dependency**: Final quality still benefits from human oversight, especially for nuanced technical "Strengths" or "Limitations".
- **API Dependency**: Relies on the availability and performance of the Google Jules agent and GitHub APIs.

## When to use it
- For routine documentation updates and maintenance tasks.
- When ingesting large batches of new tools or services from external feeds.
- To perform repository-wide audits and bulk formatting fixes.

## When not to use it
- For high-stakes architectural changes that redefine the core purpose of the stack.
- When precise, human-verified personal experience is the primary value of a documentation page.

## Getting started

### 1. Authorize the Jules GitHub App
- Visit [Jules Google](https://jules.google.com/) and sign in.
- Connect your GitHub account and authorize the Jules app for this repository.

### 2. Configure Issue-Based Triggering
- Jules natively supports triggering from issues with the label `jules`.
- Ensure the label `jules` (case-insensitive) is created in the repository.

### 3. Scheduled Tasks Configuration
The repository uses multiple workflows for different automation lanes:
- `.github/workflows/daily-digest.yml`: Collects new sources.
- `.github/workflows/daily-jules-maintenance.yml`: Triggers routine cleanup and intake processing.
- `.github/workflows/daily-jules-knowledge.yml`: Triggers deep-dives into specific topics.

## CLI examples
While primarily managed via GitHub, you can trigger specific automation scripts locally for testing:

```bash
# Validate new sources logs
python3 scripts/validate_new_sources.py

# Run a documentation quality audit
python3 scripts/audit_docs_quality.py

# Check catalog consistency (mkdocs.yml vs filesystem)
python3 scripts/check_catalog_consistency.py
```

## API examples
The system interacts with the Jules API and GitHub API to manage contributions. Below is a conceptual example of a Jules-powered contribution script:

```python
import jules
from jules.core import Agent

# Initialize the Jules agent for KnowledgeOps
agent = Agent(role="Documentation Engineer", model="gemma-3-27b")

# Analyze an issue and propose a documentation update
issue_content = jules.get_issue("repo/name", issue_id=123)
audit_results = jules.run_script("scripts/audit_docs_quality.py", target="docs/tools/example.md")

if not audit_results.is_compliant:
    proposal = agent.reason(f"Fix the following audit issues: {audit_results.issues}")
    jules.submit_pr(branch="fix-docs-123", changes=proposal)
```

## Related tools / concepts
- [Multi-Agent KnowledgeOps Governance](multi_agent_knowledgeops.md)
- [Jules Agent](../tools/ai_knowledge/jules.md)
- [KnowledgeOps Standards](../standards.md)
- [Local LLMs (Gemma 3)](../tools/ai_knowledge/local_llms.md)
- [Model Context Protocol](../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Agentic Session Orchestration](../knowledge_base/agent_protocols.md)
- [Data Copilot Architecture](data-copilot-text-to-sql.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Sources / references
- [Jules Official](https://jules.google/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Daily Jules Maintenance Workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/daily-jules-maintenance.yml)
- [MCP 3.0 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
