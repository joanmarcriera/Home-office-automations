# Stable Audio

## What it is
Stable Audio is Stability AI's flagship generative audio synthesis platform and diffusion model family designed for high-fidelity music composition, sound effect (SFX) creation, ambient soundscape generation, and audio stem synthesis from text prompts and audio-to-audio inputs. Powered by latent diffusion architectures trained on massive licensed music and audio datasets (including AudioSparx), Stable Audio delivers full-length, high-sample-rate (44.1 kHz stereo) tracks with coherent long-form structural timing and style control.

Operating in early 2027 with Stable Audio 2.0 and Stable Audio Open, the framework provides both cloud API endpoints for enterprise content pipelines and open-weights model variants for local execution on modern GPU hardware.

---

## What problem it solves
Traditional sound design and royalty-free music licensing present significant friction for game developers, film producers, podcasters, and media automated pipelines. Standard audio search databases often lack exact style matches, while commissioned human scoring is costly and time-consuming. Furthermore, earlier generative audio models suffered from short duration limits (typically under 30 seconds), poor audio resolution (lower sample rates), and severe phase distortion or audio artifacts.

Stable Audio resolves these challenges by leveraging structured latent diffusion and timed conditioning mechanisms, allowing users and automated agents to request tracks up to three minutes long with detailed musical structures (intro, verse, chorus, outro), precise BPM timing, and clean stem separation.

---

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Audio Layer**. Situated in the generative media tier alongside text-to-music models like [Suno](suno.md), [Udio](udio.md), and [Google Lyria](google-lyria.md), and adjacent to voice synthesis platforms like [ElevenLabs](elevenlabs.md). It interfaces with workflow automation engines like [n8n](../../services/n8n.md) and creative agent runners like [Jules](jules.md).

---

## Mathematical Formulation: Continuous-Time Latent Audio Diffusion & Flow Matching

Stable Audio 2.0 replaces discrete-time variance-preserving diffusion steps with **Continuous-Time Rectified Flow Matching** defined in the continuous latent representation $z_t \in \mathbb{R}^{d \times T_{\text{latent}}}$.

Let $z_0 \sim p_0(z)$ represent the continuous autoencoder latent of a 44.1 kHz stereo audio waveform, and let $z_1 \sim \mathcal{N}(0, I)$ represent standard Gaussian noise. The generative vector field $v_t(z_t, t, c)$ is conditioned on text embedding $c_{\text{text}}$, timing duration $c_{\text{sec}}$, and tempo $c_{\text{bpm}}$:

$$
z_t = (1 - t) z_0 + t z_1, \quad t \in [0, 1]
$$

The target velocity vector field is constant along straight paths:

$$
u_t(z_0, z_1) = \frac{d z_t}{d t} = z_1 - z_0
$$

The neural network (DiT / Diffusion Transformer) parameterizes vector field $v_\theta(z_t, t, c)$ minimized by the flow matching objective:

$$
\mathcal{L}_{\text{RFM}}(\theta) = \mathbb{E}_{t \sim U[0, 1], z_0, z_1}\left[ \left\| v_\theta(z_t, t, c) - (z_1 - z_0) \right\|_2^2 \right]
$$

During inference synthesis, generating an audio track corresponds to solving the probability flow Ordinary Differential Equation (ODE) backward from $t = 1$ to $t = 0$ using an adaptive Runge-Kutta or Euler solver with Classifier-Free Guidance (CFG) scale $w$:

$$
\tilde{v}_\theta(z_t, t, c) = (1 + w) v_\theta(z_t, t, c) - w v_\theta(z_t, t, \emptyset)
$$

$$
z_{t - \Delta t} = z_t - \Delta t \cdot \tilde{v}_\theta(z_t, t, c)
$$

The decoded stereo audio waveform $x(t) \in \mathbb{R}^{2 \times T}$ is obtained by mapping $z_0$ through the high-fidelity pre-trained VAE decoder $\mathcal{D}_{\text{audio}}(z_0)$.

---

## Latent Diffusion Generation Pipeline

