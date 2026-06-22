# Google Gemini CLI

## What it is
**Google Gemini CLI** is a high-performance terminal interface and agentic toolkit that brings the Gemini model family directly into developer workflows. It acts as both a standalone CLI assistant for local development and a suite of GitHub Actions for automated repository management. As of June 2026, it supports **Gemini 3.5 Ultra/Flash** and native multimodal inputs via the command line.

## What problem it solves
It eliminates the "context switching" penalty by allowing developers to access state-of-the-art AI for code generation, explanation, and refactoring without leaving the terminal. In CI/CD, it automates high-volume maintenance tasks like issue triaging, PR reviews, and changelog generation using Google's frontier context windows (2M+ tokens).

## Where it fits in the stack
**Category**: Developer Experience (DX) / Agentic Tooling. It serves as a bridge between the local terminal environment and Google's Vertex AI or AI Studio infrastructure, often used alongside tools like `gh` (GitHub CLI) and `git`.

## Typical use cases
- **Terminal Engineering Assistant**: Asking "Explain why this Docker build is failing" by piping logs directly into the CLI.
- **Automated PR Reviewer**: Using the `gemini-review` action to identify logic flaws and style violations in new code submissions.
- **Interactive Refactoring**: Using the agentic mode to "Upgrade all React components in this folder to use the new useFormStatus hook."
- **Knowledge Synthesis**: Summarizing long documentation threads or technical specs into actionable TODO lists.
- **Multimodal Debugging**: Passing screenshots of UI bugs directly to the CLI for CSS/layout remediation.

## Strengths
- **Massive Context**: Leverages Gemini's 2M+ token context window for full-project analysis.
- **Multimodal Native**: Supports image, video, and audio inputs directly via CLI flags.
- **Google Ecosystem Integration**: First-class support for ground-truth search, code execution, and Vertex AI safety filters.
- **Speed**: Extremely low latency when utilizing the 'Gemini 3.5 Flash' model family.
- **Free Tier**: Generous free-tier access via Google AI Studio for individual developers.

## Limitations
- **Internet Requirement**: Requires an active connection to Google's cloud APIs; no offline mode.
- **Privacy Trade-offs**: Standard AI Studio usage may involve data logging unless using Enterprise Vertex AI.
- **Rate Limits**: Subject to RPM (Requests Per Minute) limits which can be hit during high-volume CI/CD tasks.

## When to use it
- To automate high-volume repository maintenance on GitHub.
- For a lightweight, CLI-native alternative to heavy AI IDEs like Cursor or Windsurf.
- When working with very large files or projects that exceed the context limits of other agents (e.g., Claude or GPT-4o).

## When not to use it
- In air-gapped or high-security environments where outbound cloud traffic is prohibited.
- For tasks requiring local-only inference (use [llama-cpp](../infrastructure/llama-cpp.md) or [Ollama](../../services/ollama.md)).
- If your organization mandates the use of a different cloud provider (e.g., AWS or Azure).

## Getting started

### Installation
Google Gemini CLI requires Node.js 24+ and an API key from Google AI Studio.

```bash
# Install via npm
npm install -g @google/gemini-cli

# Set your API Key
export GEMINI_API_KEY="your_key_here"
```

### Configuration
You can configure default models and safety settings in a `.geminirc` file in your home directory:

```json
{
  "model": "gemini-3.5-pro",
  "temperature": 0.2,
  "safety": "none"
}
```

## CLI examples

### Basic Coding Questions
```bash
# Ask a general question
gemini "How do I implement a rate-limiter in Go?"

# Analyze a local file
gemini --file app.py "Refactor this to use the repository pattern"
```

### Agentic Mode (Subagents)
Spawn a subagent to handle a multi-step task:
```bash
gemini "Find all deprecated API calls in /src and create a migration plan" --agentic
```

### Multimodal Input (June 2026)
Analyze a screenshot of a terminal error:
```bash
gemini --image error_screenshot.png "What is causing this stack trace?"
```

## API examples

### Node.js Integration
You can use the Gemini CLI's underlying library in custom scripts:

```javascript
import { GeminiAgent } from '@google/gemini-cli';

const agent = new GeminiAgent({
  apiKey: process.env.GEMINI_API_KEY,
  model: 'gemini-3.5-flash'
});

const result = await agent.execute('Summarize this directory', { path: './src' });
console.log(result.summary);
```

### GitHub Actions Workflow
Automate PR reviews in `.github/workflows/ai-review.yml`:

```yaml
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Gemini Review
        uses: google-github-actions/run-gemini-cli@v1
        with:
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          prompt: "Review this PR for security vulnerabilities."
```

## Related tools / concepts
- [Google Gemini](google-gemini.md) — Underlying model family.
- [Aider](../development_ops/aider.md) — Alternative terminal-based agent.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's CLI-native agent.
- [Vertex AI](../providers/google-vertex-ai.md) — Enterprise-grade hosting.
- [Antigravity](../frameworks/anti_gravity.md) — Google's agentic framework.
- [Nano Banana](nano-banana.md) — Gemini 3.1 Flash/Pro Image models.
- [Gemini Flash TTS](gemini-flash-tts.md) — Speech synthesis model.

## Sources / references
- [Vertex AI Documentation](https://docs.cloud.google.com/vertex-ai/docs)
- [Official Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Google AI Studio Console](https://aistudio.google.com/)
- [Gemini 3.5 Technical Report (June 2026)](https://deepmind.google/technologies/gemini/)
- [GitHub Blog: Node.js 24 Support](https://github.blog/changelog/2026-01-20-node-24-actions/)
- [MCP 3.0 Gemini Connector](https://modelcontextprotocol.io/connectors/gemini)
- [Google Developer Blog: Agentic Workflows](https://developers.googleblog.com/en/gemini-cli-agentic-updates/)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
