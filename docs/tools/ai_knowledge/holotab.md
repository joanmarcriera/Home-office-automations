# HoloTab

## What it is
HoloTab is an AI browser companion developed by HCompany. It is designed to assist users with web-based tasks and navigation.

## What problem it solves
It addresses the need for a more integrated and proactive AI assistant within the browser, helping users find information, summarize content, and automate simple browser tasks.

## Where it fits in the stack
**AI & Knowledge / Browser Companion**. It sits at the interface between the user, the browser, and the web.

## Typical use cases
- **Assisted Browsing**: Getting context or summaries of websites as you visit them.
- **Task Automation**: Helping with simple, repetitive web tasks.
- **Information Retrieval**: Quickly finding relevant information across multiple open tabs or history.

## Strengths
- **Proactive Assistance**: Designed to assist as you browse rather than just responding to prompts.
- **Integrated Experience**: Aims for a seamless fit within the browser workflow.

## Limitations
- **New Tool**: As a relatively new entry, its feature set and stability may be evolving.
- **Platform Dependency**: Likely requires a browser extension or specific browser.

## When to use it
- If you are looking for an AI companion that is tightly integrated with your browsing experience.
- When you want an alternative to standard search engines or standalone chat interfaces.

## When not to use it
- If you have strict privacy requirements and are wary of an AI observing your browsing activity.
- For highly specialized technical tasks that require a more dedicated development environment.

## Getting started
HoloTab is currently available as a browser extension (Chrome, Edge).

1.  **Install the Extension**: Download HoloTab from the [Chrome Web Store](https://chromewebstore.google.com/).
2.  **Authenticate**: Log in with your HCompany account to sync your preferences and history.
3.  **Activate**: Click the HoloTab icon or use the shortcut `Alt + H` to open the sidebar.
4.  **Prompt**: Ask the assistant to help with your current page.

### Usage Example
You can use HoloTab to process web content directly in your browser:

```markdown
# Example Prompt in the HoloTab sidebar
"Summarize the key arguments in this article and find all contact emails mentioned."
```

## API examples
While primarily a browser tool, HoloTab can be interacted with via browser-level automation or custom shortcuts:

```javascript
// Example: Programmatically opening the HoloTab sidebar (conceptual)
window.postMessage({ type: "HOLOTAB_TOGGLE_SIDEBAR" }, "*");

// Example: Sending a snippet to HoloTab for processing
const selection = window.getSelection().toString();
chrome.runtime.sendMessage("holotab-extension-id", {
  action: "PROCESS_SELECTION",
  text: selection
});
```

## Related tools / concepts
- [Skills in Chrome](skills-in-chrome.md)
- [Perplexity](perplexity.md)
- [Genspark](genspark.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Open Agents](../agents/open-agents.md)

## Sources / References
- [HoloTab AI browser companion](https://huggingface.co/blog/Hcompany/holotab)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
