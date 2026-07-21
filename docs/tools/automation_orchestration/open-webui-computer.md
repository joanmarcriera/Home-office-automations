# Open WebUI Computer (cptr)

## What it is
Open WebUI Computer (also known as `cptr`) is an open-source, terminal-native AI agent and remote workstation surface designed to allow Large Language Models (LLMs) to control your computer. Engineered with a mobile-first philosophy, it serves a complete desktop interface—comprising files, shell sessions, git state, and web browser tabs—to any browser or client. It exposes an OpenAI-compatible agent API and natively integrates with Model Context Protocol (MCP 3.0/3.1) servers to execute complex, long-horizon tool and system workflows directly on the host machine.

## What problem it solves
Managing and executing developer workflows on a local or remote host usually requires navigating multiple disconnected interfaces, such as terminal multiplexers, IDEs, and browser windows. When AI agents are introduced, they often operate in isolated sandboxes without direct access to the real development environment, leading to context loss and execution errors. Open WebUI Computer bridges this gap by unifying file management, terminal state, git control, and browser automation into a single, cohesive canvas. It enables AI agents to work securely and directly within the developer's actual environment without heavy virtualization or sandbox constraints.

## Where it fits in the stack
**Automation & Orchestration Layer / Agentic Surface**. Open WebUI Computer serves as the bridging runtime and UI layer between frontier LLMs (via API keys or local runtimes) and the operating system's underlying shell and filesystem.

## Typical use cases
- **Mobile Workstation Access**: Pushing git commits, managing Docker containers, or editing source code directly from a phone or tablet.
- **Autonomous Coding Agent Sessions**: Triggering an LLM (such as Claude 3.5 Sonnet, Llama 4, or Gemma 3) to execute local tests, read compile errors, apply code changes, and push fixes.
- **Remote Systems Administration**: Running shell tasks, managing backups, and editing configuration files via secure messaging bots (Telegram, Discord, Slack) connected to the host machine.
- **Multimodal Web Scraping & Automation**: Instructing an agent to navigate websites, handle authentication, fill out forms, and capture screenshots using an automated browser.

## Strengths
- **Persistent Sessions**: Terminal processes and agent execution keep running in the background even if the browser tab is closed or disconnected.
- **Mobile-First Design**: A responsive interface crafted specifically for touch inputs, swipe gestures, and portrait layouts.
- **Extensible Agent Capabilities**: Built-in agentic modes supporting web search, voice control (speech-to-text/text-to-speech), reasoning trace rendering (e.g., o3/Claude thought blocks), and custom instruction sets (SKILL.md files).
- **Gateway API Integration**: Exposes an `/v1/chat/completions` API that turns any workspace into an OpenAI-compatible model, making it easy to plug into larger multi-agent frameworks.
- **Comprehensive Tooling**: Out-of-the-box support for visual git staging/diffs, syntax-highlighted code editing, file searching, and multi-pane terminal layouts.

## Limitations
- **No Per-User Isolation**: Exposing the UI provides root/user-level access equivalent to an open SSH port on the host machine, making it unsuitable for multi-tenant, untrusted user hosting.
- **High Resource Requirements**: Running browser automation, local inference, or background agent pipelines simultaneously requires substantial CPU, GPU, and VRAM resources.
- **Security Warning**: Exposing the instance to the public internet without secure VPN/tunnels (like Tailscale) or proper JWT/credential guards poses a major security hazard.

## When to use it
- When you need a lightweight, self-hosted, web-accessible development workspace that works beautifully on mobile screens.
- When orchestrating complex agentic tasks where the AI must have direct read/write access to files and local terminal environments.
- For secure, remote administration of home lab resources and self-hosted automation containers.

## When not to use it
- If multiple untrusted users require access to the same container/machine (due to the lack of strict tenant sandboxing).
- If you are operating under highly locked-down security compliance constraints where local shell execution by AI is strictly prohibited.
- For purely conversational AI workflows that do not require tool calling or local file/command execution.

## Getting started

### Quickstart Installation
Install the package using pip or uv, and spin up the server:

```bash
# Install with recommended MCP dependencies
pip install 'cptr[mcp]'

# Run the Open WebUI Computer server
cptr run --host 0.0.0.0 --port 8000
```

### Docker Compose Configuration
For standard homelab deployments, running `cptr` alongside your model router or local LLM server is the recommended pattern.

```yaml
services:
  cptr:
    image: ghcr.io/open-webui/computer:latest
    container_name: cptr
    ports:
      - "8000:8000"
    volumes:
      - cptr-data:/data
      - /home/user/workspace:/workspace
    working_dir: /workspace
    environment:
      - OPENAI_API_BASE=http://litellm:4000/v1
      - OPENAI_API_KEY=your-api-key-here
    restart: unless-stopped

volumes:
  cptr-data:
```

## CLI examples
The `cptr` CLI command provides simple administration controls:

```bash
# Bind to all network interfaces to allow mobile access on local Wi-Fi
cptr run --host 0.0.0.0 --port 8000

# Start cptr with diagnostic logging enabled
cptr run --log-level debug --log-format json

# Use uvx to run cptr instantly without permanent global installation
uvx cptr@latest run
```

## API examples

### Gateway Chat Completion Request
Open WebUI Computer acts as an OpenAI-compatible server. You can dispatch prompt/message lists directly to your workspace:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer workspace-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "workspace-agent",
    "messages": [
      {
        "role": "user",
        "content": "Analyze the codebase structure and draft a README.md file in the project root."
      }
    ]
  }'
```

### Dynamic Shell Command Invocation (Python Client)
Programmatically target a running workspace to execute shell commands and capture the output:

```python
import requests

url = "http://localhost:8000/api/v1/workspaces/default/terminal/execute"
headers = {
    "Authorization": "Bearer workspace-api-token",
    "Content-Type": "application/json"
}
payload = {
    "command": "git status --porcelain"
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    result = response.json()
    print("Shell Output:\n", result.get("output"))
else:
    print(f"Failed to execute command: {response.status_code} - {response.text}")
```

## Related tools / concepts
- [Open WebUI](../../services/open-webui.md) — The main parent conversational user interface that can integrate `cptr` as a gateway backend.
- [Ollama](../../services/ollama.md) — Local LLM runner to serve models like Gemma 3 and Llama 4 directly to your agent.
- [Model Context Protocol (MCP)](mcp.md) — The standardization protocol used by `cptr` to load and interact with external systems.
- [LiteLLM](../../services/litellm.md) — Useful proxy router to aggregate model endpoints (Anthropic, OpenAI, local) for cptr consumption.
- [Browser Use](browser-use.md) — Multi-agent browser automation framework similar to the built-in browser capabilities in Open WebUI Computer.
- [Playwright MCP Server](playwright-mcp.md) — A specialized tool server enabling agents to scrape and parse complex websites.
- [CliHub](clihub.md) — Unified CLI tooling platform for consolidating command interfaces.
- [Tailscale](../../services/tailscale.md) — Secure overlay mesh network to safely access your workstation from anywhere in the world.

## Sources / References
- [GitHub: Open WebUI Computer](https://github.com/open-webui/computer)
- [Official Documentation: Open WebUI Computer Integration](https://docs.openwebui.com/ecosystem/computer/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
