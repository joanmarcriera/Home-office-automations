# Voice-to-Task Research

Technical research into local speech-to-text (STT) and agentic synthesis for hands-free task orchestration in the home-office stack.

## What it is
A "voice-to-action" pipeline that captures spoken commands, transcribes them using high-performance local models (Whisper v1.2.x), and utilizes frontier models (Claude 4.8 Opus, GPT-5.5) or high-performance local models like [Gemma 3](../tools/ai_knowledge/local_llms.md) for intent decomposition. It bridges the gap between raw audio and structured task management, enabling autonomous agents to execute complex requests from a single voice prompt using the MCP 3.0 Task Protocol.

## What problem it solves
It eliminates the friction of manual data entry in "dirty-hands" environments (kitchen, workshop, lab) and reduces the cognitive load of capturing fleeting thoughts. By moving from simple command-matching to agentic synthesis, it allows users to express intent naturally without needing to remember specific wake-word syntax or command structures.

## Where it fits in the stack
Voice-to-task is a core component of the **Interaction Layer** within the [Home-Office Architecture](../architecture/README.md). It leverages [Home Assistant](../services/home-assistant.md) for audio capture and the [Model Context Protocol (MCP 3.0)](./patterns/tool-calling-and-mcp.md) for service execution. Tools are often hosted via **FastMCP 3.0** to ensure ultra-low latency execution when triggered by voice, typically routing through [n8n](../services/n8n.md) for complex workflow orchestration.

## Typical use cases
- **Multi-Step Capture**: "Hey Assist, remind me to change the HVAC filters this weekend and also add high-MERV filters to my Amazon cart."
- **Contextual Note-Taking**: "Record a note that the server rack is running 5 degrees hotter than usual after the firmware update."
- **Agentic Scheduling**: "Book a block for deep work tomorrow morning and move any conflicting non-critical meetings."
- **Household Management**: "Add detergent to the shopping list and remind me when we are at the hardware store next."

## Strengths
- **Privacy-First**: Local processing via Faster-Whisper ensuring audio never leaves the personal network.
- **Natural Language Understanding**: [Gemma 3](../tools/ai_knowledge/local_llms.md) and Claude 4.8 Opus excel at extracting latent intent from rambling or non-linear speech.
- **Low Latency**: Optimized Whisper v1.2.x backends and FastMCP 3.0 tool servers provide sub-second end-to-end execution.
- **Tool Integration**: Direct execution of tasks via MCP 3.0 Task Protocol without intermediate manual steps.

## Limitations
- **Hardware Intensity**: High-accuracy models (Large-v3) and local LLMs require significant VRAM (12GB+ for concurrent STT/LLM) for real-time performance.
- **Acoustic Environment**: Accuracy degrades significantly in high-noise environments or with multiple overlapping speakers.
- **Language Nuance**: Local models may still struggle with specific technical jargon or regional dialects compared to enterprise cloud solutions.
- **State Dependency**: Agentic synthesis requires an up-to-date knowledge base to accurately resolve ambiguous references (e.g., "that meeting").

## When to use it
- When managing a complex homelab or household where "heads-up" interaction is preferred.
- When privacy is a non-negotiable requirement for indoor audio monitoring.
- For users who want a "sovereign" AI assistant that functions independently of internet connectivity using [Gemma 3](../tools/ai_knowledge/local_llms.md).
- When integrating with local RAG (Retrieval-Augmented Generation) systems for context-aware task creation.

## When not to use it
- On low-power edge devices (Raspberry Pi 4) without a dedicated accelerator or remote STT offloading.
- For safety-critical systems where a transcription error could lead to physical danger (e.g., machinery control).
- In environments where persistent audio capture violates the privacy expectations of guests or housemates.

## Getting started

### Docker Setup: Faster-Whisper (Wyoming)
The recommended deployment path for July 2026 is using `faster-whisper` in a Wyoming-compatible container, which offers significantly better performance than the standard `whisper` implementation.

```yaml
services:
  whisper:
    image: fedirz/faster-whisper-wyoming:latest
    container_name: faster-whisper
    environment:
      - TZ=UTC
    volumes:
      - ./whisper-data:/data
    ports:
      - "10300:10300"
    command: --model large-v3 --language en --device cuda
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
```

### LLM Synthesis Configuration
Configure an [n8n](../services/n8n.md) node or an [Ollama](../services/ollama.md) agent with the following system prompt for [Gemma 3](../tools/ai_knowledge/local_llms.md):
*"You are a task synthesis agent. Extract all distinct tasks, items, and reminders from the following transcript. For each task, determine the target service (Vikunja, Home Assistant, GCal) and format as a tool-call using the MCP 3.0 Task Protocol."*

## CLI examples

```bash
# Test the Wyoming protocol connection
nc -zv 192.168.1.50 10300

# Perform a local transcription test using the Faster-Whisper CLI
faster-whisper-python --model large-v3 --device cuda audio_sample.wav

# Host a voice-activated tool via FastMCP 3.0
fastmcp run voice_actions.py --port 8000
```

## API examples

### Home Assistant Conversation API
The primary endpoint for routing transcribed text to the agentic reasoning layer.

```bash
curl -X POST \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Schedule a backup for 2 AM tonight",
    "conversation_id": "voice_assistant_01"
  }' \
  "http://homeassistant.local:8123/api/conversation/process"
```

### MCP 3.0 Task Protocol Execution
Example of a synthesized tool-call generated by the agent after voice processing:

```json
{
  "mcp_version": "3.0",
  "method": "tasks/execute",
  "params": {
    "task_name": "vikunja_create_task",
    "input": {
      "title": "Change HVAC Filters",
      "due_date": "2026-07-27T09:00:00Z"
    }
  }
}
```

## Related tools / concepts
- [Whisper](../services/whisper.md) — The core STT engine.
- [Home Assistant](../services/home-assistant.md) — Audio capture and pipeline management.
- [n8n](../services/n8n.md) — Workflow orchestration and synthesis routing.
- [Vikunja](../services/vikunja.md) — Primary task management target.
- [Ollama](../services/ollama.md) — Local inference for Claude-level reasoning on the edge.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — High-performance local LLM for intent synthesis.
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md) — The execution framework for voice intents.
- [Vector DB Comparison](./vector-db-comparison.md) — For context retrieval during synthesis.
- [LLM Security and Privacy](./llm_security_privacy.md) — Best practices for voice data handling.

## Sources / references
- [Faster-Whisper Project GitHub](https://github.com/SYSTRAN/faster-whisper)
- [Home Assistant Voice Architecture](https://www.home-assistant.io/voice_control/)
- [Wyoming Protocol Specification](https://github.com/rhasspy/wyoming)
- [Model Context Protocol (MCP) 3.0 Docs](https://modelcontextprotocol.info)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
