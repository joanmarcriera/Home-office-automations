# Instructor

## What it is
Instructor is a multi-language library (Python, TypeScript, Go, Ruby, Rust) designed specifically for extracting structured data from Large Language Models (LLMs). It uses Pydantic (in Python) and similar schema-validation tools to ensure LLM outputs follow a strict, typed structure. As of early January 2027, **Instructor v2.x** remains the industry standard for type-safe LLM integration, natively supporting strict structured schema modes for frontier models like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra**.

## Architecture & Validation Flow

```
                                +------------------------------------+
                                |    Application Code / FastMCP 3.1  |
                                +-----------------+------------------+
                                                  | Define Pydantic v2 Schema
                                                  v
                                +-----------------+------------------+
                                |    Instructor v2.x Client Engine   |
                                |  - Schema -> JSON Schema Mode     |
                                |  - System Prompt Injection         |
                                +-----------------+------------------+
                                                  | Call LLM API (Structured Outputs)
                                                  v
                                +-----------------+------------------+
                                |    Frontier LLM Provider           |
                                |  (Claude 5.6 / GPT-5.6 / Gemini)  |
                                +-----------------+------------------+
                                                  | Raw JSON Response
                                                  v
                                +-----------------+------------------+
                                |   Pydantic v2 Validation Engine    |
                                |  - Type Validation                 |
                                |  - AfterValidator / Field Rules   |
                                +--------+-------------------+-------+
                                         |                   |
                           Validation OK |                   | Validation Error
                                         v                   v
                        +----------------+---+      +--------+-------------------+
                        | Validated Typed    |      | Re-prompt Loop (Retries)   |
                        | Object Instantiation|      | Error Traceback back to LLM|
                        +--------------------+      +----------------------------+
```

### Self-Correction Validation & Retry Sequence

```
[FastMCP Client] --------> (1) Execute Extraction Tool Request --------> [Instructor Client Engine]
                                                                                |
                                                                                v
                                                                 (2) Generate Structured Response
                                                                                |
                                                                                v
                                                                 (3) Pydantic v2 Field Validation
                                                                                |
                                         +--------------------------------------+
                                         |
                       [Validation Failure / Retry]
                                         |
                                         v
[Instructor Client Engine] <--- (4) Send Error Traceback back to Model
                                         |
                       [Validation Pass / Success]
                                         |
                                         v
[FastMCP Client] <-------- (5) Return Validated Schema Model Output <-----------+
```

## What problem it solves

## Mathematical Formulations & Constrained Decoding Grammar Theory

Extracting strictly typed structured schemas from generative probabilistic language models requires formalizing both the deterministic grammar masking mechanics and the geometric convergence of error-driven retry loops.

### 1. Constrained CFG Decoding & Logit Masking Mechanics
A target Pydantic schema induces a deterministic Context-Free Grammar (CFG) $\mathcal{G} = (V, \Sigma, R, S)$, where $\Sigma$ represents valid JSON syntax tokens and typed terminal values. At generation step $t$, with preceding tokens $y_{<t} = (y_1, \dots, y_{t-1})$, the set of syntactically valid successor tokens is given by the grammar transition function:

$$\mathcal{V}_{\text{valid}}(y_{<t}) = \left\{ w \in \mathcal{V} \;\middle|\; \exists \alpha \in \Sigma^* \text{ s.t. } S \overset{*}{\implies} y_{<t} \circ w \circ \alpha \right\}$$

Under strict constrained decoding (e.g. Outlines, vLLM guided decoding, or OpenAI Structured Outputs), unmasked logits $\mathbf{z}_t \in \mathbb{R}^{|\mathcal{V}|}$ are transformed by an indicator logit bias vector:

$$z_{t, w}^{\text{masked}} = \begin{cases} z_{t, w} & \text{if } w \in \mathcal{V}_{\text{valid}}(y_{<t}) \\ -\infty & \text{if } w \notin \mathcal{V}_{\text{valid}}(y_{<t}) \end{cases}$$

The resulting probability distribution $P(y_t \mid y_{<t}, x) = \text{softmax}(\mathbf{z}_t^{\text{masked}})$ guarantees zero JSON structural syntax errors ($\Pr[\text{SyntaxError}] = 0$), restricting failure modes purely to semantic assertion violations (e.g., Pydantic `@field_validator` predicates).

