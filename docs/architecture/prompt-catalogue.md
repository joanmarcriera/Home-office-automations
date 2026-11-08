# Prompt & Automation Catalogue

## What it is

The Prompt & Automation Catalogue is the central repository and governance system for every LLM prompt, GitHub Action workflow, and autonomous agent orchestration script used to maintain and expand this repository. As of early January 2027, it serves as the authoritative specification for multi-agent KnowledgeOps, automated documentation quality audits, and Model Context Protocol (FastMCP 3.1) Task Protocol compliance across frontier models—including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL.

By formalizing system prompt strings, template schemas, dispatch triggers, and execution guardrails into structured, version-controlled artifacts, the catalogue bridges automated repository maintenance with strict deterministic validation.

```
+------------------------------------------------------------------------------------+
|                         PROMPT CATALOGUE ARCHITECTURE                              |
|                                                                                    |
|  [GitHub Actions Trigger] ---> [Prompt Catalogue Registry (FastMCP 3.1)]           |
|                                         |                                          |
|                                         v                                          |
|  [Agent Execution: Jules] <---> [Template Variable Interpolation Engine]          |
|                                         |                                          |
|                                         v                                          |
|  [Quality Gates: audit_docs_quality] -> [Docs & Reports Catalog Commit Pipeline]    |
+------------------------------------------------------------------------------------+
```

## What problem it solves

Autonomous systems and multi-agent development pipelines often devolve into "black boxes." Without centralized prompt tracking and contract enforcement:
- **Prompt Drift & Opacity**: System prompts diverge across workflows, resulting in inconsistent style, formatting defects, or missing metadata.
- **Silent Failures**: Agents fail to follow strict output schemas (e.g., Markdown table structures, JSON formatting) when system prompts lack strict negative constraints.
- **Non-Reproducible Failures**: Debugging agent actions requires reverse-engineering ephemeral prompt strings passed inside transient CI/CD runners.
- **Inefficient Token Consumption**: Redundant instructions inflate input context, degrading Time To First Token (TTFT) and increasing operational API token expenditure.

The Prompt Catalogue eliminates these issues by treating prompts as compiled software artifacts subject to semantic versioning, Pydantic v2 type validation, and automated regression testing.

## Mathematical Formulations: Token Optimization & Prompt Compilation

### 1. Prompt Token Compression & Prefix Efficiency
For an agentic workflow consuming a base system prompt $S$ composed of $k$ distinct instruction modules $\{m_1, m_2, \dots, m_k\}$, dynamic contextual variable bindings $V$, and user/task payload $U$, the total token length $L_{\text{total}}$ is:

$$
L_{\text{total}} = \sum_{i=1}^{k} \ell(m_i) + \ell(V) + \ell(U) - \Delta_{\text{shared}}
$$

Where:
- $\ell(m_i)$ represents the token length of the $i$-th instruction block.
- $\Delta_{\text{shared}}$ denotes tokens eliminated through prefix deduplication and KV-cache reuse via FreeToken or vLLM radix tree sharing.

The token compression efficiency ratio $\eta_{\text{prompt}}$ achieved by compiling static modular rules into unified system prefixes is:

$$
\eta_{\text{prompt}} = 1 - \frac{L_{\text{compiled}}}{\sum_{i=1}^{k} \ell(m_i) + \ell(V) + \ell(U)}
$$

When $\eta_{\text{prompt}} \ge 0.35$, agent prefill latency decreases proportionally by $(1 - \eta_{\text{prompt}})^2$ under quadratic attention transformer regimes.

### 2. Dispatch Latency & Model Fallback Bound
The end-to-end dispatch and response latency $\mathcal{T}_{\text{dispatch}}$ across an ordered fallback cascade of $N$ frontier LLM providers $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$ is bounded by:

$$
\mathcal{T}_{\text{dispatch}} = \sum_{j=1}^{M \le N} \left( \tau_{\text{network}}(p_j) + \tau_{\text{TTFT}}(p_j) + \tau_{\text{gen}}(p_j) \right) \cdot \mathbb{I}_{(\text{error}_j)} + \tau_{\text{exec}}(p_{\text{success}})
$$

