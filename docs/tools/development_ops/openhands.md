# OpenHands

## What it is

OpenHands (formerly OpenDevin) is an open-source platform for autonomous AI software engineering. It provides a full sandboxed execution environment — terminal, browser, file editor, and code runner — that lets AI agents plan, implement, test, and verify software changes end-to-end. As of June 2026, it is the industry-standard environment for high-autonomy agents powered by `claude-4-8-opus-20260528` and GPT-5.5. It is available as a Python SDK, a CLI, a local GUI, a hosted cloud service, and an enterprise Kubernetes deployment.

SWE-Bench score: **77.6%** (one of the highest published scores for autonomous software agents).

## What problem it solves

Complex software engineering tasks — implementing a feature, hunting a subtle bug, migrating a database schema, writing and fixing tests — require more than single-file edits. They require running code, checking browser output, iterating on failures. OpenHands provides that full loop: an AI agent that can plan, act, observe outcomes, and self-correct inside a safe sandbox without constant human supervision.

## Where it fits in the stack

**Agent Platform / Execution Environment**. OpenHands is heavier than a code-editor plugin (Aider, Cursor) and more code-focused than a general agent platform (OpenClaw). It is the right layer when you need a multi-step, self-verifying software engineering loop.

```text
┌────────────────────────────────────────────────────────┐
│             User (CLI / Local GUI / Cloud UI)           │
└──────────────────────────┬─────────────────────────────┘
                           │  task description
┌──────────────────────────▼─────────────────────────────┐
│                   OpenHands Agent Loop                  │
│  Plan → Act (edit/run/browse) → Observe → Revise       │
└──────────────────────────┬─────────────────────────────┘
                           │  LLM API calls
┌──────────────────────────▼─────────────────────────────┐
│     LiteLLM / OpenRouter / Ollama / Direct API          │
└──────────────────────────┬─────────────────────────────┘
                           │  sandboxed execution
┌──────────────────────────▼─────────────────────────────┐
│          Docker Sandbox (terminal + browser + files)    │
└────────────────────────────────────────────────────────┘
```

## Typical use cases

- **End-to-end feature implementation**: "Implement a REST endpoint for user profile updates, including input validation, error handling, and tests."
- **Bug hunting**: "The background job occasionally throws a KeyError in worker.py. Find the root cause and fix it."
- **Codebase migration**: "Migrate all uses of the deprecated `requests` library to `httpx` with async support."
- **Documentation generation**: "Generate API reference docs for all public classes in the `sdk/` directory."
- **Test coverage improvement**: "Our coverage report shows src/parsers/ at 42%. Write tests to bring it to 80%+."
- **Security review**: "Scan this codebase for SQL injection vulnerabilities and suggest fixes."
- **Microagent Orchestration**: Utilizing YAML-defined sub-agents (e.g., `.openhands/microagents/test-writer.yaml`) for scoped, domain-specific tasks like automated regression testing.

## Strengths

- **High SWE-Bench performance**: 77.6% — among the best published scores for autonomous software agents.
- **Full execution environment**: Terminal, browser, file editor, and code runner in one sandbox.
- **Model-agnostic**: Works with Claude 4.8 Opus, GPT-5.5, Gemini, local Llama/Qwen via Ollama, or any LiteLLM-routed model.
- **Flexible Deployment**: Supports CLI, Local GUI (Docker), Cloud (app.all-hands.dev), and Enterprise Kubernetes.
- **Microagent system**: Reusable, scoped sub-agents for domain-specific tasks.
- **MIT-licensed core**: Free to self-host; enterprise features source-available.
- **Comparison with alternatives**: While [Aider](aider.md) is faster for targeted edits and [Claude Code](claude-code.md) offers tighter Anthropic integration, OpenHands provides superior holistic planning and execution in a safe, isolated sandbox.

## Limitations

