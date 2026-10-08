# ripgrep (rg)

## What it is
ripgrep (rg) is an ultra-fast, line-oriented command-line search utility that recursively queries directories for regular expression patterns while strictly adhering to workspace exclusion rules (such as `.gitignore`, `.ignore`, and `.rgignore`). As of early January 2027, **v14.3+** represents the production standard across high-throughput software development and agentic tool pipelines. Native support for SIMD AVX-512 accelerations and structured JSON streaming makes it the foundational low-latency discovery engine powering terminal agents, IDE extensions, and Model Context Protocol (FastMCP 3.1) servers.

## Architecture & System Overview
ripgrep achieves its performance by pairing a Rust-based, highly concurrent multithreaded directory walker with SIMD-accelerated regex string matching routines.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            RIPGREP (RG) ARCHITECTURE                             │
└──────────────────────────────────────────────────────────────────────────────────┘

   Target Path / Working Directory
                │
                ▼
  ┌───────────────────────────┐
  │ Parallel Directory Walker │ ──> Reads .gitignore / .ignore / .rgignore
  └───────────────────────────┘
                │ (Pipes file descriptors)
                ▼
  ┌───────────────────────────┐
  │ Thread Pool (Rust Rayon)  │
  └───────────────────────────┘
        │               │
        ▼               ▼
  ┌───────────┐   ┌───────────┐
  │ Worker 1  │   │ Worker 2  │ ──> Memory Mapped Buffers (mmap)
  └───────────┘   └───────────┘
        │               │
        ▼               ▼
  ┌───────────────────────────┐
  │  AVX-512 SIMD Regex Match │ ──> SOTA Automata / Teddy String Matcher
  └───────────────────────────┘
                │
                ▼
  ┌───────────────────────────┐
  │  JSON Stream Event Engine │ ──> Programmatic Output (begin, match, end)
  └───────────────────────────┘
```

## What problem it solves
It resolves the high-latency search bottleneck in massive, multi-gigabyte code repositories. Traditional grep implementations or heavy vector indexing systems are either too slow for immediate real-time lookups or require significant pre-computation overhead. ripgrep delivers immediate search results in milliseconds by utilizing advanced finite automata, AVX-512 SIMD hardware optimizations, multi-threaded directory traversal, and memory-mapped buffers.

## Where it fits in the stack
**Development & Ops**. It resides at the **Foundational Discovery Layer**, providing high-performance text-scanning capabilities directly consumed by shell environments, terminal multiplexers, and agentic workflows (such as [Claude Code](claude-code.md), [Junie CLI](junie-cli.md), and [OpenCode](opencode.md)).

## Typical use cases
- **Multi-Threaded Code Audits**: Scanning an entire repository for specific functions, configuration patterns, or deprecated APIs in milliseconds.
- **Dynamic Context Harvesting**: Automatically finding and feeding relevant code blocks or configuration parameters into LLM prompt contexts for models like Claude 5.6, GPT-5.6, or DeepSeek-V4.
- **JSON Stream Pipeline Parsing**: Spawning ripgrep with the `--json` flag to feed line-by-line matches directly into AST parsers or multi-agent memory frameworks.
- **Strict File-Pattern Isolation**: Isolating searches to specific file patterns (e.g., `-g '*.ts'`) while honoring git exclusion files.

## Comparison Matrix

| Feature | ripgrep (rg) | grep (GNU) | git grep | fd / find |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Line-oriented code search | General text search | Git repository search | File path & name search |
| **Indexing Required** | None (On-the-fly) | None | None | None |
| **Concurrency Model** | Multi-threaded Lock-free | Single-threaded | Multi-threaded | Multi-threaded |
| **Gitignore Support** | Native & Automatic | No | Native (within repo) | Native & Automatic |
| **JSON Event Stream** | Native (`--json`) | No | No | No |
| **Hardware Accel** | SIMD (AVX-512/Neon) | Basic libc | Basic libc | File system walker |

## Strengths
- **AVX-512 SIMD Acceleration**: Leverages modern CPU instruction sets for SOTA raw pattern-matching throughput.
- **Strict Ignore Compliance**: Honors `.gitignore` hierarchies natively, saving inputs from token bloat and scanning noise.
- **Concurrency-Optimized Core**: Seamlessly scales across multiple CPU cores via highly efficient Rust thread pooling.
- **Lightweight Footprint**: Features extremely predictable memory consumption and no startup indexing lag.
- **Structured JSON Event Streaming**: Emits rich, line-oriented JSON representations of match events (begin, match, end) perfect for programmatic consumers.

## Limitations
- **Syntax and Literal Bound**: Entirely reliant on explicit character matches or regular expressions; lacks native semantic or natural language query understanding.
- **Local Filesystem Centric**: Designed for direct disk storage paths; remote filesystems require mounting or network caching protocols.
- **Shell Execution Overhead**: Integrating with Node.js or Python requires running a subprocess, requiring careful input sanitization to prevent shell-injection vulnerabilities.

## When to use it
- When an autonomous agent (such as [Claude Code](claude-code.md) or [Junie CLI](junie-cli.md)) needs to locate functional targets or system schemas across massive code bases within sub-second thresholds.
- When executing high-concurrency regex audits in continuous integration/continuous deployment (CI/CD) pipelines.
- When configuring search-tools for Model Context Protocol (FastMCP 3.1) servers where reliability and speed are paramount.

## When not to use it
- When you require natural language search queries, semantic synonym matching, or multi-modal conceptual lookups (pair with hybrid vector solutions instead).
- When looking for exact file metadata or files by name rather than actual contents (use specialized listing tools like `fd`).

## Getting started

### Installation
Install ripgrep v14.3+ across standard platforms using default package managers:

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
Verify that the binary is available and supports SIMD accelerations:
```bash
rg --version
```

## CLI examples
Use the command-line flags to tune search precision and machine readability.

### Machine-Readable Structured Event Streaming
```bash
# Output line-oriented JSON event streams while ignoring test directories
rg --json "executeTaskLoop|FastMCP" src/ -g '!*test*'
```

### Constraining Concurrency in Resource-Bounded Environments
```bash
# Force ripgrep to utilize exactly two worker threads to prevent CPU starvation
rg --threads 2 "api_token_v3" src/core/
```

### Multi-Line RegEx Pattern Matching
```bash
# Query multiline structures with -U (undisturbed/multiline) and -P (Perl-compatible) regex
rg -U -P "@Service\(\)\nclass\s+\w+Impl" src/
```

## API examples

### Node.js Event-Stream Receiver (TypeScript)
Spawn ripgrep and parse raw structured JSON match tokens:

```typescript
import { spawn } from 'child_process';
import { createInterface } from 'readline';

