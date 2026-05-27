# Curiosity

## What it is
A desktop-first AI search app and knowledge assistant that connects all your local files and cloud apps in one place.

## What problem it solves
Provides a unified search and AI assistant that runs across local folders, emails, and cloud storage (Google Drive, Dropbox, etc.), with a strong emphasis on privacy and local processing.

## Where it fits in the stack
**Category**: Enterprise AI / Personal Productivity

## Typical use cases
- **Unified Search**: Finding a file or email regardless of where it's stored.
- **AI Chat over Local Files**: Asking questions about your own documents without uploading them to a cloud AI.
- **Task Integration**: Pulling together tasks from different apps into a unified view.

## Strengths
- **Privacy-Focused**: Offers local indexing and can work with local LLMs.
- **Desktop Integration**: Fast, keyboard-driven interface (Command+Space style).
- **Extensive Connectors**: Supports a wide variety of cloud and local data sources.

## Limitations
- **Desktop Application**: Primarily designed for desktop use, not a pure web service.
- **Free Tier Limits**: Advanced features and many connectors require a Pro subscription.

## When to use it
- If you value privacy and want to search your local files alongside your cloud data.
- If you prefer a desktop-native experience for your AI assistant.

## When not to use it
- If you only use web-based tools and don't care about local file search.
- For large-scale enterprise-wide knowledge sharing (better suited for individuals and small teams).

## Getting started
Curiosity is a desktop application available for macOS, Windows, and Linux.

1.  **Download and Install**: Get the installer for your platform from the [official website](https://curiosity.ai/).
2.  **Connect Sources**: Open the app and use the "Connect" menu to link your local folders, email accounts (Gmail, Outlook), and cloud storage (Google Drive, Slack).
3.  **Index Data**: Allow Curiosity to index your data locally. This happens on your machine and remains private.
4.  **Search**: Use the global shortcut (default `Alt + Space` or `Cmd + Space`) to start searching.

### Search Examples
You can use advanced filters to narrow down your results:

```text
# Search for PDFs sent from a specific person
from:sarah type:pdf

# Find documents related to a project in a specific folder
project:alpha "budget proposal"

# Search within a specific time range
after:2026-01-01 "quarterly report"
```

## CLI examples
Curiosity is primarily GUI-driven via its Command Palette, but it supports deep-linking and keyboard-first commands:

```text
# Toggle the Curiosity search bar
alt + space

# Open the command palette within the app
cmd + k

# Quick command to connect a new source
> connect
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Pro subscription available)
- **Self-hostable**: Local app

## Related tools / concepts
- [AnythingLLM](../ai_knowledge/anythingllm.md)
- [Khoj](../intake_storage/khoj.md)
- [Msty](../infrastructure/msty.md)

## Sources / references
- [Curiosity Official Site](https://curiosity.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
