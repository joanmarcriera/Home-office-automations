# Project Genie

## What it is
Project Genie is a generative world model from Google DeepMind that can create interactive, navigable virtual environments from a single image or text prompt. Unlike traditional video generation, Genie produces a "world" that a user can actually control and explore in real-time. In June 2026, **Genie 3** (11B parameters) acts as an AI-powered game engine that learns physics and mechanics from unlabeled internet videos, supporting real-time simulation at 24fps.

## What problem it solves
It bridges the gap between passive content generation and interactive experiences. Traditionally, building a navigable 3D or 2D world requires thousands of hours of manual asset creation, physics programming, and level design. Genie automates this by "imagining" the world and its underlying rules of movement and interaction, enabling "zero-code" game mechanics.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative World Models**. It sits at the intersection of video generation and game development, providing a foundation for autonomous agent training (simulators) and interactive entertainment.

## Typical use cases
- **Rapid Game Prototyping**: Generating a playable level from a sketch or a few sentences.
- **Agent Training (Missions)**: Creating diverse "gym" environments for training robotic or digital agents in safe, simulated physics.
- **Interactive Storytelling**: Allowing users to enter and navigate a scene described in a narrative.
- **Remixing Content**: Taking an existing image and transforming it into a navigable "remix."
- **Synthetic Data Generation**: Creating edge-case visual data for autonomous vehicle or drone training.

## Strengths
- **Interactive Consistency**: The world remains stable as you move; objects don't disappear when you look away (Genie 3 improved memory horizon).
- **Zero-Code Mechanics**: Infers physics (gravity, collision, friction) without explicit programming.
- **Multi-Modal Native**: Seamlessly triggered by text, images, or even rough sketches.
- **Real-Time Performance**: Supports interactive exploration at 24fps (720p).

## Limitations
- **Resolution**: While optimized for real-time (720p), it still lacks the fidelity of modern high-end game engines like Unreal Engine 5.
- **Memory Drift**: The "consistency" of the world may drift after several minutes of continuous, far-ranging navigation.
- **Compute Intensity**: Requires significant TPU/GPU resources for real-time inference (typically hosted on Vertex AI).

## When to use it
- When you need a custom, navigable environment for an AI agent to explore.
- For "vibe-based" game development where the atmosphere is more important than specific hardcoded mechanics.
- To create interactive demos for creative concepts or architectural visualizations.
- For reinforcement learning (RL) training where traditional simulators are too rigid.

## When not to use it
- For production-grade games that require precise, pixel-perfect collision and deterministic physics.
- In low-latency applications where any frame generation delay is unacceptable.
- When running on consumer hardware without high-end GPU acceleration (use cloud-based Vertex AI instead).

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

### Generating a World via Vertex AI CLI
```bash
# Generate a world from a local image
gcloud ai worlds create --model=genie-3 --image=concept_art.png --character="red ball"

# Generate from a text prompt
gcloud ai worlds create --model=genie-3 --prompt="A floating castle in the clouds" --fps=24
```

### Inspecting World Latents
```bash
# Export the World Sketch latent bottleneck for modification
gcloud ai worlds export-sketch --world-id=WORLD_ID --output=sketch.latent
```

## API examples

### Python SDK: Agentic Mission Integration
Genie 3 can be used as a backend for reinforcement learning environments:

```python
import google_genie_sdk

# Initialize the environment with a specific concept
env = google_genie_sdk.make(
    model="genie-3",
    prompt="A lush forest with dynamic lighting and interactive stream",
    agent_goal="cross the stream without touching the water"
)

obs = env.reset()
done = False

while not done:
    # Action is a 'latent action' mapped from the model's learned space
    action = agent.compute_action(obs)
    obs, reward, done, info = env.step(action)

    if info.mission_complete:
        print("Agent achieved goal in generative world!")
```

### Advanced World Sketch Modification
Before entering the world, you can modify the latent representation to add specific constraints:

```python
world = client.get_world(world_id)
world.apply_sketch_constraint(
    type="high_perspective",
    strength=0.8,
    description="Ensure wide-angle view for tactical navigation"
)
world.refresh()
```

## Related tools / concepts
- [Sora](sora.md) — Passive video generation.
- [Luma Dream Machine](luma-dream-machine.md) — High-fidelity video.
- [Runway Gen-3](runway.md) — Professional video generation.
- [Google Lyria](google-lyria.md) — Audio generation.
- [Nano Banana](nano-banana.md) — Conversational image editing.
- [Unity / Unreal Engine](https://unity.com) — Traditional deterministic game engines.
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Knowledge-driven agent patterns.
- [Simulation-Aware Agents](../../knowledge_base/learning-map.md) — Agents designed for generative worlds.
- [Hugging Face](../providers/huggingface.md) — Model repository.
- [Anti-Gravity](../development_ops/anti_gravity.md) — Google's agentic framework.

## Sources / References
- [Google DeepMind: Genie: Generative Interactive Environments](https://deepmind.google/discover/blog/genie-generative-interactive-environments/)
- [Genie 3 Technical Report (June 2026)](https://deepmind.google/technologies/genie/report/)
- [Google Cloud: Vertex AI World Models API](https://cloud.google.com/vertex-ai/docs/generative-ai/worlds)
- [ALM Corp: Project Genie Technical Analysis](https://almcorp.com/blog/google-deepmind-project-genie-technical-analysis-applications/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
