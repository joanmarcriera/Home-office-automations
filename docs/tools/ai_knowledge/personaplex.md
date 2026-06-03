# NVIDIA PersonaPlex

## What it is
PersonaPlex is a real-time, full-duplex speech-to-speech conversational model developed by NVIDIA. It enables fine-grained persona control through text-based role prompts and audio-based voice conditioning. Built on the Moshi architecture and the Helium LLM backbone, it is designed for natural, low-latency spoken interactions.

## What problem it solves
It addresses the limitations of standard turn-based (half-duplex) voice AI by allowing for full-duplex communication where both the user and the agent can speak simultaneously, handle interruptions, and maintain a consistent persona without the "robotic" delay of serial TTS/STT pipelines.

## Where it fits in the stack
**Tool / Model / Voice AI**. It serves as a sophisticated voice interface layer for agentic systems.

## Typical use cases
- **Natural AI Assistants**: Creating conversational partners that can handle interruptions and backchanneling.
- **Customer Service Avatars**: Deploying specialized personas (e.g., "Waste Management Clerk", "Drone Rental Expert") with specific knowledge and tone.
- **Casual & Roleplay Agents**: Simulating diverse personalities for social interaction or training.

## Strengths
- **Full-Duplex Architecture**: Supports simultaneous listening and speaking.
- **Fine-grained Persona Control**: Uses text prompts to define name, role, knowledge, and personality.
- **Low Latency**: Optimized for real-time interaction.
- **Voice Conditioning**: Can be conditioned on specific audio embeddings for consistent vocal identity.

## Limitations
- **Hardware Intensive**: Requires significant GPU resources (Blackwell/Hopper preferred); CPU offloading is possible but impacts latency.
- **License**: Weights are under the NVIDIA Open Model License, which has specific usage restrictions.
- **Complexity**: Integrating full-duplex audio into standard chat applications requires specialized infrastructure (e.g., Opus codec, WebSockets).

## When to use it
- When building voice agents where natural "flow" and interruption handling are critical.
- For high-stakes customer service simulations requiring specific role-playing.

## When not to use it
- For simple text-only applications.
- If running on low-power edge devices without decent GPU acceleration.

## Licensing and cost
- **Open Source**: Code is MIT; Weights are NVIDIA Open Model License.
- **Cost**: Free to use/self-host (requires hardware).
- **Self-hostable**: Yes.

## Getting started

### Installation
PersonaPlex requires the Opus audio codec development library. On Ubuntu/Debian, install it via:

```bash
sudo apt install libopus-dev
```

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/NVIDIA/personaplex
cd personaplex
pip install -r requirements.txt
```

### Running the WebUI
The easiest way to interact with the model is through the provided WebUI, which handles the full-duplex audio stream:

```bash
python -m personaplex.web_ui --model-path nvidia/personaplex-7b-v1
```

## Architecture Details
PersonaPlex is built on a sophisticated multimodal architecture:
- **Backbone**: Helium 7B LLM for semantic understanding.
- **Audio Codec**: **Mimi** (ConvNet + Transformer) operating at 24kHz for low-latency compression/decompression.
- **Transformers**: Dual-stream Temporal and Depth Transformers that process user audio, agent text, and agent audio concurrently.
- **Prompting**: A **Hybrid System Prompt** architecture that temporally concatenates textual role descriptions with audio voice embeddings.

## CLI examples

While the model is primarily interaction-driven, you can use the CLI to test voice conditioning:

```bash
# Generate a voice embedding from a reference audio file
python -m personaplex.tools.encode_voice --input reference.wav --output voice_embedding.pt

# Run a headless interaction with a specific persona and voice
python -m personaplex.cli --text-prompt "You are a helpful astronaut." \
                          --voice-prompt voice_embedding.pt
```

## API examples

PersonaPlex uses WebSockets for its full-duplex communication. Below is a conceptual Python client using `websockets` and `opuslib`:

```python
import websockets
import opuslib

async def communicate():
    uri = "ws://localhost:8000/stream"
    async with websockets.connect(uri) as websocket:
        # Send initial Hybrid System Prompt (JSON)
        await websocket.send('{"text": "You are a ship captain.", "voice": "ref_id_01"}')

        # Continuous loop for full-duplex audio
        while True:
            # Send chunk of user audio
            await websocket.send(user_audio_chunk)

            # Receive agent audio/text
            response = await websocket.recv()
            process_agent_response(response)
```

## Hardware Requirements
To maintain sub-200ms latency for real-time conversation:
- **GPU**: NVIDIA Blackwell (B200) or Hopper (H100) is highly recommended.
- **VRAM**: Minimum 24GB (RTX 3090/4090) for the 7B model.
- **Memory**: 32GB+ system RAM.

## Related tools / concepts
- [Moshi](https://kyutai.org/blog/2024-07-02-moshi) — The base architecture developed by Kyutai.
- [Helium](https://kyutai.org/blog/2025-04-30-helium) — The core LLM backbone for semantic reasoning.
- [Chatterbox TTS](https://github.com/NVIDIA/chatterbox) — Used for generating synthetic training data for PersonaPlex.
- [Ollama](../../services/ollama.md) — For running local text-based LLMs.
- [Whisper](../../services/whisper.md) — For high-accuracy offline transcription.
- [Real-time Sync Engines](../../knowledge_base/real_time_sync_engines.md) — Patterns for low-latency state synchronization.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — For connecting PersonaPlex agents to external tools.
- [Low-Latency Audio Patterns](../../knowledge_base/learning-map.md) — Research on optimizing full-duplex pipelines.

## Sources / References
- [Official GitHub](https://github.com/NVIDIA/personaplex)
- [Research Paper](https://arxiv.org/abs/2602.06053)
- [NVIDIA Technical Demo](https://research.nvidia.com/labs/adlr/personaplex/)
- [Low-Latency Audio Patterns](../../knowledge_base/learning-map.md)

## Contribution Metadata
- Last reviewed: 2026-06-03
- Confidence: high
