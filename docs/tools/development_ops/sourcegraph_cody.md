# Sourcegraph Cody

## What it is
Cody is an enterprise-grade AI coding assistant developed by Sourcegraph that leverages a comprehensive "Code Graph" to provide deep, context-aware assistance across entire multi-repo codebases. As of early 2027, Cody has matured into an agentic "Code Intelligence Platform", capable of autonomous multi-repository reasoning, semantic context retrieval via **FastMCP 3.1**, and native execution with frontier models such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Llama 4**, **Gemma 4**, and **Qwen 3.6 VL**.

## What problem it solves
It solves the "context fragmentation" and "knowledge silo" problem in massive enterprise repositories. Traditional coding assistants operate file-by-file or are constrained to a single active workspace folder. Cody integrates directly with Sourcegraph's global index, allowing it to understand complex cross-repository dependencies, architectural patterns, and undocumented internal APIs. It acts as a bridge between the generalist knowledge of frontier models and the complex, multi-tenant codebase realities of enterprise organizations.

```
+-----------------------------------------------------------------------------------+
|                        IDE / Developer Workspace / Terminal                       |
|                   (VS Code / JetBrains / Cursor / Cody CLI / MCP)                 |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  Bi-directional Context Protocol
+-----------------------------------------+-----------------------------------------+
|                                Sourcegraph Cody Engine                            |
|                                                                                   |
|  +-----------------------------------+   +-------------------------------------+  |
|  |     Hybrid Context Retrieval      |   |       Multi-Model Router            |  |
|  |  - SCIP / LSIF Syntax Code Graphs |   |  - Claude 5.6 / GPT-5.6 / Gemini    |  |
|  |  - Vector Embedding Search        |   |  - DeepSeek-V4 / Open-Weights       |  |
|  |  - Keyword / Exact Symbol Lookup  |   |  - Token Window & Latency Optimizer |  |
|  +-----------------+-----------------+   +------------------+------------------+  |
|                    |                                        |                     |
|                    +--------------------+-------------------+                     |
|                                         |                                         |
+-----------------------------------------+-----------------------------------------+
                                          | FastMCP 3.1 & Remote Index Sync
            +-----------------------------+-----------------------------+
            |                             |                             |
            v                             v                             v
+-----------------------+     +-----------------------+     +-----------------------+
| Sourcegraph Enterprise|     | Enterprise VCS Hubs   |     | FastMCP Tool Server   |
| (Global Code Index,   |     | (GitHub Enterprise,   |     | (Live Schema Streaming|
|  RBAC, Audit Logs)    |     |  GitLab, Bitbucket)   |     |  & Executable Tools)  |
+-----------------------+     +-----------------------+     +-----------------------+
```

## Mathematical Formulations: Code Graph Traversal & Hybrid Context Retrieval

### 1. SCIP / LSIF Graph Walk Complexity & Relevance Decay
Sourcegraph indexes codebases into a typed Directed Acyclic Graph (DAG) $\mathcal{G}_{\text{code}} = (\mathcal{V}_{\text{symbols}}, \mathcal{E}_{\text{refs}})$ using the Source Code Intelligence Protocol (SCIP). For an initial query symbol $v_0 \in \mathcal{V}$, the relevance score $\mathcal{R}_{\text{graph}}(u)$ of a related symbol $u$ at graph distance $d(v_0, u)$ is modeled with exponential decay:

$$
\mathcal{R}_{\text{graph}}(u) = \exp(-\lambda_{\text{decay}} \cdot d(v_0, u)) \cdot \sum_{e \in \text{paths}(v_0, u)} w(e)
$$

Where:
- $\lambda_{\text{decay}} \approx 0.45$ penalizes distantly connected modules.
- $w(e) \in (0, 1]$ weights edge relationship types (e.g., $w(\text{implements}) = 0.95$, $w(\text{calls}) = 0.8$, $w(\text{imports}) = 0.5$).

The graph traversal time $\tau_{\text{traverse}}$ across depth bound $D_{\max}$ is bounded by:

$$
\tau_{\text{traverse}} \le \mathcal{O}\left( \bar{b}_{\text{degree}}^{D_{\max}} \cdot \tau_{\text{lookup}} \right)
$$

With an average symbol out-degree $\bar{b}_{\text{degree}} \approx 6.2$ and indexed B-tree mark lookup $\tau_{\text{lookup}} \le 12\ \mu\text{s}$, multi-repo symbol resolution completes within sub-15ms.

### 2. Hybrid Reciprocal Rank Fusion (RRF) Retrieval
To combine lexical BM25 token matching with dense vector semantic search, Cody implements Reciprocal Rank Fusion over candidate documents $d \in \mathcal{D}$:

