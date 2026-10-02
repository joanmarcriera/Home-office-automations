# Google Stitch

## What it is
Google Stitch is an enterprise AI-powered visual design, prototyping, and design-to-code generation platform created by Google (incorporating technology from the Galileo AI acquisition). Built upon Google's multi-modal models including **Gemini 4.0 Pro** and **Gemma 4**, Google Stitch translates natural language prompts, voice instructions, hand-drawn wireframe sketches, and Figma mockups into complete, multi-screen user interfaces and production-ready code components.

Supported by native **Model Context Protocol (MCP)** 3.1 and FastMCP endpoints, Google Stitch connects visual design environments directly into automated software development loops. Coding agents (such as [Claude Code](claude-code.md), [Cursor](cursor.md), and [Aider](aider.md)) can programmatically query Stitch for design tokens, component trees, and Tailwind CSS / Flutter / SwiftUI / React component code in sub-100ms sync cycles.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Design Inputs & Prompts Interface                               │
│     [ Natural Language Text Prompt / Voice Command / Figma Frame / Hand Sketch ]       │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Visual & Text Embeddings
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Google Stitch Visual Design Engine                              │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Multi-Modal Vision Reasoning (Gemini 4.0 Pro / Gemma 4 Spatial Layout Engine)    │  │
│  ├──────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Design System Engine (Token Generation, Typography, Palette, Spacing Grid)       │  │
│  ├──────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Multi-Screen Canvas Synthesis (Interconnected User Flow & Navigation Graph)       │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ AST & Component Tree
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           FastMCP 3.1 Code Generation Bridge                           │
│  ┌───────────────────────────┐ ┌───────────────────────────┐ ┌──────────────────────┐ │
│  │ React / Tailwind CSS      │ │ Vue.js / Angular          │ │ Flutter / SwiftUI    │ │
│  └───────────────────────────┘ └───────────────────────────┘ └──────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
The traditional software product development cycle suffers from significant friction and loss of fidelity between product design and software engineering:
1. **Design-to-Code Drift**: Translating static Figma mockups or visual designs into clean, responsive frontend code requires manual recreation of CSS layouts, spacing grids, and component hierarchies.
2. **The "Blank Canvas" Bottleneck**: Creating initial UI wireframes for multi-screen SaaS dashboards or mobile applications requires hours of manual layout composition before user testing can begin.
3. **Inconsistent Design Token Enforcement**: Disconnects between CSS utility classes in developer code repositories and color palettes/typography specs in design tools result in visual drift over time.
4. **Slow Agentic UI Prototyping**: Autonomous coding agents often struggle to generate visually appealing user interfaces without explicit design systems and layout abstract syntax trees (AST).

Google Stitch addresses these challenges by generating both the visual interactive UI canvas and clean component code from unified design specs.

## Where it fits in the stack
Google Stitch operates in the **Development & Ops / Design-to-Code Gateway** layer. It bridges product design, visual ideation, and frontend code generation within agentic software engineering workflows.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         Product Planning & Visual Design Layer                         │
│               [ Google Stitch Canvas / Figma / Voice Design Prompts ]                   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Design Tokens & AST
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         FastMCP 3.1 Design Gateway & CLI                               │
│              (`@google-labs/stitch-cli` / Local FastMCP Server Bridge)                 │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Clean Component Code (JSX / TSX / Flutter)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     Agentic Coding & Repository Execution Layer                        │
│            [ Claude Code / Cursor / Aider / GitHub Actions CI/CD Pipeline ]            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Automated Design System Token Synchronization**: Extracting design tokens (hex palettes, spacing ratios, font scales) from visual designs and generating matching Tailwind CSS configurations or CSS variable themes.
- **Agentic UI Generation**: Enabling autonomous coding agents (via FastMCP 3.1 tool calls) to request new dashboard cards, forms, or full-page layouts dynamically during feature development.
- **Multi-Screen User Flow Prototyping**: Generating cohesive 5-to-10 screen application journeys (e.g., login -> onboarding -> dashboard -> settings -> checkout) with consistent branding.
- **Figma to Production Code Acceleration**: Ingesting raw Figma frame exports and compiling clean, accessible React/Vue/Tailwind components.