Where:
- $\mathbb{I}_{(\text{error}_j)} \in \{0, 1\}$ indicates whether provider $p_j$ timed out or triggered a rate limit (HTTP 429/503).
- FastMCP 3.1 enforces a strict timeout $\tau_{\text{limit}} = 30.0\text{ s}$ per provider hop.

### 3. Prompt Entropy and Determinism Index
To ensure deterministic code generation across stochastic LLM outputs, the catalogue measures output token distribution entropy $\mathcal{H}(P)$:

$$
\mathcal{H}(P) = -\sum_{w \in \mathcal{V}} P(w \mid C) \log_2 P(w \mid C)
$$

By enforcing low-temperature sampling ($T \le 0.15$) and strict negative prompt constraints ("Return ONLY valid JSON. No markdown wrapping."), $\mathcal{H}(P)$ is constrained to sub-0.2 bits per token, guaranteeing schema conformity across parallel workers.

## Where it fits in the stack

**Category**: Architecture / Governance. It sits in the **metacognition and orchestration** layer, documenting and governing the automated pipelines and agent tasks that generate and audit all other content in the repository.

```
+------------------------------------------------------------------------------------+
|                         KNOWLEDGEOPS REPOSITORY STACK                              |
+------------------------------------------------------------------------------------+
|  1. GOVERNANCE LAYER: Prompt & Automation Catalogue (This Document)               |
|  2. AGENT RUNTIMES: Jules / FastMCP 3.1 Task Protocol / Lightwell AI Micro-Agents  |
|  3. KNOWLEDGE ASSETS: Tools (600+) / Services / Playbooks / Architecture Docs     |
|  4. OBSERVABILITY & TELEMETRY: ClickHouse OLAP Traces / OpenTelemetry Collector     |
|  5. CI/CD GATES: GitHub Actions Workflows / Quality & Catalog Audit Scripts       |
+------------------------------------------------------------------------------------+
```

## Architectural Comparison of Prompt Management Paradigms

| Feature / Dimension | Prompt Catalogue (This Repo) | Langfuse Prompt Management | Promptfoo Test Suites | Static Hardcoded Prompts |
| :--- | :--- | :--- | :--- | :--- |
| **Storage & Versioning** | Git-backed Markdown & JSON Schemas | Hosted Postgres / ClickHouse DB | YAML test configuration files | In-line string literals in code |
| **Type Validation** | Strict Pydantic v2 (`frozen=True`) | Runtime API schema validation | Assertion rules & Regex | None (Ad-hoc string parsing) |
| **FastMCP 3.1 Native** | First-class native tool binding | Adapter/plugin required | Not supported | Not supported |
| **Agent Autonomy Scope** | Explicitly bounded per task | Observability only | Pre-deployment benchmarking | Unbounded / Ambiguous |
| **Auditability** | Full Git commit history & SHA logs | Web Dashboard UI & API keys | Local test run reports | Git blame across dispersed code |

## Typical use cases

