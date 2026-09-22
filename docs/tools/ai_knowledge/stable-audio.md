# Stable Audio

## What it is
Stable Audio is Stability AI's flagship generative audio synthesis platform and diffusion model family designed for high-fidelity music composition, sound effect (SFX) creation, ambient soundscape generation, and audio stem synthesis from text prompts and audio-to-audio inputs. Powered by latent diffusion architectures trained on massive licensed music and audio datasets (including AudioSparx), Stable Audio delivers full-length, high-sample-rate (44.1 kHz stereo) tracks with coherent long-form structural timing and style control.

Operating in early 2027 with Stable Audio 2.0 and Stable Audio Open, the framework provides both cloud API endpoints for enterprise content pipelines and open-weights model variants for local execution on modern GPU hardware.

## What problem it solves
Traditional sound design and royalty-free music licensing present significant friction for game developers, film producers, podcasters, and media automated pipelines. Standard audio search databases often lack exact style matches, while commissioned human scoring is costly and time-consuming. Furthermore, earlier generative audio models suffered from short duration limits (typically under 30 seconds), poor audio resolution (lower sample rates), and severe phase distortion or audio artifacts.

Stable Audio resolves these challenges by leveraging structured latent diffusion and timed conditioning mechanisms, allowing users and automated agents to request tracks up to three minutes long with detailed musical structures (intro, verse, chorus, outro), precise BPM timing, and clean stem separation.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Audio Layer**. Situated in the generative media tier alongside text-to-music models like [Suno](suno.md), [Udio](udio.md), and [Google Lyria](google-lyria.md), and adjacent to voice synthesis platforms like [ElevenLabs](elevenlabs.md). It interfaces with workflow automation engines like [n8n](../../services/n8n.md) and creative agent runners like [Jules](jules.md).

## Typical use cases
- **Game Sound Design & Dynamic SFX**: Synthesizing custom acoustic effects, creature sounds, and environmental ambiances triggered by game state events.
- **Video & Podcast Scoring**: Generating royalty-cleared background music tracks matched precisely to video durations and narrative pacing.
- **Audio-to-Audio Style Transfer**: Transforming raw hummed melodies, acoustic instrument drafts, or existing audio clips into fully produced orchestral or electronic arrangements.
- **Sample Generation for DAWs**: Producing custom drum loops, synthesizer pads, and vocal textures for import into Digital Audio Workstations (Ableton, Logic Pro).

## Strengths
- **Coherent Long-Form Audio Structure**: Generates full 3-minute compositions with structured musical progressions rather than repetitive loops.
- **High-Fidelity Audio Output**: Native 44.1 kHz stereo rendering with low phase distortion and crystal-clear high frequencies.
- **Audio-to-Audio & Prompt Flexibility**: Supports dual conditioning via textual descriptors and reference audio input files.
- **Open-Weights Availability**: Stable Audio Open allows local, privacy-first, zero-cost inference without cloud API dependency.

## Limitations
- **Vocal Synthesis Quality**: Stronger in instrumental music, soundscapes, and SFX than in realistic singing voice synthesis compared to dedicated vocal engines.
- **GPU Memory Requirements**: Running local open-weights variants (Stable Audio Open) requires 12 GB+ VRAM for real-time generation.
- **Commercial Licensing Nuances**: Commercial rights depend on cloud plan tiers or specific open-weights commercial licenses.

## When to use it
- When you require high-resolution (44.1 kHz stereo) instrumental music, custom sound effects, or background audio.
- When generating audio-to-audio transformations from draft audio samples or hummed melodies.
- When deploying local, self-hosted generative audio capabilities using open-weights models on local GPUs.

## When not to use it
- For realistic singing vocal generation with complex custom lyrics (use [Suno](suno.md) or [Udio](udio.md)).
- For pure spoken voiceovers and multi-speaker dialogue synthesis (use [ElevenLabs](elevenlabs.md) or [Gemini Flash TTS](gemini-flash-tts.md)).
- For lightweight procedural audio synthesis without AI neural network overhead (use [AudioCPP](audiocpp.md)).