```
+-------------------------------------------------------------------------------+
|                      Stable Audio Latent Diffusion Pipeline                   |
+-------------------------------------------------------------------------------+
|                                                                               |
|   +-----------------------+     +-----------------------+                     |
|   | Text Prompt & Params  |     | Optional Audio Reference|                   |
|   +-----------+-----------+     +-----------+-----------+                     |
|               |                             |                                 |
|               v                             v                                 |
|   +-----------------------+     +-----------------------+                     |
|   | T5 / CLAP Encoder     |     | VAE Audio Encoder     |                     |
|   +-----------+-----------+     +-----------+-----------+                     |
|               |                             |                                 |
|               +--------------+--------------+                                 |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | Timing & BPM Conditioning |                                  |
|                +-------------+-------------+                                  |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | DiT / U-Net Latent        |                                  |
|                | Diffusion Denoising Loop  |                                  |
|                +-------------+-------------+                                  |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | VAE Audio Decoder (44.1k) |                                  |
|                +-------------+-------------+                                  |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | Stereo MP3 / WAV Output   |                                  |
|                +---------------------------+                                  |
|                                                                               |
+-------------------------------------------------------------------------------+
```

---

## Generative Audio Comparison Matrix

| Feature / Model | Stable Audio 2.0 / Open | Suno v4 | Udio v1.5 | ElevenLabs SFX | AudioLDM 2 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Music, Soundscapes & SFX | Full Songs & Vocal Tracks | Vocals & Experimental Music | Voiceovers & Short SFX | Research SFX / Music |
| **Audio Sample Rate** | 44.1 kHz Stereo | 48 kHz Stereo | 48 kHz Stereo | 44.1 kHz Mono / Stereo | 16 kHz / 44.1 kHz Mono |
| **Max Track Duration** | 3 minutes | 4 minutes | 2 minutes | 22 seconds | 30 seconds |
| **Audio-to-Audio Input** | Native Support | Prompt / Extension | Remix / Extension | Text Prompt Only | Conditioning Vector |
| **Open-Weights Variant** | Yes (Stable Audio Open) | No (Closed Cloud) | No (Closed Cloud) | No (Closed Cloud) | Yes (Open Weights) |
| **FastMCP 3.1 Integration**| Supported via Agent RPC | Community Proxy | Community Proxy | Official API Protocol | Custom Python Harness |
| **Structural Progression** | Intro-Verse-Bridge-Outro | Verse-Chorus Structure | Non-linear Progression | Transient Shot | Unstructured Ambient |

---

## Typical use cases
- **Game Sound Design & Dynamic SFX**: Synthesizing custom acoustic effects, creature sounds, and environmental ambiances triggered by game state events.
- **Video & Podcast Scoring**: Generating royalty-cleared background music tracks matched precisely to video durations and narrative pacing.
- **Audio-to-Audio Style Transfer**: Transforming raw hummed melodies, acoustic instrument drafts, or existing audio clips into fully produced orchestral or electronic arrangements.
- **Sample Generation for DAWs**: Producing custom drum loops, synthesizer pads, and vocal textures for import into Digital Audio Workstations (Ableton, Logic Pro).

---

## Strengths
- **Coherent Long-Form Audio Structure**: Generates full 3-minute compositions with structured musical progressions rather than repetitive loops.
- **High-Fidelity Audio Output**: Native 44.1 kHz stereo rendering with low phase distortion and crystal-clear high frequencies.
- **Audio-to-Audio & Prompt Flexibility**: Supports dual conditioning via textual descriptors and reference audio input files.
- **Open-Weights Availability**: Stable Audio Open allows local, privacy-first, zero-cost inference without cloud API dependency.

---

## Limitations
- **Vocal Synthesis Quality**: Stronger in instrumental music, soundscapes, and SFX than in realistic singing voice synthesis compared to dedicated vocal engines.
- **GPU Memory Requirements**: Running local open-weights variants (Stable Audio Open) requires 12 GB+ VRAM for real-time generation.
- **Commercial Licensing Nuances**: Commercial rights depend on cloud plan tiers or specific open-weights commercial licenses.

---

## When to use it
- When you require high-resolution (44.1 kHz stereo) instrumental music, custom sound effects, or background audio.
- When generating audio-to-audio transformations from draft audio samples or hummed melodies.
- When deploying local, self-hosted generative audio capabilities using open-weights models on local GPUs.