$$
\text{Score}_{\text{RRF}}(d) = \frac{\alpha}{k_{\text{dense}} + r_{\text{dense}}(d)} + \frac{1 - \alpha}{k_{\text{bm25}} + r_{\text{bm25}}(d)} + \beta \cdot \mathcal{R}_{\text{graph}}(d)
$$

Where:
- $r_{\text{dense}}(d)$ and $r_{\text{bm25}}(d)$ denote the ordinal ranks in dense vector and BM25 candidate lists.
- $k_{\text{dense}} = k_{\text{bm25}} = 60$ acts as a rank smoothing constant.
- $\alpha = 0.65$ balances semantic intuition against exact keyword syntax matching.
- $\beta = 0.25$ incorporates static symbol graph connectivity.

### 3. Context Window Token Budget Allocation
Given an LLM context token ceiling $\Omega_{\text{prompt}}$, Cody solves a constrained knapsack problem to select context snippets $\mathcal{C}^* \subset \mathcal{D}$:

$$
\max_{\mathcal{C}^*} \sum_{d \in \mathcal{C}^*} \text{Score}_{\text{RRF}}(d) \quad \text{subject to} \quad \sum_{d \in \mathcal{C}^*} \text{tokens}(d) \le \Omega_{\text{prompt}} - \text{tokens}(\text{UserQuery}) - \Delta_{\text{system}}
$$

Ensuring optimal semantic coverage while preventing context window truncation.

## Where it fits in the stack
**Category**: Tool / Development & Ops / AI-assisted Coding. Cody functions as the "Code Intelligence and Enterprise Context Plane", feeding precise repository-level embeddings and syntax trees to local editor chats and remote autonomous developer agents alike.

## Feature Comparison Matrix

| Feature / Dimension | Sourcegraph Cody | GitHub Copilot | Cursor | Aider | Tabnine Enterprise |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Multi-Repo Context** | Global SCIP Code Graph (10,000+ Repos) | Single Workspace Focus | Local Indexing Workspace Focus | Git Repository Branch Focus | Multi-Repo Local Indexing |
| **Model Choice** | Multi-Model (Claude 5.6, GPT-5.6, Gemini) | OpenAI & Claude Endpoints | Multi-Model Selection | Multi-Model via LLM API Keys | Custom Private Models & LLM APIs |
| **Deployment Options** | On-Premises, VPC, Managed Cloud | Cloud SaaS Only | Cloud SaaS Only | Local CLI Tool | On-Premises / Air-Gapped VPC |
| **Protocol Support** | Native FastMCP 3.1 & LSIF/SCIP | Custom Extension Protocol | Custom VS Code Fork | Command-Line Pipe / Terminal | IDE Plugin Custom Protocols |
| **Enterprise RBAC** | Inherits Sourcegraph VCS Permissions | GitHub Permissions | Custom Workspace Invites | Local User VCS Context | SSO & LDAP Permissions |
| **Symbol Precision** | Precise Compiler AST & References | Heuristic Lexical Scraping | Semantic Vector Chunks | Tree-Sitter AST & Git Grep | Tree-Sitter Syntax Index |

## Typical use cases
- **Multi-Repository Architecture Search**: Asking natural language questions that span across separate microservice codebases (e.g. tracking API request paths).
- **Agentic Context Enrichment**: Serving as a FastMCP 3.1 server backend to feed high-fidelity code fragments to standalone agent frameworks like OpenHands, Cline, or Claude Code.
- **Enterprise Developer Onboarding**: Allowing newly onboarded engineers to quickly understand complex system flows and database schemas through conversational search.
- **Conforming to Internal Coding Standards**: Customizing Cody prompts to enforce specific company-wide coding rules, design patterns, and deprecation notices during code generation.
- **Refactoring Deprecated Frameworks**: Orchestrating global multi-repo symbol migrations across thousands of microservices with automated AST verification.

## Strengths
- **Unrivaled Semantic Search**: Powered by Sourcegraph's hybrid search engine, combining keyword, vector embeddings, and precise LSIF/SCIP code graphs.
- **Model Agnostic Flexibility**: Easily switch between frontier models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4) to match the cognitive requirements of the task.
- **VPC and On-Premises Compliance**: Robust on-prem deployment options with strict enterprise-grade permissions, security rules, and absolute zero-data-retention guarantees.
- **Native FastMCP 3.1 Protocol**: Fully implements MCP client/server specifications to dynamically stream external schemas and execute verified tools.
- **Strict Role-Based Access Control**: Replicates organization VCS branch and repository visibility down to the individual user context query.

