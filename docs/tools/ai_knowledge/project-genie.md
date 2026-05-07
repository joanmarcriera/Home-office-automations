# Project Genie

## What it is
Project Genie is an AI research prototype from Google DeepMind that allows users to create, explore, and remix interactive virtual worlds from text prompts and images. It is powered by **Genie 3**, an 11-billion-parameter autoregressive transformer world model trained on large-scale video data.

## What problem it solves
It enables the rapid creation of interactive environments and simulations without traditional game development overhead. It demonstrates the ability of "world models" to learn physics, gameplay mechanics, and character interactions solely from observing video.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Models**. It is a foundational world model for interactive world generation.

## Typical use cases
- **Rapid Prototyping**: Creating interactive scenes for game design, storytelling, or architectural visualization.
- **Agent Training**: Generating diverse, physics-aware environments for AI agents to inhabit and learn from.
- **Interactive Entertainment**: Allowing users to "walk around" and interact with worlds generated from their imagination.

## Usage Requirements
- **Subscription**: Requires a **Google AI Ultra** subscription (approx. $249.99/mo as of early 2026).
- **Region/Age**: Currently available to users in the U.S. over the age of 18.
- **Interface**: Accessible via Google Labs and integrated into the broader Google AI ecosystem.

## Prompting Tips
- **Detailed Environments**: Describe weather, lighting, and specific structures (e.g., "a lush neon forest with constant blue rain and floating crystals").
- **Action-Oriented Characters**: Specify how the character moves—flying, rolling, hopping—and any visual effects of their movement.
- **Image Input**: Upload a centered character with enough background to define the environment for the model to extrude into 3D.
- **Perspective Switching**: Switch between first-person and third-person views in real-time to explore the generated space.

## Strengths
- **Physics-Aware Interactivity**: Generates playable worlds that respect basic physical laws (gravity, collision) learned from video.
- **Remixing**: Users can take existing worlds from a gallery and modify them using natural language.
- **High Resolution**: Genie 3 supports real-time generation at 720p/24fps.

## Limitations
- **Duration**: Current interactive sessions are often limited in duration (e.g., 60-second clips) or spatial complexity.
- **Premium Cost**: High computational requirements result in significant subscription pricing.

## When to use it
- To quickly prototype interactive environments and simulations without traditional game development.
- For research into "world models" and how AI learns physics from video.
- To generate diverse, physics-aware synthetic data for training other AI agents.

## When not to use it
- When you need permanent, highly complex game worlds with complex logic beyond physical interaction.
- If you require a fully open-source or local deployment (Genie is a managed Google research prototype).

## Getting started

### Exploring your first World
1.  Access [Project Genie](https://labs.google/projectgenie) via Google Labs (U.S. Only).
2.  **Upload an image**: Provide a starting frame for your world (e.g., a 2D platformer level design).
3.  **Prompt**: Describe the physics and character movement (e.g., "A low-gravity moon base where the character leaps between craters").
4.  **Interact**: Use the keyboard or controller icons to move your character through the generated sequence.
5.  **Refine**: Edit your prompt to change the "vibe" or physics of the world in real-time.

## Related tools / concepts
- [Google Gemini](google-gemini.md)
- [Runway ML](runwayml.md)
- [Sora](sora.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [AG2](../frameworks/ag2.md)
- [NotebookLM](notebooklm.md)
- [ElevenLabs](elevenlabs.md)

## Sources / References
- [Genie 3 — Google DeepMind](https://deepmind.google/models/genie/)
- [How to write prompts for Project Genie (The Keyword)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/tips-prompt-writing-project-genie/)
- [Project Genie - Google Labs](https://labs.google/projectgenie)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