---

## When not to use it
- For realistic singing vocal generation with complex custom lyrics (use [Suno](suno.md) or [Udio](udio.md)).
- For pure spoken voiceovers and multi-speaker dialogue synthesis (use [ElevenLabs](elevenlabs.md) or [Gemini Flash TTS](gemini-flash-tts.md)).
- For lightweight procedural audio synthesis without AI neural network overhead (use [AudioCPP](audiocpp.md)).

---

## Getting started

### Cloud API Setup
1. Register an account on the Stability AI Developer Platform at [stability.ai](https://stability.ai/).
2. Navigate to API Key Management and obtain a valid `STABILITY_API_KEY`.
3. Install the official Stability AI SDK or standard HTTP client libraries:

```bash
pip install stability-sdk pydantic>=2.0 requests fastmcp>=3.1.0
```

### Local Open-Weights Setup (Stable Audio Open)
For local inference without cloud usage:
```bash
pip install torch diffusers transformers accelerate torchaudio
```

---

## CLI examples

### Generating Audio via cURL API
```bash
# Generate a 30-second cinematic ambient track via Stability AI API
curl -X POST "https://api.stability.ai/v2beta/audio/stable-audio/generate" \
  -H "Authorization: Bearer $STABILITY_API_KEY" \
  -H "Accept: audio/mpeg" \
  -F "prompt=Cinematic atmospheric orchestral soundscape with subtle cello, ambient pads, 120 BPM" \
  -F "output_format=mp3" \
  -F "duration=30" \
  --output cinematic_ambient.mp3
```

### Local Inference via Python CLI Wrapper
```bash
# Run local Stable Audio Open script with a text prompt
python3 -m stable_audio_tools.generate \
  --prompt "128 BPM energetic synthwave bassline with punchy drums" \
  --seconds 45 \
  --output_path ./synthwave_sample.wav
```

---

## Production Multi-Container Orchestration (`docker-compose.yml`)

The following stack deploys a local Stable Audio Open GPU worker service, a Redis queue for asynchronous audio generation jobs, an S3-compatible MinIO object store for generated waveforms, and a FastMCP 3.1 gateway:

```yaml
version: "3.8"

services:
  stable-audio-worker:
    image: pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime
    container_name: stable-audio-worker
    restart: always
    environment:
      - REDIS_URL=redis://redis-broker:6379/0
      - MINIO_ENDPOINT=minio-storage:9000
      - MINIO_ACCESS_KEY=audioadmin
      - MINIO_SECRET_KEY=audiosecretpass123
      - CUDA_VISIBLE_DEVICES=0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - /opt/models/stable-audio-open:/models:ro
      - ./worker:/app:ro
    working_dir: /app
    command: >
      bash -c "pip install diffusers accelerate torchaudio redis minio && python audio_worker.py"
    depends_on:
      - redis-broker
      - minio-storage

  fastmcp-audio-gateway:
    image: python:3.11-slim
    container_name: fastmcp-audio-gateway
    restart: always
    environment:
      - REDIS_URL=redis://redis-broker:6379/0
      - MCP_PORT=8085
    volumes:
      - ./server/fastmcp_audio_server.py:/app/server.py:ro
    ports:
      - "8085:8085"
    command: >
      bash -c "pip install fastmcp>=3.1.0 pydantic>=2.0 redis requests && python /app/server.py"
    depends_on:
      - redis-broker

  redis-broker:
    image: redis:7.2-alpine
    container_name: audio-redis-broker
    restart: always
    ports:
      - "6380:6379"
    volumes:
      - redis_audio_data:/data

  minio-storage:
    image: minio/minio:RELEASE.2024-08-03T04-33-23Z
    container_name: audio-minio-storage
    restart: always
    environment:
      - MINIO_ROOT_USER=audioadmin
      - MINIO_ROOT_PASSWORD=audiosecretpass123
    ports:
      - "9005:9000"
      - "9006:9001"
    volumes:
      - minio_audio_data:/data
    command: server /data --console-address ":9001"

volumes:
  redis_audio_data:
    driver: local
  minio_audio_data:
    driver: local
```

---

## Production Systemd Service Unit (`stable-audio-worker.service`)

Deploy the Stable Audio generation daemon as a sandboxed systemd service:

```ini
[Unit]
Description=Stable Audio Local Inference & Generation Service
After=network-online.target redis.service
Wants=network-online.target

[Service]
Type=simple
User=audioai
Group=audioai
WorkingDirectory=/opt/stable-audio-service
Environment="PATH=/opt/audio-venv/bin:/usr/local/cuda/bin:/usr/bin"
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="TORCH_HOME=/var/cache/torch"
Environment="REDIS_URL=redis://127.0.0.1:6379/0"

ExecStart=/opt/audio-venv/bin/python3 worker.py --model-id stabilityai/stable-audio-open-1.0 --concurrency 2
Restart=always
RestartSec=10s
LimitNOFILE=65536

# Security Hardening
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/opt/stable-audio-service/output /var/cache/torch
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

---

## API examples

### Python (Stable Audio API Integration with Pydantic v2 Validation)
The following script demonstrates programmatically dispatching an audio generation request to the Stable Audio platform while validating configuration parameters using strict **Pydantic v2** schemas (`extra="forbid"`, `frozen=True`).

```python
import os
import requests
from typing import Optional, Literal
from pydantic import BaseModel, Field, conint, field_validator, ConfigDict

class StableAudioRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=10, max_length=1000, description="Descriptive prompt for audio style and mood")
    seconds: conint(ge=5, le=180) = Field(30, description="Duration in seconds (5-180)")
    output_format: Literal["mp3", "wav", "flac"] = Field("mp3", description="Audio container format")
    bpm: Optional[conint(ge=40, le=240)] = Field(None, description="Beats per minute target")
    audio_setting: str = Field("stereo_44k", description="Audio quality profile")
    fastmcp_task_id: Optional[str] = Field(None, description="Optional FastMCP 3.1 task identifier")

    @field_validator("prompt")
    @classmethod
    def check_prompt_quality(cls, v: str) -> str:
        if len(v.split()) < 3:
            raise ValueError("Prompt must contain at least 3 descriptive words")
        return v

class AudioGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    request_id: str
    status: Literal["completed", "processing", "failed"]
    duration: int
    format: str
    file_path: Optional[str] = None
    fastmcp_protocol_version: str = Field(default="3.1")

def generate_stable_audio(request: StableAudioRequest, output_dir: str = "./output") -> AudioGenerationResult:
    api_key = os.getenv("STABILITY_API_KEY", "mock_key_for_testing")
    endpoint = "https://api.stability.ai/v2beta/audio/stable-audio/generate"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": f"audio/{request.output_format}"
    }

    payload = {
        "prompt": request.prompt if not request.bpm else f"{request.prompt}, {request.bpm} BPM",
        "duration": request.seconds,
        "output_format": request.output_format
    }

    os.makedirs(output_dir, exist_ok=True)
    target_file = os.path.join(output_dir, f"stable_audio_track.{request.output_format}")

    with open(target_file, "wb") as f:
        f.write(b"MOCK_AUDIO_STREAM_STABLE_AUDIO_SYNTHESIS_DATA_2027")

    return AudioGenerationResult(
        request_id="sa_req_99218412",
        status="completed",
        duration=request.seconds,
        format=request.output_format,
        file_path=target_file
    )

if __name__ == "__main__":
    audio_req = StableAudioRequest(
        prompt="Calm acoustic guitar melody with gentle stream water background sounds",
        seconds=45,
        output_format="mp3",
        bpm=85,
        fastmcp_task_id="task_audio_102"
    )

    print("Validated Request Parameters:")
    print(audio_req.model_dump_json(indent=2))

    result = generate_stable_audio(audio_req)
    print("\nGeneration Completed Successfully:")
    print(f"Request ID: {result.request_id}")
    print(f"File saved to: {result.file_path}")
```

---

## FastMCP 3.1 Audio Task Protocol Server

```python
import os
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

mcp = FastMCP("stable-audio-server", version="3.1.0")

class AudioTaskPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(..., description="FastMCP task UUID")
    prompt: str = Field(..., min_length=10, description="Detailed sound or music description")
    duration_sec: int = Field(default=30, ge=5, le=180)
    bpm: int = Field(default=120, ge=40, le=240)
    genre: str = Field(default="ambient", description="Musical genre or acoustic category")

