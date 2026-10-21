# ripgrep (rg)

## What it is
ripgrep (rg) is an ultra-fast, line-oriented command-line search utility that recursively queries directories for regular expression patterns while strictly adhering to workspace exclusion rules (such as `.gitignore`, `.ignore`, and `.rgignore`). As of early January 2027, **v14.3+** represents the production standard across high-throughput software development and agentic tool pipelines. Native support for SIMD AVX-512 accelerations and structured JSON streaming makes it the foundational low-latency discovery engine powering terminal agents, IDE extensions, and Model Context Protocol (FastMCP 3.1) servers.

### High-Throughput Parallel Search Architecture

```
+-----------------------------------------------------------------------------------+
|                        RIPGREP SIMD SEARCH ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+
                                          |
  +-----------------------+     +-----------------------+     +---------------------+
  | REGEX QUERY & TARGET  | --> | DIRECTORY TRAVERSAL   | --> | EXCLUSION FILTER    |
  | PATH SPECIFICATION    |     | THREAD POOL (Rust)    |     | (.gitignore/.rgignore)
  +-----------------------+     +-----------------------+     +---------------------+
                                                                         |
                                                                         v
  +-----------------------+     +-----------------------+     +---------------------+
  | FASTMCP 3.1 SEARCH    | <-- | MEMORY-MAPPED BUFFER  | <-- | AVX-512 SIMD PATTERN|
  | EVENT STREAM (JSON)   |     | MATCH EMISSION        |     | SCANNING ENGINE     |
  +-----------------------+     +-----------------------+     +---------------------+
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

## Command-Line Search Tool Comparison Matrix

| Search Tool | Engine Language | SIMD Acceleration | `.gitignore` Support | Output Streaming Format | Memory Footprint | Indexing Lag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ripgrep (rg)** | Rust | AVX-512 / Neon | Native (Hierarchical) | Line-oriented JSON events | Minimal (<15MB) | Zero (On-demand) |
| **git grep** | C | Limited | Native (Git index) | Plain text / NULL-terminated | Low | Requires git repo |
| **silver searcher (ag)** | C | SSE4.2 | Native | Plain text / Ack style | Low | Zero |
| **ack** | Perl | None | Basic | Plain text | Moderate | Zero |
| **vector search (Chroma/pgvector)** | Python/C++ | SIMD/BLAS | Manual filter rules | JSON score vectors | High (RAM cached) | High (Background build) |

## Operational Best Practices & High-Throughput Tuning
- **Thread Count Capping**: Set `--threads N` (where N is equal to available physical CPU cores, omitting hyperthreads) when running inside containerized agent runners to avoid CPU throttling.
- **JSON Stream Buffering**: Implement line-buffered readline interfaces in wrapper processes (TypeScript/Python) to handle high-frequency match token streams without dropping memory frames.
- **Pattern Escaping**: Always pass literal strings with `-F` (`--fixed-strings`) when searching for fixed variable names or paths to bypass regular expression compilation overhead.
- **Ignore File Cascading**: Place repo-specific exclusion rules in `.rgignore` to prevent agentic searches from walking build artifacts or heavy test fixtures without modifying shared `.gitignore` rules.
- **Max File Size Guardrails**: Set `--max-filesize 5M` in automated agent invocations to avoid scanning massive minified JavaScript bundles or binary blob outputs.

## Performance Benchmark & CLI Flag Matrix

| CLI Flag | Function / Target | Throughput Impact | Recommended Agent Default |
| :--- | :--- | :--- | :--- |
| `--json` | Emits structured match events | Low overhead, enables AST parsing | **Enabled** |
| `-F / --fixed-strings` | Bypasses regex automaton | Up to 3.5x faster pattern lookup | **Enabled for literal symbols** |
| `-u / -uu / -uuu` | Bypasses `.gitignore`, hidden files, & binary filters | Higher scan volume | **Disabled (Use default filtering)** |
| `--threads N` | Binds execution worker pool | Prevents CPU contention in containers | **N = Physical Cores** |
| `--max-filesize 5M` | Skips giant files | Prevents memory spike on minified assets | **Enabled** |

## Regex Compilation & Automaton Lifecycle

```
+-----------------------------------------------------------------------------------+
|                     RIPGREP AUTOMATON LIFECYCLE & REGEX SCAN                      |
+-----------------------------------------------------------------------------------+

   +----------------+     +-------------------+     +-------------------------+
   | REGEX PATTERN  | --> | HIR COMPILATION   | --> | AVX-512 LITERAL PRE-FILTER|
   | (-P / standard)|     | (Rust Regex Core) |     | (Boyer-Moore / Teddy)   |
   +----------------+     +-------------------+     +-------------------------+
                                                               |
                                                               v
   +----------------+     +-------------------+     +-------------------------+
   | FASTMCP 3.1    | <-- | MATCH RECORDING   | <-- | DFA / NFA AUTOMATON     |
   | JSON EMISSION  |     | & LINE EXTRACTION |     | SCANNING (Zero-Copy)    |
   +----------------+     +-------------------+     +-------------------------+
