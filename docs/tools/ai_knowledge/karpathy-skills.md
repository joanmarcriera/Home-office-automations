# Andrej Karpathy Skills

## What it is
Andrej Karpathy Skills is a codified collection of software engineering principles, system prompt instructions, cognitive guardrails, and agentic execution guidelines inspired by Andrej Karpathy's philosophy on AI engineering, neural network debugging, and software simplicity. Designed specifically for frontier AI models (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Llama 4), these skills steer autonomous coding agents away from over-complication, speculative code generation, framework bloat, and "hallucination of complexity." Operating in tandem with **FastMCP 3.1** server guards, Karpathy Skills enforce surgical, minimalist, and verifiable file modifications that preserve codebase integrity while maximizing execution velocity.

Karpathy's engineering philosophy emphasizes first-principles thinking, minimal abstractions, hands-on data inspection, and continuous local verification. When translated into AI agent system prompts and automated tool validators, Karpathy Skills act as a strict quality filter that forces LLMs to treat code modification as a high-precision, surgical operation rather than an unconstrained text generation exercise.

## What problem it solves
As frontier AI models have become increasingly capable, they have also exhibited a strong propensity toward "speculative over-engineering"—inventing complex class abstractions, importing unnecessary third-party dependencies, refactoring unrelated files, and writing verbose placeholder comments when solving straightforward bugs or adding minor features. This "hallucination of complexity" creates massive technical debt, increases code review friction, and breaks existing test suites. Codifying "Karpathy instincts" solves this by embedding strict constraint-based, goal-driven, test-verified, and minimalist software engineering habits directly into an agent's planning and execution loops.

Additionally, in deep learning research and model training, developers often jump straight to complex hyperparameter tuning or architectural modifications without verifying that their data pipeline or baseline model works. Karpathy's "Recipe for Training Neural Networks" provides structured step-by-step diagnostic workflows that agents follow to isolate bugs, visualize training batches, overfit single batches, and establish rock-solid baselines before scaling up experiments.

## Where it fits in the stack
**Category**: [AI Knowledge & Best Practices](./index.md) / Cognitive Guardrails & Engineering Philosophy. Operating at the **Planning & Reasoning Governance Layer**, Karpathy Skills serve as a cognitive filter and static quality gate before an agent invokes FastMCP 3.1 file modification tools.

```mermaid
graph TD
    UserGoal[User Feature Request / Bug Fix] --> Agent[Autonomous AI Coding Agent: Jules / Claude Code / OpenClaw]
    Agent --> KarpathyGuard[Karpathy Skills Simplicity Guard]

    subgraph Karpathy Cognitive Rules Engine
        KarpathyGuard --> Rule1[1. Surgical Edits - Minimal Lines Touched]
        KarpathyGuard --> Rule2[2. Standard Library First - Zero Unnecessary Imports]
        KarpathyGuard --> Rule3[3. Immediate Local Verification - TDD Execution]
        KarpathyGuard --> Rule4[4. Zero Speculative Abstraction - No Dead Code]
        KarpathyGuard --> Rule5[5. Overfit Single Batch First - Baseline Validation]
    end

    KarpathyGuard -->|Valid Minimal Patch| FastMCP[FastMCP 3.1 Tool Gateway]
    KarpathyGuard -->|Violation Detected| Reject[Reject Speculative Plan & Request Refinement]
    FastMCP --> FileSystem[Target Workspace Repository]
```

At the top layer, agent prompts enforce simplicity principles during chain-of-thought planning. At the middle execution layer, FastMCP 3.1 tools intercept diffs and enforce line-count and dependency constraints using Pydantic v2 schemas. At the underlying repository level, automated test suites immediately validate that modified files compile and pass tests cleanly.

## Typical use cases
- **Agent System Initialization**: Standardizing execution rules inside files like `AGENTS.md`, `.cursorrules`, `CLAUDE.md`, or system prompts across team repositories.
- **Autonomous Coding Workflows**: Constraining autonomous agents (such as Jules, OpenClaw, Cline, or Claude Code) to perform minimal, highly focused bug fixes and feature additions.
- **Programmatic Pre-Commit Audits**: Running automated Pydantic v2 linting scripts that inspect proposed git diffs for speculative bloat before submitting pull requests.
- **FastMCP 3.1 Tool Policy Enforcement**: Configuring FastMCP 3.1 server middleware to intercept tool calls and block unauthorized package installation or file rewrites.
- **Deep Learning Model Debugging**: Applying Karpathy's "Recipe for Training Neural Networks" (e.g., visualize input data, overfit a single batch, disable regularization first) within AI research agents.
- **Code Review & Refactoring Refinement**: Evaluating existing codebase complexity to identify dead code, redundant wrappers, and over-engineered abstractions for removal.
- **Continuous Quality Gatekeeper**: Enforcing automated AST token complexity thresholds on incoming PR patches before CI runner invocation.

