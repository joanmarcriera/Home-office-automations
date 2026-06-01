# Skills in Chrome

## What it is
Skills in Chrome is a feature that allows users to turn AI prompts into one-click tools directly within the Chrome browser.

## What problem it solves
It simplifies the execution of recurring AI-driven tasks by allowing them to be saved and triggered as "skills" without needing to re-type prompts or switch contexts.

## Where it fits in the stack
**AI & Knowledge / Browser Automation**. It acts as a bridge between LLM prompts and browser-based workflows.

## Typical use cases
- **Content Summarization**: One-click summary of the current page.
- **Data Extraction**: Extracting specific fields from a web page into a structured format.
- **Form Filling**: Using AI to help fill out recurring web forms.

## Strengths
- **Ease of Use**: Integrates directly into the browser UI.
- **Context Awareness**: Can easily access the content of the current tab.
- **Productivity**: Reduces friction for common AI tasks.

## Limitations
- **Browser Dependent**: Only available in Google Chrome.
- **Prompt Based**: Effectiveness depends on the quality of the underlying prompt and model.

## When to use it
- For recurring tasks that involve processing web content with AI.
- If you use Chrome as your primary tool for web-based work.

## When not to use it
- For complex, multi-step agentic workflows that require external tool access beyond the browser.
- If you prefer to use non-Chromium browsers.

## Getting started
> [!NOTE]
> Skills in Chrome is a built-in consumer feature of Google Chrome and does not have official developer documentation, CLI, or a public API.

There is no separate installation required. To use it:
1. Open Google Chrome and sign in to your Google account.
2. Open the Gemini side panel or type `@gemini` in the address bar.
3. **Hello-world example**: Type a prompt like "Summarize the key points of this page" and, once the response is generated, click the **Save as Skill** button to store it for one-click access later.
4. Access your saved skills anytime by typing `/` in the Gemini chat box.

## Related tools / concepts
- [HoloTab](holotab.md)
- [Claude Plugins](../development_ops/claude-plugins.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Open Agents](../agents/open-agents.md)
- [Stagehand](../automation_orchestration/stagehand.md)

## Sources / References
- [Turn AI prompts into one-click tools in Chrome](https://blog.google/products-and-platforms/products/chrome/skills-in-chrome/)
- [Saving Prompts as Skills](https://www.zdnet.com/article/chrome-skills-prompts-saved/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
