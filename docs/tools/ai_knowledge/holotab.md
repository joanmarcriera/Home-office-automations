# HoloTab

## What it is
HoloTab is an AI browser companion developed by HCompany. It is designed to assist users with web-based tasks and navigation, serving as a proactive agentic layer within the browsing environment. It integrates deeply with Chromium-based browsers to provide real-time assistance, content synthesis, and task automation.

## What problem it solves
It addresses the need for a more integrated and proactive AI assistant within the browser, helping users find information, summarize content, and automate simple browser tasks without switching contexts. It bridges the gap between static web content and active agentic workflows.

## Where it fits in the stack
**AI & Knowledge / Browser Companion**. It sits at the interface between the user, the browser (Chrome v145+), and the web, often integrating with [Gemma 3](local_llms.md), Claude 4.8, and GPT-5.5 for complex reasoning and multi-tab orchestration.

## Typical use cases
- **Assisted Browsing**: Getting context or summaries of websites as you visit them.
- **Task Automation**: Helping with simple, repetitive web tasks like form filling or data extraction.
- **Information Retrieval**: Quickly finding relevant information across multiple open tabs or history via agentic search.
- **Agentic Navigation**: Asking the assistant to "find the pricing page" or "summarize the checkout terms" across different sites.

## Strengths
- **Proactive Assistance**: Designed to assist as you browse rather than just responding to prompts.
- **Integrated Experience**: Aims for a seamless fit within the browser workflow via the sidebar and context menus.
- **MCP 3.0 Support**: Native integration with the Model Context Protocol (MCP 3.0) for tool-use across the web and local environment.

## Limitations
- **New Tool**: As a relatively new entry, its feature set and stability may be evolving rapidly.
- **Platform Dependency**: Requires a Chromium-based browser (Chrome, Edge, Brave) and specific extension permissions.
- **Privacy Trade-offs**: Requires access to browsing data to provide contextual assistance.

## When to use it
- If you are looking for an AI companion that is tightly integrated with your browsing experience.
- When you want an alternative to standard search engines or standalone chat interfaces for real-time web tasks.
- For users who want their browser to be "agent-aware" via MCP 3.0.

## When not to use it
- If you have strict privacy requirements and are wary of an AI observing your browsing activity.
- For highly specialized technical tasks that require a more dedicated development environment like VS Code or terminal-based agents.

## Getting started

### Installation
HoloTab is currently available as a browser extension (Chrome, Edge).

1.  **Install the Extension**: Download HoloTab from the [Chrome Web Store](https://chromewebstore.google.com/).
2.  **Authenticate**: Log in with your HCompany account to sync your preferences and history.
3.  **Activate**: Click the HoloTab icon or use the shortcut `Alt + H` to open the sidebar.
4.  **Prompt**: Ask the assistant to help with your current page or navigate to a specific resource.

### Configuration (MCP 3.0)
To enable HoloTab to use local tools via MCP 3.0, configure the bridge in the extension settings:
```json
{
  "mcpBridge": {
    "enabled": true,
    "localServers": ["http://localhost:3000"]
  }
}
```

## CLI examples
While primarily a browser tool, HoloTab offers a background service CLI for managing extension state and local context:

### Service Status
```bash
# Check HoloTab service status
holotab-cli status
```

### Cache Management
```bash
# Clear local context cache
holotab-cli cache clear
```

### Version Information
```bash
# Check installed version
holotab-cli --version
```

## API examples
HoloTab can be interacted with via browser-level automation or custom shortcuts:

```javascript
// Example: Programmatically opening the HoloTab sidebar
window.postMessage({ type: "HOLOTAB_TOGGLE_SIDEBAR" }, "*");

// Example: Sending a snippet to HoloTab for processing via the background script
chrome.runtime.sendMessage("holotab-extension-id", {
  action: "PROCESS_SELECTION",
  text: window.getSelection().toString()
});
```

## Related tools / concepts
- [Skills in Chrome](skills-in-chrome.md)
- [Perplexity](perplexity.md)
- [Genspark](genspark.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Open Agents](../agents/open-agents.md)
- [Claude Code](../development_ops/claude-code.md)
- [Gemma 3](local_llms.md)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [HoloTab AI browser companion](https://huggingface.co/blog/Hcompany/holotab)
- [HCompany Documentation](https://h.company/docs/holotab)

## Contribution Metadata
- Last reviewed: 2026-07-10
- Confidence: high
