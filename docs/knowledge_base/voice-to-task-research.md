# Voice-to-Task Research

Research into local speech-to-text (STT) and its integration with Home Assistant for hands-free task creation.

## What it is
A system that captures voice commands, transcribes them using local models, and routes the resulting text to a task management system (e.g., Vikunja). It utilizes the Wyoming protocol for efficient, low-latency communication between the voice assistant and the transcription engine. In June 2026, this utilizes Whisper v1.2.x (Faster-Whisper) and Claude 4.8 for intent synthesis.

## What problem it solves
Enables "heads-up, hands-free" task capture, reducing friction for recording chores, reminders, and shopping list items without needing to open an app. This is particularly useful in "dirty hands" environments like kitchens or workshops. It bridges the gap between raw audio and structured data while maintaining 100% data sovereignty.

## Where it fits in the stack
**Knowledge Base / Pattern**. It connects [Home Assistant](../services/home-assistant.md) voice pipelines with [n8n](../services/n8n.md) for task processing. It sits in the **Interaction Layer** of the [Home-Office Architecture](../architecture/README.md).

## Typical use cases
- **Household Management**: "Hey Assist, remind me to take out the trash tonight."
- **Inventory/Shopping**: "Add milk to the grocery list."
- **Maintenance Logging**: Hands-free logging of maintenance activities during homelab repairs.
- **Deep Thought Capture**: Dictating complex notes that require LLM-based summarization before storage in [Obsidian](../tools/ai_knowledge/obsidian.md).
- **Agentic Task Decomposition**: "I need to plan a party for Saturday," which the agent decomposes into sub-tasks in [Vikunja](../services/vikunja.md).

## Strengths
- **Privacy**: No audio data is sent to the cloud when using local Whisper.
- **Low Latency**: Local processing on powerful hardware (Intel NUC/Apple Silicon) can provide sub-second responses.
- **Reliability**: Works without an internet connection, provided the local network is up.
- **Agentic Integration**: Deep integration with [Ollama](../services/ollama.md) and [Claude 4.8](../tools/ai_knowledge/claude.md) allows for sophisticated reasoning over voice inputs.

## Limitations
- **Hardware Requirements**: Running Whisper v1.2.x locally requires significant CPU/GPU resources (NVIDIA GPU recommended for `large-v3` models).
- **Accuracy**: Noise and accents can affect transcription quality, especially with smaller models (e.g., `tiny` or `base`).
- **Complexity**: Setting up the Wyoming protocol and Assist pipelines requires technical overhead compared to cloud solutions.

## When to use it
- When privacy is a top priority for household conversations.
- When you have the local compute capacity (e.g., NVIDIA GPU or Apple M-series) to run STT models efficiently.
- For users who want a "sovereign" voice assistant that doesn't depend on external APIs.
- When pairing voice with local RAG workflows for information retrieval.

## When not to use it
- On extremely low-power hardware like a Raspberry Pi 4 (latency will be high, often 5-10s per command).
- If cloud-based STT reliability and accuracy (e.g., Google Assistant or Alexa) are preferred over privacy.
- For safety-critical systems where voice command misinterpretation could lead to physical harm.

## Getting started

### Docker Compose for Wyoming-Whisper (Faster-Whisper)
Deploying the STT engine as a container is the recommended path for homelabs.

```yaml
services:
  whisper:
    image: rhasspy/wyoming-whisper:latest
    container_name: wyoming-whisper
    # Use 'base' for speed or 'large-v3' for accuracy
    command: --model base --language en --device cuda
    volumes:
      - ./whisper-data:/data
    ports:
      - "10300:10300"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  piper:
    image: rhasspy/wyoming-piper
    container_name: wyoming-piper
    command: --voice en_US-lessac-medium
    volumes:
      - ./piper-data:/data
    ports:
      - "10200:10200"
    restart: unless-stopped
```

## CLI examples

### Testing the Wyoming Endpoint
```bash
# Verify the Wyoming service is listening
nc -zv 192.168.1.50 10300

# Check logs of the Whisper container during a voice command
docker logs -f wyoming-whisper
```

### Manual Transcription via Faster-Whisper CLI
```bash
# Transcribe a local audio file using the faster-whisper model
faster-whisper-cli --model base --language en audio_sample.wav
```

## API examples

### Home Assistant Assist API
You can interact with the Assist API to send text for intent processing:

```bash
# Send a transcribed text to Home Assistant for intent processing
curl -X POST \
  -H "Authorization: Bearer YOUR_LONG_LIVED_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Add milk to the grocery list"}' \
  "http://homeassistant.local:8123/api/conversation/process"
```

### Agentic Synthesis Pattern (Python)
Using [Ollama](../services/ollama.md) to parse raw transcription into structured tasks.

```python
import ollama

def parse_voice_command(transcript):
    prompt = f"Extract tasks from this transcript: '{transcript}'. Return JSON list."
    response = ollama.chat(model='llama4', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

print(parse_voice_command("I need to fix the sink and then buy some milk"))
```

## Related tools / concepts
- [OpenAI Whisper](../services/whisper.md) - The core STT engine.
- [Home Assistant](../services/home-assistant.md) - The orchestration hub for voice.
- [n8n](../services/n8n.md) - For complex task routing logic.
- [Vikunja](../services/vikunja.md) - Self-hosted task management.
- [Ollama](../services/ollama.md) - For local LLM-based intent parsing.
- [Obsidian](../tools/ai_knowledge/obsidian.md) - For long-form dictation storage.
- [Architecture](../architecture/README.md) - For the high-level placement of voice services.
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md) - The reasoning layer.
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md) - For agentic tool execution.

## Sources / references
- [Home Assistant Whisper Integration](https://www.home-assistant.io/integrations/whisper/)
- [Wyoming Protocol Specification](https://github.com/rhasspy/wyoming)
- [Faster-Whisper Project](https://github.com/SYSTRAN/faster-whisper)
- [Home Assistant Assist: Local Voice Control](https://www.home-assistant.io/voice_control/voice_remote_local_assistant/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
