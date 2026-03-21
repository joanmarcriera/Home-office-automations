# OpenHands

## What it is

OpenHands (formerly OpenDevin) is an open-source platform for autonomous AI software engineering. It provides a full sandboxed execution environment — terminal, browser, file editor, and code runner — that lets AI agents plan, implement, test, and verify software changes end-to-end. It is available as a Python SDK, a CLI, a local GUI, a hosted cloud service, and an enterprise Kubernetes deployment.

SWE-Bench score: **77.6%** (one of the highest published scores for autonomous software agents as of early 2026).

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

## Deployment options

| Mode | Description | Best for |
|---|---|---|
| **CLI** | `openhands` terminal command; familiar to Claude Code / Codex users | Daily dev use, scripted tasks |
| **Local GUI** | React SPA + REST API; run on laptop | Interactive exploration of complex tasks |
| **Cloud** | app.all-hands.dev; free with Minimax model | Quick starts, no local setup |
| **Enterprise** | Self-hosted Kubernetes (source-available, license required > 1 month) | Teams, RBAC, Jira/Slack/Linear integration |
| **SDK** | Python library; composable agents in code | Custom agent pipelines, batch processing |

## Quickstart — Docker (local GUI)

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

## Quickstart — CLI

```bash
pip install openhands-ai
export LLM_MODEL="claude-sonnet-4-20250514"
export LLM_API_KEY="<your-anthropic-key>"

# Run a task
openhands "Fix the failing unit tests in src/tests/test_parser.py"
```

## Model configuration

OpenHands uses an OpenAI-compatible API interface. You can connect any model:

### Direct cloud providers

```bash
# Claude (recommended for complex tasks)
export LLM_MODEL="anthropic/claude-sonnet-4-20250514"
export LLM_API_KEY="<anthropic-key>"

# OpenAI
export LLM_MODEL="gpt-4o"
export LLM_API_KEY="<openai-key>"
```

### Local models via Ollama

```bash
export LLM_BASE_URL="http://localhost:11434"
export LLM_MODEL="ollama/qwen2.5-coder:32b"
export LLM_API_KEY="ollama"   # placeholder; Ollama ignores the key
```

### Local models via LiteLLM proxy (recommended for home lab)

Using LiteLLM gives you fallbacks, cost tracking, and model switching without touching OpenHands config:

```bash
# Start LiteLLM proxy (see LiteLLM doc)
docker run -p 4000:4000 -v ./litellm.yaml:/app/config.yaml \
  ghcr.io/berriai/litellm:main-latest --config /app/config.yaml

# Point OpenHands at the proxy
export LLM_BASE_URL="http://localhost:4000"
export LLM_MODEL="openai/coding-default"   # name from litellm.yaml
export LLM_API_KEY="<your-litellm-master-key>"
```

```yaml
# litellm.yaml — model routing for OpenHands
model_list:
  - model_name: coding-default
    litellm_params:
      model: ollama/qwen2.5-coder:32b
      api_base: http://192.168.0.5:30068   # TrueNAS Ollama
  - model_name: coding-fallback
    litellm_params:
      model: openrouter/anthropic/claude-sonnet-4-20250514
      api_key: os.environ/OPENROUTER_API_KEY
router_settings:
  fallback_model: coding-fallback
  allowed_fails: 2
```

## Python SDK

The SDK lets you build custom agent pipelines or run OpenHands non-interactively:

```python
from openhands import OpenHandsAgent

agent = OpenHandsAgent(
    model="anthropic/claude-sonnet-4-20250514",
    api_key="<key>",
    workspace_dir="./my-project",
)

result = agent.run(
    "Add comprehensive type annotations to all functions in src/utils.py "
    "and update the docstrings to match."
)
print(result.summary)
```

## Microagent system

OpenHands supports a **microagent** pattern for scoped, reusable tasks. Microagents are YAML-defined sub-agents that handle specific domains (testing, docs, security review) and can be composed into larger pipelines:

```yaml
# .openhands/microagents/test-writer.yaml
name: test-writer
trigger: "write tests for"
instructions: |
  You are a test-writing specialist. When asked to write tests:
  1. Identify all public functions and edge cases
  2. Write pytest tests with clear names
  3. Aim for >90% branch coverage
  4. Run the tests and fix any failures before finishing
```

## Typical workflows