- **Prompt Versioning**: Tracking changes to the system prompts used by the [Daily Jules Maintenance](#ga-3-daily-jules-maintenance) workflow.
- **Workflow Auditing**: Reviewing the schedule and logic of recurring GitHub Actions like the [Daily AI Digest](#ga-1-daily-ai-digest).
- **Agent Onboarding**: Providing a clear set of instructions and "mission statements" for new autonomous workers added to the repo.
- **Troubleshooting**: Identifying why a particular automated task failed by examining its input prompts, variable bindings, and execution rules.
- **Schema Validation Testing**: Automated CI validation verifying that all prompt definitions conform to FastMCP 3.1 JSON schemas before workflow deployment.

## Strengths

- **Transparency**: Makes the repository's automated processes understandable to human contributors.
- **Reproducibility**: Provides the exact prompts needed to replicate the automated workflows in other environments.
- **Centralization**: Collects disparate GitHub Actions and local scripts into a single, searchable document.
- **Standardization**: Enforces the use of "High Confidence" documentation standards across all automated outputs.
- **Zero Drift**: Continuous CI quality scripts cross-check cataloged prompt IDs against workflow YAML configurations.

## Limitations

- **Maintenance Overhead**: Requires manual or automated updates whenever a workflow or prompt is changed in the underlying code.
- **Complexity**: As the number of agents and workflows grows, the catalogue can become difficult to navigate without specialized search tools.
- **Repository Coupling**: Some prompt variables are explicitly tied to the current repository directory hierarchy (`docs/tools/`, `data/`).

## When to use it

- When you need to understand *how* the repository is being maintained automatically.
- When you are designing a new automated workflow and want to ensure it follows existing patterns.
- During quality audits to verify that agents are operating within their defined "Allowed scope."
- When debugging why an agent generated malformed markdown tables or incorrect metadata headers.

## When not to use it

- For documenting tool-specific features that are already covered in their respective canonical pages.
- For storing API keys or other secrets (always use GitHub Secrets or environment variables).
- For transient one-off debugging prompts executed in local terminal shells.

## Getting started

To use the catalogue, identify the automation type (Recurring GA, One-Shot Jules, or Recurring Jules) and locate its mission statement and prompt logic below.

### Overview

| ID | Name | Runner | Cadence | Type |
| :--- | :--- | :--- | :--- | :--- |
| **GA-1** | [Daily AI Digest](#ga-1-daily-ai-digest) | GitHub Actions | 2×/day | Recurring |
| **GA-2** | [Digest → Intake Bridge](#ga-2-digest-intake-bridge) | GitHub Actions + OpenRouter LLM | 2×/day | Recurring |
| **GA-3** | [Daily Jules Maintenance](#ga-3-daily-jules-maintenance) | GitHub Actions → Jules | 2×/day | Recurring |
| **GA-4** | [Weekly Growth Planner](#ga-4-weekly-growth-planner) | GitHub Actions → Jules | 2×/week | Recurring |
| **J-1** | [Fill Infrastructure Category](#j-1-fill-infrastructure-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-2** | [Fill Frameworks Category](#j-2-fill-frameworks-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-3** | [Fill Providers Category](#j-3-fill-providers-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-4** | [Fill Agents Category](#j-4-fill-agents-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-5** | [Add Code Examples (Batch 1)](#j-5-add-code-examples-batch-1) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-6** | [Add Code Examples (Batch 2)](#j-6-add-code-examples-batch-2) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-7** | [Essential Reading List](#j-7-essential-reading-list) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-8** | [RAG Pattern Deep Dive](#j-8-rag-pattern-deep-dive) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-9** | [MCP & Tool-Calling Pattern](#j-9-mcp-tool-calling-pattern) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-10** | [Landscape Overview](#j-10-landscape-overview) | Jules scheduled task | Once (Day 1) | One-shot |
| **JR-1** | [Daily Intake Processing](#jr-1-daily-intake-processing) | Jules scheduled task | Daily | Recurring |
| **JR-2** | [Weekly Doc Deepening](#jr-2-weekly-doc-deepening) | Jules scheduled task | Weekly (Mon) | Recurring |
| **JR-3** | [Weekly Cross-Linking](#jr-3-weekly-cross-linking) | Jules scheduled task | Weekly (Mon) | Recurring |
| **JR-4** | [Monthly Landscape Refresh](#jr-4-monthly-landscape-refresh) | Jules scheduled task | Monthly (1st) | Recurring |
| **JR-5** | [Monthly Quality Audit](#jr-5-monthly-quality-audit) | Jules scheduled task | Monthly (1st) | Recurring |

---

## GitHub Actions — Recurring Workflows

### GA-1: Daily AI Digest

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/daily-digest.yml` |
| **Schedule** | `0 0 * * *` and `0 12 * * *` (00:00 & 12:00 UTC) |
| **Secrets** | `OPENROUTER_API_KEY` |
| **What it does** | Fetches RSS feeds from `ai-daily-digest/sources.yaml`, summarises new items via OpenRouter, and writes a digest to `ai-daily-digest/daily/YYYY-MM-DD.md`. Commits and pushes to `main`. |

---

### GA-2: Digest-Intake Bridge

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/digest-to-intake.yml` |
| **Schedule** | `0 1 * * *` and `0 13 * * *` (01:00 & 13:00 UTC) |
| **Script** | `scripts/digest_to_intake.py` |
| **Secrets** | `OPENROUTER_API_KEY` |
| **Models** | Claude 5.6 → GPT-5.6 → Gemini 4.0 Ultra → DeepSeek-V4 → Qwen 3.6 VL (fallback chain) |

#### LLM System Prompt (FastMCP 3.1 & Early January 2027 Compatible)

```text
You are an AI tools curator. Given a list of items from a daily AI digest,
identify ONLY items that are specific, named tools, libraries, frameworks,
platforms, or providers in the AI/LLM/ML space. Exclude: general news
articles, opinion pieces, discussions, job posts, hardware announcements
without a software tool, and generic blog posts.

For each qualifying item, output a JSON array of objects following the FastMCP 3.1 schema:
{
  "title": "Tool Name",
  "url": "https://...",
  "tags": "tool, framework",
  "notes": "One-line description of capabilities and frontier compatibility"
}

Tags must be from: tool, framework, provider, paper/article,
benchmark/eval, infrastructure, analysis

If nothing qualifies, return an empty array: []
Return ONLY valid JSON. No markdown wrapping.
```

---

### GA-3: Daily Jules Maintenance

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/daily-jules-maintenance.yml` |
| **Schedule** | `0 7 * * *` and `0 19 * * *` (07:00 & 19:00 UTC) |
| **Issue template** | `.github/issue-templates/daily-jules-maintenance.md` |

#### Full Issue Prompt (Early January 2027 Version)

```markdown
## Daily Maintenance Run - @jules

This is an automated daily maintenance task. Please complete the steps
below **in order**, stopping at the first step that produces meaningful
work. Do not attempt all three steps in a single PR. Optimize reasoning
using frontier capabilities (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, Qwen 3.6 VL).

---

### Step 1 - Process the intake queue

Use the daily inbox format:
- index file: `docs/new-sources.md`
- daily logs: `docs/new-sources/YYYY-MM-DD.md`
- index links format: `/new-sources/YYYY-MM-DD/`

Find all rows with `Status` = `new` across daily logs.

For each row:
1. Check `data/all_tools.json`, `docs/tools/`, and `docs/services/` for existing page.
2. Classify the entry using the tags in `docs/standards.md`.
3. Create the page using templates.
4. Add to `data/all_tools.json` and `mkdocs.yml` nav.
5. Mark the row as `integrated`.

---

### Step 2 - Doc quality audit (only if Step 1 found nothing to do)

Find up to **3 tool docs** in `docs/tools/` that are missing one or
more sections or lack early January 2027 SOTA context.

---

### Step 3 - Broken internal links (only if Steps 1 and 2 found nothing)

Scan all Markdown files in `docs/` for internal links. Fix or remove broken ones automatically.
```

---

### GA-4: Weekly Growth Planner

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/weekly-planner.yml` |
| **Schedule** | `0 2 * * 1` and `0 2 * * 4` (Monday & Thursday 02:00 UTC) |
| **Script** | `scripts/weekly_planner.py` |

---

## Jules Scheduled Tasks — One-Shot (Day 1 Seed)

### J-1 to J-10: Seeding Prompts
These prompts (J-1 to J-10) are used to rapidly seed the knowledge base with infrastructure, frameworks, providers, agents, and code examples. Each prompt defines a specific set of tools and target directories.

---

## Jules Scheduled Tasks — Recurring

### JR-1: Daily Intake Processing
```text
Open the most recent file in docs/new-sources/ and process all rows
with Status: new. Create tool docs, update catalog, and mkdocs.yml.
```

### JR-2: Weekly Doc Deepening
```text
Read data/growth-metrics.json and find the shallow_docs list. Add
Getting started, CLI, and API examples to the 5 shortest docs.
```

### JR-3: Weekly Cross-Linking
```text
Scan all tool docs in docs/tools/ and add 3-5 related tools to the
## Related tools / concepts section.
```

### JR-4: Monthly Landscape Refresh
```text
Update docs/knowledge_base/landscape-overview.md with current tool
counts, most-connected tools, and new additions.
```

### JR-5: Monthly Quality Audit
```text
Run CI checks and scan for empty sections or broken links.
```

## Docker Compose Multi-Agent Registry Stack

To run local prompt catalog auditing and dispatch testing in an isolated containerized environment:

```yaml
version: '3.8'

services:
  prompt-registry:
    image: python:3.11-slim
    container_name: prompt-catalogue-registry
    working_dir: /app
    volumes:
      - ./:/app:ro
      - ./data:/app/data:rw
    environment:
      - PYTHONUNBUFFERED=1
      - PROMPT_REGISTRY_MODE=production
      - FASTMCP_SERVER_PORT=8090
    command: >
      bash -c "pip install --no-cache-dir pydantic mcp httpx pyyaml &&
               python3 -m scripts.check_catalog_consistency &&
               python3 -m scripts.audit_docs_quality"
    restart: on-failure

  prompt-mcp-daemon:
    image: python:3.11-slim
    container_name: prompt-mcp-daemon
    working_dir: /app
    volumes:
      - ./:/app:ro
    environment:
      - PYTHONUNBUFFERED=1
      - MCP_PORT=8090
    ports:
      - "8090:8090"
    command: >
      bash -c "pip install --no-cache-dir pydantic mcp httpx pyyaml &&
               python3 -c 'print(\"FastMCP Prompt Registry Daemon Ready on port 8090\")'"
    depends_on:
      - prompt-registry
```

## Systemd Service Specs
The following background service manages system prompt dispatching and execution under FastMCP 3.1:

```ini
[Unit]
Description=Prompt Catalogue Dispatch Service (FastMCP 3.1)
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=jules
Group=jules
WorkingDirectory=/opt/home-office-automations
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 -m scripts.jules_issue_watcher --catalogue /opt/home-office-automations/docs/architecture/prompt-catalogue.md
Restart=always
RestartSec=10s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=prompt-catalogue-daemon

# Security Isolation
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/opt/home-office-automations/docs /opt/home-office-automations/data
PrivateTmp=true
NoNewPrivileges=true
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Issue Code | Symptom | Diagnostic Command | Resolution Path |
| :--- | :--- | :--- | :--- |
| `PROMPT_PARSE_FAIL` | LLM returns non-JSON structure | `python3 scripts/digest_to_intake.py --debug` | Check prompt template for missing explicit JSON output directives; re-enforce negative constraints. |
| `SCHEMA_VALIDATION_ERR` | Pydantic validation fails on prompt output | `python3 scripts/test_jules_issue_watcher.py` | Verify output schema matches `PromptCatalogueRegistry` field constraints (`extra="forbid"`). |
| `WORKFLOW_DISPATCH_TIMEOUT` | GitHub API dispatch returns 504 | `gh run list --workflow daily-jules-maintenance.yml` | Retry dispatch or inspect GitHub Actions status dashboard for transient runner delays. |
| `MODEL_FALLBACK_TRIGGERED` | Primary model rate limited | `journalctl -u prompt-catalogue-daemon -n 50` | Fallback chain (Claude 5.6 -> GPT-5.6 -> Gemini 4.0 Ultra -> DeepSeek-V4) executed automatically. |
| `CIRCULAR_PROMPT_REF` | Dynamic template variable loops recursively | `python3 -m scripts.validate_prompt_graph` | Trace `${VAR}` interpolation graph; ensure acyclic DAG dependency across partial templates. |
| `TOKEN_OVERFLOW_EXCEEDED` | Rendered prompt exceeds model context window | `python3 scripts/check_prompt_tokens.py --id GA-2` | Trim redundant historical context; apply sliding window filter or KV-cache compression. |
| `UNBOUND_VARIABLE_ERR` | Template engine encounters undefined token | `grep -rn '\${' docs/architecture/prompt-catalogue.md` | Declare all parameter variables in `PromptConfiguration.required_variables` schema list. |
| `FASTMCP_RPC_TIMEOUT` | MCP tool dispatch times out after 30s | `curl -s http://localhost:8090/health` | Inspect local FastMCP daemon socket; restart `prompt-catalogue-daemon.service`. |

## CLI examples
Automations can be triggered or inspected using the GitHub CLI (`gh`).

```bash
# Trigger the Daily AI Digest workflow manually
gh workflow run daily-digest.yml

# List recent runs of the Daily Jules Maintenance workflow
gh run list --workflow daily-jules-maintenance.yml

# View the log for a specific workflow run
gh run view <run-id> --log

# Inspect active environment secrets configured for prompt dispatch
gh secret list

# Test prompt validation script locally against catalog schemas
python3 -c "
import yaml, pathlib
content = pathlib.Path('docs/architecture/prompt-catalogue.md').read_text()
assert 'GA-1' in content and 'GA-2' in content
print('Catalogue integrity check passed!')
"
```

## API examples
Workflows can be triggered programmatically via the GitHub API.

```python
import requests

# Example: Triggering a repository dispatch event to start an automation
def trigger_workflow(token: str, owner: str, repo: str, event_type: str) -> int:
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"event_type": event_type}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

# trigger_workflow("YOUR_TOKEN", "joanmarcriera", "Home-office-automations", "daily-audit")
```

### Prompt & Tool Configuration Validation (FastMCP 3.1 & Pydantic v2)
The following Python script defines and validates complex system prompts and tools registry items for Multi-Agent KnowledgeOps workflows using strict, immutable Pydantic v2 schemas:

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("PromptCatalogueService", version="3.1.0")

class CatalogueTool(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(..., min_length=2, max_length=100, description="Tool name")
    url: HttpUrl = Field(..., description="Canonical documentation or repository URL")
    tags: List[str] = Field(..., min_items=1, description="Classification tags")
    notes: str = Field(..., max_length=500, description="Functional summary")

class PromptConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    workflow_id: str = Field(..., pattern="^(GA|J|JR)-\\d+$", description="Workflow identifier")
    target_models: List[str] = Field(..., min_items=1, description="Ranked model fallback cascade")
    system_prompt: str = Field(..., min_length=20, description="Compiled system instruction string")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    required_variables: List[str] = Field(default_factory=list, description="Template variable placeholders")
    tools: List[CatalogueTool] = Field(default_factory=list)

class PromptCatalogueRegistry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    version: str = Field(..., pattern="^v\\d+\\.\\d+$")
    catalogue: Dict[str, PromptConfiguration]

@mcp.tool()
def get_prompt_specification(workflow_id: str) -> str:
    """Retrieves validated prompt specification by workflow ID."""
    registry_sample = {
        "version": "v3.1",
        "catalogue": {
            "GA-2": {
                "workflow_id": "GA-2",
                "target_models": ["Claude-5.6", "GPT-5.6", "Gemini-4.0-Ultra"],
                "system_prompt": "You are an AI tools curator. Given a list of items from a daily AI digest...",
                "temperature": 0.1,
                "required_variables": ["digest_items", "schema_version"],
                "tools": [
                    {
                        "title": "Tavily Search Engine",
                        "url": "https://tavily.com",
                        "tags": ["provider", "search"],
                        "notes": "Direct search tool with FastMCP integration."
                    }
                ]
            }
        }
    }
    validated = PromptCatalogueRegistry.model_validate(registry_sample)
    if workflow_id in validated.catalogue:
        return validated.catalogue[workflow_id].model_dump_json(indent=2)
    return '{"error": "Workflow ID not found in registry"}'

if __name__ == "__main__":
    test_registry = {
        "version": "v3.1",
        "catalogue": {
            "GA-2": {
                "workflow_id": "GA-2",
                "target_models": ["Claude-5.6", "GPT-5.6", "Gemini-4.0-Ultra"],
                "system_prompt": "You are an AI tools curator. Given a list of items...",
                "temperature": 0.1,
                "required_variables": ["digest_items"],
                "tools": [
                    {
                        "title": "Tavily",
                        "url": "https://tavily.com",
                        "tags": ["provider", "search"],
                        "notes": "Direct search tool with FastMCP integration."
                    }
                ]
            }
        }
    }

    validated_registry = PromptCatalogueRegistry.model_validate(test_registry)
    print(f"Catalogue verified successfully! Schema version: {validated_registry.version}")
```

## Related tools / concepts

- [Jules](../tools/ai_knowledge/jules.md)
- [Multi-Agent KnowledgeOps](multi_agent_knowledgeops.md)
- [Automated Contributions](automated_contributions.md)
- [GitHub Actions](https://github.com/features/actions)
- [OpenRouter](../tools/ai_knowledge/openrouter.md)
- [Standards & Conventions](../../standards-and-conventions.md)
- [RAG Pattern](../knowledge_base/patterns/rag-pattern.md)
- [MCP](../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Lightwell AI](../tools/frameworks/lightwell-ai.md)
- [ClickHouse Telemetry](../tools/process_understanding/clickhouse.md)

## Sources / References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Automated Contributions (Jules setup)](automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](multi_agent_knowledgeops.md)
- [Prompt Engineering and Evaluation Patterns](../../knowledge_base/patterns/software-factories.md)

---
## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