export interface RgMatchEvent {
  path: string;
  line: number;
  content: string;
}

export function streamWorkspaceSearch(pattern: string, targetPath: string): Promise<RgMatchEvent[]> {
  return new Promise((resolve, reject) => {
    const events: RgMatchEvent[] = [];
    const child = spawn('rg', ['--json', pattern, targetPath]);

    const rl = createInterface({
      input: child.stdout,
      terminal: false
    });

    rl.on('line', (line) => {
      try {
        const payload = JSON.parse(line);
        if (payload.type === 'match') {
          const matchData = payload.data;
          events.push({
            path: matchData.path.text,
            line: matchData.line_number,
            content: matchData.lines.text.trim()
          });
        }
      } catch (err) {
        // Soft-fail on malformed stream slices
      }
    });

    child.on('close', (code) => {
      if (code === 0 || code === 1) {
        resolve(events);
      } else {
        reject(new Error(`ripgrep failed with exit code ${code}`));
      }
    });
  });
}
```

### Python Programmatic Search & Pydantic v2 Event Validation
Spawns ripgrep, reads its JSON streaming output, and maps each match using Pydantic v2 schemas:

```python
import subprocess
import json
import os
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any

class Submatch(BaseModel):
    model_config = ConfigDict(extra="ignore")
    match_text: str = Field(..., alias="match")

class MatchData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    path: Dict[str, str]
    line_number: int
    submatches: List[Dict[str, Any]]

class RipgrepMatchEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: str
    data: Optional[MatchData] = None

def run_agentic_grep(pattern: str, search_dir: str) -> List[Dict]:
    """Runs high-performance ripgrep with JSON streaming and parses matching nodes."""
    if not os.path.exists(search_dir):
        return []

    cmd = ["rg", "--json", pattern, search_dir]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        matched_results = []

        for line in proc.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                # Strictly validate streaming chunk via Pydantic v2
                event = RipgrepMatchEvent.model_validate_json(line)
                if event.type == "match" and event.data:
                    file_path = event.data.path.get("text", "")
                    matched_results.append({
                        "file": file_path,
                        "line": event.data.line_number,
                        "context": event.data.submatches
                    })
            except Exception:
                continue
        return matched_results
    except Exception as e:
        print(f"Error running search pipeline: {e}")
        return []

if __name__ == "__main__":
    results = run_agentic_grep("Last reviewed:", "docs/")
    print(f"Discovered {len(results)} matches.")
```

### FastMCP 3.1 Integration Code Pattern
Exposes ripgrep high-performance searching directly to agentic environments as a FastMCP 3.1 tool.

```python
import subprocess
import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ripgrep-code-search",
    instructions="Provides ultra-fast, line-oriented regular expression search across source repositories."
)

class SearchInput(BaseModel):
    pattern: str = Field(..., description="Regex pattern or literal string to search for.")
    path: str = Field(".", description="Root directory or file path to query.")
    file_glob: Optional[str] = Field(None, description="Optional file glob pattern (e.g. '*.py' or '!*test*').")
    max_results: int = Field(50, ge=1, le=500, description="Max results to return.")

@mcp.tool()
async def execute_ripgrep_search(input_data: SearchInput) -> List[Dict[str, Any]]:
    """Executes ripgrep search and returns structured match metadata."""
    cmd = ["rg", "--json", input_data.pattern, input_data.path]
    if input_data.file_glob:
        cmd.extend(["-g", input_data.file_glob])

    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    matches = []

    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            if payload.get("type") == "match":
                data = payload.get("data", {})
                matches.append({
                    "file": data.get("path", {}).get("text"),
                    "line": data.get("line_number"),
                    "matched_text": data.get("lines", {}).get("text", "").strip()
                })
                if len(matches) >= input_data.max_results:
                    break
        except json.JSONDecodeError:
            continue

    return matches

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting
- **Input Sanitization**: When invoking ripgrep as a subprocess in production agents, pass commands as an array of string arguments (`execFile`/`subprocess.run`) rather than concatenating shell strings to prevent shell-injection exploits.
- **Large Binary Exclusion**: Pass `--no-ignore-vcs` sparingly. Use `--binary-files=without-match` to prevent non-text files from polluting token contexts.
- **Worker Thread Allocation**: In containerized agent runtime environments (Docker/K8s), constrain `--threads` to match container CPU quotas and avoid thread starvation.

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Junie CLI](junie-cli.md)
- [Aider](aider.md)
- [Melty](melty.md)
- [Terminus 2](terminus-2.md)
- [Droid](droid.md)
- [Zed](zed.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [BurntSushi/ripgrep GitHub Repository](https://github.com/BurntSushi/ripgrep)
- [ripgrep Benchmarking and Architecture Methodology](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.org)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
