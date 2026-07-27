# HoloTab

## What it is
HoloTab is an AI browser companion developed by HCompany. It is designed to assist users with web-based tasks and navigation, serving as a proactive agentic layer within the browsing environment.

## What problem it solves
It addresses the need for a more integrated and proactive AI assistant within the browser, helping users find information, summarize content, and automate simple browser tasks without switching contexts.

## Where it fits in the stack
**AI & Knowledge / Browser Companion**. It sits at the interface between the user, the browser (Chrome v145+), and the web, often integrating with [Claude 4.8, GPT-5.5, and Gemma 3](https://huggingface.co/blog/Hcompany/holotab) for complex reasoning tasks.

## Typical use cases
- **Assisted Browsing**: Getting context or summaries of websites as you visit them.
- **Task Automation**: Helping with simple, repetitive web tasks like form filling or data extraction.
- **Information Retrieval**: Quickly finding relevant information across multiple open tabs or history via agentic search.

## Strengths
- **Proactive Assistance**: Designed to assist as you browse rather than just responding to prompts.
- **Integrated Experience**: Aims for a seamless fit within the browser workflow via the sidebar and context menus.
- **MCP 3.0 Support**: Native integration with the **MCP 3.0 Task Protocol** for tool-use across the web.

## Limitations
- **New Tool**: As a relatively new entry, its feature set and stability may be evolving.
- **Platform Dependency**: Requires a Chromium-based browser (Chrome, Edge, Brave) and specific extension permissions.

## When to use it
- If you are looking for an AI companion that is tightly integrated with your browsing experience.
- When you want an alternative to standard search engines or standalone chat interfaces for real-time web tasks.

## When not to use it
- If you have strict privacy requirements and are wary of an AI observing your browsing activity.
- For highly specialized technical tasks that require a more dedicated development environment like VS Code or terminal-based agents.

## Getting started
HoloTab is a browser extension and does not have official developer documentation, command-line tools (CLI), or programmatic developer APIs.

To get started with the browser assistant:
1. **Download**: Install HoloTab from the [Chrome Web Store](https://chromewebstore.google.com/).
2. **Access**: Pin the extension and access it via Chrome's Side Panel or using the shortcut `Alt + H`.
3. **Automate**: Type or narrate a task to have the AI agent perform actions natively within your active tab.

## CLI examples
> [!NOTE]
> HoloTab does not provide an official command-line interface (CLI). Extension settings and execution behaviors are managed entirely inside the browser companion's sidebar GUI. Accordingly, CLI code examples are skipped.

## API examples
> [!NOTE]
> HoloTab does not expose a public developer API or programmatic SDK. Interaction and automation routines are recorded, scheduled, and triggered directly through the extension's user interface. Accordingly, API code examples are skipped.

## Related tools / concepts
- [Gemma 3](local_llms.md)
- [Skills in Chrome](skills-in-chrome.md)
- [Perplexity](../providers/perplexity.md)
- [Genspark](genspark.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Open Agents](../agents/open-agents.md)
- [Claude Code](../development_ops/claude-code.md)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [HoloTab AI browser companion](https://huggingface.co/blog/Hcompany/holotab)
- [HCompany Documentation](https://h.company/docs/holotab)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
