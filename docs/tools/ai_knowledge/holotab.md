# HoloTab

## What it is
HoloTab is an AI browser companion developed by HCompany. It is designed to assist users with web-based tasks and navigation, serving as a proactive agentic layer within the browsing environment.

## What problem it solves
It addresses the need for a more integrated and proactive AI assistant within the browser, helping users find information, summarize content, and automate simple browser tasks without switching contexts.

## Where it fits in the stack
**AI & Knowledge / Browser Companion**. It sits at the interface between the user, the browser (Chrome v145+), and the web. In early 2027, it is commonly integrated with frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4**, **Gemma 4**, and **Qwen 3.6** for complex reasoning tasks, providing live web session context to active agents via the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** specifications.

## Typical use cases
- **Assisted Browsing**: Getting context or summaries of websites as you visit them.
- **Task Automation**: Helping with simple, repetitive web tasks like form filling or data extraction.
- **Information Retrieval**: Quickly finding relevant information across multiple open tabs or history via agentic search.

## Strengths
- **Proactive Assistance**: Designed to assist as you browse rather than just responding to prompts.
- **Integrated Experience**: Aims for a seamless fit within the browser workflow via the sidebar and context menus.
- **MCP 3.1 Support**: Native integration with the **MCP 3.1 / FastMCP 3.1** specifications for tool-use and active context sharing across the web.

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
HoloTab is a browser extension and is primarily managed inside the browser companion's sidebar GUI. However, developers can build integrations or remote controllers utilizing its native JSON payload telemetry.

To get started with the browser assistant:
1. **Download**: Install HoloTab from the [Chrome Web Store](https://chromewebstore.google.com/).
2. **Access**: Pin the extension and access it via Chrome's Side Panel or using the shortcut `Alt + H`.
3. **Automate**: Type or narrate a task to have the AI agent perform actions natively within your active tab.

## CLI examples
> [!NOTE]
> HoloTab does not provide an official command-line interface (CLI). Extension settings and execution behaviors are managed entirely inside the browser companion's sidebar GUI. Accordingly, CLI code examples are skipped.

## API examples

### Python (Telemetry payload & Context Schema Validation with Pydantic v2)
The following Python script shows how to structure, validate, and serialize browser context and automation command payloads for HoloTab using **Pydantic v2** models. This is highly useful when syncing active browser state to backend orchestrators or multi-agent workflows.

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

# Define a strict model representing a browser tab's current state
class BrowserTabContext(BaseModel):
    tab_id: int = Field(..., description="Unique browser tab identifier")
    url: HttpUrl = Field(..., description="Currently active web address")
    title: str = Field(..., min_length=1, description="The title of the page")
    is_active: bool = Field(default=True, description="Whether this is the currently focused tab")
    selected_text: Optional[str] = Field(None, description="Text highlighted by the user in this tab")

# Define a model for automated actions to be performed by HoloTab
class HoloTabActionPayload(BaseModel):
    action_id: str = Field(..., description="Unique action transaction ID")
    action_type: str = Field(..., description="Action type, e.g., 'SUMMARIZE', 'EXTRACT_TABLE', 'FILL_FORM'")
    target_tab: BrowserTabContext = Field(..., description="The browser tab context to act upon")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Custom parameters for the action")

# Demo showing validation of inbound browser state
def validate_and_serialize_holotab_context(raw_payload: dict) -> HoloTabActionPayload:
    # Validate payload under strict Pydantic v2 rules
    action = HoloTabActionPayload.model_validate(raw_payload)
    return action

if __name__ == "__main__":
    raw_browser_telemetry = {
        "action_id": "act_89123x",
        "action_type": "SUMMARIZE",
        "target_tab": {
            "tab_id": 42,
            "url": "https://h.company/docs/holotab",
            "title": "HoloTab Documentation Portal",
            "is_active": True,
            "selected_text": "HoloTab is an AI browser companion developed by HCompany."
        },
        "parameters": {
            "max_sentences": 3,
            "tone": "concise"
        }
    }

    validated_action = validate_and_serialize_holotab_context(raw_browser_telemetry)
    print("--- HoloTab Payload Successfully Validated ---")
    print(f"Action ID: {validated_action.action_id}")
    print(f"Action Type: {validated_action.action_type}")
    print(f"Active URL: {validated_action.target_tab.url}")
    print(f"Highlighted Text: {validated_action.target_tab.selected_text}")
    print(f"Parameters: {validated_action.parameters}")
```

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
- Last reviewed: 2027-01-07
- Confidence: high