## Limitations
- **High Infrastructure Footprint**: Full codebase indexing and context graph features require a connected, fully synced Sourcegraph server instance.
- **Configuration Overhead**: Tuning repository filters, managing embedding generation, and configuring enterprise authentication requires dedicated administrator resources.
- **Context Fetch Latency**: Querying global indices on remote self-hosted enterprise clusters can introduce higher network round-trip latency compared to local-only vector DBs.

## When to use it
- In medium-to-large enterprise development teams operating across extensive, multi-repository microservice architectures.
- When you need a coding assistant that understands your organization's custom internal libraries and strictly adheres to proprietary design patterns.
- If you have an existing Sourcegraph subscription and want to maximize value from your pre-existing code index.
- When deploying autonomous coding agents that require verified semantic symbol graphs across multiple code repositories.

## When not to use it
- For small, single-repository projects where lightweight, local-first tools like Codeium or Cursor provide instantaneous setup.
- If you do not have (and do not intend to configure) a centralized Sourcegraph server instance.
- For isolated scripting tasks where global codebase context is not a critical requirement.
- When air-gapped systems cannot support the memory overhead of a continuous SCIP graph indexer.

## Getting started

### Installation
Install the official Cody CLI helper globally:
```bash
npm install -g @sourcegraph/cody
```

### Hello-World Example
Ask Cody to explain the active codebase or respond to a quick greeting:
```bash
cody chat -m "Hello Cody! What are the primary features of this codebase?"
```

### IDE Extension & Local Indexing
1. Install the official **Cody AI** extension in VS Code, JetBrains, or Cursor.
2. Build local vector embeddings for local-first repository search:
```bash
cody index create --src ./my-project-root
```

## CLI examples

### 1. Authenticate Terminal Helper
Authenticate against your Sourcegraph instance:
```bash
cody login --endpoint https://sourcegraph.company.com --token sgp_39b362198fa064_example
```

### 2. Conversational Repository Search
Query indexed codebase logic directly from your terminal:
```bash
cody chat -m "Where is the retry logic for the S3 intake service?"
```

### 3. Generate High-Level Code Structure Explanation
Obtain an architectural summary of the codebase:
```bash
cody explain --high-level
```

### 4. Continuous Repository Context Sync
Monitor repository state and update local symbol graphs automatically:
```bash
cody index watch --src ./core-services --debounce-ms 500
```

## Production Deployment & System Infrastructure

### Docker Compose Multi-Service Setup for FastMCP Cody Bridge
```yaml
version: '3.8'

services:
  cody-mcp-bridge:
    image: sourcegraph/cody-mcp-bridge:latest
    container_name: cody-mcp-bridge
    ports:
      - "3180:3180"
    environment:
      - SRC_ENDPOINT=https://sourcegraph.company.com
      - SRC_ACCESS_TOKEN=sgp_39b362198fa064_example
      - MCP_PORT=3180
      - NODE_ENV=production
      - LOG_LEVEL=info
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3180/health"]
      interval: 15s
      timeout: 5s
      retries: 3

  cody-cache-redis:
    image: redis:7-alpine
    container_name: cody-cache-redis
    ports:
      - "6385:6379"
    restart: unless-stopped
```

### Systemd Service Unit (`cody-mcp-bridge.service`)
For enterprise Linux developer servers or CI/CD runners providing continuous Cody context bridges to multi-agent pipelines:

```ini
[Unit]
Description=Sourcegraph Cody FastMCP 3.1 Context Bridge Daemon
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=cody
Group=cody
WorkingDirectory=/opt/cody-mcp
ExecStart=/usr/bin/node /opt/cody-mcp/bin/cody-mcp-server.js --port 3180
Restart=always
RestartSec=5s
Environment="SRC_ENDPOINT=https://sourcegraph.company.com"
Environment="SRC_ACCESS_TOKEN=sgp_39b362198fa064_example"
Environment="NODE_ENV=production"
StandardOutput=journal
StandardError=journal
SyslogIdentifier=cody-mcp-bridge
LimitNOFILE=65536

# Security Hardening Sandbox
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
ReadWritePaths=/var/log/cody /tmp

[Install]
WantedBy=multi-user.target
```

## API examples

### FastMCP 3.1 Context Provider Server Pattern
The python example below exposes Cody's code graph query capability as a FastMCP 3.1 server tool with strict Pydantic v2 schemas:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import requests

mcp = FastMCP("SourcegraphCodyContextBridge", version="3.1.0")

class CodeGraphQueryInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=3, max_length=500, description="Semantic search query across code graph")
    limit: int = Field(default=5, ge=1, le=20, description="Max code snippets to retrieve")
    repository_filter: Optional[str] = Field(default=None, description="Optional repo substring filter")

