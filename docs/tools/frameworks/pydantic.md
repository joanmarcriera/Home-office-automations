# Pydantic

## What it is
Pydantic is the standard data validation, serialization, and settings management library for Python. By combining type annotations with fast, compiled C Rust core validation logic (Pydantic V2 built on `pydantic-core`), Pydantic guarantees that input data conforms to defined schema boundaries, converting raw inputs (JSON, environment variables, dicts) into strongly-typed Python objects.

In early 2027, Pydantic forms the architectural backbone of modern Python backend engineering and AI software stacks. It powers core web frameworks (FastAPI), agentic AI frameworks ([Pydantic AI](pydantic-ai.md)), vector database interfaces, and LLM structured output parsing engines.

## What problem it solves
Python's dynamic typing allows data payload mismatch errors to surface at runtime deep within application execution pipelines. Parsing untrusted JSON payloads or environment configuration variables manually requires verbose validation code, error checking, and type casting.

Pydantic solves these challenges by providing:
- **Type Safety at Runtime**: Guarantees that data structures conform strictly to declared types at runtime.
- **High-Performance Validation**: Rust-compiled engine evaluates data validation rules significantly faster than traditional pure-Python validation libraries.
- **Automatic Schema Generation**: Generates standard JSON Schema definitions automatically from models for OpenAPI documentation and LLM tool-calling schemas.

## Where it fits in the stack
**AI Frameworks & Data Processing Layer**. Pydantic functions as the foundational schema layer for Python backend microservices, API request/response validation, environment configuration management, and LLM structured outputs in frameworks like [Pydantic AI](pydantic-ai.md).

## Typical use cases
- **LLM Structured Output Generation**: Forcing Large Language Models to return valid JSON payloads adhering strictly to Pydantic models (JSON Mode / Function Calling).
- **Agent Tool Calling & Action Schemas**: Defining strict tool parameters and state structures in agent frameworks like [Pydantic AI](pydantic-ai.md) and AutoGen.
- **API Request Validation & Serialization**: Serving as the data validation layer in web frameworks (FastAPI, Litestar).
- **Settings & Environment Configuration**: Loading and validating environment variables from `.env` files into strongly typed configuration objects (`pydantic-settings`).

## Strengths
- **Rust Speed Engine**: Pydantic V2 core is written in Rust, offering up to 20x performance speedups over legacy validation libraries.
- **Native IDE & Static Type Support**: Works seamlessly with mypy, pyright, VS Code, and PyCharm without requiring custom plugins.
- **JSON Schema Integration**: Exports standard JSON Schemas out-of-the-box via `.model_json_schema()`, making it the primary standard for OpenAI / Anthropic tool definition APIs.
- **Extensible Field Validators**: Powerful custom field validators, pre-parsing transforms, and custom error formatting.

## Limitations
- **Immutability Overhead**: Creating frozen Pydantic instances incurs slight overhead when modifying nested attributes frequently in tight mathematical loops.
- **V1 vs V2 Migration**: Minor syntax differences remain between legacy Pydantic V1 (`@validator`) and V2 (`@field_validator`).

## When to use it
- When validating untrusted API payloads, external database entries, or user inputs in Python services.
- When defining structured outputs or tool argument contracts for LLM agents ([Pydantic AI](pydantic-ai.md)).
- When parsing environment variables into application settings.

## When not to use it
- In ultra-low-latency numerical compute or array loops (e.g., NumPy/PyTorch tensor manipulations) where dynamic runtime object creation introduces unacceptable overhead.

## Getting started

### Installation
Install Pydantic v2 and settings plugin:

```bash
pip install pydantic pydantic-settings
```

## CLI examples

### Inspecting Installed Pydantic System Details
```bash
# Print Pydantic environment compiled C/Rust extensions details
python3 -c "import pydantic; print(pydantic.__version__)"
```

## API examples

### Python (Pydantic BaseSettings Environment Variable Parser)
```python
from pydantic import Field
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    api_key: str = Field(..., env="API_KEY")
    debug_mode: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"

settings = AppSettings()
```

## Code examples

### Python (Data Validation & Field Constraint Modeling)
```python
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator

class UserProfile(BaseModel):
    id: int = Field(..., description="Unique user identifier")
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr = Field(..., description="Valid primary user email address")
    is_active: bool = Field(default=True)
    roles: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("roles")
    @classmethod
    def validate_roles(cls, v: List[str]) -> List[str]:
        valid_roles = {"admin", "developer", "viewer"}
        for role in v:
            if role not in valid_roles:
                raise ValueError(f"Invalid role '{role}'. Must be one of {valid_roles}")
        return v

if __name__ == "__main__":
    # Valid Payload Parsing
    raw_json = '{"id": 101, "username": "jules_ops", "email": "jules@example.com", "roles": ["developer", "admin"]}'
    user = UserProfile.model_validate_json(raw_json)
    print("Parsed User Object:")
    print(user.model_dump())

    # Exporting JSON Schema for LLM Tool Definition
    print("\nGenerated JSON Schema:")
    print(UserProfile.model_json_schema())
```

### Python (Structured LLM Output Schema)
```python
from pydantic import BaseModel, Field
from typing import List

class CodeReviewIssue(BaseModel):
    file_path: str = Field(..., description="Path to the file containing the issue")
    line_number: int = Field(..., description="Line number of the issue")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', 'critical'")
    suggestion: str = Field(..., description="Specific recommended fix")

class CodeReviewReport(BaseModel):
    summary: str = Field(..., description="Executive summary of the code review findings")
    issues: List[CodeReviewIssue] = Field(..., description="List of detected code issues")
    score: int = Field(..., ge=0, le=100, description="Overall code quality score out of 100")

# The report model can be passed directly to LLM provider structured outputs APIs:
# client.beta.chat.completions.parse(model="gpt-4o", response_format=CodeReviewReport, ...)
```

## Related tools / concepts
- [Pydantic AI](pydantic-ai.md) — Agentic framework built entirely on Pydantic schema validation.
- [DeepSpeed](deepspeed.md) — Optimization library configured via validated JSON models.
- [Bloomberg Terminal](../enterprise/bloomberg-terminal.md) — Enterprise data source whose API outputs are mapped into Pydantic models.

## Sources / references
- [Pydantic Official Website](https://docs.pydantic.dev/)
- [Pydantic GitHub Repository](https://github.com/pydantic/pydantic)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
