# Project Genie

## What it is
Project Genie (specifically the Genie 3 platform as of July 2026) is a generative world model from Google DeepMind that can create interactive, navigable virtual 2D and 3D environments from a single image, text prompt, or rough sketch. Unlike traditional video generation models, Genie produces a fully controllable, interactive "world" that a user or agent can explore in real-time. It acts as an AI-powered game and simulation engine that infers physics, mechanics, and latent actions from unlabeled internet videos. Optimized for TPU v6 clusters, Genie 3 achieves 720p/24fps real-time inference and serves as a foundational simulation and training layer for advanced agentic frameworks like [Anti-Gravity](../agents/agno.md).

## What problem it solves
It bridges the gap between passive video content generation (like Sora or Luma Dream Machine) and interactive experiences. Building navigable 3D or 2D environments traditionally requires thousands of hours of manual asset creation, physics programming, level design, and collision mapping. Genie automates this by "imagining" the world and its underlying rules of movement and interaction from scratch. This allows for the rapid, automated creation of "synthetic training grounds" or sandboxes for autonomous reinforcement learning agents to safely practice complex tool use, navigation, and physical reasoning without real-world risk or hardcoded environments.

## Where it fits in the stack
Project Genie sits at the **Generative World Models** layer of the AI stack. It provides the environmental substrate and physics simulation engine for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) and reinforcement learning, frequently interfaced via Model Context Protocol (MCP 3.0/3.1) to serve as a secure, sandboxed playground for downstream frontier agents.

## Typical use cases
- **Rapid Game Prototyping**: Instantly generating playable levels and game concepts from sketches, doodles, or brief text descriptions.
- **Agent Training and Simulation**: Creating diverse, infinite "gym" environments for robotic or digital agents to practice physical tasks in simulated physics.
- **Interactive Storytelling and Media**: Allowing users to enter, navigate, and dynamically influence scenes described in written narratives or images.
- **Simulated Mission Design**: Creating complex environments and scenarios for [Anti-Gravity](../agents/agno.md) agents running Gemini 3.5 Pro, Llama 4, or Claude 5.1 to solve multi-step objectives.
- **Remixing Concept Art**: Converting static concept art into interactive, fully traversable virtual environments.

## Strengths
- **Interactive Consistency**: Maintains spatial stability; objects and structural components remain persistent as the camera or player moves, preventing visual drift when looking away.
- **Zero-Code Physics & Mechanics**: Automatically infers complex physics (gravity, collision, friction, momentum) without any explicit coding or engine programming.
- **Multi-Modal Native Support**: Accepts diverse input types including text prompts, static photos, high-fidelity renders, or rough drawings.
- **Ultra-Low Latency TPU v6 Tuning**: Highly optimized for TPU v6 hardware, supporting real-time interactive generation at 720p resolution and 24 frames per second.

## Limitations
- **Visual Resolution Limitations**: Although excellent for real-time generative video (720p), it does not match the visual fidelity or deterministic rendering of modern high-end traditional game engines like Unreal Engine 5.
- **Memory Horizon Limits**: Long-term spatial consistency can begin to drift or degrade after several minutes of continuous, far-ranging, non-repetitive exploration.
- **High Computational Overhead**: Real-time world generation requires massive TPU or GPU resources, usually restricting local deployment and forcing reliance on cloud APIs.

## When to use it
- When you need to generate highly customized, dynamic, or non-deterministic environments for an AI agent to explore and interact with.
- For rapid prototyping of video games, interactive fiction, or narrative design where atmosphere and fast iteration are prioritized over pixel-perfect precision.
- To test [Agent Protocols](../../knowledge_base/agent_protocols.md) in rich, generative physics environments that present unpredictable variables.
- For automated generation of multi-modal simulation sandboxes to evaluate agentic reasoning capabilities.

## When not to use it
- In production-grade game environments requiring pixel-perfect collision, complex hardcoded game logic, or exact deterministic physics.
- In low-latency consumer products where any frame generation latency (above sub-16ms) is unacceptable.
- In fully offline, air-gapped, or resource-constrained local environments that lack access to cloud-hosted TPU clusters.

## Getting started

### Prompting Genie 3
Effective world generation in Genie 3 involves specifying three core components: the **Environment**, the **Character/Object**, and the **World Sketch**.

#### Example: Text-to-World Prompt
```text
Environment: A neon-lit cyberpunk cityscape during a rainy night. Surfaces are slick asphalt with neon reflections. Distant skyscrapers with glowing advertisements.
Character: A sleek hover-bike that drifts through corners.
Action: Navigate the bike through tight alleys and over high-rise bridges.
```

### Navigating the World
Once the environment is generated and rendered:
1. **Select the Character**: Designate the controllable entity or object.
2. **Input Actions**: Use standard WASD keys or controllers. Genie translates these actions into latent vectors that steer the character relative to the generated physics.

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
The following example shows how to load a Genie environment for a Gemini 3.5 Pro agent using the Managed Agents API in July 2026.

```python
import google_antigravity as ag
from google_genie import GenieEnvironment

# Load the generative world environment
world = GenieEnvironment.load("cyberpunk_city_v3")

# Initialize the agent with the Genie world as its physical simulation substrate
agent = ag.Agent(
    model="gemini-3.5-pro",
    surface=world,
    mission="Locate the hidden terminal in the neon alley"
)

# Run the agentic mission and evaluate success
status = agent.run()
print(f"Mission Status: {status.success}")
```

### Manual Latent Action Control
```python
import genie_sdk

# Initialize the generative simulation
env = genie_sdk.make("platformer_forest")
obs = env.reset()

# Action is a 'latent action' vector inferred from the world model
# Latent step size determines the granularity and speed of simulation execution
obs, reward, done, info = env.step(action=[0.1, -0.5], latent_step_size=0.05)
```

## Related tools / concepts
- [Sora](sora.md) — Passive high-fidelity video generation.
- [Luma Dream Machine](luma-dream-machine.md) — High-quality generative video.
- [Runway Gen-3](runwayml.md) — Professional video generation suite.
- [Google Lyria](google-lyria.md) — Generative music and audio for worlds.
- [Nano Banana](nano-banana.md) — Multimodal image-to-video capabilities.
- [Wan-Dancer](wan-dancer.md) — Coherent music-to-dance video generation.
- [Anti-Gravity](../agents/agno.md) — The agentic framework using Genie as a simulator.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent interaction.
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Universal protocol for model integration.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) — Guidelines and interfaces for agent-to-agent communication.
- [Simulation-Aware Agents](../../knowledge_base/agent_framework_learning_map.md) — Framework and curriculum for agents navigating physics simulators.

## Sources / references
- [Google DeepMind: Genie: Generative Interactive Environments](https://deepmind.google/discover/blog/genie-generative-interactive-environments/)
- [Genie 3 Prompt Guide (Internal Release 2026.5)](https://deepmind.google/models/genie/prompt-guide/)
- [ALM Corp: Project Genie Technical Analysis](https://almcorp.com/blog/google-deepmind-project-genie-technical-analysis-applications/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
