# DeepTutor

## What it is
DeepTutor is an AI-powered educational framework designed for personalized learning and intelligent tutoring. As of late October / November 2026, it leverages advanced reasoning models like **Claude 5.1** and **GPT-5.5** to guide students through complex curricula using a pedagogical layer that prioritizes cognitive scaffolding over direct answers.

## What problem it solves
It addresses the "tutor's dilemma"—the challenge of assisting a student without solving the problem for them. Standard LLMs are prone to providing immediate answers too quickly, which stunts active learning. DeepTutor enforces a structured, multi-turn reasoning workflow that evaluates student intent, isolates conceptual misconceptions, and supplies targeted prompts to encourage independent problem-solving.

## Where it fits in the stack
**Agentic Education Layer**. It sits between the user interface and foundational reasoning models, offering an orchestrator for deploying educational agents. It integrates directly with custom knowledge bases and **MCP 3.1** servers to supply domain-specific expertise grounded in verified curriculum standards.

## Typical use cases
- **Personalized STEM Tutoring**: Guiding students through physics or advanced calculus problems using sequential, Socratic questioning.
- **Developer Coding Mentorship**: Guiding engineers learning complex languages (e.g., Mojo, Rust) by analyzing logic flows and suggesting architectural improvements rather than writing syntax directly.
- **Enterprise Onboarding Assistance**: Automating developer and operational training using grounded internal repositories.
- **Multimodal Visual Diagnostics**: Utilizing frontier vision capabilities (GPT-5.5, Claude 5.1) to analyze student-drawn molecular schemas, electrical circuits, or handwritten equations.

## Strengths
- **Pedagogical Scaffolding**: Programmed to adhere to established educational guidelines (e.g., Vygotsky's Zone of Proximal Development).
- **Misconception Mapping**: Employs deep reasoning chains to locate and classify specific cognitive gaps in student explanations.
- **Model Agnostic**: Supports leading commercial and open-weight models natively.
- **MCP 3.1 & Task Protocol Compatibility**: Seamlessly reads local curriculum databases, code repositories, or third-party educational APIs.

## Limitations
- **Interaction Latency**: Executing multi-turn Socratic reasoning chains over high-tier frontier models can result in slower chat turnarounds.
- **High Inference Costs**: Maintaining deep tutoring swarms requires continuous reasoning calls to high-tier models like Opus, which can be expensive.
- **Persona Engineering Complexity**: Building customized academic personas ("Souls") and mapping correct curriculum taxonomies requires specialized knowledge engineering.

## When to use it
- When designing academic software that demands a "Socratic" or scaffolded teaching methodology over instant answers.
- For building responsive virtual teaching assistants that track user progress and adjust teaching profiles.
- When conducting research on agentic pedagogy and Intelligent Tutoring Systems (ITS).

## When not to use it
- For generic search or direct Q&A tasks where users only expect immediate facts or code blocks.
- In low-latency platforms where speed of response is valued above pedagogical value.
- If using basic, low-reasoning models that cannot sustain complex multi-turn Socratic states.

## Getting started

### Installation (Local)
DeepTutor requires Python 3.12+ and Node.js 22+.

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/HKUDS/DeepTutor.git
   cd DeepTutor
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e ".[server,reasoning]"
   ```
2. **Environment Configuration**:
   Create a `.env` file containing your `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.
3. **Launch the Server**:
   ```bash
   python scripts/start_tutor.py --model claude-5-1-opus-20261015
   ```

### Docker Deployment
```bash
docker compose up -d deeptutor-server
```

## CLI examples

### Initiate an Interactive Socratic Chat
```bash
deeptutor chat --subject "Thermodynamics" --mode socratic --model gpt-5.5-preview
```

### Ground a Knowledge Base
```bash
# Ingest textbook and curriculum chapters using MCP 3.1 protocols
deeptutor kb ingest ./curriculum/advanced_math/ --name math-advanced
```

### Analyze Student Response
```bash
# Analyze a student's response to detect underlying misconceptions
deeptutor analyze "The heavier object falls faster because of its mass"
```

## API examples

### Python Agent Instantiation
```python
from deeptutor import TutorAgent

# Initialize an agent with a specific "Soul" and knowledge grounding
tutor = TutorAgent(
    model="claude-5-1-opus-20261015",
    soul="encouraging-mentor",
    kb="organic-chemistry-v2"
)

# Perform a pedagogical turn
response = tutor.step("I don't see why the reaction is exothermic.")
print(f"Tutor Response: {response.content}")
```

### Defining Socratic Scaffolding and Session Validation with Pydantic v2
This Python script registers customized intervention behaviors and validates student tutoring session schemas using **Pydantic v2**:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class Misconception(BaseModel):
    concept_id: str = Field(..., description="Concept code under evaluation")
    description: str = Field(..., description="Detected misconception details")
    severity: str = Field("medium", description="Level of cognitive intervention needed")

class TutorSessionState(BaseModel):
    session_id: str = Field(..., description="Unique tutoring session identifier")
    student_id: str = Field(..., description="Student profile reference")
    current_topic: str = Field(..., description="Curriculum node under study")
    scaffolding_step: int = Field(0, description="Dialogue turn index in Socratic scaffold")
    detected_misconceptions: List[Misconception] = Field(default_factory=list, description="Identified cognitive gaps")

def validate_tutor_session(raw_json: str) -> Optional[TutorSessionState]:
    try:
        data = json.loads(raw_json)
        # Validate result object with Pydantic v2 model_validate
        response_data = TutorSessionState.model_validate(data)
        return response_data
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
```

## Related tools / concepts
- [NotebookLM](notebooklm.md) — For knowledge synthesis and grounded research.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — For connecting tutors to external datasets.
- [Claude](claude.md) — The primary reasoning model for pedagogical depth.
- [ChatGPT](chatgpt.md) — Alternative reasoning model provider.
- [AutoReason](../agents/autoreason.md) — Multi-agent reasoning framework.
- [GPT Researcher](../agents/gpt-researcher.md) — For generating the grounded content used by tutors.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The architectural pattern behind DeepTutor.
- [Local LLMs](local_llms.md) — For running tutoring sessions with open-weights models like Llama 4.

## Sources / references
- [DeepTutor GitHub Repository](https://github.com/HKUDS/DeepTutor)
- [DeepTutor: Agentic Scaffolding in STEM Education (arXiv 2026)](https://arxiv.org/abs/2604.26962)
- [Official Documentation and Soul Gallery](https://deeptutor.ai/docs)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
