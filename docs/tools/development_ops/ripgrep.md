# ripgrep (rg)

## What it is
ripgrep (rg) is a line-oriented search tool that recursively searches your current directory for a regex pattern while respecting your gitignore. As of June 2026, **v14.1.1** is the widely used stable version in production environments. It is a fundamental component of the "Agentic Ingestion" pattern, providing the high-speed search capabilities required for AI agents to navigate large codebases efficiently.

## What problem it solves
It provides extremely fast searching capabilities across large repositories, significantly outperforming legacy tools like `grep` or `ack`. It solves the "needle in a haystack" problem for both humans and AI agents, allowing them to quickly find relevant code blocks, configuration files, or stale metadata without the overhead of building a full semantic index.

## Where it fits in the stack
**Utility / CLI Tool**. A high-speed search utility often exposed to AI agents via direct tool calls or MCP servers. It serves as the primary "discovery" layer in the [Software Factory](../../knowledge_base/patterns/software-factories.md) architectural pattern.

## Typical use cases
- **Agentic Ingestion**: Quickly identifying relevant files for an LLM to read before an edit begins.
- **Repository Discovery**: Finding likely entry points, configuration files, and naming conventions in an unfamiliar codebase.
- **Multi-line search**: Locating complex patterns that span across multiple lines using the `-U` flag.
- **Stale Metadata Detection**: Auditing large documentation sets for outdated "Last reviewed" dates or low-confidence markers.

## Strengths
- **Performance**: Often faster than other search tools due to its Rust-based implementation and use of SIMD.
- **Smart Defaults**: Automatically respects `.gitignore` and ignores hidden/binary files, reducing noise.
- **Cross-platform**: Consistent behavior across Windows, macOS, and Linux.
- **Multi-line Support**: Robust support for multi-line regex searching with the `-U` flag.
- **Memory Efficiency**: Low memory footprint even when searching through gigabytes of text.

## Limitations
- **CLI-focused**: Primarily a command-line tool, requiring wrappers for programmatic library use.
- **Binary Files**: While it can search binary files with `-a`, it is optimized for text and may produce garbled output if not used carefully.
- **Non-Semantic**: Lacks the ability to perform semantic or vector-based search (use a Vector DB for "meaning" based queries).

## When to use it
- When you need to find text in a large project quickly and precisely.
- When building tools that provide search functionality to an AI agent (e.g., [Claude Code](claude-code.md)).
- For complex searches requiring PCRE2 support (`-P`).
- When performing bulk audits or find-and-replace operations across a repository.

## When not to use it
- For simple searches in a single, small file where standard `grep` is already pre-installed.
- If you need full-text indexing and semantic search (use [RAGFlow](../process_understanding/ragflow.md) or a Vector DB).
- When you require a visual, interactive search interface (use the IDE's built-in search or [Melty](melty.md)).

## Getting started
### Installation
ripgrep v14.1.1 can be installed via most major package managers.

```bash
# macOS (Homebrew)
brew install ripgrep

# Ubuntu/Debian
sudo apt-get install ripgrep

# Rust/Cargo
cargo install ripgrep
```

### Basic Usage
```bash
# Search for a pattern recursively
rg "my_pattern"
```

## CLI examples
### Agent discovery workflow
Use `rg` first when an agent needs to understand a repo without reading too much context:

```bash
# Find likely entry points and config files
rg --files -g 'package.json' -g 'pyproject.toml' -g 'go.mod' -g 'Cargo.toml'

# Locate feature ownership and existing naming
rg -n "class .*Client|def .*client|function .*Client" src tests docs

# Search only markdown docs for stale metadata
rg -n "Last reviewed: 202[0-4]|Confidence: (low|medium)" docs -g '*.md'
```

### Multi-line search
```bash
# Multi-line search for a class with a specific decorator
rg -U "\[decorator\]\nclass .*:"
```

### Token-efficiency for Agents
```bash
# Prefer -l when you only need file names to save context tokens
rg -l "OpenAI-compatible" docs/

# Use -n with narrow paths to provide precise line evidence
rg -n "TODO" src/core/
```

## API examples
While `rg` is a CLI tool, it is often invoked via subprocess or used through wrapper libraries in agentic pipelines.

### Node.js (via shell)
```javascript
const { execSync } = require('child_process');

function findInRepo(pattern) {
  try {
    const output = execSync(`rg -l "${pattern}"`).toString();
    return output.split('\n').filter(Boolean);
  } catch (err) {
    return [];
  }
}
```

### Python (Agentic Wrapper)
```python
import subprocess

def search_metadata(date_threshold):
    # Find docs that haven't been reviewed since 2024
    cmd = ["rg", "-n", f"Last reviewed: {date_threshold}", "docs", "-g", "*.md"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
```

## Related tools / concepts
- [grep](https://www.gnu.org/software/grep/) — The classic search utility.
- [fd](https://github.com/sharkdp/fd) — Fast file finding utility, often paired with `rg`.
- [Aider](aider.md) — Terminal coding agent that uses `rg` for context discovery.
- [Claude Code](claude-code.md) — High-fidelity agent that leverages `rg` for codebase navigation.
- [FZF](https://github.com/junegunn/fzf) — Fuzzy finder that can use `rg` as its back-end.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Architectural pattern for automated development.
- [Agentic Ingestion](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for feeding context to AI agents.
- [Docling](../process_understanding/docling.md) — High-performance document parsing for RAG.

## Sources / references
- [GitHub Repository](https://github.com/BurntSushi/ripgrep)
- [User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
- [ripgrep FAQ](https://github.com/BurntSushi/ripgrep/blob/master/FAQ.md)
- [Release 14.1.0 Notes](https://github.com/BurntSushi/ripgrep/releases/tag/14.1.0)
- [v14.1.1 Release Details](https://github.com/BurntSushi/ripgrep/releases)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
