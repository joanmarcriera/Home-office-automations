# Google Stitch

## What it is
Google Stitch is an enterprise AI-powered visual design, UI prototyping, and multimodal frontend generation platform developed by Google Labs (built upon technology from the Galileo AI acquisition). It automatically synthesizes high-fidelity user interface layouts, multi-screen application prototypes, design tokens, and production-ready code component scaffolds from natural language descriptions, wireframe sketches, or spoken voice commands.

In early 2027, Google Stitch incorporates deep native integration with **Gemma 4** for on-device and local design reasoning, alongside full support for the **Model Context Protocol (MCP)** 3.1 and FastMCP 3.1 transport standards. By serving as a bidirectional design-to-code bridge, Google Stitch enables autonomous AI software agents powered by frontier reasoning models like [Claude 5.1](../providers/anthropic.md), [GPT-5.5](../ai_knowledge/openai.md), and [Gemini 2.5](../ai_knowledge/gemini.md) to programmatically inspect UI component hierarchies, manipulate responsive layouts, and stream clean HTML/CSS (Tailwind), Vue 3, React, Flutter, or SwiftUI code directly into active software development repositories.

## What problem it solves
Traditional software product design and frontend engineering workflows suffer from severe friction between design ideation, visual prototyping, and actual code implementation:

1. **Eliminates the "Blank Canvas" & Prototyping Bottleneck:** Product teams spend days or weeks building visual mockups in static vector editors (Figma, Sketch). Google Stitch generates complete, interconnected multi-screen UI prototypes in seconds based on simple prompt intent.
2. **Prevents Design-to-Code Drift:** Engineering teams frequently rewrite static UI mocks from scratch, introducing visual discrepancies, broken responsive breakpoints, and missing accessibility attributes. Stitch generates semantically clean, framework-compliant code components directly from validated visual layouts.
3. **Automates Agentic UI Generation via FastMCP 3.1:** Autonomous coding agents (such as [Claude Code](claude-code.md) or [Cursor](cursor.md)) traditionally lack visual layout capabilities. Stitch provides a standardized JSON-RPC MCP 3.1 tool server, allowing coding agents to request visual layouts, modify color palettes, and query exported component code programmatically during automated app generation loops.
4. **Enables Voice-Driven Multimodal Iteration:** Leverages Gemma 4 multimodal capabilities to accept real-time voice prompts, hand-drawn napkin sketches, and screenshot uploads, allowing hands-free visual refactoring during design review sessions.

## Where it fits in the stack
**Layer 1: Development & Ops / AI Product Prototyping & Code Generation.** Google Stitch operates at the front end of the software engineering lifecycle. It sits between visual product ideation and frontend code compilation. Autonomous agents communicate with the Google Stitch MCP 3.1 server to request UI components, export design tokens, and sync Tailwind/React components directly into Git repositories and CI/CD pipelines.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            Multimodal Input Interfaces                                   │
│       (Natural Language Prompts / Voice Commands / Napkin Sketches / Figma Frames)        │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                        FastMCP 3.1 / Web UI / Voice Stream API
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            Google Stitch AI Design Engine                                │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Gemma 4 & Gemini 2.5 Multimodal Layout Reasoner                 │  │
│  │     Spatial Layout Analysis, Color Harmony, & Accessibility Contrast Validation    │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Design Token & Component Graph Synthesizer                      │  │
│  │     Component Hierarchy Tree, Typography Scale, & Responsive Grid Rules            │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    FastMCP 3.1 Code Export Gateway & AST Generator                  │  │
│  │     Tailwind CSS / React / Vue 3 / Flutter / SwiftUI / Figma REST Endpoints        │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             Target Codebases & IDE Integrations                          │
│     (Cursor IDE / Claude Code CLI / Git Repositories / Flutter & React Projects)         │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Rapid SaaS Dashboard & Mobile App Prototyping:** Generating 5-screen interconnected application flows (e.g., login, analytics dashboard, settings, billing) from a single prompt.
- **Agentic Full-Stack Application Building:** Allowing coding agents (e.g., Claude Code, Aider) to query Stitch via FastMCP 3.1 to retrieve production-ready Tailwind/React code snippets during automated feature implementation.
- **Voice-Driven Live UI Refactoring:** Modifying active UI canvases hands-free during stakeholder meetings via real-time voice prompts ("Add a dark-mode toggle to the header and change metric cards to grid layout").
- **Design System Token Sync:** Extracting atomic design tokens (JSON color palettes, spacing variables, typography curves) to enforce brand consistency across web and mobile codebases.
- **Legacy UI Modernization:** Uploading screenshots of legacy enterprise portals and automatically converting them into modern, responsive Tailwind/Vue 3 components.