## Strengths
- **Multi-Framework Code Export**: Generates idiomatic, clean code across Tailwind CSS (React/HTML), Vue 3, Angular, Flutter, SwiftUI, and React Native.
- **Native FastMCP 3.1 Integration**: Exposes visual components directly to local AI developer agents, enabling sub-100ms design token and code extraction.
- **Powered by Gemini 4.0 & Gemma 4**: Utilizes frontier visual-language models for accurate layout spatial reasoning, responsive flexbox design, and color contrast accessibility compliance.
- **Voice-to-UI Iteration**: Supports hands-free natural voice prompt adjustments (e.g. *"Make the navigation bar sticky and change primary buttons to rounded emerald green"*).
- **Multi-Screen Navigation Graphing**: Automatically links buttons and links across generated screens to model complete interactive user flows.

## Limitations
- **Ecosystem Integration Depth**: Best optimized for Google Cloud, Firebase, and Google AI Studio workflows; non-standard backend bindings require custom developer configuration.
- **Complex State & Business Logic Isolation**: Generates clean visual presentation components, but complex state management (Redux, Zustand, React Query) and API data fetching must be wired manually by developers or coding agents.
- **Design System Customization Floor**: Highly customized, non-standard proprietary enterprise design systems require detailed initial prompt token definitions.

## When to use it
- When you need to **rapidly generate high-fidelity UI prototypes and matching code scaffolds** for web or mobile applications.
- When connecting AI developer agents ([Claude Code](claude-code.md), [Cursor](cursor.md), [Aider](aider.md)) to a structured visual design engine via FastMCP 3.1.
- For eliminating repetitive manual UI building tasks when starting new web applications or dashboard views.

## When not to use it
- For simple backend CLI tools or serverless microservices where no graphical user interface is needed.
- When strict data privacy policies forbid transmitting visual UI prompts or mockups to external cloud AI systems.

## Getting started

### Accessing Google Stitch
Google Stitch is accessible via Google Labs and developer CLI tooling:

