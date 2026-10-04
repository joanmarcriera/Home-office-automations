# AWS Strands Decider Model

## What it is
The **AWS Strands Decider Model** is a specialized, lightweight reasoning and orchestration model family developed by Amazon Web Services (AWS) specifically designed for agentic decision routing, tool selection, and execution planning in autonomous workflows. Built as part of the AWS Strands Agentic Ecosystem, the Decider model functions as a high-speed, low-latency control plane component that parses multi-step user prompts, evaluates available tool capabilities, and emits structured action plans (JSON/FastMCP function calls) with minimal token overhead and deterministic decision boundaries.

In modern multi-agent systems, general-purpose frontier models (such as Claude 3.7 / 5.1 or GPT-5) are often over-parameterized and cost-prohibitive when used solely for intermediate routing, schema validation, or tool selection. The AWS Strands Decider Model addresses this by decoupling high-level reasoning from high-frequency tool selection and parameter generation, serving as an intelligent middleware router across AWS Bedrock, local microservices, and hybrid cloud infrastructures.

```
+-----------------------------------------------------------------------------------+
|                        AWS STRANDS DECIDER MODEL ARCHITECTURE                      |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +------------------------+      +---------------------------------------------+  |
|  | Multi-Step User Task   | ---> |  AWS Strands Decider Model                  |  |
|  | / Agent Context        |      |  (Zero-Shot Tool Router & Task Planner)    |  |
|  +------------------------+      +---------------------------------------------+  |
|                                                         |                         |
|                                                         v                         |
|                                  +---------------------------------------------+  |
|                                  | FastMCP 3.1 & Bedrock Agent Tool Dispatcher |  |
|                                  +---------------------------------------------+  |
|                                         /               |               \         |
|                                        v                v                v        |
|                            +---------------+    +---------------+    +----------+ |
|                            | AWS Lambda    |    | DynamoDB      |    | S3 Data  | |
|                            | Microservices |    | State Store   |    | Pipeline | |
|                            +---------------+    +---------------+    +----------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
- **Routing Latency & Token Costs**: Eliminates the heavy latency and compute cost of invoking 100B+ parameter LLMs for routine conditional logic, schema matching, and tool invocation decisions.
- **Deterministic Tool Calling**: Reduces tool hallucination and invalid parameter generation by training specifically on strict JSON Schema contracts and FastMCP 3.1 tool call specifications.
- **Agent Orchestration Overhead**: Simplifies multi-agent state machines by providing explicit next-action outputs, stop-conditions, and parallel tool dispatch configurations in unified structured payloads.
- **Vendor & Infrastructure Lock-in**: Works seamlessly across AWS Bedrock, local containerized runtimes (via vLLM / Ollama), and hybrid agentic frameworks (FastMCP, LangChain, AutoGen).

## Where it fits in the stack
**AI Knowledge / Agent Orchestration / Model Infrastructure**. The AWS Strands Decider Model operates as an intermediate orchestration and decision engine within the agentic stack. It sits between user-facing conversational models/interfaces and execution tools (FastMCP servers, AWS Lambda, API Gateways, databases).

```
+-----------------------------------------------------------------------------------+
|                            ENTERPRISE AGENTIC STACK                               |
+-----------------------------------------------------------------------------------+
| Application / Chat Layer : Open WebUI / Enterprise Chat / CLI / IDE Extensions    |
+-----------------------------------------------------------------------------------+
| Task Planner & Router   : AWS Strands Decider Model (Fast Orchestration)          |
+-----------------------------------------------------------------------------------+
| Tool Execution Engine   : FastMCP 3.1 Servers / AWS Bedrock Agent Runtime          |
+-----------------------------------------------------------------------------------+
| Execution Services      : AWS Lambda, ECS Tasks, Vector DBs, Cloud APIs           |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Tool Autonomous Workflows**: Automatically evaluating 50+ available MCP tools, filtering irrelevant functions, and emitting precise tool call parameters in under 100 milliseconds.
- **State Machine Next-Action Resolution**: Evaluating intermediate output from previous tool executions to decide whether to continue execution, request human intervention, or finalize output.
- **Dynamic Tool Schema Filtering**: Pruning excessive tool definitions from LLM prompt context windows by dynamically pre-selecting top-$N$ relevant tools prior to calling primary frontier reasoning models.
- **Cost-Optimized Enterprise RAG Routing**: Route user queries between vector search, SQL query generation, live web search, or static knowledge bases based on query intent classification.

