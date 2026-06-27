# Task Decomposition Report - Batch 153
**Date**: 2026-06-28
**Batch ID**: 153
**Status**: Decomposed

## Overview
This report decomposes the next five oldest documentation freshness issues identified by `find_oldest_issues.py` into granular, actionable sub-tasks. Each task follows the High Confidence documentation standard (13 mandatory sections) and incorporates June 2026 technical context.

## Decomposed Issues

### 1. Freshness Audit: GSM8K (`docs/tools/benchmarking/gsm8k.md`)
**Context**: Primary benchmark for multi-step mathematical reasoning.
- [ ] Upgrade to 13-section High Confidence standard.
- [ ] Update performance metrics for June 2026 (Claude 4.8, GPT-5.5, Llama 4 Maverick).
- [ ] Add CLI examples for `lm-eval` with specific June 2026 model flags.
- [ ] Ensure 7+ unique relative links to related tools (e.g., `math-benchmark.md`, `dream.md`, `gpqa.md`).
- [ ] Verify sources include the original OpenAI paper and Hugging Face dataset URL.

### 2. Freshness Audit: GPQA (`docs/tools/benchmarking/gpqa.md`)
**Context**: Expert-level science reasoning benchmark.
- [ ] Upgrade to 13-section High Confidence standard.
- [ ] Incorporate June 2026 performance table (Diamond accuracy for frontier models).
- [ ] Add API examples for programmatic evaluation using the `lm_eval` library.
- [ ] Update 'Related tools' with links to `mmlu.md`, `human-eval.md`, and `chatbot-arena.md`.
- [ ] Ensure `Last reviewed` is updated to 2026-06-28.

### 3. Freshness Audit: HumanEval (`docs/tools/benchmarking/human-eval.md`)
**Context**: Standard benchmark for zero-shot Python code generation.
- [ ] Upgrade to 13-section High Confidence standard.
- [ ] Update Pass@1 SOTA metrics for Claude 4.8 Opus and GPT-5.5.
- [ ] Add CLI examples for running evaluation with `--allow_code_execution`.
- [ ] Cross-link with coding assistants like `aider.md`, `cursor.md`, and `claude-code.md`.
- [ ] Ensure 'Sources' includes the official HumanEval GitHub repository.

### 4. Freshness Audit: NVIDIA (`docs/tools/providers/nvidia.md`)
**Context**: Core infrastructure and inference microservices (NIM).
- [ ] Upgrade to 13-section High Confidence standard.
- [ ] Incorporate June 2026 context (Rubin architecture, NIM GA status).
- [ ] Add Docker CLI examples for running local NIM microservices.
- [ ] Update 'Related tools' with links to `groq.md`, `together.md`, and `tgi.md`.
- [ ] Ensure valid external URLs for NVIDIA API Catalog and NIM documentation.

### 5. Freshness Audit: Make (`docs/tools/automation_orchestration/make.md`)
**Context**: Cloud-based visual automation platform (formerly Integromat).
- [ ] Upgrade to 13-section High Confidence standard.
- [ ] Incorporate June 2026 context regarding agentic handoffs and cloud/hybrid orchestration.
- [ ] Add Python API examples for programmatic scenario management.
- [ ] Update 'Related tools' with links to `zapier.md`, `pipedream.md`, `skyvern.md`, and `browser-use.md`.
- [ ] Ensure `Last reviewed` date is set to 2026-06-28.

## Verification Checklist
- [ ] Each task includes the 13 mandatory sections in the defined order.
- [ ] Each task requires 7+ relative markdown links.
- [ ] Each task requires at least one valid external source URL.
- [ ] All June 2026 technical context (Claude 4.8, GPT-5.5, MCP 3.0) is preserved.

## Next Steps
These tasks will be prioritized in Batch 154 for execution.
