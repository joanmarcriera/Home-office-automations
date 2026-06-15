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

There is no separate installation required for this feature, as it is integrated directly into the browser.

### Hello-world example
To create your first skill:
1. Open Google Chrome and sign in to your Google account.
2. Open the Gemini side panel (click the Gemini icon next to the address bar) or type `@gemini` in the address bar.
3. Type a prompt like: `"Summarize the key points of this page into a 3-bullet list."`
4. Once the response is generated, click the **Save as Skill** button.
5. Give it a name (e.g., `Quick Summary`) and save it.

## CLI examples

> [!NOTE]
> This feature is a browser-native UI component and does not currently offer an official CLI.

Interaction is performed via the Chrome address bar ("Omnibox"):
- **Trigger Gemini**: Type `@gemini` followed by your prompt.
- **Trigger a Skill**: Type `@gemini` followed by `/` and the skill name.
- **Manage Skills**: Type `@gemini`, press `/`, and click the compass icon to open the Skills management interface.

## API examples

> [!NOTE]
> This feature does not currently offer an official public API for external programmatic access.

However, users can "remix" skills from the official library:
1. Open the **Skills Library** via the compass icon in the Gemini panel.
2. Select a pre-built skill (e.g., "Ingredient Breakdown").
3. Click **Add to my skills**.
4. You can now modify the underlying prompt (the "code" of the skill) to customize its behavior.

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
