# MultiOn

## What it is
MultiOn is an enterprise-grade AI agent framework, SDK, and API designed specifically for autonomous web navigation, interaction, and stateful browser control. As of late July 2026, it operates on the mature API v3 architecture, serving as a high-performance "motor cortex" for AI. It enables frontier models like Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6, and Gemini 3.5 Pro to execute complex, multi-step actions across any web surface by combining real-time visual grounding with structural DOM parsing.

## What problem it solves
Traditional web scraping, RPA (Robotic Process Automation), and heuristic automation frameworks are notoriously brittle, requiring constant maintenance when website layouts or class names change. Standard LLMs without browser grounding are "read-only" and cannot interact with authenticated user sessions or complete transaction loops. MultiOn bridges this gap by providing autonomous web execution environments that handle state management, user authentication, CAPTCHAs, dynamic JS execution, and self-healing navigation trajectories without brittle hardcoded rules.

## Where it fits in the stack
**Category**: [Agents](index.md) / [Automation & Orchestration](../automation_orchestration/index.md).
It functions as the execution and interaction layer of the agentic stack. SOTA models generate semantic intents or command paths (such as using Model Context Protocol (MCP 3.1) Task Protocol structures), which are translated by MultiOn's browser orchestrator into physical browser operations (click, type, hover, scroll, extract).

## Typical use cases
- **Transaction Orchestration**: Completing automated purchases, hotel/flight bookings, or filling out long corporate forms across disjointed websites.
- **Enterprise SaaS Workflows**: Automating repetitive data entry or cross-platform synchronization between internal tools, legacy portals, and third-party SaaS dashboards.
- **Dynamic Data Ingestion**: Gathering structured market intelligence or downloading reports from behind complex, multifactor-authenticated (MFA) client portals.
- **Social Media & Workspace Automation**: Managing profiles, scheduling posts, reviewing pull requests on GitHub, and interacting with team portals.
- **Competitive Benchmarking & Live Audits**: Continuously navigating e-commerce websites to monitor real-time pricing and stock adjustments under varying simulation profiles.

## Strengths
- **Visual Grounding & Self-Healing**: Utilizing visual analysis from frontier VLMs to accurately target UI elements, making it highly resilient to HTML structural changes.
- **Model Context Protocol (MCP 3.1) Native**: Seamlessly maps web browsing capabilities to MCP-compatible agents as an external tool, providing structured inputs/outputs.
- **Continuous Session State**: Maintains persistent, secure browser environments that carry over cookies, logins, and session states across multi-step flows.
- **Anti-Bot and CAPTCHA Handling**: Integrates advanced proxy routing and automated CAPTCHA solving to navigate complex security gates smoothly.
- **Multi-Modal Execution**: Supports both headless high-throughput sessions and visual debug sessions in a real-time local or cloud window.

## Limitations
- **Operational Latency**: Multi-step web interaction is bound by browser rendering times, network latencies, and visual verification steps (often 5 to 15 seconds per step).
- **Execution Cost**: High consumption of VLM and LLM reasoning tokens when performing long-horizon vision tasks or DOM parsing on dense websites.
- **Safety and Guardrails**: Requires rigorous application-level filtering (e.g., via [Lakera Guard](../benchmarking/lakera-guard.md)) to prevent unintended transactional actions or modifications of sensitive accounts.
- **Deterministic Limits**: Unpredictable web design shifts or custom iframe-based interfaces may occasionally require fallback prompt corrections or manual human-in-the-loop overrides.

## When to use it
- When an agent must perform write actions (e.g., submit forms, transfer data, book services) on websites lacking public API access.
- For long-horizon agentic missions requiring interaction across multiple web domains with persistent sessions.
- When building multi-agent systems that need a reliable, fully managed browser orchestration gateway instead of maintaining a complex Selenium, Puppeteer, or Playwright cluster.

## When not to use it
- For static data extraction or massive-scale crawling where high-performance local scrapers like [Crawl4AI](../process_understanding/crawl4ai.md) can run headless with significantly lower cost and latency.
- If the target systems already expose secure, robust REST or GraphQL APIs, which are always faster, cheaper, and more reliable than web-based automation.
- For strictly local, completely air-gapped deployments where external API endpoints or third-party visual model APIs cannot be queried.