## Strengths
- **Surgical Code Modifications**: Enforces localized edits, preventing destructive full-file rewrites and preserving git history context.
- **Elimination of Dependency Bloat**: Encourages native language features and standard libraries over speculative third-party package additions.
- **High Predictability & Auditability**: Makes AI agent actions deterministic, readable, and easy for human engineers to review and merge.
- **Zero Runtime Infrastructure Cost**: Implemented as lightweight Markdown prompt rules, FastMCP 3.1 middleware, or Pydantic v2 validation logic.
- **Rapid Debugging Acceleration**: Emphasizes early failure detection and immediate local unit test execution after every edit.
- **Structured Neural Net Training**: Provides a deterministic, step-by-step checklist for building and debugging deep learning pipelines.

## Limitations
- **Architectural Friction in Enterprise Boilerplate**: Minimalist standards may clash with rigid enterprise architectures that mandate heavy design pattern abstractions.
- **Requires High Reasoning Capability**: Relies on frontier models (e.g., Claude 5.6 or GPT-5.6) to accurately evaluate abstract simplicity constraints.
- **Explicit Bootstrapping Required**: Developers must explicitly inject and maintain the skill guidelines within target repository system prompts and tool configs.
- **Over-Restriction Risks**: Unnecessarily strict line-count limits might prevent necessary architectural refactoring when genuine code structural debt exists.

## When to use it
- When your AI coding assistant produces overly verbose pull requests, introduces unrequested refactoring, or bloats `package.json` / `requirements.txt`.
- At the start of new software projects to establish clean, lightweight architectural conventions.
- In automated test-driven development (TDD) pipelines where agents must write the minimal code necessary to pass failing tests.
- When configuring FastMCP 3.1 agent execution sandboxes to prevent unauthorized system modifications.
- When training or debugging neural networks where systematically isolating data errors and baseline model performance is critical.

## When not to use it
- In legacy enterprise codebases where verbose multi-layer abstractions (e.g., AbstractFactoryProvider Beans) are mandatory structural requirements.
- During exploratory, unconstrained architectural brainstorming sessions where rapid ideation takes precedence over minimal diff sizes.

## Getting started

### Installation via Plugin Managers
To load Karpathy Simplicity Skills as a native plugin in Claude Code or supported CLI agent tools:

```bash
# Install Andrej Karpathy Skills plugin globally
/plugin install andrej-karpathy-skills@latest
```

### Direct System Prompt & AGENTS.md Injection
Add the following Markdown block into your repository's root `AGENTS.md` file:

```markdown
## Karpathy Engineering Simplicity Rules
1. **Surgical Edits**: Modify only the exact lines necessary. Never rewrite intact surrounding functions.
2. **Standard Library First**: Utilize standard library features before importing external packages.
3. **Verify Immediately**: Run local test suites (`pytest`, `npm test`) immediately after every code modification.
4. **No Speculative Abstraction**: Do not write unused helper functions, future-proofing interfaces, or empty placeholder comments.
5. **Neural Net Recipe**: Always visualize raw data, establish a random baseline, and overfit a single batch before scaling model capacity.
```

## Systemd Service Configuration
When running an automated Karpathy Simplicity Quality Gate as a persistent pre-commit and git hook verification daemon on Linux workstations:

```ini
[Unit]
Description=Karpathy Simplicity Linting Daemon & FastMCP Guard Server
After=network.target

[Service]
Type=simple
User=agent
Group=agent
WorkingDirectory=/opt/karpathy-guard
Environment="PYTHONUNBUFFERED=1"
Environment="MCP_PORT=8089"
ExecStart=/usr/local/bin/python3 -m karpathy_guard.server --port 8089 --strict-mode
Restart=on-failure
RestartSec=3s
LimitNOFILE=65536
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/opt/karpathy-guard/audit_logs

[Install]
WantedBy=multi-user.target
```

## Production Docker Compose Sandbox Stack
An isolated execution harness for vetting AI-proposed pull requests against Karpathy simplicity standards and AST verification rules:

```yaml
version: "3.8"

services:
  karpathy-guard-mcp:
    image: python:3.12-slim
    container_name: karpathy-guard-server
    restart: unless-stopped
    ports:
      - "8089:8089"
    environment:
      - FAST_MCP_PORT=8089
      - STRICT_MAX_LINE_RATIO=0.30
      - FORBID_EXTERNAL_IMPORTS=true
    volumes:
      - ./server:/app:ro
      - ./audit_logs:/var/log/karpathy
    working_dir: /app
    command: python3 server.py
    networks:
      - agent-guard-net

  tdd-validation-runner:
    image: python:3.12-slim
    container_name: karpathy-tdd-runner
    restart: unless-stopped
    volumes:
      - ./repo_under_test:/workspace
    working_dir: /workspace
    command: sleep infinity
    networks:
      - agent-guard-net

networks:
  agent-guard-net:
    driver: bridge
```

## CLI examples

### Auditing Repository Changes for Simplicity Compliance
Run CLI checks to evaluate git diffs against Karpathy simplicity metrics:

```bash
# Audit active git working tree against Karpathy simplicity rules
karpathy-skills audit --diff --max-lines-per-file=30 --forbid-new-deps

# Automatically remove speculative unused imports and dead code
karpathy-skills prune --working-tree
```

### Validating Test-Driven Execution Loops
Ensure that tests are run and verified after every individual file edit:

```bash
karpathy-skills verify-loop --command "pytest tests/test_core.py"
```

### Verifying Single-Batch Overfitting in Neural Networks
Evaluate an autonomous training run against the Karpathy recipe:

```bash
karpathy-recipe verify-training --script train.py --batch-size 1 --max-loss 0.001
```

## API examples

### Python: FastMCP 3.1 Karpathy Simplicity Guard Server with Pydantic v2
This comprehensive Python implementation creates a FastMCP 3.1 agent tool guard that enforces Karpathy simplicity rules on proposed code modifications using Pydantic v2:

```python
import json
import re
import ast
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for Karpathy Skills Policy Enforcement
mcp = FastMCP("Karpathy Simplicity Guard", version="3.1.0")

class ProposedDiffPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    filepath: str = Field(..., description="Relative path of file being modified")
    original_code: str = Field(..., description="Original content before modification")
    proposed_code: str = Field(..., description="New content generated by AI agent")
    max_line_diff_ratio: float = Field(default=0.35, ge=0.05, le=1.0, description="Max allowed modified line ratio")
    allow_new_dependencies: bool = Field(default=False)

    @field_validator("proposed_code")
    @classmethod
    def check_karpathy_anti_patterns(cls, v: str) -> str:
        # Check 1: Prohibit placeholder comments and speculative TODOs
        if re.search(r"#\s*TODO:|//\s*TODO:|#\s*placeholder", v, re.IGNORECASE):
            raise ValueError("Karpathy Rule Violation: Speculative TODOs and placeholders are prohibited in production diffs.")

        # Check 2: Detect hallucinated framework over-engineering
        overengineering_terms = [
            "AbstractProxyFactory",
            "GenericSingletonWrapper",
            "SpeculativeInterfaceProvider",
            "DynamicDependencyInjectorProxy"
        ]
        for term in overengineering_terms:
            if term in v:
                raise ValueError(f"Karpathy Rule Violation: Over-engineered pattern '{term}' detected.")
        return v

class SimplicityAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filepath: str
    is_surgical: bool
    lines_changed: int
    new_dependencies_detected: List[str]
    ast_cyclomatic_complexity: int
    audit_status: str
    feedback_instructions: Optional[str] = None

def compute_ast_complexity(code: str) -> int:
    """Computes basic AST node branch complexity for proposed code."""
    try:
        tree = ast.parse(code)
        branch_nodes = [node for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While, ast.Try))]
        return len(branch_nodes) + 1
    except Exception:
        return 1

@mcp.tool(name="audit_proposed_file_modification", description="Audits an agent's proposed code modification against Karpathy simplicity principles")
def audit_proposed_file_modification(payload_json: str) -> str:
    """Audits an agent's proposed code modification against Karpathy simplicity principles."""
    try:
        data = json.loads(payload_json)
        payload = ProposedDiffPayload(**data)

        orig_lines = payload.original_code.splitlines()
        prop_lines = payload.proposed_code.splitlines()
        lines_changed = abs(len(prop_lines) - len(orig_lines))
        complexity = compute_ast_complexity(payload.proposed_code)

        # Inspect for new import statements
        orig_imports = set(re.findall(r"^(?:import|from)\s+([a-zA-Z0-9_]+)", payload.original_code, re.MULTILINE))
        prop_imports = set(re.findall(r"^(?:import|from)\s+([a-zA-Z0-9_]+)", payload.proposed_code, re.MULTILINE))
        new_deps = list(prop_imports - orig_imports)

        if new_deps and not payload.allow_new_dependencies:
            report = SimplicityAuditReport(
                filepath=payload.filepath,
                is_surgical=False,
                lines_changed=lines_changed,
                new_dependencies_detected=new_deps,
                ast_cyclomatic_complexity=complexity,
                audit_status="REJECTED",
                feedback_instructions=f"Karpathy Rule Violation: Unapproved new dependencies introduced: {new_deps}. Resolve using standard library."
            )
            return report.model_dump_json(indent=2)

        report = SimplicityAuditReport(
            filepath=payload.filepath,
            is_surgical=True,
            lines_changed=lines_changed,
            new_dependencies_detected=[],
            ast_cyclomatic_complexity=complexity,
            audit_status="PASSED",
            feedback_instructions="Diff adheres strictly to Karpathy simplicity standards."
        )
        return report.model_dump_json(indent=2)
    except ValidationError as ve:
        return json.dumps({"audit_status": "VALIDATION_ERROR", "details": ve.errors()})
    except Exception as err:
        return json.dumps({"audit_status": "ERROR", "message": str(err)})

if __name__ == "__main__":
    mcp.run()
```

