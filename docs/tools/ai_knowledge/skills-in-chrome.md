# Skills in Chrome

## What it is
Skills in Chrome is a native browser feature (v145+) that transforms AI prompts into one-click, reusable tools directly integrated into the Google Chrome interface. Powered by Gemini 3.5 Ultra and Nano (local-on-device), it allows users to codify complex instructions into "Agentic Hooks" that can be triggered via the omnibox, side panel, or right-click context menu.

## What problem it solves
It eliminates "prompt fatigue" and the friction of repetitive typing for recurring AI tasks. By bridging the gap between static LLM chats and actionable browser workflows, it enables users to treat AI as a set of specialized, context-aware browser extensions without needing to write code.

## Where it fits in the stack
**AI Knowledge / Browser Agentic Layer**. It sits at the edge of the user's interaction with the web, providing a "Sidecar Agent" capability that can observe page DOM, summarize content, and interact with web elements as part of an integrated agentic ecosystem.

## Typical use cases
- **Automated Research**: One-click "TL;DR" and key takeaway extraction for long technical documents or research papers.
- **Data Structuring**: Extracting product specifications, pricing, or ingredients from a webpage directly into a structured clipboard format.
- **Workflow Automation**: Generating contextual email replies or PR descriptions based on the active tab's content.
- **Multi-Tab Synthesis**: Using the "Agentic Search" capability to synthesize information across several open tabs into a single comparison table.

## Strengths
- **Zero-Latency Context**: Native integration allows the AI to access the current tab's context without manual copy-pasting.
- **Agentic Hooks**: Supports automated triggering based on specific URL patterns (e.g., automatically offer to "Compare Prices" when on an e-commerce site).
- **Security & Privacy**: Operates within the browser's sandbox, utilizing Google's "Identity-Aware Tool Routing" for secure data handling.
- **Cross-Device Sync**: Saved skills are synchronized across desktop (Windows, Mac, Linux) and mobile (Android) via the user's Google account.

## Limitations
- **Ecosystem Lock-in**: Exclusively available for Google Chrome and Chromium-based browsers that adopt the Gemini API.
- **Context Window**: While Gemini 3.5 offers massive context windows, extremely large web documents or multi-media pages may still face truncation.
- **Sandbox Constraints**: Cannot interact with local filesystems or system-level processes outside the browser without specialized extensions.

## When to use it
- For high-frequency, low-complexity AI tasks performed during active browsing sessions.
- When you need immediate AI assistance that is aware of the specific "here and now" context of a webpage.
- If you want to build simple "agentic workflows" without setting up complex orchestration tools like [n8n](../../services/n8n.md).

## When not to use it
- For heavy coding tasks or repository-wide analysis (use [Claude Code](everything-claude-code.md) or [Cursor](../development_ops/cursor.md)).
- When working with highly sensitive data that requires local-only inference (use [Ollama](../../services/ollama.md) or [Local LLMs](local_llms.md)).
- For complex, multi-step agentic workflows that require external tool access beyond the browser's reach.

## Getting started
> [!IMPORTANT]
> Requires Google Chrome v145+ and a Google Account with Gemini features enabled.

### Local Setup
1. **Enable AI Features**: Navigate to `chrome://settings/ai` and ensure "Gemini Side Panel" and "Agentic Hooks" are toggled ON.
2. **Open the Side Panel**: Click the Gemini icon in the top-right corner of the browser or press `Cmd+K` (Mac) / `Ctrl+K` (Windows).
3. **Create Your First Skill**:
   - Type a prompt in the Gemini chat (e.g., "Extract all dates and events from this page into a markdown list").
   - After the response, click the **Save as Skill** button.
   - Name the skill (e.g., `Event Extractor`) and assign a shortcut (e.g., `/events`).

### Basic Usage
- **Via Omnibox**: Type `@gemini /events` and press Enter.
- **Via Context Menu**: Highlight text, right-click, and select `Skills > Event Extractor`.

## CLI examples
While Skills in Chrome is primarily a UI-driven feature, developers can interact with the underlying agentic engine via the Chrome DevTools Protocol (CDP).

```bash
# Example: Triggering a Chrome Skill via CDP (Headless)
# Note: Requires a debug-enabled Chrome instance
curl -X POST http://localhost:9222/json/rpc \
  -d '{
    "id": 1,
    "method": "AI.executeSkill",
    "params": { "skillId": "event-extractor", "tabId": 123 }
  }'
```

## API examples
Extensions can call saved skills or define new ones using the experimental `chrome.ai` API.

```javascript
// Example: Extension calling a Chrome Skill
chrome.ai.skills.execute({
  skillName: 'summarize',
  context: 'active_tab',
  options: { detailLevel: 'concise' }
}).then((result) => {
  console.log("Skill Output:", result.text);
});
```

## Related tools / concepts
- [Google Search](google-search.md) — The underlying "Agentic Search" platform.
- [Gemini](gemini.md) — The frontier model powering the skills.
- [Nano Banana](nano-banana.md) — On-device small language model integration in Chrome.
- [HoloTab](holotab.md) — Advanced browser-based AI visualization.
- [Browser Use](../automation_orchestration/browser-use.md) — Playwright-based agentic browser control.
- [Stagehand](../automation_orchestration/stagehand.md) — AI-first browser automation framework.
- [Claude Desktop](claude-desktop.md) — Alternative desktop-sidecar agent.
- [Open WebUI](../../services/open-webui.md) — Local interface for multiple model orchestration.
- [n8n](../../services/n8n.md) — Workflow automation for complex agentic pipelines.

## Sources / References
- [Google I/O 2026: Powering the Agentic Web](https://developer.chrome.com/blog/chrome-at-io26)
- [Turn AI prompts into one-click tools in Chrome](https://blog.google/products-and-platforms/products/chrome/skills-in-chrome/)
- [Chrome Developer: The AI-Powered Browser](https://developer.chrome.com/docs/ai/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
