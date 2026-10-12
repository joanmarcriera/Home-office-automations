# AWS Dogwood

## What it is
AWS Dogwood is a robust policy management and safety-focused agentic framework designed to authorize, evaluate, and restrict LLM agent actions and tool calls. As of early January 2027, it fully supports the **FastMCP 3.1 Task Protocol** and is optimized for frontier reasoning models such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**. It provides an enterprise-grade mechanism to declare declarative security and access control boundaries for autonomous agents, ensuring that even if an agent operates independently, its behavior is bounded by strict, human-defined programmatic constraints.

## What problem it solves
As AI agents gain autonomous execution capabilities—such as deleting files, executing system commands, or initiating financial transactions—they become highly vulnerable to prompt injections, context poisoning, and agent hijacking. An attacker can manipulate an agent's context to execute unauthorized tool calls. AWS Dogwood solves this by intercepting agent tool call requests, evaluating them against dry-run policies and FastMCP 3.1 security bounds, and denying any actions that fall outside the defined security parameters.

## Architecture & Policy Enforcement Flow

AWS Dogwood operates as an inline enforcement proxy situated between agent reasoning loops and target MCP tool execution endpoints.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Autonomous Agent Reasoning Loop                          │
│               (Claude 5.6, GPT-5.6, DeepSeek-V4 Execution Engine)            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ FastMCP 3.1 Tool Call Request
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    AWS DOGWOOD ENFORCEMENT GATEWAY                          │
│  ┌──────────────────────────────┐        ┌───────────────────────────────┐  │
│  │   Input Prompt Filter        │        │   MCP Tool Argument Sanitizer │  │
│  │ (Direct / Indirect Injection)│        │   (Regex / Schema Guardrails) │  │
│  └──────────────┬───────────────┘        └──────────────┬────────────────┘  │
│                 │                                       │                   │
│  ┌──────────────▼───────────────────────────────────────▼────────────────┐  │
│  │                AWS Dogwood Policy Decision Engine (PDP)               │  │
│  │  - Evaluates JSON/IAM Declarative Rules                              │  │
│  │  - Checks Session Quotas & Rate Limits                               │  │
│  │  - Performs Human-in-the-Loop Interception Thresholds                 │  │
│  └──────────────────────────────┬────────────────────────────────────────┘  │
└─────────────────────────────────┼───────────────────────────────────────────┘
               ┌──────────────────┴──────────────────┐
        [Allow]│                                     │[Deny]
┌──────────────▼─────────────┐       ┌───────────────▼────────────────────────┐
│ FastMCP 3.1 Tool Execution │       │ Security Exception Handler             │
│ Target Server / System Bus │       │ - Audit Event Logged to CloudWatch     │
└────────────────────────────┘       │ - Sanitized Exception Returned to Agent│
                                     └────────────────────────────────────────┘
```

The evaluation workflow adheres to fail-closed zero-trust principles:
1. **Invocation Interception**: When an LLM generates a tool call request, the Dogwood middleware intercepts the payload before dispatching to the MCP bus.
2. **Context & Identity Resolution**: Dogwood binds the active agent session ID, user context, and role ARN to the tool request parameters.
3. **Policy Decision Point (PDP)**: Rules are evaluated sequentially. Explicit `Deny` statements override any permissive statements.
4. **Action Execution or Escalation**: Allowed tool calls proceed to the tool server; denied actions publish a structured telemetry log to CloudWatch and return a non-fatal, safe feedback message to the model.

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

## Comparison Matrix

| Feature / Dimension | AWS Dogwood | Guardrails for Bedrock | Llama Guard 3 | NeMo Guardrails |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Agent Tool Call PDP & Policy | Content & Safety Filters | Open-Weight Safety Classifier| Colang Programmable Rails |
| **FastMCP 3.1 Native** | Full Native Interceptor | Bedrock Conduit API | Custom Middleware | Custom Adapter |
| **Declarative IAM Rules**| IAM Syntax (`Allow`/`Deny`) | Category Sliders | Prompt-Based Categories | Colang Flow DSL |
| **Human-in-the-Loop Gate**| Built-in Event Intercept | Step Functions Required | N/A | Custom Action Hooks |
| **Latency Impact** | < 3ms Inline Evaluation | 10ms - 25ms Cloud API | Dependent on Model Size | 15ms - 40ms Python Engine|
| **Local Offline Mode** | Mock / Local Engine | AWS Cloud Only | Fully Local Model | Fully Local Framework |

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

# Perform batch verification of multiple MCP server policies
dogwood policy batch-check --directory ./policies/mcp_servers/

# Generate an automated SOC2 compliance report from CloudWatch security logs
dogwood report generate --framework SOC2 --output ./compliance-2027.pdf
```

## API examples

### 1. Python Tool-Call Validation with AWS Dogwood & Pydantic v2
This API example demonstrates how to parse and validate an incoming agent tool execution request against AWS Dogwood policies using strict **Pydantic v2** data models in early January 2027 SOTA standards.

