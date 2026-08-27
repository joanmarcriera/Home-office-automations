# Wan-Dancer

## What it is
Wan-Dancer is a state-of-the-art hierarchical framework for minute-scale coherent music-to-dance video generation. Developed by the Wan-AI team, it utilizes a 14B parameter model to generate high-definition (720p/30fps), rhythmically synchronized dance videos from audio and textual prompts, overcoming the temporal limitations of traditional video diffusion models. By early January 2027, it is widely integrated with frontier orchestration frameworks via the **Model Context Protocol (MCP) 3.1 / FastMCP 3.1 specifications**, allowing autonomous workflows to trigger generative multi-modal choreography in real time.

## What problem it solves
Most video diffusion models struggle to maintain coherence beyond 15-20 seconds, often suffering from temporal drift, identity inconsistency, and repetitive motion patterns. Wan-Dancer solves this by using a hierarchical approach that decouples global keyframe planning from local temporal refinement, allowing for stable, high-quality video generation exceeding one minute in duration.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Creative AI. It functions as a specialized generative media tool that can be integrated into creative workflows, automated social media content pipelines, or as a component of a larger multi-modal agentic system.

## Typical use cases
- **Long-form Video Production**: Generating music videos or dance performances that exceed the typical 10-second "GIF" limit of standard models.
- **Rhythmic Synchronization**: Creating visual content that is precisely aligned with the beats and mood of a provided audio track.
- **Genre-Specific Generation**: Producing motion across various distinct dance genres (e.g., hip-hop, ballet, contemporary) based on textual descriptions.

## Strengths
- **Superior Duration**: One of the first open-weight frameworks capable of minute-scale coherent video synthesis.
- **High Fidelity**: Supports 720p resolution at 30fps with significant detail preservation.
- **Rhythmic Accuracy**: Employs time-mapped RoPE embeddings to ensure motion is perfectly synced with musical context.
- **Temporal Stability**: Optical-flow-based loss functions minimize flickering and motion artifacts.
- **Frontier Compatibility**: Fully integrated with systems using **Claude 5.6**, **GPT-5.6**, **Gemini 4.0**, and **Qwen 3.6** to generate highly descriptive orchestration prompts.

## Limitations
- **Computational Requirements**: The 14B model requires significant VRAM for inference (typically 24GB+ for fp16, though 4-bit/8-bit quantization is supported).
- **Inference Time**: Generating minute-scale video is computationally intensive and takes substantial time even on high-end hardware.
- **Pose Complexity**: While excellent for dance, extremely complex or non-humanoid motion may still exhibit occasional artifacts.

## When to use it
- When you need rhythmic video generation longer than 20 seconds.
- When brand or character identity must remain consistent throughout a long performance.
- When you have access to high-end NVIDIA hardware (A100/H100/RTX 4090/5090).

## When not to use it
- For real-time applications; the generation process is currently asynchronous and slow.
- For non-music-driven video generation where rhythmic sync is not a requirement (standard Sora or Kling style models may be better for generic scenes).

## Getting started
To run Wan-Dancer-14B locally:

1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/Wan-Video/Wan-Dancer
   pip install -r requirements.txt
   ```
2. Download the model weights from HuggingFace.
3. Run the inference script:
   ```bash
   python predict.py --audio path/to/music.mp3 --prompt "A professional dancer performing hip-hop" --duration 60
   ```

## CLI examples
Registering a Wan-Dancer generation server via MCP:
```bash
mcp register "wan-dancer-api" --command "python" --args "mcp_server.py --checkpoint ./weights/wan-dancer-14b"
```

Generating a 30-second clip via CLI:
```bash
wan-dancer-cli generate --input "beat.wav" --text "ballet on ice" --output "output.mp4" --fps 30
```

## API examples
Using the Wan-Dancer Python API with strict Pydantic v2 payload validation:

```python
import os
from typing import Tuple, Optional
from pydantic import BaseModel, Field, ValidationError

# Define structured configuration schema with Pydantic v2
class DanceGenerationRequest(BaseModel):
    audio_path: str = Field(..., description="Path to input audio file")
    prompt: str = Field(..., min_length=3, max_length=500, description="Creative style prompt")
    duration: float = Field(..., gt=0.0, le=120.0, description="Duration in seconds (max 120s)")
    resolution: Tuple[int, int] = Field((1280, 720), description="Video resolution tuple (width, height)")
    fps: int = Field(30, ge=24, le=60, description="Target frames per second")

def trigger_wan_dancer_pipeline(request_data: dict):
    # Perform strict Pydantic v2 validation
    try:
        validated_request = DanceGenerationRequest(**request_data)
    except ValidationError as e:
        print(f"Schema validation failed: {e.errors()}")
        raise

    print(f"Validating request for: {validated_request.prompt} ({validated_request.duration}s)")

    # In a real environment, load WanDancerPipeline from wan_dancer
    # and run generation. For validation/mock execution:
    video_path = f"/tmp/generated_{int(validated_request.duration)}s.mp4"
    print(f"Simulating generation saved to {video_path}")
    return video_path

if __name__ == "__main__":
    test_payload = {
        "audio_path": "jazz_track.mp3",
        "prompt": "A person dancing contemporary jazz in a rainy street",
        "duration": 65.0,
        "resolution": (1280, 720),
        "fps": 30
    }

    try:
        path = trigger_wan_dancer_pipeline(test_payload)
        print("Pipeline triggered successfully. Path:", path)
    except Exception as e:
        print("Error triggering pipeline:", e)
```

## Related tools / concepts
- **[Luma Dream Machine](../ai_knowledge/luma-dream-machine.md)**: A competing video generation model, typically focused on shorter durations.
- **[Sora](../ai_knowledge/sora.md)**: The industry benchmark for video generation (not currently open-weights).
- **[ComfyUI](../ai_knowledge/comfyui.md)**: Can be used to build custom Wan-Dancer workflows via community nodes.
- **[RoPE Embeddings](../ai_knowledge/index.md)**: The underlying positional encoding technology used for rhythmic alignment.
- **[Synthesia](synthesia.md)**: Enterprise AI video generation platform for human-like avatars.
- **[ElevenLabs](elevenlabs.md)**: Industry-leading audio generation and voice synthesis API.
- **[Fish Audio](fish-audio.md)**: High-performance open-source voice synthesis and cloning.

## Sources / References
- [Wan-Dancer: A Hierarchical Framework for Minute-scale Coherent Music-to-Dance Generation](https://arxiv.org/abs/2607.09581)
- [Official GitHub Repository](https://github.com/Wan-Video/Wan-Dancer)
- [HuggingFace: Wan-Dancer-14B](https://huggingface.co/Wan-AI/Wan-Dancer-14B)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: High
- Category: AI Assistants & Knowledge
- Tags: Video-Generation, Music-to-Dance, Long-Form-Video, Wan-AI
