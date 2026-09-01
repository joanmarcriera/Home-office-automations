# faster-whisper

## What it is
faster-whisper is a high-performance reimplementation of OpenAI's Whisper speech-to-text model using the [CTranslate2](https://github.com/OpenNMT/CTranslate2) inference engine. It produces identical transcripts as Whisper while running roughly **4x to 6x faster** and using significantly less memory. It features support for 8-bit and float16 quantization on both CPU and GPU, running fully offline once the model is cached. As of early January 2027, it natively supports **Whisper v3-turbo**, Silero VAD v5, FastMCP 3.1 Task Protocol ingestion schemas, and advanced CTranslate2 v4.x optimizations, making it a cornerstone for local agentic audio-to-text workflows across Claude 5.6 and GPT-5.6 agent environments.

## What problem it solves
Reference Whisper is accurate but slow and memory-hungry, which makes large transcription backlogs painful on home-lab and consumer hardware. faster-whisper makes local, private transcription highly practical: it transcribes hours of audio quickly on a CPU or a modest GPU, with no cloud speech API dependencies and no audio ever leaving the local perimeter.

## Where it fits in the stack
**Process & Understanding / Speech-to-text.** It is the transcription engine that feeds downstream pipelines — turning voice notes, meeting recordings, or scanned-media audio into text for [Paperless-ngx](../../services/paperless-ngx.md), Obsidian notes, or RAG indexes. It is the engine behind many self-hosted transcription front-ends and agentic ingestion servers.

## Typical use cases
- Batch-transcribing a backlog of recordings offline on a TrueNAS box or Apple Silicon workstation.
- Adding searchable transcripts to archived audio/video before ingestion into [Paperless-ngx](../../services/paperless-ngx.md).
- Powering a local voice-to-text step in an [n8n](../../services/n8n.md) automation or FastMCP 3.1 audio tool pipeline.
- Generating subtitles/captions for a personal media library or video search indexing.

## Strengths
- **Fast and lightweight:** ~4x to 6x faster than reference Whisper with lower memory via CTranslate2 execution.
- **Whisper v3-turbo Support**: Native support for the ultra-fast turbo models with high-fidelity outputs.
- **Offline and private:** no cloud dependency; audio stays local.
- **Quantization options:** int8/float16 let large models run on commodity hardware.
- **Word-level timestamps & VAD:** built-in Silero voice-activity detection (VAD) v5 improves long-audio accuracy.
- **Agent Protocol Compatibility:** Ready for FastMCP 3.1 Task Protocol audio ingestion pipelines.

## Limitations
- **Library, not an app:** it is a Python package — you build or adopt a front-end around it.
- **Model accuracy ceiling:** inherits Whisper's limits on heavy accents, overlapping speech, and rare languages.
- **GPU setup:** GPU acceleration needs a compatible CUDA/cuDNN or Apple-silicon MLX stack.

## When to use it
- When you need **offline**, fast, private transcription at volume on local hardware.
- As the engine inside a self-hosted transcription or note-taking pipeline.
- When reference Whisper is too slow or too memory-heavy for your machine.
- For building FastMCP 3.1 Task Protocol audio processing tools for autonomous agents.

## When not to use it
- When you want a turnkey GUI rather than a library to integrate.
- For real-time, ultra-low-latency streaming at scale (specialized streaming ASR may fit better).
- When the highest possible accuracy on difficult audio outweighs local/offline constraints.

## Getting started

### Installation
```bash
pip install faster-whisper
```

### Basic Usage
```python
from faster_whisper import WhisperModel

# Initialize model (downloads on first run)
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")

# Transcribe audio file
segments, info = model.transcribe("audio.mp3", beam_size=5)

print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## CLI examples

### 1. Simple Transcription via Python one-liner
```bash
python3 -c "from faster_whisper import WhisperModel; m=WhisperModel('large-v3-turbo'); s,_=m.transcribe('audio.mp3'); [print(seg.text) for seg in s]"
```

### 2. Using community CLI (whisper-ctranslate2)
```bash
# Install CLI tool
pip install whisper-ctranslate2

