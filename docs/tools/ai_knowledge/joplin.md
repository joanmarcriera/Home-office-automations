# Joplin

## What it is
Joplin is a free, open-source note-taking and to-do application, which can handle a large number of notes organized into notebooks.

## What problem it solves
It provides a secure, private way to sync notes across multiple devices (desktop and mobile) using various cloud or self-hosted services (Nextcloud, Dropbox, WebDAV, etc.). It supports end-to-end encryption (E2EE).

## Where it fits in the stack
**Tool / AI Assistants & Knowledge**. It serves as a privacy-focused knowledge management and note-taking tool.

## Typical use cases
- Organizing personal and professional notes in a structured notebook format.
- Capturing web pages and screenshots using the web clipper extension.
- Syncing notes across devices with E2EE for maximum privacy.

## Getting started
To start using Joplin, download the application for your platform:

1. **Desktop**: Download from the [Official Website](https://joplinapp.org/).
2. **Mobile**: Available on the App Store and Google Play.
3. **CLI**: Install the terminal application via NPM:
   ```bash
   npm install -g joplin
   ```
4. **Web Clipper**: Install the extension for Chrome or Firefox to capture web content directly into Joplin.

## Technical Details: Data API
Joplin provides a REST API to interact with your notes locally. The API is available when the Joplin application is running and the "Web Clipper" service is enabled.

### API Configuration
1. Enable "Web Clipper" in Joplin settings.
2. Note the "Authorization token" provided in the settings.
3. The default port is `41184`.

### CLI Example (REST API)
To list all notebooks using `curl`:
```bash
curl -X GET "http://localhost:41184/folders?token=YOUR_TOKEN"
```

To create a new note in a specific folder:
```bash
curl -X POST "http://localhost:41184/notes?token=YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My New Note",
       "body": "Content of the note in Markdown",
       "parent_id": "FOLDER_ID"
     }'
```

## Technical Details: Terminal Application
Joplin also offers a full-featured terminal application for users who prefer working in a console environment.

```bash
# Start the terminal application
joplin

# Use internal commands
:help
:ls
:edit "Note Title"
```

## Encryption (E2EE)
Joplin supports End-to-End Encryption (E2EE) for all your notes. When enabled, notes are encrypted on your device before being synced to any cloud target. This ensures that even if the sync target (e.g., Dropbox or Nextcloud) is compromised, your notes remain unreadable without your master password.

## Web Clipper
The Web Clipper is a browser extension that allows you to save web pages and screenshots directly from your browser. It supports:
- Simplified page capture (removing ads and clutter).
- Complete web page capture.
- Selection capture.
- Screenshot capture.

## Strengths
- **Privacy**: Strong E2EE and support for various sync targets (including self-hosted).
- **Format**: Notes are stored in Markdown format.
- **Extensibility**: Support for plugins and themes.
- **Web Clipper**: Powerful extension for capturing online content.

## Limitations
- **Sync Conflict Resolution**: Can sometimes be less intuitive than cloud-native alternatives like Notion.
- **UI**: While functional, the UI might feel less "polished" to some users compared to proprietary tools.

## When to use it
- When you need a cross-platform, open-source note-taking app with strong privacy features.
- When you want to host your own note synchronization (e.g., using Nextcloud).

## When not to use it
- When real-time, multi-user collaboration is the primary requirement.
- When you prefer the "canvas" or "block" based approach of tools like Obsidian or Notion.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes (sync targets can be self-hosted)

## Related tools / concepts
- [Obsidian](obsidian.md)
- [Logseq](logseq.md)
- [Trilium Notes](../../services/trilium.md)
- [Anytype](../intake_storage/anytype.md)
- [Nextcloud](../../services/nextcloud.md)
- [Khoj](../intake_storage/khoj.md)
- [Notion AI](notion-ai.md)

## Sources / References
- [Official Website](https://joplinapp.org/)
- [Joplin Data API Reference](https://joplinapp.org/api/references/rest_api/)
- [Joplin GitHub](https://github.com/laurent22/joplin)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