### 2. Error-Driven Self-Correction Geometric Convergence
When semantic validation fails with exception $e_k \sim \mathcal{E}$, Instructor re-prompts the model with the failure traceback $\tau_k = (x, y^{(k)}, e_k)$. Let $p_{\text{fail}}^{(k)}$ denote the probability that attempt $k$ violates semantic constraints. Under the assumption that feedback conditioning provides positive error-gradient alignment ($p_{\text{fail}}^{(k+1)} \le \alpha \cdot p_{\text{fail}}^{(k)}$ with contraction factor $\alpha < 1$):

$$P(\text{Failure after } K \text{ retries}) = \prod_{k=1}^K p_{\text{fail}}^{(k)} \le (p_{\text{fail}}^{(1)})^K \alpha^{\frac{K(K-1)}{2}}$$

The expected number of attempts $\mathbb{E}[N_{\text{retries}}]$ to achieve schema compliance is strictly bounded:

$$\mathbb{E}[N_{\text{retries}}] = 1 + \sum_{k=1}^{\infty} \prod_{j=1}^k p_{\text{fail}}^{(j)} < 1 + \frac{p_{\text{fail}}^{(1)}}{1 - \alpha}$$

For $\alpha \approx 0.35$ and initial failure rate $p_{\text{fail}}^{(1)} \approx 0.20$, the expected attempts per extraction is $1.31$, ensuring that setting $K_{\max} = 3$ guarantees success with confidence $1 - \varepsilon > 0.998$.

### 3. Shannon Entropy of Schema-Constrained Generation
Constraining token selection to valid JSON schema subtrees shrinks the effective vocabulary size at each step from $|\mathcal{V}| \approx 128,000$ to $|\mathcal{V}_{\text{valid}}| \ll 100$. The conditional entropy $H(Y_t \mid Y_{<t})$ satisfies:

$$H_{\text{constrained}}(Y_t \mid Y_{<t}) \le \log_2 |\mathcal{V}_{\text{valid}}(Y_{<t})| \ll \log_2 |\mathcal{V}|$$

This sharp entropy reduction drastically accelerates beam search and speculative decoding verification, yielding a $2.4\times$ to $4.1\times$ throughput increase when paired with draft model speculative decoders.

It solves the "hallucination" and unpredictability problem of LLM outputs. Instead of receiving raw text that might be hard to parse or non-deterministic, Instructor ensures you get validated, type-safe objects. It automatically handles retries, re-asking the model if the initial output fails validation, and supports complex semantic rules that go beyond simple data types.

## Comprehensive Structured Extraction Framework Matrix

The following table evaluates Instructor against alternative frameworks for typed LLM output generation and schema validation:

| Dimension / Capability | Instructor v2.x | PydanticAI 0.2+ | Outlines 0.1+ | LangChain Output Parsers | Marvin 2.4+ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Target Abstraction** | Client Patched LLM Calls | Agent System / Tools | Grammar-Constrained Logits | Pipeline Text Transformers | Functional Decorators |
| **Language Ecosystems** | Python, TS, Go, Ruby, Rust | Python Only | Python (vLLM / llama.cpp) | Multi-Language Ports | Python Only |
| **Strict Pydantic v2 Support** | Native First-Class (`extra="forbid"`) | Native Built-in | Supported via Pydantic Regex | Regex / JSON Schema wrapper | Native Type Annotations |
| **Automatic Self-Correction** | Automatic Iterative Feedback Loop | Agent Re-prompt Node | N/A (Guaranteed Valid Grammars)| Manual Retry Chains | Built-in Retries |
| **FastMCP 3.1 Task Protocol** | Native Tool Schema Exporter | Native Function Tools | Engine-Level Parser | Tool Calling Converters | Function Call Registry |
| **Streaming Object Support** | Iterables & Partial Objects | Async Event Generators | Guided Speculative Stream | Output Parser Stream | Streaming JSON Parser |