```

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

### FastMCP 3.1 Search Tool Integration (Python)
Exposes ripgrep searches as a FastMCP 3.1 tool for agentic context harvesting:

```python
import subprocess
import json
import os
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RipgrepSearchServer", version="3.1.0")

class Submatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    match_text: str = Field(..., alias="match")

class MatchData(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    path: Dict[str, str]
    line_number: int
    submatches: List[Dict[str, str]]

class RipgrepMatchEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    type: str
    data: Optional[Dict] = None

class SearchQuerySpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    pattern: str = Field(..., min_length=1, description="Regex pattern or literal string to search")
    search_dir: str = Field(default=".", description="Target directory path")
    max_filesize: str = Field(default="5M", description="Max filesize threshold e.g. 5M")

@mcp.tool()
def search_repository(spec: SearchQuerySpec) -> str:
    """
    FastMCP 3.1 tool for high-performance code pattern searching using ripgrep JSON event streams.
    """
    if not os.path.exists(spec.search_dir):
        return json.dumps({"error": f"Directory '{spec.search_dir}' does not exist."})

    cmd = ["rg", "--json", "--max-filesize", spec.max_filesize, spec.pattern, spec.search_dir]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        matched_results = []

        for line in proc.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                event = RipgrepMatchEvent.model_validate_json(line)
                if event.type == "match" and event.data:
                    matched_results.append({
                        "file": event.data.get("path", {}).get("text"),
                        "line": event.data.get("line_number"),
                        "context": [s.get("match", {}).get("text") for s in event.data.get("submatches", [])]
                    })
            except Exception:
                continue
        return json.dumps({"query": spec.pattern, "results": matched_results}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

class BatchSearchSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    patterns: List[str] = Field(..., min_length=1, description="List of regex patterns to query in parallel")
    target_dir: str = Field(default=".", description="Target workspace directory")
    max_matches_per_pattern: int = Field(default=50, ge=1, le=500)

@mcp.tool()
def batch_search_patterns(batch_spec: BatchSearchSpec) -> str:
    """
    FastMCP 3.1 tool for parallel multi-pattern ripgrep execution across workspace repositories.
    """
    summary = {}
    for pat in batch_spec.patterns:
        query_spec = SearchQuerySpec(pattern=pat, search_dir=batch_spec.target_dir)
        res_raw = search_repository(query_spec)
        summary[pat] = json.loads(res_raw)
    return json.dumps({"batch_results": summary}, indent=2)

if __name__ == "__main__":
    mcp.run()
```

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
    const child = spawn('rg', ['--json', '--max-filesize', '5M', pattern, targetPath]);

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

## Troubleshooting & Diagnostic Matrix

| Symptom / Error | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **No matches returned for known files** | File path ignored by `.gitignore` or hidden by default | `rg -u "pattern" filepath` | Add path override in `.rgignore` or use `-u` / `--no-ignore` flag |
| **Memory spike during stream parsing** | Giant single-line minified file matching regex | `rg --files-with-matches "pattern"` | Set `--max-filesize 5M` and limit submatch output length |
| **Subprocess execution timeout in FastMCP** | Deep recursive traversal over unignored node_modules/build dirs | `rg --files \| wc -l` | Ensure build directories are listed in `.rgignore` or passed via `-g '!dist/*'` |
| **Regex Syntax Error (PCRE Lookaround)** | PCRE features used without enabling PCRE2 engine | `rg -P "(?<=foo)bar"` | Pass `-P` / `--pcre2` flag to explicitly enable Rust PCRE2 engine |

## Enterprise Governance & Agent Safety Guardrails

1. **Subprocess Sanitization**: FastMCP servers and wrappers must pass arguments array-formatted directly to `subprocess.run` or `spawn` without shell interpolation (`shell=False`) to avoid command injection.
2. **Secret Masking Filters**: Automated agent runs must apply pattern suppressions for credentials (e.g. `rg -g '!*.pem' -g '!*.key'`).
3. **Execution Timeouts**: Enforce a 5-second hard execution deadline on ripgrep subprocesses in automated loop agents to prevent hangs on network-mounted shares.

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
## Production Deployment & Systemd Service Architecture

For enterprise Linux servers deploying high-throughput FastMCP 3.1 ripgrep search daemon workers, deploy the following hardened `systemd` service unit:

```ini
[Unit]
Description=Ripgrep FastMCP 3.1 Code Search Gateway
After=network.target

[Service]
Type=simple
User=ripgrep-agent
Group=ripgrep-agent
WorkingDirectory=/opt/ripgrep-mcp
ExecStart=/usr/bin/python3 -m mcp.server.fastmcp run ripgrep_server.py
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=RIPGREP_MAX_FILESIZE=5M
Environment=RIPGREP_THREADS=4

# Hardened Security Guardrails
ProtectSystem=strict
ProtectHome=read-only
NoNewPrivileges=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
ReadOnlyPaths=/var/repo_storage

[Install]
WantedBy=multi-user.target
```

## Contribution Metadata
- Last reviewed: 2026-10-12
- Confidence: high