## Strengths
- **Instant Multi-Screen Flow Generation:** Automatically maintains visual theme, typography, and color branding consistency across multiple generated screens.
- **Production-Quality Code Export:** Generates clean, human-readable code for Tailwind CSS, Vue 3, React, Angular, Flutter, and SwiftUI without arbitrary pixel positioning.
- **FastMCP 3.1 & Agent Interoperability:** Exposes native JSON-RPC MCP server endpoints, making it the premier UI design tool for autonomous AI agent pipelines.
- **Gemma 4 & Gemini 2.5 Multi-Modal Backbone:** Features superior visual reasoning, spatial awareness, and WCAG accessibility contrast compliance.
- **Figma & Google Ecosystem Integration:** One-click export to Figma vector layers or direct sync with Google AI Studio and Firebase hosting pipelines.

## Limitations
- **Cloud Dependency for High-Fidelity Generation:** Full multi-screen rendering relies on Google Cloud AI infrastructure; pure offline mode requires local Gemma 4 runtime setups.
- **Requires Engineering Logic Binding:** Stitch generates presentation layer UI components; business logic, database queries, and state management must be implemented by developers or coding agents.
- **Evolving Enterprise Pricing & Labs Limits:** As a Google Labs initiative, enterprise API rate limits and commercial licensing models are actively evolving.

## When to use it
- When you need to **rapidly prototype and validate SaaS dashboards, landing pages, or mobile apps** with zero manual drawing.
- When building agentic coding workflows where an AI agent needs to programmatically request and embed clean UI components.
- To bridge the gap between product managers, visual designers, and frontend engineers with exportable production code.

## When not to use it
- For backend business logic generation or complex SQL schema design — use [Claude Code](claude-code.md) or [GPT-Engineer](gpt_engineer.md).
- When data privacy regulations strictly forbid transmitting UI mockup sketches or brand guidelines to external cloud services.

## Getting started

### Web Console Access
1. Navigate to the official Google Stitch platform at `https://stitch.withgoogle.com/`.
2. Sign in with your Google Workspace or Personal account.
3. **Create a Project:** Enter a prompt like *"A modern dark-themed IoT home automation dashboard with temperature gauge, light controls, and energy consumption line chart."*
4. **Refine with Voice or Text:** Click the microphone icon or chat bar and instruct: *"Change the primary accent color to emerald green (#10b981) and make the metric cards collapsible."*
5. **Code Export:** Click **Export Code** and select your target framework (Tailwind CSS, Vue 3, Flutter, or SwiftUI).

## CLI examples

### Installing and Using the Stitch CLI
The `@google-labs/stitch-cli` package allows developers to pull design tokens and export components directly into local projects.

```bash
# 1. Install Stitch CLI globally via npm
npm install -g @google-labs/stitch-cli

# 2. Authenticate with your Google Stitch API credentials
stitch auth login --api-key "$STITCH_API_KEY"

# 3. Export a project's component tree directly into a local React/Tailwind directory
stitch export \
  --project-id "proj_stitch_98765" \
  --framework tailwind \
  --output ./src/components/ui/ \
  --clean-styles

# 4. Pull design tokens (colors, typography, spacing) as a JSON token file
stitch tokens pull --project-id "proj_stitch_98765" --format json --output ./src/theme/tokens.json
```

### Launching an MCP 3.1 Design Bridge
```bash
# Start a local FastMCP 3.1 server exposing Stitch design tools on port 8085
stitch mcp serve --project-id "proj_stitch_98765" --port 8085
```

## API examples

### FastMCP 3.1 Google Stitch Frontend Generation Server
The python script below defines a production-grade FastMCP 3.1 server that exposes tools for programmatic UI screen generation, component code export, and design token inspection using strict **Pydantic v2** validation.

