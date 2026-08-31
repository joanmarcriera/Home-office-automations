# AWS Dogwood

## What it is
AWS Dogwood is a robust policy management and safety-focused agentic framework designed to authorize, evaluate, and restrict LLM agent actions and tool calls. As of early January 2027, it fully supports the **FastMCP 3.1 Task Protocol** and is optimized for frontier reasoning models such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**. It provides an enterprise-grade mechanism to declare declarative security and access control boundaries for autonomous agents, ensuring that even if an agent operates independently, its behavior is bounded by strict, human-defined programmatic constraints.

## What problem it solves
As AI agents gain autonomous execution capabilities—such as deleting files, executing system commands, or initiating financial transactions—they become highly vulnerable to prompt injections, context poisoning, and agent hijacking. An attacker can manipulate an agent's context to execute unauthorized tool calls. AWS Dogwood solves this by intercepting agent tool call requests, evaluating them against dry-run policies and FastMCP 3.1 security bounds, and denying any actions that fall outside the defined security parameters.

## Where it fits in the stack
**Agent Security and Policy Layer**. It acts as an inline authorization gateway between the LLM agent and the host system, environment, or Model Context Protocol (FastMCP 3.1) tool servers.

## Typical use cases
- **Secure System Execution**: Preventing local system commands from deleting system-critical files or exposing private data during autonomous agent sessions.
- **Resource Boundary Enforcement**: Restricting database write permissions or cloud-infrastructure changes for developer-assist agents.
- **Human-in-the-Loop Validation**: Intercepting highly sensitive tool calls (such as sending emails, moving funds, or making API updates) to request human operator validation.
- **Prompt Injection Guardrails**: Sifting and validating user-supplied prompt inputs and MCP tool arguments before forwarding them to downstream agent components.

## Strengths
- **Declarative Policies**: Simplifies security configurations using an AWS IAM-like policy model designed for prompts, tools, and FastMCP 3.1 tasks.
- **Negligible Latency**: Implements high-performance validation layers that introduce almost zero execution lag during agent decisions.
- **Native Ecosystem Integration**: Seamlessly connects with AWS services (such as Bedrock, CloudWatch, and KMS) as well as open-source FastMCP 3.1 servers.
- **Extensible Validation Filters**: Allows custom Python validator code blocks to inspect and sanitize tool arguments before execution.

## Limitations
- **AWS Environment Reliance**: Full enterprise features require AWS credentials and access to cloud services, though local mocking is supported.
- **Complexity in Schema Definition**: Managing complex tool parameters and nested structures can result in large, difficult-to-maintain policy files.
- **Fringe Model Support**: Built-in parsers are optimized primarily for frontier models (Claude 5.6, GPT-5.6, Llama 4, DeepSeek-V4), requiring custom adapters for lesser-known open-weight models.

## When to use it
- When deploying autonomous agents in production environments with access to databases, local shell execution, or sensitive user accounts.
- When you need to satisfy strict corporate compliance and auditing standards (such as SOC2) for autonomous agent operations.
- For sandboxing and testing developer tools like Claude Code and Roo Code with real-time guardrails.

## When not to use it
- In lightweight, isolated sandboxes where agents only read static text files and have no write or execution permissions.
- When building simple proof-of-concepts with completely predefined, deterministic pipelines that do not use dynamic tool-calling.
- In resource-constrained micro-edge servers where any external AWS API dependency or cloud networking is impossible.

## Getting started
1. **Install the SDK**: Add AWS Dogwood to your project dependencies:
   ```bash
   pip install aws-dogwood-sdk
   ```
2. **Initialize the Client**: Set up your local AWS credentials and initialize Dogwood:
   ```python
   import boto3
   from aws_dogwood import DogwoodClient

   session = boto3.Session()
   dogwood = DogwoodClient(session=session)
   ```
3. **Load a Tool Policy**: Create a policy JSON and load it into your agent context:
   ```json
   {
     "Version": "2027-01-07",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "tools:execute",
         "Resource": "tools:calculator",
         "Condition": {
           "NumericLessThan": {"tools:args:value": 1000}
         }
       }
     ]
   }
   ```

## CLI examples
AWS Dogwood offers a command-line interface for policy syntax verification, tool simulation, and dry-run compliance checks.

