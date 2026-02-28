# Prompt & Automation Catalogue

Every prompt, issue template, and LLM call used to keep this repository growing — collected in one place for auditability and tuning.

---

## Overview

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

No LLM prompt is embedded in the workflow — the digest script (`ai-daily-digest/scripts/digest.py`) handles all OpenRouter calls internally.

---

### GA-2: Digest-Intake Bridge

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/digest-to-intake.yml` |
| **Schedule** | `0 1 * * *` and `0 13 * * *` (01:00 & 13:00 UTC) |
| **Script** | `scripts/digest_to_intake.py` |
| **Secrets** | `OPENROUTER_API_KEY` |
| **Models** | Llama 3.3 70B → DeepSeek R1 → Qwen 2 7B (fallback chain) |

#### LLM System Prompt

```text
You are an AI tools curator. Given a list of items from a daily AI digest,
identify ONLY items that are specific, named tools, libraries, frameworks,
platforms, or providers in the AI/LLM/ML space. Exclude: general news
articles, opinion pieces, discussions, job posts, hardware announcements
without a software tool, and generic blog posts.

For each qualifying item, output a JSON array of objects:
{"title": "Tool Name", "url": "https://...", "tags": "tool, framework",
 "notes": "One-line description"}

Tags must be from: tool, framework, provider, paper/article,
benchmark/eval, infrastructure, analysis

If nothing qualifies, return an empty array: []
Return ONLY valid JSON. No markdown wrapping.
```

#### LLM User Prompt Template

```text
Classify these items:

- [Item Title](https://item-url.com)
- [Item Title](https://item-url.com)
...
```

---

### GA-3: Daily Jules Maintenance

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/daily-jules-maintenance.yml` |
| **Schedule** | `0 7 * * *` and `0 19 * * *` (07:00 & 19:00 UTC) |
| **Issue template** | `.github/issue-templates/daily-jules-maintenance.md` |

The workflow creates a GitHub issue with the `jules` label. Jules picks it up automatically.

#### Full Issue Prompt

```markdown
## Daily Maintenance Run - @jules

This is an automated daily maintenance task. Please complete the steps
below **in order**, stopping at the first step that produces meaningful
work. Do not attempt all three steps in a single PR.

---

### Step 1 - Process the intake queue

Use the daily inbox format:
- index file: `docs/new-sources.md`
- daily logs: `docs/new-sources/YYYY-MM-DD.md`
- index links format: `/new-sources/YYYY-MM-DD/` (do not use
  `new-sources/YYYY-MM-DD.md`)

Find all rows with `Status` = `new` across daily logs.

For each row:
1. Check `data/all_tools.json`, `docs/tools/`, and `docs/services/` to
   see if a canonical page already exists. If it does, add the source
   URL to `## Sources / References` on that page and mark the row
   `integrated`. Move to the next row.
2. Classify the entry using the tags in `docs/standards.md`: `tool`,
   `framework`, `provider`, `paper/article`, `tutorial/guide`,
   `benchmark/eval`, `infrastructure`, `analysis`
3. Determine the correct target directory from the taxonomy table in
   `docs/standards.md`.
4. Create the page using `docs/templates/tool_template.md` (for tools,
   frameworks, providers) or `docs/templates/article_template.md` (for
   papers and articles). Fill in **all required sections** with concise,
   neutral, technically accurate content. Do not leave any section empty.
5. If it is a tool, framework, or provider: add an entry to
   `data/all_tools.json` and add the page to the correct section of
   `mkdocs.yml` nav in alphabetical order.
6. Mark the row as `integrated` in that daily file and add/update
   `Canonical Page`.

If today's daily file does not exist yet, create
`docs/new-sources/$TODAY.md` using the schema documented in
`docs/new-sources.md`.

Before opening the PR, run:
`python3 scripts/validate_new_sources.py`
If it fails, fix the intake files until it passes.

If the queue is empty (no `new` entries), proceed to Step 2.

---

### Step 2 - Doc quality audit (only if Step 1 found nothing to do)

The 10 required sections for every tool doc are defined in
`docs/standards.md`.

Find up to **3 tool docs** in `docs/tools/` that are missing one or
more of these sections. For each:
- Add the missing section(s) with a one-sentence placeholder marked
  `<!-- needs-content -->`
- Do not change any existing content

Limit: 3 files per run.

---

### Step 3 - Broken internal links (only if Steps 1 and 2 found nothing)

Scan all Markdown files in `docs/` for internal links of the form
`[text](relative-path)`. For any link where the target file does not
exist at that path:
- Fix the path if the file exists at a different location
- Otherwise, remove the link anchor and leave the text inline

Limit: 10 broken links per run.

---

After completing whichever step produced changes, open a pull request
titled: `chore: daily maintenance $TODAY`.
```

---

### GA-4: Weekly Growth Planner

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/weekly-planner.yml` |
| **Schedule** | `0 2 * * 1` and `0 2 * * 4` (Monday & Thursday 02:00 UTC) |
| **Script** | `scripts/weekly_planner.py` |

No LLM call — this script reads `data/growth-metrics.json` and creates two Jules issues programmatically.

#### Generated Issue 1 — Doc Deepening

Template from `.github/issue-templates/weekly-deepen-docs.md`:

```markdown
## Weekly Doc Deepening

The following N docs are the shallowest in the knowledge base and need
practical content added.

### Target docs
- `docs/services/focalboard.md`
- `docs/services/storj.md`
- ... (5 shallowest by character count)

### Instructions
For each doc above:
1. Read the tool's official website/GitHub from its
   **Sources / References** section
2. Add a `## Getting started` section after `## When not to use it`
   with:
   - Installation command (pip, npm, docker pull, or equivalent)
   - A minimal working example in a fenced code block
3. If the tool has a CLI, add `## CLI examples` with 2-3 common commands
4. If the tool has an API/SDK, add `## API examples` with a Python or
   curl snippet
5. Keep all existing content unchanged
6. Update `- Last reviewed:` in the Contribution Metadata section

### Quality checks
- Verify: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml'));
  print('OK')"`
- Ensure all code examples are complete and runnable
```

#### Generated Issue 2 — Category Gap Fill

Template from `.github/issue-templates/category-gap-filler.md`:

```markdown
## Category Gap Fill: <category>

The **<category>** category currently has only **N docs**, making it
underdeveloped.

### Instructions
1. Research and identify **up to 8 tools** that belong in this category.
   Consider: <search hints from CATEGORY_HINTS dict>
2. For each tool, create a doc using `docs/templates/tool_template.md`
3. Place in `docs/tools/<category>/`
4. Add to `data/all_tools.json` and `mkdocs.yml` navigation
5. Add an intake row to today's `docs/new-sources/YYYY-MM-DD.md` with
   `Status: integrated`
6. Do NOT create stub pages — every doc must have substantive content

### Deduplication
Before creating any page, search the repo for the tool name and common
aliases. If it already exists elsewhere, update the existing page
instead.

### Quality checks
- Verify mkdocs.yml syntax
- Run: `python3 scripts/validate_new_sources.py`
```

---

## Jules Scheduled Tasks — One-Shot (Day 1 Seed)

These 10 prompts run once on the first day to rapidly seed the knowledge base. They are designed as a **sequential chain** — later runs build on the output of earlier ones.

### J-1: Fill Infrastructure Category

| | |
| :--- | :--- |
| **Schedule** | Day 1, 08:00 |
| **Jules slot** | 1 of 10 |

```text
Research and create documentation for 5 key AI infrastructure tools.
Target category: docs/tools/infrastructure/

Create docs for: vLLM, Text Generation Inference (TGI), SGLang,
ExLlamaV2, and Aphrodite Engine.

For each tool:
1. Use the template at docs/templates/tool_template.md
2. Fill ALL required sections with substantive, technically accurate
   content
3. Place the file in docs/tools/infrastructure/
4. Add to data/all_tools.json
5. Add to mkdocs.yml nav under Tool Catalogue > Infrastructure in
   alphabetical order
6. Add an intake row to docs/new-sources/YYYY-MM-DD.md with
   Status: integrated

Before committing, verify:
python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml'));
print('OK')"

Open a single PR titled: "feat: add 5 infrastructure tool docs"
```

---

### J-2: Fill Frameworks Category

| | |
| :--- | :--- |
| **Schedule** | Day 1, 09:30 |
| **Jules slot** | 2 of 10 |

```text
Research and create documentation for 5 key AI/LLM frameworks. Target
category: docs/tools/frameworks/

Create docs for: Haystack, Semantic Kernel, DSPy, Spring AI, and
Instructor.

For each tool:
1. Use the template at docs/templates/tool_template.md
2. Fill ALL required sections with substantive content
3. Place in docs/tools/frameworks/
4. Add to data/all_tools.json and mkdocs.yml nav under
   Tool Catalogue > Frameworks in alphabetical order
5. Add intake row to docs/new-sources/YYYY-MM-DD.md with
   Status: integrated

Check for duplicates first — if any of these tools already exist
elsewhere in docs/tools/, update the existing page instead.

Verify mkdocs.yml: python3 -c "import yaml;
yaml.safe_load(open('mkdocs.yml')); print('OK')"

PR title: "feat: add 5 framework docs"
```

---

### J-3: Fill Providers Category

| | |
| :--- | :--- |
| **Schedule** | Day 1, 11:00 |
| **Jules slot** | 3 of 10 |

```text
Research and create documentation for 5 LLM API providers. Target
category: docs/tools/providers/

Create docs for: Cohere, Mistral AI, Together AI, Fireworks AI, and
Groq.

For each:
1. Use docs/templates/tool_template.md — fill every section
2. Place in docs/tools/providers/
3. Add to data/all_tools.json and mkdocs.yml nav under
   Tool Catalogue > Providers alphabetically
4. Add intake row with Status: integrated

Note: OpenAI, Anthropic, Google Gemini, OpenRouter, and DeepSeek
already exist in docs/tools/ai_knowledge/. Do NOT duplicate them.

Verify mkdocs.yml syntax before committing.

PR title: "feat: add 5 provider docs"
```

---

### J-4: Fill Agents Category

| | |
| :--- | :--- |
| **Schedule** | Day 1, 12:30 |
| **Jules slot** | 4 of 10 |

```text
Research and create documentation for 5 AI agent frameworks. Target
category: docs/tools/agents/

Create docs for: AutoGen, CrewAI, LangGraph, Smolagents, and Agency
Swarm.

For each:
1. Use docs/templates/tool_template.md — fill every section
2. Place in docs/tools/agents/
3. Add to data/all_tools.json and mkdocs.yml nav under
   Tool Catalogue > Agents alphabetically
4. Add intake row with Status: integrated

Check: Jules and OpenHands already exist in other categories. Do NOT
create duplicates. In the Related tools section of each new doc, link
to existing agent-related pages.

Verify mkdocs.yml. PR title: "feat: add 5 agent framework docs"
```

---

### J-5: Add Code Examples (Batch 1)

| | |
| :--- | :--- |
| **Schedule** | Day 1, 14:00 |
| **Jules slot** | 5 of 10 |

```text
Add practical code examples to the 5 most important tool docs that
currently lack them.

Target docs (pick the 5 most popular/important from this list that
don't already have code fences):
- docs/tools/ai_knowledge/langchain.md
- docs/tools/ai_knowledge/llamaindex.md
- docs/tools/development_ops/aider.md
- docs/tools/development_ops/cursor.md
- docs/tools/ai_knowledge/dify.md

For each doc:
1. Visit the URLs in its Sources / References section
2. Add ## Getting started with: install command + minimal hello-world
3. Add ## CLI examples with 2-3 common commands (if applicable)
4. Add ## API examples with a Python or curl snippet (if applicable)
5. Do NOT change any existing content — only add new sections
6. Update the Last reviewed date

All code examples must be complete and runnable — no placeholder
`...` blocks.

PR title: "feat: add code examples to 5 tool docs (batch 1)"
```

---

### J-6: Add Code Examples (Batch 2)

| | |
| :--- | :--- |
| **Schedule** | Day 1, 15:30 |
| **Jules slot** | 6 of 10 |

```text
Add practical code examples to 5 more tool docs.

Target docs:
- docs/services/ollama.md
- docs/services/n8n.md
- docs/services/paperless-ngx.md
- docs/tools/process_understanding/crawl4ai.md
- docs/tools/automation_orchestration/browser-use.md

Same instructions as the previous run:
1. Add ## Getting started, ## CLI examples, ## API examples as
   appropriate
2. All code must be complete and runnable
3. Do NOT modify existing content
4. Update Last reviewed date

PR title: "feat: add code examples to 5 tool docs (batch 2)"
```

---

### J-7: Essential Reading List

| | |
| :--- | :--- |
| **Schedule** | Day 1, 17:00 |
| **Jules slot** | 7 of 10 |

```text
Create a curated "Essential Reading" page for anyone wanting to become
an AI-literate engineer.

Create file: docs/knowledge_base/essential-reading.md

Structure:
## What this page covers
Brief intro.

## Foundational papers
List 8-10 landmark papers (Attention Is All You Need, BERT, GPT-3,
InstructGPT, Constitutional AI, etc.) with one-line summaries.

## Key technical blogs
List 10 high-signal blogs/newsletters (Simon Willison, Lilian Weng,
The Gradient, Latent Space, etc.) with what they cover.

## Getting started guides
Link to 5 of the best "start here" guides for LLMs, RAG, agents,
fine-tuning, and prompt engineering.

## Community hubs
List the top communities: r/LocalLLaMA, Hugging Face forums, LLM
Discord servers, etc.

Add the page to mkdocs.yml under Knowledge Base.
Include Sources / References and Contribution Metadata sections.

PR title: "feat: add essential reading page"
```

---

### J-8: RAG Pattern Deep Dive

| | |
| :--- | :--- |
| **Schedule** | Day 1, 18:30 |
| **Jules slot** | 8 of 10 |

```text
Create a comprehensive pattern page about Retrieval-Augmented
Generation (RAG).

Create file: docs/knowledge_base/patterns/rag-patterns.md

Required sections:
## What it is — define RAG in 2-3 sentences
## Core architecture — describe the retrieve→augment→generate pipeline
## Variants — cover: naive RAG, advanced RAG (re-ranking, query
   rewriting, HyDE), modular RAG, graph RAG
## When to use it — scenarios where RAG beats fine-tuning
## When not to use it — anti-patterns
## Tools in this repo that implement RAG — link to existing docs
   (RAGFlow, LlamaIndex, LangChain, Crawl4AI, etc.)
## Code example — a minimal Python RAG pipeline using LlamaIndex
   or LangChain (pick whichever has better docs)
## Sources / References (authoritative sources)
## Contribution Metadata

Add to mkdocs.yml under Knowledge Base > Patterns.

PR title: "feat: add RAG patterns deep dive"
```

---

### J-9: MCP-Tool-Calling Pattern

| | |
| :--- | :--- |
| **Schedule** | Day 1, 20:00 |
| **Jules slot** | 9 of 10 |

```text
Create a pattern page about MCP (Model Context Protocol) and LLM
tool-calling patterns.

Create file: docs/knowledge_base/patterns/mcp-tool-calling.md

Required sections:
## What it is — define MCP and tool/function calling
## How MCP works — server/client architecture, tool discovery,
   transport protocols
## How tool calling works — the request/response cycle in
   OpenAI-style and Anthropic-style APIs
## Comparison — MCP vs native function calling vs LangChain tools
   vs custom REST
## When to use MCP — multi-tool orchestration, IDE integration
## When to use native tool calling — simple single-tool scenarios
## Tools in this repo — link to existing MCP-related docs (MCP
   Registry, ServiceNow MCP, CliHub, Claude Code, etc.)
## Code example — a minimal MCP server in Python
## Sources / References (standard sections)
## Contribution Metadata (standard sections)

Add to mkdocs.yml under Knowledge Base > Patterns.

PR title: "feat: add MCP and tool-calling pattern page"
```

---

### J-10: Landscape Overview

| | |
| :--- | :--- |
| **Schedule** | Day 1, 21:30 |
| **Jules slot** | 10 of 10 |

```text
Create a landscape overview page that gives readers a bird's-eye view
of every category in the knowledge base.

Create file: docs/knowledge_base/landscape-overview.md

Required sections:
## Overview — what this page covers and when it was last generated
## Category breakdown — for each category in docs/tools/, list:
   the number of docs, the 3-5 most notable tools, and a one-line
   summary of what the category covers
## Self-hosted services — summarise the 47 services with top picks
   per use case (media, productivity, storage, security)
## Growth areas — list categories with fewer than 8 docs as areas
   where the repo is actively expanding
## How this repo stays current — brief description of the daily
   digest → bridge → Jules → weekly planner pipeline
## Sources / References (architecture links)
## Contribution Metadata

Add to mkdocs.yml under Knowledge Base.

PR title: "feat: add landscape overview page"
```

---

## Jules Scheduled Tasks — Recurring

These prompts run on an ongoing basis after the initial seed.

### JR-1: Daily Intake Processing

| | |
| :--- | :--- |
| **Schedule** | Daily, 08:00 |
| **Cadence** | Every day |

```text
Open the most recent file in docs/new-sources/ and process all rows
with Status: new. For each row:
1. Check if a doc already exists in data/all_tools.json — if yes,
   skip it
2. Classify it using the taxonomy in docs/standards.md
3. Create a full tool doc using the template in
   docs/templates/tool_template.md in the correct category directory
4. Add the tool to data/all_tools.json and mkdocs.yml nav
5. Update the row's Status to integrated and set the Canonical Page
6. Run python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml'));
   print('OK')" before committing
```

---

### JR-2: Weekly Doc Deepening

| | |
| :--- | :--- |
| **Schedule** | Monday, 10:00 |
| **Cadence** | Weekly |

```text
Read data/growth-metrics.json and find the shallow_docs list. Pick the
5 shortest docs. For each one:
1. Visit the URLs in its Sources/references section
2. Add a ## Getting started section with install command and
   hello-world example
3. Add a ## CLI examples section with 3 common commands
4. Add a ## API examples section with a minimal code snippet
If the tool has no official docs, note that in the doc and skip the
code sections. Commit all changes in a single PR.
```

---

### JR-3: Weekly Cross-Linking

| | |
| :--- | :--- |
| **Schedule** | Monday, 14:00 |
| **Cadence** | Weekly |

```text
Scan all tool docs in docs/tools/. For each doc, check its
## Related tools / concepts section. If it's empty or says 'TBD',
find 3-5 related tools that already exist in the repo and add them
as markdown links (e.g., [n8n](../orchestration/n8n.md)). Also check
that every tool mentioned in Related sections actually has a doc — if
not, add a row to today's docs/new-sources/YYYY-MM-DD.md with
Status: new. Commit all changes.
```

---

### JR-4: Monthly Landscape Refresh

| | |
| :--- | :--- |
| **Schedule** | 1st of month, 08:00 |
| **Cadence** | Monthly |

```text
Read data/all_tools.json and data/growth-metrics.json. Update
docs/knowledge_base/landscape-overview.md with: current tool count
per category, a table of the top 10 most-connected tools (most
Related links), a list of categories with fewer than 8 docs, and a
"What's new this month" section listing tools added in the last 30
days (check git log for files created under docs/tools/). Keep the
doc concise and factual.
```

---

### JR-5: Monthly Quality Audit

| | |
| :--- | :--- |
| **Schedule** | 1st of month, 10:00 |
| **Cadence** | Monthly |

```text
Run the three CI checks: python scripts/validate_new_sources.py,
python scripts/check_docs_contract.py, and
python scripts/check_catalog_consistency.py. For any failures: fix
them directly. Then scan all tool docs for:
1. Empty or placeholder sections (containing only 'TBD', 'TODO',
   or '...')
2. Broken internal links
3. Docs not listed in mkdocs.yml
Fix all issues found and commit in a single PR titled
"chore: monthly quality audit YYYY-MM".
```

---

## Sources / References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Automated Contributions (Jules setup)](automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](multi_agent_knowledgeops.md)
- [Daily Jules Maintenance workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/daily-jules-maintenance.yml)
- [Digest-to-Intake Bridge workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/digest-to-intake.yml)
- [Weekly Planner workflow](https://github.com/joanmarcriera/Home-office-automations/blob/main/.github/workflows/weekly-planner.yml)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high