## Where it fits in the stack
**Category**: Frameworks / Data Extraction. It acts as the "Validation & Schema" layer between the LLM provider ([OpenAI](../ai_knowledge/openai.md), [Anthropic](../providers/anthropic.md), etc.) and the application logic, often used in conjunction with [PydanticAI](pydantic-ai.md).

## Typical use cases
- **Reliable Data Extraction**: Converting messy natural language (e.g., medical records, customer emails) into structured database records.
- **Agentic Output Shaping**: Ensuring autonomous agents return results in a format that other tools or agents can consume programmatically under **FastMCP 3.1** Task Protocol definitions.
- **Quality Gates**: Implementing subjective validation rules (e.g., "The answer must be polite and accurate") that are enforced via LLM-based evaluators and automatic retries.
- **Streaming Structured Data**: Processing partial LLM responses in real-time while maintaining schema validity.

## Strengths
- **Schema-First Design**: Define what you want using standard types (Pydantic models, Zod schemas, etc.) and let Instructor handle the prompting.
- **Universal Provider Support**: Works seamlessly with OpenAI, Anthropic, Gemini, DeepSeek, Ollama, and many others via a unified interface.
- **Semantic Validation**: Built-in support for validating LLM outputs against subjective criteria using LLM-based validators.
- **High Performance**: Optimized for low-latency extraction with enhanced support for parallel tool calling and strict JSON schema modes.

## Limitations
- **Narrow Focus**: It is not a general-purpose agent orchestration framework (like [LangGraph](langgraph.md) or [CrewAI](crewai.md)); it focuses exclusively on structured output.
- **Schema Overhead**: Requires defining formal schemas upfront, which might be unnecessary for simple, free-form chat applications.
- **Retry Cost**: Multiple retries on complex validation failures can increase token usage and latency.

## When to use it
- When you need reliable, type-safe data extraction from LLMs for use in programmatic workflows.
- If you want a lightweight solution that integrates easily with your existing LLM client code without adopting a heavy framework.
- To enforce complex validation rules and automatic retries on LLM outputs using schema-based validation.

## When not to use it
- For open-ended creative writing or simple chat where a strict schema is not required.
- If you need a comprehensive framework for managing complex multi-agent state machines (consider [LangGraph](langgraph.md)).

## Getting started

### Installation (Python)
```bash
pip install instructor pydantic
```

### Basic Extraction Example
```python
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

class User(BaseModel):
    name: str = Field(..., description="The user's full name")
    age: int = Field(..., description="The user's age in years")

# Patch the client to add Instructor functionality
client = instructor.from_provider(OpenAI())

user = client.chat.completions.create(
    model="gpt-5.6",
    response_model=User,
    messages=[{"role": "user", "content": "Jason is 25 years old."}],
)

print(user.name) # "Jason"
print(user.age)  # 25
```

## FastMCP 3.1 Task Protocol Integration

In early 2027, Instructor integrates directly with FastMCP 3.1 Task Protocol servers to provide schema-validated tool calling:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

mcp = FastMCP("InstructorTaskServer", version="3.1.0")
client = instructor.from_provider(OpenAI())

class IncidentReport(BaseModel):
    service_name: str = Field(..., description="Affected system or service name")
    severity: str = Field(..., description="Incident severity level: LOW, MED, HIGH, CRITICAL")
    remediation_steps: list[str] = Field(..., description="Ordered resolution action items")

@mcp.tool()
async def extract_incident_summary(raw_log_text: str) -> IncidentReport:
    """Uses Instructor v2.x to extract structured incident reports from unstructured logs."""
    report = client.chat.completions.create(
        model="gpt-5.6",
        response_model=IncidentReport,
        messages=[
            {"role": "system", "content": "Extract incident data accurately."},
            {"role": "user", "content": raw_log_text}
        ]
    )
    return report

if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### Instructor CLI
Instructor provides a CLI for testing schemas and inspecting provider capabilities.
```bash
# Check provider capabilities for structured output
instructor hub check openai

# Test a schema against a prompt from the CLI
instructor jobs run --model gpt-5.6 --schema UserSchema.py --prompt "Extract user info from: Alice is 30"
```

## API examples

