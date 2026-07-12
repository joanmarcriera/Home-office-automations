# Google Stitch

## What it is
Google Stitch is an AI-powered design and prototyping tool from Google (built on technology from the 2025 Galileo AI acquisition). It generates complete, high-fidelity user interfaces from natural language descriptions and voice commands. As of July 2026, it features deep integration with **Gemma 3** for edge-based design reasoning and supports the **MCP 3.0 Task Protocol** for automated UI-to-code pipelines.

## What problem it solves
It eliminates the "blank canvas" problem for designers and developers by instantly generating polished UI layouts, multi-screen prototypes, and production-ready code scaffolds from simple prompts. The inclusion of **FastMCP 3.0** support allows development environments to bridge design and code in sub-100ms sync cycles.

## Where it fits in the stack
**Development & Ops / Product Prototyping**. It is useful early in the build loop when teams want concrete UI output quickly and integrated into their agentic workflows.

## Typical use cases
- **Rapid UI Concept Generation**: Instantly creating visual mockups for SaaS dashboards, mobile apps, and landing pages.
- **Agentic Prototyping**: Using the **MCP 3.0** interface to allow coding agents (like Claude Code) to request UI refinements programmatically.
- **Voice-to-Design**: Native support for voice commands to iterate on designs hands-free, powered by **Gemma 3**'s multi-modal capabilities.
- **Production-Ready Scaffolding**: Exporting designs directly into Tailwind, Vue, Flutter, or SwiftUI codebases.

## Strengths
- **Real-Time AI Agent**: Features a streaming AI agent that reflows and modifies layouts in real-time as you type or speak.
- **Multi-Screen Generation**: Can generate up to 5 interconnected screens from a single prompt, maintaining consistent branding and design language.
- **Robust Code Export**: Supports a wide range of formats including HTML/CSS (Tailwind), Vue, Angular, Flutter, and SwiftUI.
- **Gemma 3 Powered**: Leverages the latest open models for superior design reasoning and multi-modal understanding.
- **MCP 3.0 Support**: Allows external tools and agents to interact with the design canvas programmatically.

## Limitations
- **Google Ecosystem Tie-in**: Best integrated with Google services and AI Studio; less flexible for non-standard stacks.
- **Labs Status**: Still in the "Google Labs" phase, meaning features and pricing models are subject to rapid change (Paid plans expected Q4 2026).
- **Engineering Review Required**: While code export is advanced, the logic behind the UI components often requires manual implementation.

## When to use it
- For rapid prototyping of SaaS dashboards, mobile apps, and landing pages.
- When you need high-fidelity visual mockups quickly for stakeholder review.
- To bridge the gap between design and front-end development using production-ready code exports.

## When not to use it
- For complex, highly customized UI components that require proprietary design systems.
- When data privacy requirements prohibit the use of cloud-based AI design tools.

## Getting started
Google Stitch is a web-based design platform accessible through Google Labs.

To begin using it:
1. Visit the [official Stitch website](https://stitch.withgoogle.com/).
2. Sign in with your Google account.
3. **Draft your first screen**: Enter a prompt like *"A dark-themed meditation app with a focus timer and audio player"* or use the voice icon to describe your idea.
4. **Iterate with the Agent**: Use the real-time chat bar to say *"Add a profile section in the top right"* or *"Change the primary color to emerald green."*
5. **Multi-screen Expansion**: Click "Generate Connected Screens" to build out the user journey (e.g., login, settings, success states).
6. **Export**: Click the **Export** button to get code in your preferred framework (Tailwind, Vue, Flutter, etc.) or send the design to Figma.

## CLI examples
*Note: Google Stitch is primarily a web-based GUI tool, but it offers a CLI for asset synchronization and code export pipelines.*

### Install Stitch CLI
```bash
npm install -g @google-labs/stitch-cli
```

### Export a Project to Code
```bash
stitch export --project-id "proj_12345" --framework tailwind --output ./src/components
```

### Start an MCP Design Server
```bash
stitch mcp serve --project-id "proj_12345"
```

## API examples

### Programmatic Screen Generation (Node.js)
```javascript
import { StitchClient } from '@google-labs/stitch-sdk';

const client = new StitchClient({ apiKey: process.env.STITCH_API_KEY });

const project = await client.createProject({
  name: "My AI App",
  initialPrompt: "A minimalist dashboard for task management using Gemma 3 tokens",
  theme: "modern-dark"
});

console.log(`Project created: ${project.url}`);
```

### Fetching Component Code via MCP
```javascript
// Using an MCP client to interact with Stitch
const mcpClient = new MCPClient({ serverUrl: 'http://localhost:8080' });
const tailwindCode = await mcpClient.callTool('get_component_code', {
  projectId: 'proj_12345',
  componentId: 'comp_6789',
  framework: 'tailwind'
});
console.log(tailwindCode);
```

## Related tools / concepts
- [Google Gemini](../ai_knowledge/google-gemini.md) — The underlying model ecosystem.
- [Google AI Studio](../ai_knowledge/google-ai-studio.md) — For deeper model configuration.
- [Cursor](cursor.md) — IDE that can consume Stitch-generated code.
- [Claude Code](claude-code.md) — CLI agent for building apps with Stitch assets.
- [Gemma 3](../ai_knowledge/local_llms.md) — Local models used for design reasoning.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for interoperability.
- [Aider](aider.md) — For automated code implementation of designs.
- [v0.dev](https://v0.dev) — Alternative AI-native UI generation.

## Sources / References
- [Official Website](https://stitch.withgoogle.com/)
- [Google I/O 2026: The Future of Design with Stitch](https://io.google/2026/sessions/stitch-design-ai)
- [Stitch Developer Docs](https://stitch.withgoogle.com/docs)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
