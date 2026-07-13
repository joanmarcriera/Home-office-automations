# Google Gemini for macOS

## What it is
Google Gemini for macOS is a native desktop application designed to integrate Google's multimodal AI capabilities directly into the macOS ecosystem. It provides a system-wide interface for interacting with Gemini models, leveraging the MCP 3.0 Task Protocol for agentic workflows and local system integration.

## What problem it solves
It eliminates context switching between applications and browsers by offering a dedicated desktop surface accessible via global keyboard shortcuts. It leverages native macOS features like screen awareness and local file access to provide more contextual assistance than the standard web interface.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Desktop Agents. It serves as a direct system-level entry point to the Gemini ecosystem, supporting integration with [Gemma 3](local_llms.md) via MCP-bridged services.

## Typical use cases
- **Development & Coding**: Share a debugger window to get instant troubleshooting advice or code explanations.
- **Research & Synthesis**: Summarize complex reports or web pages without leaving the active document.
- **Creative Workflows**: Generate and iterate on visual assets using natural language prompts within the desktop environment.
- **Workspace Automation**: Use Gemini to find specific information buried in Google Workspace via native connectors and MCP 3.0 tool routing.

## Strengths
- **Native Shortcut Access**: Invoke Gemini from any app using the `Option + Space` shortcut.
- **Screen Awareness**: Share specific windows or the entire screen with Gemini to ask questions about charts, code, or documents currently in view.
- **Multimodal Creation**: Support for generating images via [Nano Banana](nano-banana.md) and videos via Veo directly from the desktop UI.
- **MCP 3.0 Support**: Native support for Model Context Protocol 3.0, allowing the desktop app to act as an MCP host for local tools.

## Limitations
- **Hardware Bound**: Runs exclusively on Apple Silicon (M1/M2/M3/M4/M5) Macs.
- **OS Requirement**: Requires macOS Sequoia (15.0) or later.
- **Cloud Dependent**: While the app is native, reasoning and generation still happen in Google's cloud (requires internet).

## When to use it
- When you are deeply integrated into the Google Workspace ecosystem.
- When you frequently need to query information about on-screen content (code, spreadsheets, visuals).
- If you prefer a native macOS experience over browser-based chat interfaces.

## When not to use it
- On Intel-based Macs or older macOS versions.
- If you require a fully local, offline AI experience (see [Ollama](../../services/ollama.md) or [Gemma 3](local_llms.md)).
- If your workflow is strictly CLI-based (see [Gemini CLI](gemini-cli.md)).

## Getting started
1. Download the Gemini for macOS installer from the [official Gemini page](https://gemini.google/mac/).
2. Move the application to your `/Applications` folder.
3. Launch the app and sign in with your Google account.
4. **Grant Accessibility Permissions**: Required for screen awareness and tab management features in System Settings > Privacy & Security.

## CLI examples
The macOS application can be controlled or queried via the `gemini-mac` CLI tool (installed via the app's settings):

```bash
# Query the active screen context via CLI
gemini-mac query "Summarize the active window"

# List available MCP tools connected to the desktop app
gemini-mac mcp list

# Trigger a system-wide capture and analysis
gemini-mac capture --analyze "Identify UI bugs"
```

## API examples
Interact with the Gemini macOS bridge via the local MCP 3.0 endpoint (default: `localhost:3000`):

```python
import mcp
from mcp.client.session import ClientSession

async def query_desktop_context():
    async with mcp.connect("http://localhost:3000") as session:
        # Get context from the active macOS window
        context = await session.get_resource("macos://active_window/text")

        # Query Gemini 1.5 Pro via the desktop session
        response = await session.call_tool(
            "gemini_query",
            {"prompt": f"Analyze this context: {context}"}
        )
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(query_desktop_context())
```

## Related tools / concepts
- [ChatGPT for Desktop](chatgpt.md)
- [Claude for Desktop](claude.md)
- [Gemini CLI](gemini-cli.md)
- [Nano Banana](nano-banana.md)
- [Google Gemini](google-gemini.md)
- [Gemma 3](local_llms.md)
- [NotebookLM](notebooklm.md)
- [Gemini Flash TTS](gemini-flash-tts.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)

## Sources / references
- [Google Gemini Mac app debuts to end the clunky hunt for browser tabs](https://thenewstack.io/gemini-app-macos-launch/) (The New Stack, 2026-04-16)
- [Official Gemini macOS Landing Page](https://gemini.google/mac/)
- [Google Blog: Gemini app now on macOS](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-mac-os/)
- [MCP 3.0 Specification for Desktop Agents](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
