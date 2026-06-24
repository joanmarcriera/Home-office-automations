# Task Decomposition Report: Patterns (Extraction) — 2026-06-04

This report documents the decomposition of documentation tasks for structured data extraction patterns, as identified during the Ralph-loop source integration (Items 83-84).

## New Issues Created

| Task ID | Title | Priority | Target Location | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **PATTERN-EXT-01** | Create 'Extraction and Classification' Pattern Doc | High | `docs/knowledge_base/patterns/extraction-and-classification.md` | Documenting schema-first extraction using Instructor, Pydantic, and Zod. |
| **PATTERN-EXT-02** | Create 'Date Extraction' Pattern Doc | Medium | `docs/knowledge_base/patterns/date-extraction.md` | Best practices for extracting and normalizing temporal data from unstructured text. |

## Context & Requirements

### PATTERN-EXT-01: Extraction and Classification
- **Core Concept**: Using structured output libraries (Instructor, Vercel AI SDK) to enforce types on LLM responses.
- **Key Tools**: [Instructor](../tools/frameworks/instructor.md), [PydanticAI](../tools/frameworks/pydantic-ai.md).
- **Sections Required**: What it is, Problem solved, Stack fit, Use cases (Sentiment, Intent, Entity extraction), Strengths/Limitations, When to use, and a Python/Pydantic code example.

### PATTERN-EXT-02: Date Extraction
- **Core Concept**: The specific challenge of normalizing relative dates (e.g., "next Tuesday") into absolute ISO8601 strings.
- **Key Tools**: [Instructor](../tools/frameworks/instructor.md), [Duckling](https://github.com/facebook/duckling).
- **Sections Required**: The "Context Problem" (LLMs need a reference date), Prompting strategies (SYSTEM_DATE injection), Tool-calling vs. direct extraction, and validation patterns.

## Definition of Done
- Both files created and meeting 'High Confidence' standards (>=10 headers, >=7 internal links).
- Files added to `docs/knowledge_base/patterns/index.md`.
- `docs/tools/frameworks/instructor.md` updated to point to these files without placeholders.

---
- Status: Verified & Closed
- Assigned to: Ralph-loop (Future Run)
