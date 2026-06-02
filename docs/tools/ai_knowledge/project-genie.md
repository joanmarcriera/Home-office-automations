# Project Genie

## What it is
Project Genie is a generative world model from Google DeepMind that can create interactive, navigable virtual environments from a single image or text prompt. Unlike traditional video generation, Genie produces a "world" that a user can actually control and explore in real-time, essentially acting as an AI-powered game engine that learns physics and mechanics from unlabeled internet videos.

## What problem it solves
It bridges the gap between passive content generation (like Sora) and interactive experiences. Traditionally, building a navigable 3D or 2D world requires thousands of hours of manual asset creation, physics programming, and level design. Genie automates this by "imagining" the world and its underlying rules of movement and interaction.

## Where it fits in the stack
**AI & Knowledge / Generative World Models**. It sits at the intersection of video generation and game development, providing a foundation for autonomous agent training (simulators) and interactive entertainment.

## Typical use cases
- **Rapid Game Prototyping**: Generating a playable level from a sketch or a few sentences.
- **Agent Training**: Creating diverse "gym" environments for training robotic or digital agents in safe, simulated physics.
- **Interactive Storytelling**: Allowing users to enter and navigate a scene described in a narrative.
- **Remixing Content**: Taking an existing image and transforming it into a navigable "remix."

## Technical Architecture
- **Model**: Genie 3 (11-billion parameter autoregressive transformer).
- **Performance**: 720p resolution at 24 frames per second (real-time).
- **Inference**: Uses a "World Sketch" as a latent bottleneck to maintain consistency across frames.
- **Training**: Trained on over 200,000 hours of unlabeled 2D platformer and 3D navigation video footage.

## Strengths
- **Interactive Consistency**: The world remains stable as you move; objects don't disappear when you look away.
- **Zero-Code Mechanics**: Infers physics (gravity, collision, friction) without explicit programming.
- **Multi-Modal Input**: Can be triggered by text, images, or even rough sketches.

## Limitations
- **Resolution**: While high for real-time generative video (720p), it still lacks the fidelity of modern high-end game engines.
- **Memory Horizon**: The "consistency" of the world may drift after several minutes of continuous, far-ranging navigation.
- **Compute Intensity**: Requires significant TPU/GPU resources for real-time inference.

## When to use it
- When you need a custom, navigable environment for an AI agent to explore.
- For "vibe-based" game development where the atmosphere is more important than specific hardcoded mechanics.
- To create interactive demos for creative concepts or architectural visualizations.

## When not to use it
- For production-grade games that require precise, pixel-perfect collision and deterministic physics.
- In low-latency applications where any frame generation delay is unacceptable.

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
2.  **Input Actions**: Use standard WASD or arrow keys. Genie interprets these "latent actions" based on the character's inferred physics (e.g., "W" might mean "Thrust" for a bike but "Jump" for a platformer character).

## Technical examples

### Advanced World Sketch Modification
Before entering the world, you can modify the **World Sketch** (the latent representation) to add specific constraints:

```text
Add a "High Perspective" constraint to the Environment prompt to ensure a wide-angle view suitable for tactical navigation.
```

### World-Generation Technical Parameters
When generating environments, you can fine-tune the output using technical parameters in the advanced interface:

- **Consistency Horizon**: `1200 frames` (Controls how long the model remembers distant parts of the world).
- **Physics Fidelity**: `high` (Enables more complex interactions like fluid dynamics or multi-body collisions).
- **Latent Step Size**: `0.05` (Determines the granularity of character movement).
- **Seed Persistence**: `Enabled` (Allows for deterministic world regeneration using the same seed).

### Integration Pattern for Agent Training
Genie 3 can be used as a backend for reinforcement learning environments where a traditional simulator (like MuJoCo) is too rigid:

```python
# Conceptual integration with an RL agent
import genie_sdk

env = genie_sdk.make("cyberpunk_city_v1")
obs = env.reset()

while not done:
    # Action here is a 'latent action' mapped from the model's learned space
    action = agent.get_action(obs)
    obs, reward, done, info = env.step(action)
```

## Related tools / concepts
- [Sora](sora.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Runway Gen-3](https://app.runwayml.com/)
- [Runway Gen-3](runway.md)
- [Google Lyria](google-lyria.md)
- [Nano Banana](nano-banana.md)
- [Unity / Unreal Engine](https://unity.com) (Traditional counterparts)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Simulation-Aware Agents](../../knowledge_base/learning-map.md)
- [Hugging Face](../providers/huggingface.md)

## Sources / References
- [Google DeepMind: Genie: Generative Interactive Environments](https://deepmind.google/discover/blog/genie-generative-interactive-environments/)
- [Genie 3 Prompt Guide](https://deepmind.google/models/genie/prompt-guide/)
- [ALM Corp: Project Genie Technical Analysis](https://almcorp.com/blog/google-deepmind-project-genie-technical-analysis-applications/)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
