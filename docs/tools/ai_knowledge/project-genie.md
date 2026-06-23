# Project Genie

## What it is
Project Genie is a generative world model from Google DeepMind that can create interactive, navigable virtual environments from a single image or text prompt. Unlike traditional video generation, Genie produces a "world" that a user can actually control and explore in real-time, essentially acting as an AI-powered game engine that learns physics and mechanics from unlabeled internet videos. In June 2026, it serves as a foundational layer for the [Anti-Gravity](../../tools/agents/agno.md) agentic framework, providing simulated "Missions" for Gemini 3.5 agents.

## What problem it solves
It bridges the gap between passive content generation (like Sora) and interactive experiences. Traditionally, building a navigable 3D or 2D world requires thousands of hours of manual asset creation, physics programming, and level design. Genie automates this by "imagining" the world and its underlying rules of movement and interaction. It allows for the rapid creation of "synthetic training grounds" for agents to practice tool-use and navigation without real-world risk.

## Where it fits in the stack
Project Genie sits at the **Generative World Models** layer of the AI stack. It provides the environmental substrate for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) and acts as a high-fidelity simulator for reinforcement learning, often interfaced via [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) for agent interaction.

## Typical use cases
- **Rapid Game Prototyping**: Generating a playable level from a sketch or a few sentences.
- **Agent Training**: Creating diverse "gym" environments for training robotic or digital agents in safe, simulated physics.
- **Interactive Storytelling**: Allowing users to enter and navigate a scene described in a narrative.
- **Remixing Content**: Taking an existing image and transforming it into a navigable "remix."
- **Simulated Mission Design**: Creating complex environments for [Anti-Gravity](../../tools/agents/agno.md) agents to solve multi-step objectives.

## Strengths
- **Interactive Consistency**: The world remains stable as you move; objects don't disappear when you look away.
- **Zero-Code Mechanics**: Infers physics (gravity, collision, friction) without explicit programming.
- **Multi-Modal Input**: Can be triggered by text, images, or even rough sketches.
- **Real-Time Performance**: Optimized for low-latency inference on TPU v6 clusters, achieving 720p/24fps.

## Limitations
- **Resolution**: While high for real-time generative video (720p), it still lacks the fidelity of modern high-end game engines like Unreal Engine 5.
- **Memory Horizon**: The "consistency" of the world may drift after several minutes of continuous, far-ranging navigation.
- **Compute Intensity**: Requires significant TPU/GPU resources for real-time inference, typically served via cloud APIs.

## When to use it
- When you need a custom, navigable environment for an AI agent to explore.
- For "vibe-based" game development where the atmosphere is more important than specific hardcoded mechanics.
- To create interactive demos for creative concepts or architectural visualizations.
- For testing [Agent Protocols](../../knowledge_base/agent_protocols.md) in non-deterministic environments.

## When not to use it
- For production-grade games that require precise, pixel-perfect collision and deterministic physics.
- In low-latency applications where any frame generation delay is unacceptable (sub-16ms).
- When operating in extremely resource-constrained environments without cloud connectivity.

## Getting started

### Prompting Genie 3
Effective world generation in Genie 3 involves three core elements: the **Environment**, the **Character**, and the **World Sketch**.

#### Example: Text-to-World Prompt
```text
Environment: A neon-lit cyberpunk cityscape during a rainy night. Surfaces are slick asphalt with neon reflections. Distant skyscrapers with glowing advertisements.
Character: A sleek hover-bike that drifts through corners.
Action: Navigate the bike through tight alleys and over high-rise bridges.
```

### Navigating the World
Once the world is generated:
1.  **Select the Character**: Click on the object you wish to control.
2.  **Input Actions**: Use standard WASD or arrow keys. Genie interprets these "latent actions" based on the character's inferred physics.

## CLI examples

### Generating a World from a Sketch
Using the `genie-cli` (v2026.4):

```bash
# Generate a world from an image and save the latent representation (world sketch)
genie-cli generate --image ./concept_art.png --output ./worlds/cyberpunk.genie

# Start an interactive session with a specific latent action mapping
genie-cli play ./worlds/cyberpunk.genie --mapping platformer
```

### Exporting World Metadata
```bash
# View the physics parameters inferred by the model
genie-cli inspect ./worlds/cyberpunk.genie --physics
```

## API examples

### Integration with Anti-Gravity Agent
The following example shows how to load a Genie environment for a Gemini 3.5 agent using the Managed Agents API (June 2026).

```python
import google_antigravity as ag
from google_genie import GenieEnvironment

# Load the generative world
world = GenieEnvironment.load("cyberpunk_city_v3")

# Initialize the agent with the Genie world as its surface
agent = ag.Agent(
    model="gemini-3.5-pro",
    surface=world,
    mission="Locate the hidden terminal in the neon alley"
)

# Run the agentic mission
status = agent.run()
print(f"Mission Status: {status.success}")
```

### Manual Latent Action Control
```python
import genie_sdk

env = genie_sdk.make("platformer_forest")
obs = env.reset()

# Action is a 'latent action' vector inferred from the world model
# 0.05 determines the granularity of the movement
obs, reward, done, info = env.step(action=[0.1, -0.5], latent_step_size=0.05)
```

## Related tools / concepts
- [Sora](sora.md) — Passive high-fidelity video generation.
- [Luma Dream Machine](luma-dream-machine.md) — High-quality generative video.
- [Runway Gen-3](runway.md) — Professional video generation suite.
- [Google Lyria](google-lyria.md) — Generative music and audio for worlds.
- [Nano Banana](nano-banana.md) — Multimodal image-to-video capabilities.
- [Anti-Gravity](../agents/agno.md) — The agentic framework using Genie as a simulator.
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for agent interaction.
- [Simulation-Aware Agents](../../knowledge_base/learning-map.md) — Research on agents that understand generative physics.

## Sources / references
- [Google DeepMind: Genie: Generative Interactive Environments](https://deepmind.google/discover/blog/genie-generative-interactive-environments/)
- [Genie 3 Prompt Guide (Internal Release 2026.5)](https://deepmind.google/models/genie/prompt-guide/)
- [ALM Corp: Project Genie Technical Analysis](https://almcorp.com/blog/google-deepmind-project-genie-technical-analysis-applications/)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