- **Resource intensive**: The Docker sandbox requires significant RAM; minimum 8 GB for practical use, 16 GB+ recommended for complex tasks.
- **Slower than simple editors**: The agent loop adds latency compared to single-file editors.
- **Token consumption**: Autonomous multi-step loops consume many tokens; budget management via LiteLLM is recommended.
- **Security & Isolation**: While sandboxed, users must manage Docker socket access and network policies. Enterprise RBAC is required for team-based security.

## When to use it

- For complex, multi-step software engineering tasks requiring iteration and verification.
- When the agent needs to run code and observe results to confirm correctness.
- When you want a sandboxed environment that protects your host machine.
- When building custom agent pipelines via the SDK.
- When you want enterprise-grade features (RBAC, Slack/Jira integration) at scale.

## When not to use it

- For simple file edits — use [Aider](aider.md) or [Claude Code](claude-code.md).
- On machines with less than 8 GB RAM available for Docker.
- When you need sub-second response times.
- For tasks outside software engineering (use [OpenClaw](openclaw.md) for general personal-assistant tasks).

## Getting started

### Docker Installation (Local GUI)
```bash
# Pull and run the official container
docker run -it --rm \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.39-nikolaik \
  -e LOG_ALL_EVENTS=true \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands-state:/.openhands-state \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  --name openhands-app \
  docker.all-hands.dev/all-hands-ai/openhands:0.39

# Access the GUI at http://localhost:3000
```

### Model Configuration
OpenHands uses an OpenAI-compatible API interface. You can connect any model:

```bash
# Claude 4.8 Opus (Recommended)
export LLM_MODEL="anthropic/claude-4-8-opus-20260528"
export LLM_API_KEY="<anthropic-key>"

# Local models via LiteLLM proxy
export LLM_BASE_URL="http://localhost:4000"
export LLM_MODEL="openai/coding-default"
export LLM_API_KEY="<your-litellm-master-key>"
```

## CLI examples

### Installation
```bash
pip install openhands-ai
```

### Running a task
```bash
export LLM_MODEL="anthropic/claude-4-8-opus-20260528"
export LLM_API_KEY="<key>"

# Run an autonomous engineering task
openhands "Fix the failing unit tests in src/tests/test_parser.py"
```

## API examples

The Python SDK lets you build custom agent pipelines or run OpenHands non-interactively:

```python
from openhands import OpenHandsAgent

agent = OpenHandsAgent(
    model="anthropic/claude-4-8-opus-20260528",
    api_key="<key>",
    workspace_dir="./my-project",
)

result = agent.run(
    "Add comprehensive type annotations to all functions in src/utils.py "
    "and update the docstrings to match."
)
print(result.summary)

# Interactive session via SDK
with agent.session() as session:
    session.run("Fix imports in main.py")
    session.run("Run pytest and report failures")
```

## Related tools / concepts

- [LiteLLM](../../services/litellm.md) — recommended model proxy for local-LLM routing and fallbacks.
- [Aider](aider.md) — lighter-weight alternative for targeted file edits.
- [Claude Code](claude-code.md) — interactive CLI with tight Anthropic model integration.
- [OpenClaw](openclaw.md) — general-purpose agent runtime for messaging-channel automation.
- [Ollama](../../services/ollama.md) — local model serving backend.
- [OpenRouter](../ai_knowledge/openrouter.md) — cloud model routing fallback.
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — adapt local models for better code task performance.
- [SWE-Bench](../benchmarking/swe-bench.md) — benchmark for evaluating software engineering agents.
- [Cursor](cursor.md) — AI-powered code editor.
- [Claude Code Container MCP](claude-code-container-mcp.md) — sandboxed execution for Claude Code.

## Sources / references

- [GitHub — All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands Documentation](https://docs.openhands.dev/)
- [OpenHands SDK Docs](https://docs.openhands.dev/sdk)
- [SWE-Bench Leaderboard](https://docs.google.com/spreadsheets/d/1wOUdFCMyY6Nt0AIqF705KN4JKOWgeI4wUGUP60krXXs/)
- [Tech Report (arXiv 2511.03690)](https://arxiv.org/abs/2511.03690)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
