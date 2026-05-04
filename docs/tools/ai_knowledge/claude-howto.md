# Claude How-To

## What it is
`claude-howto` is a collection of guides and examples focused on learning how to effectively use Claude and its associated tools, such as Claude Code and MCP.

## What problem it solves
It provides practical, hands-on instructions to bridge the gap between basic chat usage and advanced agentic workflows.

## Where it fits in the stack
**AI Assistants & Knowledge / Educational Layer**.

## Typical use cases
- Learning tool-calling patterns.
- Mastering MCP configuration.
- Optimizing prompts for agentic performance.

## Getting started
1.  **Install dependencies**:
    ```bash
    pip install uv
    uv venv
    source .venv/bin/activate
    uv pip install -r scripts/requirements-dev.txt
    ```
2.  **Install pre-commit hooks**:
    ```bash
    pip install pre-commit
    pre-commit install
    ```

## CLI examples
Run all quality checks manually:
```bash
pre-commit run --all-files
```

Build the EPUB ebook:
```bash
uv run scripts/build_epub.py
```

## Related tools / concepts
- [Claude](claude.md)
- [Claude Code](../development_ops/claude-code.md)
- [Everything Claude Code](everything-claude-code.md)
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Cline](../agents/cline.md)

## Sources / references
- [claude-howto GitHub](https://github.com/luongnv89/claude-howto)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
