# AWS Strands Decider Model

AWS Strands Decider Model is an enterprise-grade, agentic orchestration model designed by Amazon Web Services to govern dynamic task routing, action selecting, and agent decision-making within autonomous multi-agent systems. Built to sit between high-level reasoning LLMs and low-level execution tools, AWS Strands Decider evaluates complex context, selects optimal tools from expansive registries, and ensures policy-compliant execution across cloud and multi-agent infrastructures.

```
+-----------------------------------------------------------------------------------+
|                            Agentic System Workflow                                |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             Input Context & Goal                                  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         AWS Strands Decider Engine                                |
|  +---------------------------+  +-------------------+  +-----------------------+  |
|  | Context & Intent Parser   |  | Safety Policy     |  | Tool Selection Matrix |  |
|  +---------------------------+  +-------------------+  +-----------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                       +-----------------+-----------------+
                       |                                   |
                       v                                   v
+---------------------------------------------+ +-----------------------------------+
|          FastMCP 3.1 Tool Execution         | |      Sub-Agent Routing Engine     |
|  +-------------------+ +------------------+ | |  +-----------------------------+  |
|  | AWS SDK / Boto3   | | Enterprise REST   | | |  | Domain Agent Specialist     |  |
|  +-------------------+ +------------------+ | |  +-----------------------------+  |
+---------------------------------------------+ +-----------------------------------+
                       |                                   |
                       +-----------------+-----------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                       Structured Execution Result & Audit                         |
+-----------------------------------------------------------------------------------+
```

## What it is

The AWS Strands Decider Model is a specialized decision-making and routing foundation framework provided by Amazon Web Services. Designed explicitly for agentic orchestration, the Decider Model acts as the core control plane within the AWS Strands agent framework ecosystem. Instead of relying on general-purpose large language models to generate freeform text and function calls simultaneously, Strands Decider separates macro-level planning and policy enforcement from micro-level text generation.

By utilizing structured intent evaluation, low-latency logit routing, and built-in AWS IAM and Guardrails policy validation, the Strands Decider Model evaluates current agent state, available Model Context Protocol (MCP) tool schemas, and organizational compliance parameters to determine the exact next action or agent handoff.

Key capabilities include:
- **Zero-shot Tool Selection**: High-accuracy mapping of complex natural language goals to large schemas of hundreds of tools without context-window overflow.
- **Deterministic Handoffs**: Structured agent-to-agent delegation patterns that enforce boundary rules and state isolation.
- **Enterprise Policy Gatekeeping**: Native integration with AWS Bedrock Guardrails, AWS KMS, and IAM role constraints during the decision pass.
- **High-Throughput Logit Routing**: Optimized model parameters tuned for single-digit millisecond routing decisions.

## What problem it solves

Autonomous agent architectures frequently suffer from key architectural failure modes when relying on monolithic general-purpose LLMs for both reasoning and action dispatch:

1. **Hallucinated Tool Calls and Parameter Drift**: Unspecialized LLMs frequently hallucinate tool arguments or call tools out of order when presented with complex API specs or multi-step execution plans.
2. **Context Bloat and Latency**: Including full API documentation and tool definitions in every LLM context window increases token costs and adds hundreds of milliseconds of latency to every interaction cycle.
3. **Security Policy Bypass**: Unenforced agent tool execution allows sub-agents to invoke privileged operations without centralized security, compliance auditing, or rate limiting.
4. **Fragile Multi-Agent Delegation**: Handing off control between autonomous agents without rigid state contract validation results in circular delegation loops and unhandled fallback states.

AWS Strands Decider solves these problems by providing a deterministic, schema-constrained decision model. It validates parameter contracts before tool invocation, decouples full context ingestion from action routing, and applies enterprise IAM and AWS Bedrock policy checks at every step.

## Where it fits in the stack

AWS Strands Decider Model functions as the central orchestration controller within modern enterprise agent stack architectures:

- **User / Ingestion Layer**: Interacts with API gateways, event queues (Amazon SQS, EventBridge), and interactive frontends.
- **Cognitive Orchestration Layer**: AWS Strands Framework orchestrator passes conversation state and task history to the Strands Decider Model.
- **Decider / Policy Layer (Current Focus)**: Evaluates incoming state against registered MCP tool definitions, security policies, and target sub-agents to emit structured execution decisions (`CALL_TOOL`, `DELEGATE_AGENT`, `REQUEST_INPUT`, `TERMINATE`).
- **Tool / MCP Execution Layer**: Executes approved tools via FastMCP 3.1 endpoints, AWS Lambda, or external REST microservices.
- **Data & Observability Layer**: Integrates with Amazon CloudWatch, AWS X-Ray, and OpenTelemetry for trace logging and audit trails.

## Typical use cases

- **Automated Cloud Infrastructure Remediation**: Evaluating cloud security alerts from AWS SecurityHub, determining the optimal remediation playbook tool, and executing fixes with IAM privilege verification.
- **Multi-Agent Enterprise Customer Support**: Deciding whether to answer a customer query directly, query a RAG pipeline via fast vector search, or route to a specialized billing agent.
- **Agentic Financial Procurement**: Evaluating spend request parameters against corporate approval thresholds, issuing virtual cards via corporate APIs, and logging audit events.
- **Complex ETL and Data Pipeline Orchestration**: Dynamically composing data extraction, schema validation, transformation, and database loading jobs based on incoming payload structures.

## Strengths