# Transcribe with the CLI using large-v3-turbo and float16 on GPU
whisper-ctranslate2 audio.mp3 --model large-v3-turbo --device cuda --compute_type float16
```

## API examples

### 1. Word-level Timestamps & Custom Dictionary
Injecting initial prompt vocabulary to guide model output on technical jargon.
```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cpu")
segments, _ = model.transcribe(
    "audio.mp3",
    word_timestamps=True,
    initial_prompt="PydanticAI, FastMCP 3.1 Task Protocol, MCP, Claude 5.6"
)

for segment in segments:
    for word in segment.words:
        print(f"[{word.start:.2f}s -> {word.end:.2f}s] {word.word}")
```

### 2. Structured FastMCP 3.1 Task Protocol Output Validation with Pydantic v2
This example parses and validates the unstructured segments produced by `faster-whisper` into a robust, schema-validated JSON structure, ensuring logical timeline consistency, confidence intervals, and agent execution tracking.
```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from faster_whisper import WhisperModel

# Define strict schemas for transcription segments
class ValidatedSegment(BaseModel):
    model_config = ConfigDict(extra="forbid", freeze=True)

    start: float = Field(..., description="Segment start time in seconds", ge=0.0)
    end: float = Field(..., description="Segment end time in seconds", ge=0.0)
    text: str = Field(..., description="Decoded transcription text content")
    avg_logprob: float = Field(..., description="Average log probability of decoded tokens")

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def check_timestamps(self) -> "ValidatedSegment":
        if self.end <= self.start:
            raise ValueError(f"Segment end time ({self.end}s) must be greater than start time ({self.start}s).")
        return self

class FastMCPTranscriptionTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(..., description="FastMCP 3.1 task identifier")
    language: str = Field(..., description="Detected ISO language code")
    language_probability: float = Field(..., description="Probability of language detection", ge=0.0, le=1.0)
    segments: List[ValidatedSegment] = Field(..., description="List of chronologically validated audio segments")

    @model_validator(mode="after")
    def verify_chronological_order(self) -> "FastMCPTranscriptionTask":
        for i in range(1, len(self.segments)):
            prev = self.segments[i - 1]
            curr = self.segments[i]
            if curr.start < prev.end:
                raise ValueError(
                    f"Segment overlap or non-chronological order found between segment {i-1} "
                    f"(ends at {prev.end}s) and segment {i} (starts at {curr.start}s)."
                )
        return self

def run_validated_transcription(audio_path: str, task_id: str = "task_audio_01") -> str:
    # Initialize the model
    model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")

    # Transcribe with custom parameters
    segments, info = model.transcribe(audio_path, beam_size=5, vad_filter=True)

    # Collect raw results
    raw_segments = []
    for s in segments:
        raw_segments.append({
            "start": s.start,
            "end": s.end,
            "text": s.text,
            "avg_logprob": s.avg_logprob
        })

    # Strictly validate structured outputs via Pydantic v2
    transcription = FastMCPTranscriptionTask(
        task_id=task_id,
        language=info.language,
        language_probability=info.language_probability,
        segments=raw_segments
    )

    return transcription.model_dump_json(indent=2)
```

## Related tools / concepts
- [Whisper](../../services/whisper.md) — The reference model faster-whisper reimplements.
- [Paperless-ngx](../../services/paperless-ngx.md) — Common downstream destination for transcripts.
- [Ollama](../../services/ollama.md) — Pair with a local LLM to summarize transcripts offline.
- [n8n](../../services/n8n.md) — Orchestrate transcription as an automation step.
- [MLX](../infrastructure/mlx.md) — Apple-silicon backend for accelerated local inference.
- [Docling](docling.md) — Local document parser for the text side of ingestion.
- [Audiobookshelf](../../services/audiobookshelf.md) — Self-hosted audio library that benefits from transcripts.
- [Apache Tika](../../services/tika.md) — Content/text extraction companion in ingestion pipelines.
- [Ragas](ragas.md) — Evaluating the quality of transcription-fed RAG pipelines.

## Sources / references
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [CTranslate2 GitHub](https://github.com/OpenNMT/CTranslate2)
- [OpenAI Whisper](https://github.com/openai/whisper)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