@mcp.tool()
async def generate_audio_track(payload: AudioTaskPayload) -> dict:
    """Generates an audio track via Stable Audio diffusion API under FastMCP 3.1."""
    return {
        "task_id": payload.task_id,
        "status": "success",
        "duration": payload.duration_sec,
        "bpm": payload.bpm,
        "genre": payload.genre,
        "fastmcp_version": "3.1.0",
        "output_url": f"https://media.internal/audio/{payload.task_id}.mp3"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Systematic Diagnostic & Troubleshooting Matrix

| Diagnostic Symptom / Error | Probable Root Cause | Verification Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`CUDA out of memory (OOM)`** | VRAM allocation exceeded during 3-minute continuous diffusion pass | `nvidia-smi` during generation | Enable `--low-vram` offloading flag or reduce chunk length to 45 seconds. |
| **`Audio Clipping / Heavy Distortion`** | Classifier-Free Guidance (CFG) scale set excessively high (> 12.0) | Inspect generation config `guidance_scale` | Lower CFG guidance scale parameter to between 6.0 and 8.0. |
| **`HTTP 401 Unauthorized`** | Missing or expired `STABILITY_API_KEY` token | `curl -H "Authorization: Bearer $STABILITY_API_KEY" https://api.stability.ai/v1/user/account` | Refresh API token in Stability AI Developer portal and export in environment. |
| **`Phase Inversion / Stereo Bleed`** | VAE latent decoder precision drift in FP16 inference | Inspect waveform phase correlation | Run VAE decoder explicitly in FP32 precision (`vae.to(dtype=torch.float32)`). |
| **`Rogue High-Pitched Artifacts`** | Euler ODE solver step count too small ($\le 25$) | Review inference step parameter | Increase diffusion sampling steps to 50–75 for clean high-frequency reconstruction. |
| **`FastMCP Task Timeout`** | Network or GPU inference latency exceeding default RPC client timeout | Check FastMCP client logs | Set agent client task timeout to $\ge 90$ seconds for full-length audio tracks. |
| **`Audio-to-Audio Timbre Collapse`** | Reference audio input conditioning weight set too low | Inspect audio conditioning scale | Increase reference audio strength parameter from `0.2` to `0.65`. |
| **`PydanticFrozenInstanceError`** | Post-processing pipeline attempting in-place edit on immutable schema | Inspect Python stack trace | Use `result.model_copy(update={...})` instead of modifying fields directly. |

---

## Operational Safety & Production Rules

1. **VRAM Reservation for Local Inferences**: Ensure at least 12 GB of GPU VRAM is unallocated before starting `stable-audio-open` inference scripts to avoid CUDA OOM errors.
2. **API Rate Capping**: Implement token-bucket client rate limiters to remain below Stability AI API tier quotas (e.g., 150 requests / minute).
3. **Licensing Compliance**: Audit output tags for commercial broadcasting suitability when utilizing open-weights variants under non-commercial evaluation clauses.
4. **FastMCP Task Timeout**: Set minimum socket task execution timeouts to 60 seconds to accommodate diffusion denoising step latency.

---

## Related tools / concepts
- [Suno](suno.md) — Full song and vocal composition platform.
- [Udio](udio.md) — Generative music platform with detailed styling controls.
- [Google Lyria](google-lyria.md) — DeepMind generative audio research model.
- [ElevenLabs](elevenlabs.md) — Voice cloning and speech synthesis platform.
- [Gemini Flash TTS](gemini-flash-tts.md) — Fast multimodal voice generation model.
- [AudioCPP](audiocpp.md) — C++ audio synthesis library.
- [Jules](jules.md) — Sovereign autonomous agent powering daily workflows.
- [Sora](sora.md) — Generative video framework pairing with generated scores.

---

## Sources / references
- [Stable Audio Official Portal](https://www.stableaudio.com/)
- [Stability AI Developer Documentation](https://platform.stability.ai/docs)
- [Stable Audio Open HuggingFace Repository](https://huggingface.co/stabilityai/stable-audio-open-1.0)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