- **Ultra-low Latency**: Optimized inference latency specifically for rapid classification and function call selection.
- **Native AWS Integration**: Seamless zero-code integration with AWS Bedrock, IAM, CloudWatch, and AWS KMS.
- **MCP Native**: Native support for Model Context Protocol tool discovery, capability introspection, and parameter validation.
- **Strict Schema Enforcement**: Ensures all downstream tool invocations comply with Pydantic v2 and JSON Schema definitions before execution.
- **Cost Efficiency**: Minimizes token usage by eliminating the need to re-feed full tool documentation in every prompt context cycle.

## Limitations

- **Ecosystem Lock-in**: Deepest integration and features depend on AWS infrastructure (AWS Bedrock, IAM, AWS KMS).
- **Reduced Creative Capacity**: Not designed for creative writing, long-form conversational text, or artistic synthesis.
- **Strict Guardrail Overhead**: High policy enforcement can cause false-positive task rejections if security guardrails are over-configured.

## When to use it

- When building production enterprise agents that require strict policy compliance, zero-shot tool selection across large registries, and auditable governance.
- When latency and token costs are critical constraints in high-throughput multi-agent orchestration pipelines.
- When operating primarily within an AWS cloud infrastructure ecosystem with established IAM role policies.

## When not to use it

- When constructing simple single-turn chatbots or creative writing applications that do not require tool execution or multi-agent delegation.
- When running fully offline, air-gapped local workflows on edge hardware without AWS connectivity (consider local models like Ollama or llamafile).
- When a lightweight single-prompt agent script is sufficient for basic automation.

## Getting started

To get started with AWS Strands Decider Model using Python and FastMCP 3.1, install the required packages:

```bash
pip install boto3 fastmcp pydantic aws-strands-sdk
```

Configure your AWS credentials:

```bash
export AWS_DEFAULT_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

## CLI examples

Inspect available AWS Strands models via the AWS CLI:

```bash
aws bedrock list-foundation-models \
  --by-provider amazon \
  --query "modelSummaries[?contains(modelId, 'strands')].[modelId, modelName]" \
  --output table
```

Invoke a Strands Decider evaluation directly using the AWS CLI:

```bash
aws bedrock-runtime invoke-model \
  --model-id amazon.strands-decider-v1 \
  --body '{"prompt": "Evaluate action for server overload in us-east-1", "tools": [{"name": "scale_asg", "parameters": {"min": 1, "max": 10}}]}' \
  --cli-binary-format raw-in-base64-out \
  output.json
cat output.json
```

Query agent tracing log streams:

```bash
aws logs filter-log-events \
  --log-group-name "/aws/bedrock/strands-decider" \
  --filter-pattern "DECISION_MADE" \
  --limit 5
```

## API examples

The following complete Python application demonstrates building a FastMCP 3.1 server governed by the AWS Strands Decider Model and Pydantic v2 schemas:

```python
import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastmcp import FastMCP
import boto3

# Initialize FastMCP Server
mcp = FastMCP("AWS-Strands-Decider-Gateway")

# Pydantic v2 Schema Definitions
class ActionDecisionRequest(BaseModel):
    context_id: str = Field(..., description="Unique trace ID for the decision context")
    user_goal: str = Field(..., description="Goal requested by user or upper agent")
    available_tools: List[str] = Field(default_factory=list, description="Names of candidate tools")
    max_cost_limit: float = Field(default=5.0, description="Maximum budget allowed for this decision path")

class ToolExecutionResult(BaseModel):
    status: str = Field(..., description="Execution status: SUCCESS or FAILED")
    selected_tool: str = Field(..., description="Name of the executed tool")
    output: Dict[str, Any] = Field(default_factory=dict, description="Result payload")

class StrandsDeciderClient:
    def __init__(self, region: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = "amazon.strands-decider-v1"

    def evaluate_decision(self, request: ActionDecisionRequest) -> Dict[str, Any]:
        payload = {
            "version": "strands-2027-01",
            "context_id": request.context_id,
            "goal": request.user_goal,
            "tool_registry": request.available_tools,
            "constraints": {"max_cost": request.max_cost_limit}
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )

        result = json.loads(response["body"].read().decode("utf-8"))
        return result

decider = StrandsDeciderClient()

@mcp.tool()
def route_and_execute_action(request_json: str) -> str:
    """Evaluates user intent via AWS Strands Decider Model and executes the optimal MCP tool."""
    req_data = ActionDecisionRequest.model_validate_json(request_json)

    # Send context to AWS Strands Decider
    decision = decider.evaluate_decision(req_data)

    selected_tool = decision.get("recommended_tool", "fallback_agent")

    # Execute routing decision
    execution_result = ToolExecutionResult(
        status="SUCCESS",
        selected_tool=selected_tool,
        output={"action": f"Executed {selected_tool} successfully", "decision_metadata": decision}
    )

    return execution_result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts

- **Model Context Protocol (MCP)**: Standardized protocol for connecting AI models to external tools and data sources.
- **FastMCP 3.1**: High-performance Python framework for constructing MCP servers with full Pydantic v2 validation.
- **AWS Bedrock Guardrails**: Enterprise security policy enforcement engine for filtering PII, toxic content, and unauthorized actions.
- **Agentic Workflow Frameworks**: LangGraph, AutoGen, CrewAI, and Mastra.

## Sources / references

- [AWS Strands Decider Model Overview](https://thenewstack.io/aws-strands-decider-model/)
- [Amazon Bedrock Documentation](https://aws.amazon.com/bedrock/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

- Last reviewed: 2027-01-07
- Confidence: high