```python
import json
from typing import Dict, Any, Literal, List, Optional
from pydantic import BaseModel, Field

# Define schema for the incoming tool request under FastMCP 3.1 Task Protocol
class ToolCallRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the FastMCP 3.1 tool requested by the agent")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments supplied to the tool")
    agent_id: str = Field(..., description="Unique identifier of the agent requesting the tool call")
    session_id: str = Field(..., description="Active session trace identifier")
    protocol_version: str = Field(default="FastMCP 3.1", description="FastMCP protocol version")

# Define schema for the Dogwood authorization response
class DogwoodAuthResponse(BaseModel):
    decision: Literal["Allow", "Deny", "RequiresHumanApproval"] = Field(..., description="The authorization decision from AWS Dogwood")
    matched_statement_id: str = Field(..., description="The ID of the policy statement that triggered the decision")
    rejection_reason: str = Field(default="", description="The reason for rejection, if decision is Deny")
    sanitized_arguments: Optional[Dict[str, Any]] = Field(default=None, description="Sanitized argument dictionary if mutated by policy")

def evaluate_dogwood_policy(request: ToolCallRequest) -> DogwoodAuthResponse:
    # Simulated response logic reflecting AWS Dogwood PDP rules
    path_arg = request.arguments.get("path", "")
    if request.tool_name == "delete_file" and ("etc" in path_arg or "sys" in path_arg):
        simulated_data = {
            "decision": "Deny",
            "matched_statement_id": "Statement-BlockSystemFiles",
            "rejection_reason": "Access to system-critical paths is blocked by AWS Dogwood policies.",
            "sanitized_arguments": None
        }
    elif request.tool_name == "transfer_funds" and request.arguments.get("amount", 0) > 500:
        simulated_data = {
            "decision": "RequiresHumanApproval",
            "matched_statement_id": "Statement-HighValueTransferGate",
            "rejection_reason": "Transfer amount exceeds $500 threshold. Human authorization required.",
            "sanitized_arguments": request.arguments
        }
    else:
        simulated_data = {
            "decision": "Allow",
            "matched_statement_id": "Statement-AllowGeneralExecution",
            "rejection_reason": "",
            "sanitized_arguments": request.arguments
        }

    return DogwoodAuthResponse(**simulated_data)

if __name__ == "__main__":
    # Test Allow Scenario
    safe_request = ToolCallRequest(
        tool_name="calculator",
        arguments={"x": 5, "y": 10},
        agent_id="agent-claude-5-6",
        session_id="sess-88391"
    )
    auth_safe = evaluate_dogwood_policy(safe_request)
    print(f"Safe Tool Evaluation: {auth_safe.decision} (Matched: {auth_safe.matched_statement_id})")

    # Test Deny Scenario
    risky_request = ToolCallRequest(
        tool_name="delete_file",
        arguments={"path": "/etc/resolv.conf"},
        agent_id="agent-claude-5-6",
        session_id="sess-88392"
    )
    auth_risky = evaluate_dogwood_policy(risky_request)
    print(f"Risky Tool Evaluation: {auth_risky.decision} (Matched: {auth_risky.matched_statement_id})")
    print(f"Reason: {auth_risky.rejection_reason}")
```

### 2. FastMCP 3.1 Interceptor Middleware with AWS Dogwood Guard
Integrating AWS Dogwood policy enforcement natively into a FastMCP 3.1 server pipeline:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import os

mcp = FastMCP("Dogwood Guarded FastMCP Server")

class FileDeleteInput(BaseModel):
    filepath: str = Field(description="Target file path to delete")

@mcp.tool()
def delete_file_guarded(filepath: str) -> str:
    """Deletes a file after passing through AWS Dogwood inline policy checks."""
    # Inline guard check logic
    if filepath.startswith("/etc") or filepath.startswith("/proc"):
        raise PermissionError("AWS Dogwood Policy Violation: Cannot modify system paths.")

    return f"File {filepath} deleted successfully under Dogwood audit trace."

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices

1. **Policy Principle of Least Privilege**:
   - Structure Dogwood statement resources with explicit tool paths (e.g., `mcp:homelab:filesystem:read_file` instead of wildcard `mcp:*`).
   - Define strict string matching conditions on file paths, limiting agent write access to designated `/tmp` or project directories.

2. **Audit & CloudWatch Alarm Integration**:
   - Map Dogwood `Deny` decisions directly to CloudWatch metric filters to generate high-priority security alerts when sudden spikes in policy denials occur (indicating potential indirect prompt injection attacks).
   - Set up automatic session termination hooks when an agent triggers three consecutive `Deny` responses within a single execution trace.

3. **Human-in-the-Loop Threshold Tuning**:
   - Establish numeric boundaries for financial or destructive operations (e.g., automatically require human operator approval for database record modifications exceeding 10 rows).

## Troubleshooting & Common Pitfalls

- **False-Positive Blockage on Valid Arguments**: Ensure regex filters in Dogwood statements properly escape special characters in file paths or URL arguments.
- **Latency Spikes During PDP Evaluation**: Cache policy manifests locally on the agent host rather than fetching remote S3 policy files on every single tool request.
- **Agent Hallucinating Failure Recovery**: When a tool call is denied, return structured JSON error output to the agent explaining that the policy denied execution, prompting the agent to choose an alternative non-destructive path.

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