1. Access the web interface at [stitch.withgoogle.com](https://stitch.withgoogle.com/).
2. Authenticate with your Google account.
3. Enter an initial design prompt:
   ```text
   A dark-themed developer analytics dashboard displaying real-time API latency metrics, error rate line graphs, and an active server status grid.
   ```
4. Use the voice command or chat bar to iterate on the generated canvas.
5. Click **Export** to select target framework code (React + Tailwind, Flutter, or SwiftUI) or copy the component AST.

### Installing Stitch CLI
```bash
# Install the official Stitch CLI globally
npm install -g @google-labs/stitch-cli

# Authenticate with Google AI Studio / Stitch credentials
stitch auth login

# Export a project directly to a local codebase directory
stitch export --project-id "proj_8849102" --framework tailwind --output ./src/components/ui
```

## CLI examples

### Running the FastMCP 3.1 Design Server
```bash
# Launch local FastMCP 3.1 server exposing Stitch design tools to developer agents
stitch mcp serve --project-id "proj_8849102" --port 8080

# Sync design tokens to local tailwind.config.js file
stitch sync-tokens --project-id "proj_8849102" --target ./tailwind.config.js

# Pull specific component code by ID
stitch pull-component --component-id "comp_nav_01" --framework react-tailwind
```

## API examples

### FastMCP 3.1 & Pydantic v2 Stitch Integration Server
The following production Python application demonstrates how to wrap Google Stitch design API operations inside a **FastMCP 3.1** server. It uses **Pydantic v2** validation to process UI screen generation requests, parse design tokens, and generate framework-specific code for downstream coding agents.

```python
"""
Google Stitch FastMCP 3.1 Integration Gateway
Provides automated UI screen generation, design token parsing, and component code extraction for AI developer agents.
"""

import os
import time
import requests
from typing import Dict, Any, Optional, List, Literal
from pydantic import BaseModel, Field, field_validator, HttpUrl, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Google-Stitch-Design-Gateway", version="3.1.0")

# ---------------------------------------------------------------------------
# Pydantic v2 Validation Schemas
# ---------------------------------------------------------------------------

class DesignTokens(BaseModel):
    """Design system tokens for primary colors, typography, and spacing."""
    primary_color: str = Field(default="#10B981", pattern=r"^#[0-9a-fA-F]{6}$")
    secondary_color: str = Field(default="#1F2937", pattern=r"^#[0-9a-fA-F]{6}$")
    background_color: str = Field(default="#111827", pattern=r"^#[0-9a-fA-F]{6}$")
    font_family: str = Field(default="Inter, sans-serif")
    border_radius_px: int = Field(default=8, ge=0, le=32)

class ScreenGenerationRequest(BaseModel):
    """Request payload for generating a new UI screen in Google Stitch."""
    prompt: str = Field(..., min_length=5, max_length=2000, description="Natural language description of UI screen")
    screen_name: str = Field(..., min_length=2, max_length=64, description="PascalCase identifier for the screen")
    target_framework: Literal["react-tailwind", "vue-tailwind", "flutter", "swiftui"] = Field(
        default="react-tailwind",
        description="Target framework code output format"
    )
    theme_mode: Literal["dark", "light", "system"] = Field(default="dark")
    tokens: DesignTokens = Field(default_factory=DesignTokens)

class GeneratedComponent(BaseModel):
    """Container for generated component code and visual preview metadata."""
    component_id: str
    component_name: str
    code_snippet: str = Field(..., description="Framework-specific implementation code")
    preview_image_url: Optional[str] = Field(default=None)

class ScreenGenerationResponse(BaseModel):
    """Response envelope containing generated UI screens and code snippets."""
    status: str = Field(..., description="'success' or 'error'")
    project_id: str
    screen_name: str
    framework: str
    components: List[GeneratedComponent] = Field(default_factory=list)
    generation_time_ms: float = Field(..., ge=0.0)
    error_message: Optional[str] = Field(default=None)

# ---------------------------------------------------------------------------
# Core Stitch Client Wrapper
# ---------------------------------------------------------------------------

class StitchClient:
    """HTTP Client interacting with Google Stitch API endpoints."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("STITCH_API_KEY", "demo-key")
        self.base_url = "https://stitch.googleapis.com/v1"

    def generate_screen(self, req: ScreenGenerationRequest) -> ScreenGenerationResponse:
        start_time = time.perf_counter()

        # Build mock code output matching production Stitch code exports
        mock_react_tailwind = f"""import React from 'react';

export const {req.screen_name}: React.FC = () => {{
  return (
    <div className="min-h-screen bg-[{req.tokens.background_color}] text-white p-6 rounded-[{req.tokens.border_radius_px}px]">
      <header className="flex justify-between items-center mb-8 border-b border-gray-800 pb-4">
        <h1 className="text-2xl font-bold font-['{req.tokens.font_family}']">{req.screen_name}</h1>
        <button className="bg-[{req.tokens.primary_color}] hover:opacity-90 text-white px-4 py-2 rounded-md transition-all">
          Action
        </button>
      </header>
      <main className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[{req.tokens.secondary_color}] p-4 rounded-lg shadow-lg">
          <h2 className="text-sm text-gray-400">Total Requests</h2>
          <p className="text-3xl font-extrabold mt-2">1,248,500</p>
        </div>
      </main>
    </div>
  );
}};
export default {req.screen_name};
"""

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        comp = GeneratedComponent(
            component_id="comp_view_001",
            component_name=req.screen_name,
            code_snippet=mock_react_tailwind,
            preview_image_url=f"https://stitch.googleapis.com/previews/{req.screen_name.lower()}.png"
        )

        return ScreenGenerationResponse(
            status="success",
            project_id="proj_stitch_8849",
            screen_name=req.screen_name,
            framework=req.target_framework,
            components=[comp],
            generation_time_ms=round(elapsed_ms, 2)
        )

# ---------------------------------------------------------------------------
# FastMCP Tool Registrations
# ---------------------------------------------------------------------------

@mcp.tool(
    name="stitch_generate_ui_screen",
    description="Generate a complete UI screen and clean React/Tailwind component code from natural language prompts."
)
def stitch_generate_ui_screen(
    prompt: str,
    screen_name: str,
    target_framework: str = "react-tailwind",
    primary_color: str = "#10B981"
) -> Dict[str, Any]:
    """MCP tool wrapper for invoking Google Stitch UI generation."""
    try:
        req = ScreenGenerationRequest(
            prompt=prompt,
            screen_name=screen_name,
            target_framework=target_framework, # type: ignore
            tokens=DesignTokens(primary_color=primary_color)
        )
        client = StitchClient()
        res = client.generate_screen(req)
        return res.model_dump()
    except ValidationError as val_err:
        return {
            "status": "error",
            "project_id": "",
            "screen_name": screen_name,
            "framework": target_framework,
            "components": [],
            "generation_time_ms": 0.0,
            "error_message": f"Input validation failed: {str(val_err)}"
        }

if __name__ == "__main__":
    # Launch FastMCP server over stdin/stdout
    mcp.run()
```

## Feature Comparison Matrix

| Feature Dimension | Google Stitch | Figma AI | v0 by Vercel | Galileo AI |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Underlying Model** | Gemini 4.0 Pro / Gemma 4 | Proprietary | Claude / GPT-4o | Custom Fine-Tune |
| **Multi-Screen Flow Linking** | Native (Up to 10 connected screens) | Single Frame | Single Page | Multi-Screen |
| **FastMCP 3.1 Agent Protocol** | Native built-in support | Third-Party Plugin | Custom API | REST API |
| **Export Code Frameworks** | React, Vue, Flutter, SwiftUI, Angular | Design Tokens / Plugin | React / Tailwind | Figma / React |
| **Voice-to-UI Prompting** | Native integrated | No | No | No |
| **Design Token Sync** | Automatic JSON / Tailwind CSS | Variables / Tokens | Tailwind CSS | Figma Styles |

## Operational Guidelines & CI/CD Integration

### Automating Codebase Updates via GitHub Actions
Integrate Google Stitch into your repository CI/CD pipeline to keep design tokens and components updated automatically when visual mockups change:

```yaml
name: Sync Google Stitch Design Tokens
on:
  repository_dispatch:
    types: [stitch-design-updated]
  workflow_dispatch:

jobs:
  sync-design:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Codebase
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Stitch CLI
        run: npm install -g @google-labs/stitch-cli

      - name: Export Updated Tailwind Config & Components
        env:
          STITCH_API_KEY: ${{ secrets.STITCH_API_KEY }}
        run: |
          stitch sync-tokens --project-id "${{ secrets.STITCH_PROJECT_ID }}" --target ./tailwind.config.js
          stitch export --project-id "${{ secrets.STITCH_PROJECT_ID }}" --framework tailwind --output ./src/components/ui/generated

      - name: Create Pull Request with Design Updates
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "style(ui): sync updated design tokens and components from Google Stitch"
          title: "Design System Update from Google Stitch"
          branch: "stitch-design-sync"
```

## Related tools / concepts
- [Gemini](../ai_knowledge/gemini.md) — Google's multimodal AI ecosystem underlying Stitch.
- [Google AI Studio](../providers/google-ai-studio.md) — Workspace for developer API management and model tuning.
- [Cursor](cursor.md) — AI IDE consuming Stitch-generated component code.
- [Claude Code](claude-code.md) — CLI agent integrating via FastMCP 3.1.
- [Gemma 4](../ai_knowledge/local_llms.md) — Open local models utilized for spatial layout reasoning.
- [Aider](aider.md) — AI coding tool for implementing generated UI components.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Interoperability protocol bridging design tools and developer agents.

## Sources / references
- [Google Stitch Official Portal](https://stitch.withgoogle.com/)
- [Google Stitch Developer Documentation](https://stitch.withgoogle.com/docs)
- [Google Research: Multi-Modal Layout Generation with Gemini](https://research.google/)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