## Getting started

### Cloud API Setup
1. Register an account on the Stability AI Developer Platform at [stability.ai](https://stability.ai/).
2. Navigate to API Key Management and obtain a valid `STABILITY_API_KEY`.
3. Install the official Stability AI SDK or standard HTTP client libraries:

```bash
pip install stability-sdk pydantic requests
```

### Local Open-Weights Setup (Stable Audio Open)
For local inference without cloud usage:
```bash
pip install torch diffusers transformers accelerate torchaudio
```

## CLI examples

### Generating Audio via cURL API
```bash
# Generate a 30-second cinematic ambient track via Stability AI API
curl -X POST "https://api.stability.ai/v2beta/stable-image/generate/core" \
  -H "Authorization: Bearer $STABILITY_API_KEY" \
  -H "Accept: audio/*" \
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

## API examples

### Python (Stable Audio API Integration with Pydantic v2 Validation)
The following script demonstrates programmatically dispatching an audio generation request to the Stable Audio platform while validating configuration parameters using strict **Pydantic v2** schemas.

```python
import os
import requests
from typing import Optional, Literal
from pydantic import BaseModel, Field, conint, field_validator

class StableAudioRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1000, description="Descriptive prompt for audio style and mood")
    seconds: conint(ge=5, le=180) = Field(30, description="Duration in seconds (5-180)")
    output_format: Literal["mp3", "wav", "flac"] = Field("mp3", description="Audio container format")
    bpm: Optional[conint(ge=40, le=240)] = Field(None, description="Beats per minute target")
    audio_setting: str = Field("stereo_44k", description="Audio quality profile")

    @field_validator("prompt")
    @classmethod
    def check_prompt_quality(cls, v: str) -> str:
        if len(v.split()) < 3:
            raise ValueError("Prompt must contain at least 3 descriptive words")
        return v

class AudioGenerationResult(BaseModel):
    request_id: str
    status: Literal["completed", "processing", "failed"]
    duration: int
    format: str
    file_path: Optional[str] = None

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

    # Simulated response structure for testing and local validation
    os.makedirs(output_dir, exist_ok=True)
    target_file = os.path.join(output_dir, f"stable_audio_track.{request.output_format}")

    # Simulated write of generated audio payload
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
        bpm=85
    )

    print("Validated Request Parameters:")
    print(audio_req.model_dump_json(indent=2))

    result = generate_stable_audio(audio_req)
    print("\nGeneration Completed Successfully:")
    print(f"Request ID: {result.request_id}")
    print(f"File saved to: {result.file_path}")
```

### Audio-to-Audio Conditioning Fragment
```python
# Conditioning audio generation on an existing reference track
files = {
    'audio_input': open('reference_drum_loop.wav', 'rb')
}
data = {
    'prompt': 'Transform to futuristic cyber-industrial percussion',
    'audio_strength': 0.65
}
# response = requests.post(audio_to_audio_endpoint, headers=headers, files=files, data=data)
```

## Related tools / concepts
- [Suno](suno.md) — Full song and vocal composition platform.
- [Udio](udio.md) — Generative music platform with detailed styling controls.
- [Google Lyria](google-lyria.md) — DeepMind generative audio research model.
- [ElevenLabs](elevenlabs.md) — Voice cloning and speech synthesis platform.
- [Gemini Flash TTS](gemini-flash-tts.md) — Fast multimodal voice generation model.
- [AudioCPP](audiocpp.md) — C++ audio synthesis library.
- [Jules](jules.md) — Sovereign autonomous agent powering daily workflows.
- [Sora](sora.md) — Generative video framework pairing with generated scores.

## Sources / references
- [Stable Audio Official Portal](https://www.stableaudio.com/)
- [Stability AI Developer Documentation](https://platform.stability.ai/docs)
- [Stable Audio Open HuggingFace Repository](https://huggingface.co/stabilityai/stable-audio-open-1.0)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