## Strengths
- **Ultra-Low Latency Execution**: Optimized for sub-100ms inference times on AWS Inferentia2 and NVIDIA GPUs, drastically improving agent response speed.
- **Native FastMCP 3.1 Support**: Direct formatting alignment with Model Context Protocol tool specifications and Pydantic schema contracts.
- **Strict Deterministic Outputs**: Minimal propensity for hallucinating non-existent tool names or invalid schema properties.
- **Bedrock & Hybrid Flexibility**: Available as a native AWS Bedrock serverless endpoint or deployable as an ONNX/GGUF model container on local edge hardware.

## Limitations
- **Narrow General Knowledge**: Not designed for open-ended creative writing, deep multi-page synthesis, or complex mathematical reasoning without external tool access.
- **Fixed Context Windows**: Standard context windows (32k–64k tokens) require active context management and context-pruning strategies when handling massive document sets.
- **Fine-Tuning Dependency**: Optimal performance on enterprise-proprietary tool sets requires providing clean JSON Schema definitions or domain-specific fine-tuning examples.

## When to use it
- When building high-throughput agent systems that invoke dozens of tool calls per user transaction.
- To drastically reduce AWS Bedrock / OpenAI API token bills by offloading routing logic from heavy LLMs.
- When deploying FastMCP 3.1 tool execution backends in latency-sensitive production environments.
- For hybrid cloud architectures where decision logic must run locally or on sovereign cloud infrastructure.

## When not to use it
- When requiring deep open-ended conversational synthesis, creative narrative generation, or direct long-form document drafting.
- For simple static API endpoints where deterministic code logic (if/else statements or regex) is sufficient without AI models.
- In low-throughput, single-turn chat applications where model invocation cost and latency are non-critical.

## Getting started

### Prerequisites
- AWS CLI configured with Bedrock permissions (`bedrock:InvokeModel`) or a local vLLM / Ollama instance.
- Python 3.10+ with `boto3`, `pydantic` v2, and `fastmcp` installed.

### Deploying / Accessing via AWS Bedrock
```bash
# Verify AWS Bedrock model availability for AWS Strands Decider Model
aws bedrock list-foundation-models \
  --by-provider amazon \
  --query "modelSummaries[?contains(modelId, 'strands-decider')].[modelId, modelName]" \
  --output table
```

### Quickstart Execution with Python
```python
import boto3
import json

bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

payload = {
    "prompt": "User wants to list all active S3 buckets and summarize storage usage.",
    "tools": [
        {"name": "list_s3_buckets", "description": "Lists all S3 buckets in account"},
        {"name": "get_bucket_metrics", "description": "Returns storage usage metrics for a bucket"}
    ]
}

response = bedrock.invoke_model(
    modelId="amazon.strands-decider-v1",
    contentType="application/json",
    accept="application/json",
    body=json.dumps(payload)
)

result = json.loads(response["body"].read())
print("Decider Decision Output:", result)
```

## CLI examples

### Invoking AWS Strands Decider via AWS CLI
```bash
# Execute direct model invocation with CLI payload
aws bedrock-runtime invoke-model \
  --model-id amazon.strands-decider-v1 \
  --content-type application/json \
  --accept application/json \
  --body '{"prompt":"Determine target tool for query: Check CPU utilization for i-0123456789","tools":[{"name":"get_cloudwatch_metric","parameters":{"instance_id":"string","metric":"string"}}]}' \
  output.json

# Read structured decision response
cat output.json | jq .
```

