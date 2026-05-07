# ripgrep (rg)

## What it is
ripgrep (rg) is a line-oriented search tool that recursively searches your current directory for a regex pattern while respecting your gitignore.

## What problem it solves
It provides extremely fast searching capabilities across large codebases. It is often used by AI agents to quickly find relevant code blocks or configuration files within a repository.

## Where it fits in the stack
[Utility / CLI Tool] - A high-speed search utility often exposed to AI agents via tools or MCP servers.

## Typical use cases
- Searching for specific strings or patterns in a large repository.
- Filtering files by type or content.
- Integration into IDEs or AI agents for codebase navigation.
- Building repeatable repository discovery commands for coding agents before edits begin.

## Strengths
- **Performance**: Often faster than other search tools like `grep`, `ack`, or `ag`.
- **Smart Defaults**: Respects `.gitignore` and ignores hidden files/binary files by default.
- **Cross-platform**: Works on Windows, macOS, and Linux.

## Limitations
- **CLI-focused**: Primarily a command-line tool, though libraries and integrations exist.
- **Not for Binary Analysis**: Designed for text files, not suitable for searching inside binary blobs.

## When to use it
- When you need to find text in a large project quickly.
- When building tools that need to provide search functionality to an AI agent.

## When not to use it
- For simple searches in a single, small file where standard `grep` is already available.
- If you need full-text indexing and semantic search (use a Vector DB instead).

## CLI examples
```bash
# Search for "FastAPI" in the current directory
rg "FastAPI"

# Search for "TODO" in .md files only
rg -t md "TODO"

# Search and replace (using sed-like output)
rg 'pattern' --replace 'replacement'
```

### Agent discovery workflow

Use `rg` first when an agent needs to understand a repo without reading too much context:

```bash
# Find likely entry points and config files
rg --files -g 'package.json' -g 'pyproject.toml' -g 'go.mod' -g 'Cargo.toml'

# Locate feature ownership and existing naming
rg -n "class .*Client|def .*client|function .*Client" src tests docs

# Search only markdown docs for stale metadata
rg -n "Last reviewed: 202[0-4]|Confidence: (low|medium)" docs -g '*.md'

# List matching files before opening large content
rg -l "OpenAI-compatible|custom base URL|Ollama" docs
```

For autonomous workflows, pair `rg --files` with targeted `rg -n` searches before broad file reads. That keeps context budgets small and makes the agent's next action easier to audit.

## Token-efficiency notes

- Prefer `rg -l` when you only need file names.
- Prefer `rg -n` with a narrow path or glob when you need line-level evidence.
- Use `--glob` or `-g` exclusions for generated output, vendored code, and large archives.
- Keep discovery commands in issue or PR comments when they explain why a file was touched.

## Getting started
### Installation
```bash
# macOS (Homebrew)
brew install ripgrep

# Ubuntu/Debian
sudo apt-get install ripgrep
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [grep](https://www.gnu.org/software/grep/)
- [The Silver Searcher (ag)](https://github.com/ggreer/the_silver_searcher)
- [Aider](../development_ops/aider.md)
- [Claude Code](../development_ops/claude-code.md)

## Sources / References
- [GitHub Repository](https://github.com/BurntSushi/ripgrep)
- [User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
- [ripgrep FAQ](https://github.com/BurntSushi/ripgrep/blob/master/FAQ.md)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
