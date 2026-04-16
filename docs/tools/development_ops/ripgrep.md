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

## Contribution Metadata
- Last reviewed: 2026-03-19
- Confidence: high
