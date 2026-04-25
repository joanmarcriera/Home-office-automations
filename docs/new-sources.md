# New Sources — Daily Intake Logs

This index tracks daily source-ingestion files. Each day gets a dedicated log file in `docs/new-sources/` to avoid overlap between concurrent agents.

## Daily Log Files

| Date | Log File | New | Integrated | Notes |
| :--- | :--- | :---: | :---: | :--- |
| 2026-04-16 | [2026-04-16](/new-sources/2026-04-16/) | 0 | 28 | AI Daily Digest discovery. |
| 2026-04-08 | [2026-04-08](/new-sources/2026-04-08/) | 0 | 29 | Staged General Tools/Services from older logs. |
| 2026-04-07 | [2026-04-07](/new-sources/2026-04-07/) | 0 | 12 | Staged Benchmarking items; integrated all items. |
| 2026-04-06 | [2026-04-06](/new-sources/2026-04-06/) | 0 | 1 | Audit of tool documentation related sections and missing local docs. |
| 2026-03-30 | [2026-03-30](/new-sources/2026-03-30/) | 0 | 58 | Staged entries to manageable daily logs. |
| 2026-03-29 | [2026-03-29](/new-sources/2026-03-29/) | 0 | 9 | Added OpenClaw ecosystem patterns plus four source-driven updates from issue #179. |
| 2026-03-21 | [2026-03-21](/new-sources/2026-03-21/) | 0 | 16 | Divided intake from 2026-03-17 (Automation, Miscellaneous). |
| 2026-03-20 | [2026-03-20](/new-sources/2026-03-20/) | 0 | 12 | Divided intake from 2026-03-17 (Benchmarking). |
| 2026-03-19 | [2026-03-19](/new-sources/2026-03-19/) | 0 | 16 | Divided intake from 2026-03-17 (Process Understanding, Development & Ops). Integrated ripgrep. |
| 2026-03-18 | [2026-03-18](/new-sources/2026-03-18/) | 0 | 12 | Divided intake from 2026-03-17 (Infrastructure, Frameworks, Agents). Integrated FastAPI. |
| 2026-03-16 | [2026-03-16](/new-sources/2026-03-16/) | 0 | 0 | Standardized related tools sections across all documentation. |
| 2026-03-15 | [2026-03-15](/new-sources/2026-03-15/) | 0 | 11 | Added website-hosting canonicals, free website playbook, and discovery-style builder index |
| 2026-03-14 | [2026-03-14](/new-sources/2026-03-14/) | 0 | 33 | Added Claude ecosystem coverage, search/backend/browser tools, Google AI product pages, direct pages for memory/context/local inference, and company-stack extensions |
| 2026-03-11 | [2026-03-11](/new-sources/2026-03-11/) | 8 | 5 | Ingested Daily Digest (Gemini in Sheets, Qwen 3.5 Watch/Doom, instruction hierarchy). |
| 2026-03-09 | [2026-03-09](/new-sources/2026-03-09/) | 0 | 8 | Integrated Software Factory, Symphony, Superpowers, BigSwitch, NanoClaw, and Filesystem-as-Interface patterns |
| 2026-03-08 | [2026-03-08](/new-sources/2026-03-08/) | 2 | 6 | Added local AI desktop tools and integrated Qwen/Local LLM, Whisper/SearXNG, Home Assistant Ollama, and LocalAI |
| 2026-03-07 | [2026-03-07](/new-sources/2026-03-07/) | 8 | 4 | Ingested Daily Digest (llama.cpp MCP, Open WebUI terminal, GPT-5.4 AINews). |
| 2026-03-06 | [2026-03-06](/new-sources/2026-03-06/) | 11 | 6 | Ingested Daily Digest (GPT-5.4 launch, ChatGPT Excel, Qwen 3.5 122B impressions). |
| 2026-03-05 | [2026-03-05](/new-sources/2026-03-05/) | 0 | 2 | New providers: MiniMax, Moonshot AI |
| 2026-03-04 | [2026-03-04](/new-sources/2026-03-04/) | 18 | 6 | Ingested Daily Digest (GPT-5.3 Instant, Gemini 3.1 Flash-Lite, Qwen 3.5 vibe coding). |
| 2026-03-03 | [2026-03-03](/new-sources/2026-03-03/) | 0 | 21 | Provider, agent, and infrastructure updates |
| 2026-03-02 | [2026-03-02](/new-sources/2026-03-02/) | 0 | 18 | Daily ingestion (infrastructure, agents, frameworks) |
| 2026-03-01 | [2026-03-01](/new-sources/2026-03-01/) | 0 | 0 | Daily ingestion (empty) |
| 2026-02-28 | [2026-02-28](/new-sources/2026-02-28/) | 0 | 10 | Daily ingestion (infrastructure, benchmarking) |
| 2026-02-27 | [2026-02-27](/new-sources/2026-02-27/) | 0 | 21 | Daily ingestion (agents, frameworks, providers, and analysis) |
| 2026-02-26 | [2026-02-26](/new-sources/2026-02-26/) | 0 | 18 | Daily ingestion plus open-issue catch-up integrations |
| 2026-02-25 | [2026-02-25](/new-sources/2026-02-25/) | 0 | 9 | Initial daily migration |
| 2025-02-25 | [2025-02-25](/new-sources/2025-02-25/) | 0 | 5 | Legacy entries migrated from old monolithic inbox |

## Required Daily Log Schema

Each `docs/new-sources/YYYY-MM-DD.md` file must contain one table with this exact header:

`| Title | URL | Tags | Status | Canonical Page | Notes |`

Allowed values for `Status`:

- `new`
- `integrated`
- `duplicate`
- `needs-more-info`
- `low-confidence`

## Workflow Rules

1. New discoveries are appended only to today's file.
2. Integration updates should only modify status/canonical-page fields in the same row.
3. Do not create free-form sections or mixed formats in daily logs.
4. Keep this index updated with a row for each new day file.
5. In this index table, date links must use `/new-sources/YYYY-MM-DD/` (absolute site path).

## Related

- [Contributing Guide](CONTRIBUTING.md)
- [Standards](standards.md)