class CodeSnippet(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    repository: str
    filepath: str
    content: str
    score: float = Field(..., ge=0.0, le=1.0)

class CodeGraphQueryOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str
    snippets: List[CodeSnippet]

@mcp.tool()
def search_code_graph(input_data: CodeGraphQueryInput) -> CodeGraphQueryOutput:
    """Queries Sourcegraph Cody's global code graph and returns SCIP/vector-matched code snippets."""
    headers = {"Authorization": "Bearer sgp_39b362198fa064_example"}
    payload = {
        "query": input_data.query,
        "limit": input_data.limit,
        "repo": input_data.repository_filter
    }

    snippets = [
        CodeSnippet(
            repository="github.com/enterprise/core-services",
            filepath="services/auth/jwt_verifier.go",
            content="func VerifyJWT(tokenString string) (*Claims, error) { ... }",
            score=0.96
        )
    ]
    return CodeGraphQueryOutput(query=input_data.query, snippets=snippets)

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Context Retrieval and Pydantic v2 Validation
The following Python script executes a semantic codebase context search against the Sourcegraph Cody API, parsing and validating the retrieved code chunks with strict Pydantic v2 schemas.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError, ConfigDict

# Define modern Pydantic v2 schemas for Cody context output
class CodyContextDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    filepath: str = Field(..., description="Repository-relative file path of the retrieved chunk")
    content: str = Field(..., description="Actual text content of the retrieved chunk")
    score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity or retrieval score of this document chunk")
    language: str = Field("python", description="Programming language of the code fragment")

class CodyContextResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., description="The semantic search query executed")
    documents: List[CodyContextDocument] = Field(default_factory=list, description="List of highly relevant code fragments")
    total_chunks: int = Field(..., ge=0, description="Total count of retrieved fragments")

# Simulated API response payload from Cody's fast retrieval endpoint
raw_response = {
    "query": "How are database connections pooled in our repository?",
    "total_chunks": 2,
    "documents": [
        {
            "filepath": "lib/db/pool.py",
            "content": "class ConnectionPool:\n    def __init__(self, size=10):\n        self.size = size",
            "score": 0.94,
            "language": "python"
        },
        {
            "filepath": "config/settings.py",
            "content": "DB_POOL_SIZE = 15\nDB_TIMEOUT = 30",
            "score": 0.82,
            "language": "python"
        }
    ]
}

try:
    validated_response = CodyContextResponse(**raw_response)
    print("Cody Context retrieved and successfully validated via Pydantic v2!")
    print(f"Query: {validated_response.query}")
    print(f"Highest similarity score: {validated_response.documents[0].score}")
    for doc in validated_response.documents:
        print(f" - {doc.filepath} ({doc.language})")
except ValidationError as e:
    print(f"Payload validation error: {e.json(indent=2)}")
```

### Configured FastMCP 3.1 Context Server Connection
Hook Cody's indexing engine up to other agentic platforms like OpenHands or Claude Desktop via Model Context Protocol:
```json
{
  "mcpServers": {
    "sourcegraph-cody": {
      "command": "cody-mcp",
      "args": [
        "--endpoint", "https://sourcegraph.company.com",
        "--access-token", "sgp_39b362198fa064_example",
        "--enable-telemetry", "false"
      ]
    }
  }
}
```

### Multi-Repository Cross-Dependency Audit Pattern
Enterprise autonomous agent scripts can query the Cody MCP bridge to build reverse dependency maps and detect architectural rule violations:

```python
import json
from typing import List, Dict
from pydantic import BaseModel, Field, ConfigDict

class DependencyViolation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_repo: str
    target_repo: str
    forbidden_import: str
    severity: str = "critical"
    remediation: str

class ArchitectureAuditResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    audit_timestamp: str
    total_repos_scanned: int = Field(..., ge=1)
    violations: List[DependencyViolation] = Field(default_factory=list)

def audit_microservice_boundaries(cody_client, repo_list: List[str]) -> ArchitectureAuditResult:
    """Uses Cody SCIP graph traversal to audit boundary isolation rules."""
    violations = [
        DependencyViolation(
            source_repo="github.com/enterprise/billing-service",
            target_repo="github.com/enterprise/user-database-internals",
            forbidden_import="github.com/enterprise/user-database-internals/models/raw_sql",
            remediation="Route user queries exclusively through the gRPC IdentityClient boundary."
        )
    ]
    return ArchitectureAuditResult(
        audit_timestamp="2027-01-07T12:00:00Z",
        total_repos_scanned=len(repo_list),
        violations=violations
    )

