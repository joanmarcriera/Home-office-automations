# Tabnine

## What it is
Tabnine is an AI code assistant that focuses on privacy, security, and enterprise-grade control. It provides AI-powered code completions and chat capabilities, with a strong emphasis on local-only execution and private model hosting to ensure code never leaves a secure environment.

## What problem it solves
It addresses the critical security concern of sending proprietary or sensitive source code to external cloud-based LLMs. By offering local-only inference and private cloud deployments, Tabnine enables teams in regulated industries (finance, healthcare, defense) to leverage AI productivity without compromising data sovereignty.

## Where it fits in the stack
**Development & Ops / AI Coding Assistant**. It functions as a privacy-first alternative to cloud-heavy assistants like GitHub Copilot, often serving as the primary completion engine in air-gapped or high-security environments.

## Typical use cases
- **Secure Code Completion**: Real-time suggestions in environments where cloud access is restricted.
- **Local LLM Inference**: Running small, optimized models directly on developer workstations.
- **Enterprise Private Cloud**: Deploying Tabnine's infrastructure on-premises or in a private VPC.
- **Legacy Codebases**: Training custom models on private repositories to improve completion relevance for internal libraries.

## Strengths
- **Uncompromising Privacy**: Local-only options are a primary differentiator.
- **Enterprise Ready**: Support for VPC, on-prem, and air-gapped deployments.
- **Custom Model Training**: Can be trained on your own code for better context awareness.
- **Multi-IDE Support**: Excellent coverage for VS Code, JetBrains, Sublime, Vim, and more.

## Limitations
- **Completion Quality**: Local models may occasionally lag behind state-of-the-art cloud models like **Claude 5.1** or **GPT-5.5**.
- **Resource Usage**: Local inference requires significant RAM and CPU/GPU resources on the developer's machine.
- **Cost**: The most advanced privacy and custom features are locked behind high-tier enterprise pricing.

## When to use it
- When code privacy is a non-negotiable requirement and cloud-based AI is prohibited.
- When working in air-gapped or restricted network environments.
- When you need a consistent AI experience across a diverse set of IDEs (e.g., mixing JetBrains and Vim).

## When not to use it
- When you prioritize the absolute highest reasoning and completion quality over privacy.
- When you are a solo developer looking for the best free tier (consider [Codeium](codeium.md)).
- When you want an agent that can execute terminal commands and manage your whole OS (consider [Claude Code](claude-code-setup.md)).

## Getting started

### Installation (VS Code)
1. Open VS Code and go to the Extensions view (`Ctrl+Shift+X`).
2. Search for "Tabnine".
3. Click **Install**.
4. Sign in or configure your local model path if using Tabnine Pro/Enterprise.

### Installation (JetBrains)
1. Go to `Settings` -> `Plugins`.
2. Search for "Tabnine" in the Marketplace.
3. Install and restart the IDE.

### Configuring Local-Only Mode
For users with Tabnine Pro/Enterprise, you can force the agent to use only local models.

```json
// Example Tabnine configuration (config.json or IDE settings)
{
  "tabnine.model_type": "local",
  "tabnine.local_model_path": "/opt/tabnine/models/tabnine-6b-local",
  "tabnine.cloud_inference_enabled": false,
  "tabnine.telemetry_enabled": false
}
```

## CLI examples
> [!NOTE]
> Official CLI examples for Tabnine are primarily managed through IDE extensions or enterprise-specific binaries.

```bash
# Example: Check the version of the Tabnine local binary (if available in path)
Tabnine --version

# Example: Run the Tabnine binary in 'chat' mode for testing (Enterprise)
Tabnine --chat-only

# Example: Configure Tabnine Enterprise endpoint via environment
export TABNINE_REMOTE_ENDPOINT="https://tabnine.internal.company.com"
```

## API examples

### Local Autocomplete Request
Tabnine's API is primarily consumed via JSON-RPC over a local socket or stdin/stdout by IDE extensions.

```json
// Example JSON request to the Tabnine local binary
{
  "version": "1.0.0",
  "request": {
    "Autocomplete": {
      "before": "def hello_world():\n    ",
      "after": "",
      "filename": "test.py",
      "region_includes_beginning": true,
      "region_includes_end": true,
      "max_num_results": 5
    }
  }
}
```

### Enterprise Self-Hosting (Docker)
Tabnine Enterprise can be deployed as a private server to serve completions to a whole organization.

```yaml
# Simple representation of a private Tabnine Enterprise server
services:
  tabnine-server:
    image: tabnine/enterprise-server:latest
    environment:
      - LICENSE_KEY=${TABNINE_LICENSE}
      - MODEL_VARIANT=enterprise-high-perf
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    restart: always
```

## Related tools / concepts
- [VS Code](vscode.md): The most common platform for Tabnine.
- [Superconductor](superconductor.md): Cloud-native parallel agent orchestration.
- [OpenCode](opencode.md): Open-source alternative for AI coding assistance.
- [Zed](zed.md): A high-performance editor with native AI capabilities.
- [Cursor](cursor.md): An AI-native IDE that prioritizes integrated features.
- [Codeium](codeium.md): A leading privacy-conscious competitor with a generous free tier.
- [GitHub Copilot](github_copilot.md): The standard cloud-based coding assistant.
- [Sourcegraph Cody](sourcegraph_cody.md): Focuses on codebase-wide context and search.
- [Aider](aider.md): Terminal-based AI coding that can be used alongside IDE completions.
- [LocalAI](../infrastructure/localai.md): A platform for serving local models.
- [Claude Code](claude-code-setup.md): High-autonomy agent CLI.
- [Model Context Protocol](../automation_orchestration/mcp.md): For extending agent capabilities.

## Sources / references
- [Official Website](https://www.tabnine.com/)
- [Tabnine Documentation](https://docs.tabnine.com/)
- [Tabnine for Enterprise](https://www.tabnine.com/enterprise)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