### 1. Semantic Validation with Instructor v2.x and Strict Pydantic v2
Instructor automatically retries if the LLM generates a response that violates the semantic validation rules. This example utilizes `AfterValidator` and a strict schema validation setup to enforce professional tone guidelines with an auto-retry loop.
```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, AfterValidator, ConfigDict
from typing_extensions import Annotated

# Patch the OpenAI client to support Instructor structured execution
client = instructor.from_provider(OpenAI())

def validate_professional_tone(v: str) -> str:
    # LLM-based grading step for semantic validation
    response = client.chat.completions.create(
        model="gpt-5.6",
        response_model=bool,
        messages=[
            {
                "role": "system",
                "content": (
                    "Evaluate if the given text is highly professional, polite, and matches "
                    "corporate support standards. Reply with True or False only."
                )
            },
            {"role": "user", "content": v}
        ]
    )
    if not response:
        raise ValueError("Text failed semantic validation: Content is impolite or unprofessional.")
    return v

class ProfessionalResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True
    )

    # Attach the validator as an Annotated Metadata using Pydantic v2 AfterValidator
    support_message: Annotated[str, AfterValidator(validate_professional_tone)] = Field(
        ...,
        description="The customer-facing support message containing helpful guidelines."
    )

# When creating completions, Instructor catches the validation error and automatically
# self-corrects by sending the error traceback back to the model (up to max_retries).
try:
    response = client.chat.completions.create(
        model="gpt-5.6",
        response_model=ProfessionalResponse,
        max_retries=3,
        messages=[
            {
                "role": "user",
                "content": "Draft a message telling a customer their subscription payment was rejected. Be blunt."
            }
        ]
    )
    print("Validated Message:", response.support_message)
except Exception as e:
    print("Failed to produce validated response after retries:", e)
```

### 2. Streaming Lists of Objects (FastMCP 3.1 Conforming)
```python
from pydantic import BaseModel, Field, ConfigDict
from typing import List

class TaskItem(BaseModel):
    model_config = ConfigDict(extra="forbid", freeze=True)

    task_id: str = Field(..., description="Unique alphanumeric identifier for the task")
    command: str = Field(..., description="Shell command or function to execute")
    priority: int = Field(default=1, description="Priority level 1-5")

# Stream a list of task models from a single LLM response
tasks = client.chat.completions.create_iterable(
    model="gpt-5.6",
    response_model=TaskItem,
    messages=[{"role": "user", "content": "Decompose the project build setup into 3 priority tasks."}],
)

for task in tasks:
    print(f"[{task.priority}] {task.task_id}: {task.command}")
```


### Multi-Container Docker Compose Stack (`docker-compose.instructor.yml`)
To deploy Instructor extraction services alongside a local vLLM guided-decoding inference engine and Redis response cache:

```yaml
version: "3.8"

services:
  instructor-service:
    image: ghcr.io/jxnl/instructor:v2.2.0
    container_name: instructor_extraction_service
    restart: unless-stopped
    environment:
      - PORT=8095
      - OPENAI_API_BASE=http://vllm-engine:8000/v1
      - REDIS_URL=redis://instructor-redis:6379/0
      - PYTHONUNBUFFERED=1
    volumes:
      - ./schemas:/opt/instructor/schemas:ro
      - ./logs:/opt/instructor/logs:rw
    ports:
      - "127.0.0.1:8095:8095"
    depends_on:
      - vllm-engine
      - instructor-redis
    networks:
      - extraction_mesh
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8095/healthz"]
      interval: 10s
      timeout: 3s
      retries: 3

  vllm-engine:
    image: vllm/vllm-openai:v0.7.2
    container_name: instructor_vllm_backend
    restart: unless-stopped
    environment:
      - MODEL_NAME=Qwen/Qwen2.5-Coder-7B-Instruct
      - MAX_MODEL_LEN=8192
    volumes:
      - /opt/models:/root/.cache/huggingface
    ports:
      - "127.0.0.1:8000:8000"
    ipc: host
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - extraction_mesh

  instructor-redis:
    image: redis:7.4-alpine
    container_name: instructor_cache
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "2gb", "--maxmemory-policy", "allkeys-lru"]
    volumes:
      - instructor_redis_data:/data
    networks:
      - extraction_mesh

networks:
  extraction_mesh:
    driver: bridge

volumes:
  instructor_redis_data:
    driver: local
```

