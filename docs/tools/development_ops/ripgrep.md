# ripgrep (rg)

## What it is
ripgrep (rg) is an ultra-fast, line-oriented search utility that recursively searches the current directory for regex patterns while strictly respecting workspace exclusion rules (such as `.gitignore`, `.ignore`, and `.rgignore`). As of July 2026, **v14.1.x+** is the stable production baseline across standard enterprise architectures. In modern agentic ecosystems, ripgrep serves as the foundational low-latency discovery layer, feeding critical code slices and structural maps to frontier models (including Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6) and driving real-time codebase navigation within modern Multi-Agent Software Factories.

## What problem it solves
It solves the high-latency "needle in a haystack" lookup bottleneck inherent in massive multi-gigabyte code repositories. Traditional search methods (like standard `grep` or slower semantic embeddings) either lack the performance to execute within tight sub-second loop deadlines or require heavy index rebuilding overhead. ripgrep provides immediate, raw search capabilities by using advanced finite automata, AVX-512 SIMD multi-threading optimizations, and regex engine compilation caching, returning highly targeted results in milliseconds.

## Where it fits in the stack
**Development & Ops**. It serves as the primary high-speed text retrieval and scanning utility. Positioned at the bottom of the development stack, it is consumed directly by terminal-bound developers, orchestrator daemons, and Model Context Protocol (MCP 3.0/3.1) servers to discover context and inject relevant code snippets directly into LLM prompt contexts.

## Typical use cases
- **Multi-Threaded Agentic Codebase Scanning**: Giving autonomous agents the ability to run ultra-fast, parallelized regex audits to locate specific APIs, configuration structures, or credentials.
- **Dynamic Regex Pattern Caching**: Performing repeated, micro-targeted search loops over active workspaces without rebuilding index DBs.
- **Structured JSON Streaming**: Generating machine-readable, line-by-line JSON streams (`--json`) to feed AST-parsers or programmatic filter pipelines.
- **Selective Ignore Compliance**: Skipping large compiler outputs, node modules, build artifacts, and multi-gigabyte media files while auditing pure source structures.

## Strengths
- **SOTA Performance**: Built in Rust and optimized with AVX-512 and SIMD vector instructions, making it significantly faster than standard grep, ack, or silver searcher.
- **High Concurrency Scale**: Seamlessly scales across multi-core systems, using thread pooling to search through millions of lines in parallel.
- **JSON Stream Output**: Natively streams search events (begin, match, context, end) in structured JSON format, enabling simple piping into agent memory.
- **Smart Ignore Hierarchy**: Automatically respects `.gitignore`, `.ignore`, and custom `.rgignore` configurations to prevent token-bloating and noise.
- **Memory Efficiency**: Employs lazy memory mapping and optimized buffer-sharing, maintaining a highly stable and minimal RAM profile under extreme load.

## Limitations
- **CLI-Native Architecture**: Primarily designed as a command-line binary; requires shell execution wrappers or subprocess handling for integration into Node.js or Python codebases.
- **Zero Semantic Insight**: Completely reliant on regex and exact character sequences; cannot locate synonymous terms or resolve conceptual/semantic relationships (requires pairing with a hybrid [RAGFlow](../process_understanding/ragflow.md) architecture).
- **Disk I/O Bound**: In environments with slow or virtual network file systems, concurrent thread scaling can saturate disk channels if limits are not configured.

## When to use it
- When an autonomous agent (e.g., [Claude Code](claude-code.md) or [Junie CLI](junie-cli.md)) needs to scan an entire codebase for functional entry points or schema patterns within sub-second thresholds.
- When performing bulk find-and-replace, metadata extraction, or repository auditing in pipelines.
- When configuring Model Context Protocol (MCP 3.0/3.1) file-search tools that require high accuracy and strict exclusion compliance.

## When not to use it
- When you require natural language, semantic, or conceptual query matching (use a vector database or hybrid retrieval framework).
- When looking for exact files by name rather than content (use `fd` or a specialized file listing tool).
- For simple, single-file searches inside a graphical editor where local editor-buffer searching is already immediate.

## Getting started
### Installation
ripgrep v14.1.x can be installed across standard operating platforms using default package managers:

```bash
# macOS (Homebrew)
brew install ripgrep

# Ubuntu / Debian
sudo apt-get install ripgrep

# Alpine Linux
apk add ripgrep

# Cargo (Rust package manager)
cargo install ripgrep
```

### Verification
Confirm the installation and check the current stable version details:

```bash
rg --version
```

## CLI examples
### Advanced Agentic Scanning
Stream structural JSON matches from files containing specific authentication endpoints while ignoring test directories:

```bash
# Stream match details structured as line-oriented JSON
rg --json "registerUser|authenticateSession" src/ -g '!*test*'
```

### Concurrency and Core Bounding
In cloud environments or multi-agent runtimes, bound thread execution to prevent CPU starvation:

```bash
# Restrict ripgrep execution to exactly 2 worker threads
rg --threads 2 "api_endpoint_v3" src/core/
```

### Multi-line Regex Search
Locate multi-line declarations with custom regex patterns using the `-U` (undisturbed/multi-line) flag:

```bash
# Match decorators immediately preceding a class declaration
rg -U -P "@Injectable\(\)\nclass\s+\w+Service" src/
```

### Token-Conscious Discovery
When querying for large lists to feed into LLMs, restrict output to filenames only to save input token costs:

```bash
# Return only the names of files containing the target string
rg -l "deprecatedAuthMethod" docs/tools/
```

## API examples
To build seamless agent toolkits, ripgrep's CLI is typically wrapped programmatically to parse JSON streams.

### Node.js (High-Speed Stream Processor)
This example spawns a ripgrep process with `--json` output, streaming and parsing match events dynamically:

```typescript
import { spawn } from 'child_process';
import { readline } from 'readline';

interface RgMatch {
  path: { text: string };
  line_number: number;
  submatches: Array<{ match: { text: string } }>;
}

export function streamRepoSearch(pattern: string, targetPath: string): Promise<RgMatch[]> {
  return new Promise((resolve, reject) => {
    const matches: RgMatch[] = [];
    const rg = spawn('rg', ['--json', pattern, targetPath]);

    const rl = readline.createInterface({
      input: rg.stdout,
      terminal: false
    });

    rl.on('line', (line) => {
      try {
        const payload = JSON.parse(line);
        if (payload.type === 'match') {
          matches.push({
            path: payload.data.path,
            line_number: payload.data.line_number,
            submatches: payload.data.submatches
          });
        }
      } catch (err) {
        // Handle malformed JSON chunks gracefully
      }
    });

    rg.on('close', (code) => {
      if (code === 0 || code === 1) { // 1 indicates no matches found
        resolve(matches);
      } else {
        reject(new Error(`ripgrep exited with code ${code}`));
      }
    });
  });
}
```

### Python (Multi-Threaded Agentic Search Wrapper)
This Python script simulates a workspace search tool for agent execution, enforcing regex compiling, core limits, and JSON stream compilation:

```python
import subprocess
import json
import os
from typing import List, Dict

def execute_agentic_search(pattern: str, search_dir: str, thread_limit: int = 4) -> List[Dict]:
    """
    Executes a high-speed ripgrep command with JSON streaming and thread-bounding.
    Returns a structured list of match results.
    """
    if not os.path.exists(search_dir):
        return []

    cmd = [
        "rg",
        "--json",
        "--threads", str(thread_limit),
        "--ignore-case",
        pattern,
        search_dir
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        matches = []

        # Parse the line-oriented JSON stream
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get("type") == "match":
                    match_data = data["data"]
                    matches.append({
                        "file": match_data["path"]["text"],
                        "line": match_data["line_number"],
                        "text": "".join([sub["match"]["text"] for sub in match_data["submatches"]])
                    })
            except json.JSONDecodeError:
                continue

        return matches
    except Exception as e:
        print(f"Error executing search: {e}")
        return []

if __name__ == "__main__":
    results = execute_agentic_search("Last reviewed:", "docs/", thread_limit=2)
    print(f"Discovered {len(results)} fresh metadata pointers.")
```

## Related tools / concepts
- [Aider](aider.md) — For terminal-based, interactive collaborative pair programming and incremental editing.
- [Claude Code](claude-code.md) — Interactive terminal coding agent from Anthropic leveraging high-speed search tools.
- [Junie CLI](junie-cli.md) — Blazing-fast JetBrains AI Lab terminal companion natively embedding ripgrep queries.
- [Melty](melty.md) — Open-source AI-native IDE offering deep shell and git execution loops.
- [Terminus 2](terminus-2.md) — Terminal-native AI agent baseline leveraging a tmux-to-LLM bridge.
- [Droid](droid.md) — Specialized enterprise-grade coding orchestrator configuring dedicated sub-agents.
- [Zed](zed.md) — High-performance, collaborative AI-native visual text editor.
- [Docling](../process_understanding/docling.md) — High-performance document parsing for structural knowledge base assembly.
- [RAGFlow](../process_understanding/ragflow.md) — Open-source RAG engine and layout analyzer for document comprehension.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Conceptual architectures for fully automated code production lines.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Recurring patterns for multi-step AI planning and execution.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized tool integration protocol natively supported by modern search tools.

## Sources / references
- [BurntSushi/ripgrep GitHub Repository](https://github.com/BurntSushi/ripgrep)
- [ripgrep User Guide & Benchmark Methodology](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
- [Model Context Protocol v3.0 Specification](https://modelcontextprotocol.org)
- [Rust SIMD Vectorization Reference](https://doc.rust-lang.org/stable/std/simd/index.html)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