## Getting started

### Installation
Install the official MultiOn client library for Python using pip:
```bash
pip install multion
```

### Authentication and Setup
Acquire an API key from the [MultiOn Console](https://console.multion.ai/) and export it to your environment variables:
```bash
export MULTION_API_KEY="mo_live_abcdef1234567890abcdef"
```

## CLI examples
The MultiOn CLI allows you to execute immediate web tasks and monitor active visual sessions directly from your terminal.

```bash
# Install the command-line companion tool
pip install multion-cli

# Run a simple, headless visual navigation task
multion browse --cmd "Search for the top trending AI research paper of the week on arXiv and summarize its abstract"

# Launch a session in a local debug window to observe browser actions
multion browse --url "https://news.ycombinator.com" --cmd "Find the top story and print its author" --local

# Maintain a persistent session across commands
multion session create --url "https://github.com"
```

## API examples

### 1. Programmatic Web Browsing with API v3 (Python)
Execute a complete visual navigation task using the native client.

```python
import os
from multion.client import MultiOn

# Initialize the v3 client
client = MultiOn(api_key=os.environ.get("MULTION_API_KEY"))

# Run a headless browsing command
result = client.browse(
    cmd="Navigate to GitHub, locate the trending Python repositories, and return the name of the top repository.",
    url="https://github.com/trending",
    include_screenshot=True,
    local=False
)

print("Execution Status:", result.status)
print("Execution Summary:", result.message)
if result.screenshot:
    print("Screenshot captured and stored.")
```

### 2. Multi-Step Stateful Sessions with MCP 3.1 Task Protocol Integration
Maintain state across successive steps for long-horizon agentic missions.

```python
import os
from multion.client import MultiOn

client = MultiOn(api_key=os.environ.get("MULTION_API_KEY"))

# Step A: Spin up a persistent session with secure proxy routing
session = client.sessions.create(
    url="https://wikipedia.org",
    local=False,
    load_plugins=True
)
session_id = session.session_id
print(f"Active Session established: {session_id}")

try:
    # Step B: Execute the first action
    step_1 = client.sessions.step(
        session_id=session_id,
        cmd="Type 'Quantum Computing' in the search bar and press Enter"
    )
    print("Step 1 Response:", step_1.message)

    # Step C: Execute a follow-up action within the same session
    step_2 = client.sessions.step(
        session_id=session_id,
        cmd="Click on the section link for 'Quantum decoherence' and extract the introductory paragraph"
    )
    print("Step 2 Response:", step_2.message)

finally:
    # Step D: Always clean up and close active sessions
    client.sessions.close(session_id=session_id)
    print("Session terminated successfully.")
```

## Related tools / concepts
- [Stagehand](../automation_orchestration/stagehand.md) — Node-based visual automation using SOTA vision-language models and Playwright.
- [Browser Use](../automation_orchestration/browser-use.md) — LangChain-native framework for steering web browsers with SOTA visual LLMs.
- [Skyvern](../automation_orchestration/skyvern.md) — Open-source visual web-automation and scraping agent platform.
- [Playwright](../development_ops/playwright.md) — The core high-performance browser automation engine.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Lightning-fast open-source scraping and chunking optimized for LLM ingestion.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Stateful, multi-step patterns for executing long-horizon tasks.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Industry-standard protocol for integrating web tools with frontier LLMs.
- [Exa AI](../providers/exa_ai.md) — Semantic search provider used to identify target URLs before initiating MultiOn browser interactions.

## Sources / references
- [MultiOn Developer Portal](https://docs.multion.ai/)
- [MultiOn Official Site](https://www.multion.ai/)
- [MultiOn Python SDK GitHub](https://github.com/multion-ai/multion-python)
- [API v3 Architecture and Vision-Grounding Update](https://www.multion.ai/blog/v3-api-release)

## Contribution Metadata
- Last reviewed: 2026-07-28
- Confidence: high