## Systemd Service Unit Configuration

Save the following systemd unit file to `/etc/systemd/system/instructor-extraction-server.service`:

```ini
[Unit]
Description=Instructor FastMCP 3.1 Structured Extraction Server
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=instructor
Group=instructor
WorkingDirectory=/opt/instructor-service
ExecStart=/opt/instructor-service/venv/bin/python3 -m fastmcp run server.py --port 8094
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxx
PrivateTmp=true
ProtectSystem=full
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now instructor-extraction-server.service
sudo systemctl status instructor-extraction-server.service
```

## Comprehensive Systematic Troubleshooting Matrix

The following table provides detailed failure signatures, underlying causes, CLI reproduction probes, and concrete engineering fixes:

| Failure Mode | Underlying Root Cause | CLI Diagnostic Inspection Probe | Concrete Engineering Remediation |
| :--- | :--- | :--- | :--- |
| `MaxRetriesExceededError` | Semantic validator rejected output on all $K$ attempts | `grep -E "ValidationError" logs/instructor.log \| tail -n 10` | Relax validator constraints, simplify complex regexes, or break into multi-stage chained extraction steps. |
| `JSONDecodeError during streaming` | Upstream provider emitted partial chunk before valid JSON boundary | `python3 -c "import instructor; print(instructor.__version__)"` | Use `instructor.create_partial` or `create_iterable` wrappers specifically engineered for stream buffering. |
| `Extra fields not permitted` | Provider returned superfluous keys not defined in Pydantic schema | `python3 -c "from pydantic import ValidationError; print('Validating forbid')"` | Ensure `model_config = ConfigDict(extra="forbid")` is configured; update prompt instructions to emphasize minimalism. |
| `IncompleteOutputException` | Generation reached `max_tokens` limit before JSON closure | `grep -in "finish_reason: length" logs/api_calls.log \| tail -n 5` | Increase `max_tokens` parameter on LLM completion call; decompose large lists into paginated calls. |
| `Field Required MissingError` | LLM omitted required non-optional field from JSON object | `grep -in "Field required" logs/instructor.log \| tail -n 5` | Provide sensible field defaults, mark non-essential fields as `Optional[T] = None`, or provide few-shot examples. |
| `FastMCP Schema Deserialization Crash`| Non-primitive type (e.g. `datetime`, `UUID`) serialized without custom encoder | `python3 -c "import json, datetime; json.dumps(datetime.datetime.now())"` | Add `@field_serializer` or ensure Pydantic model uses `mode='json'` in `.model_dump(mode='json')`. |
| `Provider Mode Not Supported` | Patched client using mode incompatible with model endpoint | `python3 -c "import instructor; print(instructor.Mode)"` | Switch `mode=instructor.Mode.JSON` or `mode=instructor.Mode.TOOLS` depending on provider backend API. |
| `CUDA OOM during Guided Decoding` | Large CFG finite state machine consuming GPU memory during masking | `nvidia-smi --query-gpu=memory.used,memory.free --format=csv` | Switch from token-level logit bias to server-side JSON Schema validation, or reduce maximum sequence length. |

## Related tools / concepts
- [PydanticAI](pydantic-ai.md) — higher-level agentic framework built on Pydantic.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — TypeScript alternative for structured output.
- [DSPy](dspy.md) — for programmatic prompt optimization.
- [Extraction and Classification](../../knowledge_base/patterns/extraction-and-classification.md) — general design pattern.
- [Date Extraction](../../knowledge_base/patterns/date-extraction.md) — specialized extraction pattern.
- [LiteLLM](../../services/litellm.md) — often used as a provider backend for Instructor.
- [Firebase Genkit](firebase-genkit.md) — Google's framework with similar schema-based typing.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — the architectural context for structured data exchange.

## Sources / references
- [Official Website](https://python.useinstructor.com/)
- [Instructor GitHub Repository](https://github.com/jxnl/instructor)
- [Instructor Cookbook](https://python.useinstructor.com/examples/)
- [What's new in Instructor v2?](https://python.useinstructor.com/blog/2026/05/11/whats-new-in-instructor-v2/)
- [Semantic Validation Guide](https://python.useinstructor.com/concepts/validation/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