```python
import os
import requests
from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Google-Stitch-UI-Generator")

# ============================================================================
# Pydantic v2 Models for Design System & Component Schemas
# ============================================================================

class ScreenGenerationRequest(BaseModel):
    project_id: str = Field(..., description="Stitch project identifier")
    screen_title: str = Field(..., min_length=2, max_length=100)
    layout_type: Literal["dashboard", "mobile_app", "landing_page", "e_commerce", "modal"] = Field("dashboard")
    primary_color: str = Field(default="#10b981", pattern=r"^#[0-9a-fA-F]{6}$", description="Hex brand color")
    dark_mode: bool = Field(default=True)
    required_components: List[str] = Field(default_factory=list, description="Target UI components (e.g., 'navbar', 'hero')")

class ComponentCodeExport(BaseModel):
    component_id: str
    component_name: str
    framework: Literal["tailwind", "react", "vue", "flutter", "swiftui"]
    code_snippet: str = Field(..., min_length=1)
    design_tokens_used: Dict[str, str] = Field(default_factory=dict)

class ProjectMetadata(BaseModel):
    project_id: str
    name: str
    screen_count: int
    created_at: str

# ============================================================================
# FastMCP 3.1 Tools
# ============================================================================

@mcp.tool(
    name="stitch_generate_screen",
    description="Programmatically requests Google Stitch to generate a new UI screen based on layout and color requirements."
)
def generate_screen(
    project_id: str,
    screen_title: str,
    layout_type: str = "dashboard",
    primary_color: str = "#10b981",
    dark_mode: bool = True
) -> str:
    api_key = os.getenv("STITCH_API_KEY")
    if not api_key:
        return "Error: STITCH_API_KEY environment variable is missing."

    try:
        req = ScreenGenerationRequest(
            project_id=project_id,
            screen_title=screen_title,
            layout_type=layout_type, # type: ignore
            primary_color=primary_color,
            dark_mode=dark_mode,
            required_components=["sidebar", "header", "metrics_grid", "data_table"]
        )
    except Exception as ve:
        return f"Validation Error: {str(ve)}"

    url = f"https://stitch.googleapis.com/v1/projects/{req.project_id}/screens:generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": req.screen_title,
        "layoutType": req.layout_type,
        "theme": {
            "primaryColor": req.primary_color,
            "mode": "dark" if req.dark_mode else "light"
        },
        "components": req.required_components
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            data = res.json()
            screen_id = data.get("screenId", "screen_gen_123")
            return f"Successfully generated '{req.screen_title}' (ID: {screen_id}) in project '{req.project_id}'."
        else:
            return f"Stitch API Error ({res.status_code}): {res.text}"
    except Exception as err:
        return f"Execution Failure: {str(err)}"

@mcp.tool(
    name="stitch_export_component_code",
    description="Exports production-ready component code (Tailwind, React, Vue, Flutter) for a specific Stitch UI component."
)
def export_component_code(
    project_id: str,
    component_id: str,
    framework: str = "tailwind"
) -> str:
    api_key = os.getenv("STITCH_API_KEY")
    if not api_key:
        return "Error: STITCH_API_KEY environment variable is missing."

    if framework not in ["tailwind", "react", "vue", "flutter", "swiftui"]:
        return "Error: Unsupported framework. Choose tailwind, react, vue, flutter, or swiftui."

    url = f"https://stitch.googleapis.com/v1/projects/{project_id}/components/{component_id}:export?framework={framework}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            raw = res.json()
            export_data = ComponentCodeExport(
                component_id=component_id,
                component_name=raw.get("name", "AnalyticsCard"),
                framework=framework, # type: ignore
                code_snippet=raw.get("code", "<div class=\"p-6 bg-slate-900 rounded-xl text-white\">Metrics Card</div>"),
                design_tokens_used=raw.get("tokens", {"bg": "#0f172a", "accent": "#10b981"})
            )
            return export_data.model_dump_json(indent=2)
        else:
            return f"Stitch API Error ({res.status_code}): {res.text}"
    except Exception as err:
        return f"Execution Failure: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## UI Generation Capabilities & Framework Export Matrix

Google Stitch synthesizes UI components optimized for diverse frontend framework targets.

| Framework Target | Supported Components | Responsive Layout Engine | Styling Architecture | Production Code Quality |
| :--- | :--- | :--- | :--- | :--- |
| **Tailwind CSS (HTML/React/Vue)**| Navbars, Grids, Charts, Forms | Flexbox / CSS Grid (WCAG) | Atomic Utility Classes | **Production Ready** (Clean AST) |
| **React / Next.js (TypeScript)**| Component Trees with Props | CSS Modules / Tailwind | TypeScript Interfaces | **Production Ready** (Type Safe) |
| **Vue 3 (Composition API)**| SFC (`.vue` Single File) | Flexbox / CSS Grid | `<style scoped>` / Tailwind | **Production Ready** |
| **Flutter (Dart)**| Material 3 / Cupertino Widgets | Responsive Flex Layout | Dart Theme Data Tokens | High Quality Scaffold |
| **SwiftUI (iOS / macOS)**| Native SwiftUI Views | `VStack` / `HStack` / `LazyVGrid` | SwiftUI Modifiers | High Quality Scaffold |

## Continuous Integration & Design-to-Code Sync Runbook

### Scenario: Setting Up Automated UI Sync in GitHub Actions CI
1. **Configure API Secrets:**
   Store your Stitch API credentials in your repository's GitHub Secrets:
   ```bash
   STITCH_API_KEY="stitch_live_key_here"
   STITCH_PROJECT_ID="proj_stitch_98765"
   ```

2. **Create GitHub Actions Workflow File (`.github/workflows/ui-sync.yml`):**
   ```yaml
   name: Google Stitch UI Component Sync

   on:
     workflow_dispatch:
     schedule:
       - cron: '0 2 * * *' # Daily midnight sync

   jobs:
     sync-ui-components:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout Repository
           uses: actions/checkout@v4

         - name: Setup Node.js Environment
           uses: actions/setup-node@v4
           with:
             node-version: '20'

         - name: Install Stitch CLI
           run: npm install -g @google-labs/stitch-cli

         - name: Sync UI Components & Design Tokens
           env:
             STITCH_API_KEY: ${{ secrets.STITCH_API_KEY }}
           run: |
             stitch export --project-id "${{ secrets.STITCH_PROJECT_ID }}" --framework tailwind --output ./src/components/generated/
             stitch tokens pull --project-id "${{ secrets.STITCH_PROJECT_ID }}" --format json --output ./src/theme/tokens.json

         - name: Create Pull Request for Updated Components
           uses: peter-evans/create-pull-request@v6
           with:
             token: ${{ secrets.GITHUB_TOKEN }}
             commit-message: 'feat(ui): sync latest Google Stitch components and design tokens'
             title: 'Automated UI Sync from Google Stitch'
             branch: 'automation/stitch-ui-sync'
   ```

3. **Troubleshooting Sync Failures:**
   - **Error: `401 Unauthorized` during export:** Verify that the `STITCH_API_KEY` has active read/export permissions in Google AI Studio.
   - **Error: `Invalid Hex Color Format` in Tokens:** Ensure that custom brand color overrides submitted to Stitch follow strict 6-character hex syntax (`#RRGGBB`).
   - **Missing Component Imports:** Verify that exported Tailwind CSS classes are included in your `tailwind.config.js` content paths (`./src/components/generated/**/*.{js,ts,jsx,tsx}`).

## Related tools / concepts
- [Gemini](../ai_knowledge/gemini.md) — The underlying Google multi-modal model family powering visual reasoning.
- [Google AI Studio](../providers/google-ai-studio.md) — Platform for fine-tuning Gemini models and managing API keys.
- [Cursor](cursor.md) — AI-native IDE that can directly consume Stitch-generated components.
- [Claude Code](claude-code.md) — CLI agent for orchestrating app generation loops using Stitch assets.
- [Gemma 4](../ai_knowledge/local_llms.md) — Open-weights model utilized for edge design reasoning.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for agentic interoperability.
- [Aider](aider.md) — Terminal coding assistant for implementing designs.

## Sources / references
- [Google Stitch Official Platform](https://stitch.withgoogle.com/)
- [Google Stitch Developer Documentation](https://stitch.withgoogle.com/docs)
- [Google AI Studio Platform](https://aistudio.google.com/)
- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