### Inspecting Local Containerized Decider Instance
```bash
# Running containerized local strands decider via vLLM
docker run -d --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model aws-strands/strands-decider-4b \
  --max-model-len 32768

# Test OpenAI-compatible endpoint with tool payload
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "aws-strands/strands-decider-4b",
    "messages": [{"role": "user", "content": "Fetch logs for container webservice-prod"}],
    "tools": [{
      "type": "function",
      "function": {
        "name": "fetch_container_logs",
        "description": "Fetches logs from ECS/Docker container",
        "parameters": {
          "type": "object",
          "properties": {"container_name": {"type": "string"}},
          "required": ["container_name"]
        }
      }
    }]
  }' | jq .
```

## API examples

### FastMCP 3.1 Integration Server
This example demonstrates constructing a FastMCP 3.1 tool server that uses the AWS Strands Decider Model as an internal decision and routing dispatcher:

```python
from fastmcp import FastMCP
import boto3
import json
from pydantic import BaseModel, Field

# Initialize FastMCP Server
mcp = FastMCP("AWS-Strands-Decider-Router")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

class DecisionRequest(BaseModel):
    user_query: str = Field(..., description="User query or task prompt requiring routing")
    context_data: dict = Field(default_factory=dict, description="Current agent execution state/context")

class DecisionResponse(BaseModel):
    selected_tool: str = Field(..., description="Name of the selected tool to execute")
    parameters: dict = Field(default_factory=dict, description="Extracted parameters matching tool schema")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")

@mcp.tool()
def route_agent_task(request: DecisionRequest) -> DecisionResponse:
    """Routes an agent task to the optimal tool using AWS Strands Decider Model."""
    decider_payload = {
        "query": request.user_query,
        "context": request.context_data,
        "mode": "deterministic_tool_select"
    }

    raw_response = bedrock_client.invoke_model(
        modelId="amazon.strands-decider-v1",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(decider_payload)
    )

    res_data = json.loads(raw_response["body"].read().decode("utf-8"))

    # Return validated Pydantic model response
    return DecisionResponse(
        selected_tool=res_data.get("tool", "unknown_tool"),
        parameters=res_data.get("args", {}),
        confidence=res_data.get("confidence", 0.95)
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Schema & Validation
```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class ToolParameterSpec(BaseModel):
    param_name: str = Field(..., description="Name of parameter")
    param_type: str = Field(..., description="Data type (string, integer, boolean, object)")
    required: bool = Field(default=True, description="Whether parameter is mandatory")

class DeciderSchemaContract(BaseModel):
    tool_name: str = Field(..., description="Target tool identifier")
    parameters: List[ToolParameterSpec] = Field(default_factory=list)
    execution_timeout_sec: int = Field(default=30, ge=1, le=300)

    @field_validator("tool_name")
    @classmethod
    def validate_tool_name_format(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError(f"Tool name '{v}' must be a valid Python identifier")
        return v

# Example schema validation test
try:
    contract = DeciderSchemaContract(
        tool_name="aws_s3_sync_bucket",
        parameters=[
            ToolParameterSpec(param_name="source_bucket", param_type="string", required=True),
            ToolParameterSpec(param_name="dest_bucket", param_type="string", required=True)
        ],
        execution_timeout_sec=45
    )
    print("Schema Contract Validated:", contract.model_dump_json(indent=2))
except ValidationError as e:
    print("Validation Failure:", e.json())
```

## Related tools / concepts
- [AWS Bedrock](../providers/aws.md) — Managed AWS foundation model and agent service platform.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — High-performance tool server standard for agent ecosystems.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Universal standard for connecting models to data sources.
- [LangChain](langchain.md) — Popular framework for developing applications powered by language models.
- [AutoGen](../frameworks/autogen.md) — Multi-agent conversation framework from Microsoft.
- [Local LLMs](../ai_knowledge/local_llms.md) — Deploying open-weights models locally via vLLM or Ollama.

## Sources / references
- [AWS Strands Decider Model Announcement](https://thenewstack.io/aws-strands-decider-model/)
- [AWS Bedrock Developer Documentation](https://docs.aws.amazon.com/bedrock/)
- [FastMCP 3.1 Ecosystem Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