```bash
# Validate policy syntax and verify JSON schema correctness
dogwood policy validate --file ./policies/agent-db-policy.json

# Simulate an agent tool call dry-run against a target policy
dogwood simulate --policy ./policies/agent-db-policy.json --tool "tools:delete_record" --args '{"id": 45}'

# Sync dogwood agent logs to AWS CloudWatch for real-time security auditing
dogwood audit sync --log-group "/aws/agent/dogwood" --limit 100
```

## API examples

### Python Tool-Call Validation with AWS Dogwood & Pydantic v2
This API example demonstrates how to parse and validate an incoming agent tool execution request against AWS Dogwood policies using strict **Pydantic v2** data models in early January 2027 SOTA standards.

```python
import json
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

# Define schema for the incoming tool request under FastMCP 3.1 Task Protocol
class ToolCallRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the FastMCP 3.1 tool requested by the agent")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments supplied to the tool")
    agent_id: str = Field(..., description="Unique identifier of the agent requesting the tool call")
    protocol_version: str = Field(default="FastMCP 3.1", description="FastMCP protocol version")

# Define schema for the Dogwood authorization response
class DogwoodAuthResponse(BaseModel):
    decision: Literal["Allow", "Deny"] = Field(..., description="The authorization decision from AWS Dogwood")
    matched_statement_id: str = Field(..., description="The ID of the policy statement that triggered the decision")
    rejection_reason: str = Field(default="", description="The reason for rejection, if decision is Deny")

def evaluate_dogwood_policy(request: ToolCallRequest) -> DogwoodAuthResponse:
    # Under real conditions, you would pass the serialized request to the Dogwood SDK:
    # response = dogwood_client.evaluate(request.model_dump())

    # Simulated response logic: Deny if tool is delete_file and path is critical
    if request.tool_name == "delete_file" and "etc" in request.arguments.get("path", ""):
        simulated_data = {
            "decision": "Deny",
            "matched_statement_id": "Statement-BlockSystemFiles",
            "rejection_reason": "Access to system-critical paths is blocked by AWS Dogwood policies."
        }
    else:
        simulated_data = {
            "decision": "Allow",
            "matched_statement_id": "Statement-AllowGeneralExecution",
            "rejection_reason": ""
        }

    return DogwoodAuthResponse(**simulated_data)

if __name__ == "__main__":
    # Test Allow Scenario
    safe_request = ToolCallRequest(
        tool_name="calculator",
        arguments={"x": 5, "y": 10},
        agent_id="agent-claude-5-6"
    )
    auth_safe = evaluate_dogwood_policy(safe_request)
    print(f"Safe Tool Evaluation: {auth_safe.decision} (Matched: {auth_safe.matched_statement_id})")

    # Test Deny Scenario
    risky_request = ToolCallRequest(
        tool_name="delete_file",
        arguments={"path": "/etc/resolv.conf"},
        agent_id="agent-claude-5-6"
    )
    auth_risky = evaluate_dogwood_policy(risky_request)
    print(f"Risky Tool Evaluation: {auth_risky.decision} (Matched: {auth_risky.matched_statement_id})")
    print(f"Reason: {auth_risky.rejection_reason}")
```

## Related tools / concepts
- [AWS Bedrock](../providers/aws-bedrock.md) — The cloud framework providing foundation models integrated with AWS Dogwood.
- [OpenAI Agents SDK](../frameworks/openai-agents-sdk.md) — Multi-agent orchestrator requiring strict security and validation boundaries.
- [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) — Definition framework for tools and functional skill calls.
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md) — Conceptual core pattern detailing prompt injection and tool protection.
- [n8n](../../services/n8n.md) — Self-hosted node workflow engine supporting agent policies and security configurations.
- [Home Admin Tools](../agents/home-admin-tools.md) — Suite of local agent tasks protected by access boundaries.
- [Claude Code](../development_ops/claude-code.md) — CLI coding agent that benefits from robust tool action interceptors.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The underlying protocol for standardizing tool calls and resources.

## Sources / references
- [AWS Dogwood: Policy Management and Safety Guardrails](https://thenewstack.io/aws-dogwood-agent-policies/)
- [AWS Official Security and Policy Enforcement Guidelines](https://aws.amazon.com/security/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