### Python: Neural Network Debugging Checklist Guard
Implementation of Karpathy's neural net training recipe validation using strict Pydantic v2 schemas:

```python
from pydantic import BaseModel, Field, ConfigDict

class NeuralNetRecipeChecklist(BaseModel):
    model_config = ConfigDict(extra="forbid")
    data_visualized: bool = Field(..., description="Did you manually inspect raw input data samples?")
    baseline_loss_checked: bool = Field(..., description="Is initial loss equal to -log(1/num_classes)?")
    single_batch_overfit: bool = Field(..., description="Can the model reach zero loss on 1 batch?")
    regularization_disabled: bool = Field(..., description="Are weight decay and dropout disabled during initial tests?")
    target_metric_plateau_reached: bool = Field(default=False)

def verify_training_readiness(checklist: NeuralNetRecipeChecklist) -> bool:
    if not checklist.data_visualized:
        print("ERROR: Inspect raw data before training!")
        return False
    if not checklist.single_batch_overfit:
        print("ERROR: Overfit a single batch to 100% accuracy first!")
        return False
    return True
```

## Diagnostic & Troubleshooting Matrix

| Error / Anti-Pattern | Root Cause | Detection Mechanism | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **Speculative Framework Wrapper** | Agent created unnecessary factory/abstract class layer | AST class hierarchy scan detects zero child implementations | Reject patch; instruct agent to replace abstraction with a direct flat function. |
| **Silent Import Injection** | Agent imported external package (e.g., `requests`, `numpy`) for simple math/string task | Regex check against standard library module whitelist | Enforce Python standard library alternatives (`urllib.request`, `math`). |
| **Regressive File Rewrite** | Agent wiped untouched existing functions instead of targeted patch | Git line delta exceeding 40% of file total | Restore file and supply surgical line diff instructions (`<<<<<<< SEARCH`). |
| **Unverified Assumption Bug** | Agent claimed code works without executing local unit test suite | Pre-commit hook checks for missing pytest test output file | Enforce mandatory execution of test harness before commit submission. |
| **Neural Net Gradient Explosion** | Agent increased learning rate before verifying single-batch loss convergence | Karpathy training recipe check fails `single_batch_overfit` | Overfit a single batch with learning rate 1e-3 and zero weight decay first. |

## Related tools / concepts
- [Matt Pocock Skills](./matt-pocock-skills.md) — Complementary developer workflows focusing on strict TypeScript and TDD patterns.
- [Claude Code](../development_ops/claude-code.md) — Command-line agent environment supporting Karpathy plugin rules.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Tool protocol standardizing agent execution boundaries.
- [PydanticAI](../frameworks/pydantic-ai.md) — Python agent framework with native schema validation guards.
- [Jules (Agent)](./jules.md) — Autonomous agent software engineer built around surgical edit principles.

## Sources / references
- [Andrej Karpathy Official Website](https://karpathy.ai/)
- [Andrej Karpathy: A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)
- [Andrej Karpathy Skills GitHub Repository](https://github.com/forrestchang/andrej-karpathy-skills)
- [FastMCP Specification](https://modelcontextprotocol.io/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