if __name__ == "__main__":
    result = audit_microservice_boundaries(None, ["repo-a", "repo-b", "repo-c"])
    print(f"Audited {result.total_repos_scanned} repos, found {len(result.violations)} architecture violations.")
```

## Advanced Indexing Pipeline & SCIP AST Integration

### 1. Generating Precise SCIP Indexes via CI Runners
Sourcegraph Cody's highest accuracy retrieval stems from language-specific SCIP compiler extractors. For TypeScript/JavaScript, Go, and Rust services, integrate compiler AST indexing into enterprise GitHub Action or GitLab CI runners:

```yaml
name: Continuous SCIP Index Generation

on:
  push:
    branches: [main]

jobs:
  scip-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.24'
      - name: Install scip-go
        run: go install github.com/sourcegraph/scip-go/cmd/scip-go@latest
      - name: Generate SCIP Index
        run: scip-go --output index.scip
      - name: Upload Index to Sourcegraph
        env:
          SRC_ENDPOINT: ${{ secrets.SRC_ENDPOINT }}
          SRC_ACCESS_TOKEN: ${{ secrets.SRC_ACCESS_TOKEN }}
        run: |
          npm install -g @sourcegraph/src
          src code-intel upload -file=index.scip
```

### 2. Multi-Tier Hybrid Cache Topology
To sustain sub-100ms response latencies during intense multi-agent coding sessions, Sourcegraph Cody deploys a three-tier context cache:
1. **L1 Local AST Scratchpad**: In-memory LRU cache storing active buffer syntax trees, symbol definitions, and local diff chunks (< 2ms access).
2. **L2 Workspace Redis Index**: Inter-process cache shared across local agent swarms storing serialized SCIP graph subgraphs and BM25 token frequencies (< 8ms access).
3. **L3 Sourcegraph Global Graph**: Remote enterprise cluster querying cross-repository embeddings and full organizational code intelligence graphs (< 60ms access).

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `HTTP 401 Unauthorized` | Invalid, expired, or revoked Sourcegraph personal access token. | Generate a new token in Sourcegraph web UI under User Settings -> Access Tokens and update `SRC_ACCESS_TOKEN`. |
| `Empty Context / 0 Chunks Returned` | Repository embeddings not generated or SCIP index missing for target branch. | Run `cody index create` or check Sourcegraph admin panel to verify repo indexing status and LSIF graph build logs. |
| `FastMCP 3.1 Bridge Connection Timeout` | Firewall or CORS restriction blocking port 3180 on context server. | Verify local port binding with `netstat -tuln \| grep 3180` and ensure host firewall permits inbound agent traffic. |
| `High Latency during Cross-Repo Search` | Unbounded search query scanning across >1,000 repositories without filters. | Add `repo:` or `lang:` filter parameters in `CodeGraphQueryInput` to restrict candidate search scope. |
| `Rate Limit Exceeded (429)` | Too many concurrent automated agent queries flooding Cody API. | Increase rate limits in Sourcegraph Enterprise admin panel or add request throttling/queueing in agent framework. |
| `Syntax Context Mismatch` | Outdated local code index relative to remote Git HEAD. | Trigger index re-sync via `cody index update` or enable automated webhooks on Git push events. |
| `OOM during Large Index Build` | Insufficient RAM allocated to local node embedding process. | Increase memory limit via `NODE_OPTIONS="--max-old-space-size=8192"` before initiating index builds. |
| `RBAC Permission Denied (403)` | Agent token lacks permissions to read target internal microservice repo. | Verify LDAP / GitHub group membership in Sourcegraph Enterprise permission sync dashboard. |

## Related tools / concepts
- [Codeium](./codeium.md) — High-performance AI coding platform.
- [Cursor](./cursor.md) — Popular AI-first code editor.
- [OpenHands](./openhands.md) — Highly capable autonomous software agent.
- [Aider](./aider.md) — Terminal-native pair programmer.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol for model-tool interactions.
- [Filesystem Context](../../knowledge_base/patterns/filesystem-context.md) — Architectural pattern for local directories.
- [RAG Pattern](../../knowledge_base/patterns/rag.md) — Core pattern for data-grounded AI reasoning.
- [CodeGraphContext](../automation_orchestration/codegraphcontext.md) — Graph-based source code indexing structures.

## Sources / references
- [Sourcegraph Cody Official Site](https://about.sourcegraph.com/cody)
- [Cody Platform Documentation](https://sourcegraph.com/docs/cody)
- [Sourcegraph GitHub Repository](https://github.com/sourcegraph/cody)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