- **End-to-end feature implementation**: "Implement a REST endpoint for user profile updates, including input validation, error handling, and tests."
- **Bug hunting**: "The background job occasionally throws a KeyError in worker.py. Find the root cause and fix it."
- **Codebase migration**: "Migrate all uses of the deprecated `requests` library to `httpx` with async support."
- **Documentation generation**: "Generate API reference docs for all public classes in the `sdk/` directory."
- **Test coverage improvement**: "Our coverage report shows src/parsers/ at 42%. Write tests to bring it to 80%+."
- **Security review**: "Scan this codebase for SQL injection vulnerabilities and suggest fixes."

## Strengths

- **High SWE-Bench performance**: 77.6% — among the best published scores for autonomous software agents
- **Full execution environment**: Terminal, browser, file editor, and code runner in one sandbox
- **Model-agnostic**: Works with Claude, GPT-4o, Gemini, local Llama/Qwen via Ollama, or any LiteLLM-routed model
- **Multiple deployment modes**: CLI to cloud to enterprise Kubernetes
- **SDK composability**: Build custom agent pipelines in Python
- **Microagent system**: Reusable, scoped sub-agents for domain-specific tasks
- **MIT-licensed core**: Free to self-host; enterprise features source-available

## Limitations

- **Resource intensive**: The Docker sandbox requires significant RAM; minimum 8 GB for practical use, 16 GB+ recommended for complex tasks
- **Slower than simple editors**: For single-file edits, [Aider](aider.md) is faster and cheaper
- **Complex local setup**: Docker socket access, runtime container image, and correct networking are required
- **Token consumption**: Autonomous multi-step loops consume many tokens; budget management via LiteLLM recommended
- **Experimental local model quality**: Open models (Qwen, Llama) work but produce lower task-completion rates than Claude or GPT-4o for complex tasks

## When to use it

- For complex, multi-step software engineering tasks requiring iteration and verification
- When the agent needs to run code and observe results to confirm correctness
- When you want a sandboxed environment that protects your host machine
- When building custom agent pipelines via the SDK
- When you want enterprise-grade features (RBAC, Slack/Jira integration) at scale

## When not to use it

- For simple file edits — use [Aider](aider.md) or [Claude Code](claude-code.md)
- On machines with less than 8 GB RAM available for Docker
- When you need sub-second response times; the agent loop adds latency
- For tasks outside software engineering (use [OpenClaw](openclaw.md) for general personal-assistant tasks)

## Comparison with similar tools

| Tool | Autonomy | Sandboxed | Local LLM | Best domain |
|---|---|---|---|---|
| **OpenHands** | Very high (plan+act+verify) | Yes (Docker) | Yes (LiteLLM/Ollama) | Full software engineering |
| **Claude Code** | High | No (host filesystem) | No (Anthropic only) | Codebase editing + CLI |
| **Aider** | Medium | No | Yes | Targeted file edits |
| **Cursor** | Low–Medium | No | Partial | IDE-centric editing |
| **OpenClaw** | High | Yes (Docker) | Yes | Messaging-channel agents |

## Security considerations

- **Docker isolation**: The sandbox container has no access to the host filesystem beyond the workspace directory
- **Credential handling**: Never pass secrets in task descriptions; use environment variables
- **Network access**: The sandbox has outbound network access by default; restrict with Docker network policies if needed
- **Enterprise RBAC**: The enterprise tier adds user-level permissions and audit logging
- **API key security**: LiteLLM virtual keys allow per-agent budget caps and revocable access

## Related tools / concepts

- [LiteLLM](../../services/litellm.md) — recommended model proxy for local-LLM routing and fallbacks
- [Aider](aider.md) — lighter-weight alternative for targeted file edits
- [Claude Code](claude-code.md) — interactive CLI with tight Anthropic model integration
- [OpenClaw](openclaw.md) — general-purpose agent runtime for messaging-channel automation
- [Ollama](../../services/ollama.md) — local model serving backend
- [OpenRouter](../ai_knowledge/openrouter.md) — cloud model routing fallback
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — adapt local models for better code task performance

## Sources / References

- [GitHub — All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands Documentation](https://docs.openhands.dev/)
- [OpenHands SDK Docs](https://docs.openhands.dev/sdk)
- [SWE-Bench Leaderboard](https://docs.google.com/spreadsheets/d/1wOUdFCMyY6Nt0AIqF705KN4JKOWgeI4wUGUP60krXXs/)
- [Tech Report (arXiv 2511.03690)](https://arxiv.org/abs/2511.03690)

## Contribution Metadata

- Last reviewed: 2026-03-21
- Confidence: high
