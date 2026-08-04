# Gemini Robotics

## What it is
Gemini Robotics (anchored by **Gemini Robotics 2** and its embodied reasoning variant, **Gemini Robotics ER 2**) is Google DeepMind's flagship model family designed for physical hardware orchestration and multi-robot coordination. It operates as a Vision-Language-Action (VLA) model that directly translates multimodal sensory streams (video, audio, text, and spatial coordinate feeds) into physical control commands (such as humanoid motor joints, multi-finger gripping forces, or mobile base routing).

## What problem it solves
Traditional robotics architectures rely on fragmented, hand-engineered pipelines where vision models detect objects, separate symbolic planners devise logical subgoals, and low-level control loops handle motor dynamics. This modular approach is fragile and struggles with novel environments or general natural language instructions. Gemini Robotics replaces these modules with an end-to-end reasoning and action engine, allowing robots to perform complex physical tasks in dynamic settings (e.g., placing watering cans in low-tier bins or unscrewing light bulbs) with broad spatial and logical understanding.

## Where it fits in the stack
**Category**: Agents / Embodied AI. Gemini Robotics bridges high-level cognitive agent planning with real-world physical actuators. It consumes instructions and environmental data, reasons about multi-step orchestration (using `gemini-robotics-er-2` for logical task sequencing), and executes native motor trajectories (using the on-device `gemini-robotics-on-device-2` runtime).

## Typical use cases
- **Multi-Robot Collaboration**: Organizing diverse robots (e.g., humanoid arms paired with mobile carts) to cooperatively complete sorting workflows in a workspace.
- **Physical Task Orchestration**: Understanding task start and end points to pinpoint key events and adapt to unexpected physical blockages.
- **Whole-Body Humanoid Control**: Commanding complex movements (such as walking, crouching, reaching, and multi-finger object manipulation) on hardware platforms like Apptronik Apollo 2.

## Strengths
- **End-to-End Multimodality**: Native understanding of real-time video and ambient audio streams paired with textual instructions.
- **High-Performance Spatial Reasoning**: Exceptional precision in locating coordinate regions and identifying object orientations without separate computer vision pipelines.
- **Flexible Deployments**: Supports hosted cloud environments for deep orchestration reasoning alongside lightweight, local, on-device runtimes for zero-latency execution.
- **Collaborative Protocol**: Native task planning mechanisms for multi-agent negotiation, allowing multiple robots to negotiate workloads dynamically.

## Limitations
- **Actuation Speed**: Complex multi-step reasoning cycles can introduce slight latency, causing humanoid movements to appear deliberate or slower than specialized control loops.
- **Variable Fine-Motor Success**: Success rates vary significantly across tasks (e.g., 92% for unscrewing light bulbs, but lower for precise tying or complex socket insertions).
- **Compute Requirements**: Deep embodied reasoning requires significant local accelerated compute or a reliable, low-latency network connection to Vertex AI.

## When to use it
- When building multi-agent or multi-robot home-office automation pipelines that require coordinated physical manipulation.
- When your robotic automation stack requires advanced spatial awareness, video progress monitoring, and natural language instruction decoding.

## When not to use it
- For ultra-low latency, pure industrial automation tasks where standard deterministic PID loops or traditional motion profiling are safer and more efficient.
- If your target device lacks native accelerator hardware and cannot maintain a persistent high-bandwidth cloud uplink.

## Getting started

### Vertex AI API Configuration
Google provides Gemini Robotics endpoints via Vertex AI and Google AI Studio under the `gemini-robotics-er-2-preview` model tag.

1. Ensure you have a Google Cloud Project with the Vertex AI API enabled.
2. Install the official Google GenAI SDK:

```bash
pip install google-genai
```

## CLI examples

### Querying the Embodied Reasoning Model
Send a multi-step task instruction and a workspace snapshot to plan a robotic coordination sequence:

```bash
gcloud ai custom-jobs create \
  --region=us-central1 \
  --display-name=robotics-er2-job \
  --args="--model=gemini-robotics-er-2-preview,--instruction='Locate the green bin and coordinate with Cart-A to transport the can.'"
```

## API examples

### Programmatic Python Task Validation
The following script sends an environmental video frame and user instruction to `gemini-robotics-er-2` to generate a structured, validated task sequence utilizing **Pydantic v2**.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# Define Pydantic v2 schemas for the robotic action sub-goals
class RoboticSubgoal(BaseModel):
    step_id: int
    action: str = Field(..., description="Action name (e.g., WALK, REACH, GRASP)")
    target_object: str = Field(..., description="The physical object targeted")
    coordinates: Optional[List[float]] = Field(None, description="3D coordinates for spatial target")

class RoboticsPlan(BaseModel):
    task_id: str
    success_criteria: str
    steps: List[RoboticSubgoal]

def generate_validated_robotics_plan(prompt: str, image_path: Optional[str] = None) -> Optional[RoboticsPlan]:
    # Initialize Google GenAI client
    try:
        client = genai.Client()

        # Build contents containing text and optional environmental media
        contents = [prompt]
        if image_path:
            with open(image_path, 'rb') as f:
                contents.append(
                    types.Part.from_bytes(
                        data=f.read(),
                        mime_type="image/jpeg"
                    )
                )

        # Request structured plan matching our Pydantic model
        response = client.models.generate_content(
            model='gemini-robotics-er-2-preview',
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RoboticsPlan,
            ),
        )

        # Load and validate using Pydantic v2
        validated_plan = RoboticsPlan.model_validate_json(response.text)
        return validated_plan

    except Exception as e:
        print(f"Error querying Gemini Robotics ER 2: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initializing Gemini Robotics Embodied Reasoning sequence...")
    # Example task
    task_prompt = "Retrieve the yellow watering can from the floor and place it on the lower shelf."
    plan = generate_validated_robotics_plan(task_prompt)
    if plan:
        print(f"Plan generated successfully with {len(plan.steps)} subgoals!")
        for step in plan.steps:
            print(f" - Step {step.step_id}: {step.action} -> {step.target_object}")
    else:
        print("API offline or environment unconfigured. Skipping integration sequence.")
```

## Related tools / concepts
- [Gemini](../ai_knowledge/gemini.md) — Base multimodal LLM architecture.
- [Google Gemini](../ai_knowledge/google-gemini.md) — Main Google Vertex AI model portfolio.
- [Gemini CLI](../ai_knowledge/gemini-cli.md) — CLI integration for Google LLMs.
- [Gemini for macOS](../ai_knowledge/gemini-macos.md) — Native Apple Silicon agent integration.
- [Gemini API Managed Agents](gemini-managed-agents.md) — Autonomous agent framework.
- [MageVL](../frameworks/magevl.md) — Multimodal spatial framework for localized drone and robot control.
- [Roo Code](roo-code.md) — High-level autonomous agent runner.
- [Cline](cline.md) — Developer agent platform.

## Sources / references
- [Introducing Gemini Robotics ER 2 - Google DeepMind](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- [Gemini Robotics ER 2 Developer Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-robotics-er-2-preview)
- [Google DeepMind says Gemini Robotics 2 enables full body control - The Robot Report](https://www.therobotreport.com/google-deepmind-says-gemini-robotics-2-enables-full-body-control/)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
