# AWS Bedrock

## What it is
AWS Bedrock is a fully managed service from Amazon Web Services that makes foundational models (FMs) available through an API. It provides a single interface to access models from leading AI providers including Amazon, Anthropic, AI21 Labs, Cohere, Meta, Mistral AI, and Stability AI. In early 2027, it serves as a primary enterprise gateway for deploying models like Claude 5.1 Sonnet, [Gemma 3](../ai_knowledge/local_llms.md), and Llama 4 Maverick, featuring native integration with **AWS DynamoDB Vector Search** for real-time transactional vector storage and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) tool integration using **FastMCP 3.1**.

## System Architecture

The following flowchart illustrates AWS Bedrock's enterprise runtime architecture, including KMS encryption boundaries, IAM role enforcement, DynamoDB Vector Search retrieval, and FastMCP 3.1 agent execution:

```mermaid
flowchart TD
    subgraph Enterprise Security Boundary (AWS VPC)
        UserAgent[Client Application / FastMCP Agent] -->|TLS 1.3 / SigV4| BedrockEndpoint[AWS Bedrock Runtime Endpoint]
        BedrockEndpoint --> IAMAuth{AWS IAM & Policy Engine}
        IAMAuth -->|Access Granted| Guardrails[AWS Bedrock Guardrails & PII Redaction]
    end

    subgraph Bedrock Model Execution Layer
        Guardrails --> IngressRouter[Bedrock Model Ingress Router]
        IngressRouter -->|Claude 5.1 / Llama 4| ModelCluster[Managed Inferentia3 / NVIDIA Rubin Cluster]
        IngressRouter -->|RAG Knowledge Base| KBEngine[Bedrock Knowledge Base Engine]
    end

    subgraph Data & Vector Storage Layer
        KBEngine <-->|Hybrid Search| DynamoVector[AWS DynamoDB Vector Search]
        KBEngine <-->|Document Embeddings| S3Storage[Amazon S3 Document Bucket]
        ModelCluster <-->|KMS Customer Managed Keys| AWSKMS[AWS KMS Encryption Engine]
    end
```

### Converse API Execution Sequence

```
Client App / MCP Host               Bedrock Runtime Gateway          Guardrails & Model Engine
          |                                   |                                   |
          |---- 1. Converse Request --------->|                                   |
          |     (Messages + InferenceConfig)  |---- 2. IAM SigV4 Authentication ->|
          |                                   |---- 3. PII & Safety Scan -------->|
          |                                   |                                   |
          |                                   |<--- 4. Stream Tokens -------------|
          |<--- 5. Return Converse Response --|
```

## AWS Bedrock Provider Comparison Matrix

| Provider / Service | Hosted Models | Latency SLA | Private Link Support | Custom Fine-Tuning | Target Enterprise Tier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AWS Bedrock** | Claude 5.1, Llama 4, Nova, Command R+ | <150ms TTFT | Native VPC Endpoints | Continual Pre-training / Fine-Tuning | Global Enterprise / Fortune 500 |
| **Azure OpenAI** | GPT-5.5, GPT-5.6, O3 | <180ms TTFT | Private Endpoints | Fine-Tuning / Hyper-tuning | Microsoft Enterprise Ecosystem |
| **Google Cloud Vertex AI**| Gemini 4.0 Pro, PaLM 2 | <160ms TTFT | PSC (Private Service Connect) | Adapter / LoRA Tuning | GCP Enterprise Ecosystem |
| **Self-Hosted vLLM / K3s**| Any Open Weights | Variable (<80ms) | Internal Mesh Overlay | Full Unsloth / Axolotl Fine-Tuning| Private Homelab / Sovereignty |

## What problem it solves
It simplifies the process of building and scaling generative AI applications by removing the need to manage underlying infrastructure. It provides a unified API for multiple models, along with tools for fine-tuning, RAG (Knowledge Bases for Amazon Bedrock), and agentic workflows (Agents for Amazon Bedrock). It addresses enterprise concerns regarding data privacy, security, and high-performance execution on next-generation hardware.

## Where it fits in the stack
**Provider / Infrastructure**. It serves as an enterprise-grade gateway and orchestration layer for high-performance LLMs, often paired with [Docker](../infrastructure/docker.md) for specialized containerized deployments.

## Typical use cases
- **Enterprise AI Applications**: Building secure, scalable AI solutions within the AWS ecosystem.
- **Retrieval-Augmented Generation (RAG)**: Using "Knowledge Bases for Amazon Bedrock" and AWS DynamoDB Vector Search to connect models to low-latency transactional vector data and S3 assets.
- **Agentic Workflows**: Deploying autonomous agents that leverage the **FastMCP 3.1** Task Protocol to execute multi-step tasks across AWS resources.
- **Hardware-Accelerated Inference**: Utilizing NVIDIA Rubin GPUs for ultra-low latency inference of frontier models.

## Strengths
- **Enterprise-Grade Security**: Strong data privacy and compliance features (HIPAA, GDPR, SOC2, FedRAMP High). Data is never used to train or refine underlying foundation models.
- **Model Variety & Agility**: Direct unified access to [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1 Sonnet, Llama 4 Maverick, and Amazon Nova through a standardized endpoint contract.
- **NVIDIA Rubin Acceleration**: Hardware-optimized infrastructure configurations delivering industry-leading time-to-first-token (TTFT) metrics.
- **Native AWS Ecosystem Integration**: Direct integration with S3, DynamoDB Vector Search, AWS Lambda, IAM, KMS, and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) gateways.
- **Managed RAG Pipelines**: Automated vectorization, hybrid chunking, and similarity retrieval via Knowledge Bases for Amazon Bedrock.

## Limitations
- **AWS Cloud Dependency**: Deep coupling with AWS IAM, KMS, and CloudWatch can increase lock-in and complicate multi-cloud portability.
- **Regional Model Allocation Limits**: Enterprise models (e.g., high-context Claude Sonnet variants) may experience regional quota caps or capacity restrictions during peak surges.
- **Cost Accumulation at High Scale**: Deep context windows (>100k tokens) and streaming converse calls incur cumulative API costs compared to fixed self-hosted GPU infrastructure.

## When to use it
- When your architecture is heavily invested in AWS and requires strict compliance frameworks (HIPAA, SOC2, FedRAMP).
- When you require serverless access to multi-vendor state-of-the-art models without managing physical GPU hardware clusters.
- When building automated RAG pipelines connected directly to enterprise S3 buckets and transactional DynamoDB tables.

## When not to use it
- For strict local-only or fully offline sovereign home lab deployments (use [Ollama](../../services/ollama.md) or [LiteLLM](../../services/litellm.md)).
- If your primary requirement is complete control over low-level CUDA kernels or open-weights model fine-tuning.

## Getting started

### Installation & AWS CLI Setup
Install the AWS SDK (`boto3`) and Pydantic v2:
```bash
pip install boto3 pydantic mcp
```

### AWS CLI Model Access Verification
```bash
# List available foundation models in us-east-1
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?providerName=='Anthropic'].modelId"
```

## CLI examples

```bash
# Invoke Claude Sonnet model directly using AWS CLI converse
aws bedrock-runtime converse \
    --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
    --messages '[{"role": "user", "content": [{"text": "Summarize AWS Bedrock features."}]}]' \
    --region us-east-1

# Check provisioned throughput model capacity
aws bedrock list-provisioned-model-throughputs --region us-east-1
```

## FastMCP 3.1 Server & Pydantic v2 AWS Bedrock Gateway

The following Python script implements a complete FastMCP 3.1 server that interfaces with AWS Bedrock Runtime, utilizing Pydantic v2 schemas for strict request/response validation:

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Server Tool for AWS Bedrock Runtime Converse Operations
"""

import sys
import json
import boto3
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("aws-bedrock-gateway-server", version="1.4.0")

class BedrockInvokeConfig(BaseModel):
    """Pydantic v2 validation schema for AWS Bedrock model invocation requests."""
    model_id: str = Field(..., description="Target AWS Bedrock model ID (e.g. anthropic.claude-3-5-sonnet-20241022-v2:0).")
    prompt: str = Field(..., min_length=5, description="Input query prompt.")
    max_tokens: int = Field(default=512, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)

    @field_validator("model_id")
    @classmethod
    def validate_model_prefix(cls, v: str) -> str:
        valid_prefixes = ("anthropic.", "meta.", "amazon.", "cohere.", "mistral.")
        if not any(v.startswith(p) for p in valid_prefixes):
            raise ValueError(f"model_id must start with one of {valid_prefixes}")
        return v

class BedrockOutputPayload(BaseModel):
    """Validated response payload returned from Bedrock Runtime."""
    model_id: str
    completion_text: str
    input_token_count: int = Field(..., ge=0)
    output_token_count: int = Field(..., ge=0)
    stop_reason: str

@mcp.tool()
def invoke_bedrock_model(req_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Validates parameters and executes an AWS Bedrock converse invocation."""
    try:
        config = BedrockInvokeConfig.model_validate(req_dict)

        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        response = client.converse(
            modelId=config.model_id,
            messages=[{"role": "user", "content": [{"text": config.prompt}]}],
            inferenceConfig={
                "maxTokens": config.max_tokens,
                "temperature": config.temperature,
                "topP": config.top_p
            }
        )

        content_list = response.get("output", {}).get("message", {}).get("content", [])
        completion_text = content_list[0].get("text", "") if content_list else ""
        usage = response.get("usage", {})

        output = BedrockOutputPayload(
            model_id=config.model_id,
            completion_text=completion_text,
            input_token_count=usage.get("inputTokens", 0),
            output_token_count=usage.get("outputTokens", 0),
            stop_reason=response.get("stopReason", "end_turn")
        )

        return {
            "success": True,
            "data": output.model_dump()
        }
    except ValidationError as e:
        return {
            "success": False,
            "error": e.errors()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

## API examples

```python
# Programmatic AWS Bedrock Runtime invocation using boto3
import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.converse(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    messages=[{"role": "user", "content": [{"text": "Hello AWS Bedrock"}]}],
    inferenceConfig={"maxTokens": 200, "temperature": 0.5}
)

print("Bedrock Output:", response["output"]["message"]["content"][0]["text"])
```

## Production Systemd Gateway Service Unit (`aws-bedrock-gateway.service`)

Deploying the Bedrock FastMCP gateway daemon on Linux enterprise systems:

```ini
[Unit]
Description=AWS Bedrock FastMCP Gateway & Converse Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=bedrock-runner
Group=bedrock-runner
WorkingDirectory=/opt/aws-bedrock-gateway
Environment=AWS_DEFAULT_REGION=us-east-1
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 /opt/aws-bedrock-gateway/bedrock_mcp_server.py
Restart=always
RestartSec=5s
LimitNOFILE=65536
CapabilityBoundingSet=
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/aws-bedrock-gateway

[Install]
WantedBy=multi-user.target
```

## Operational Safety & IAM Hardening

1. **Least-Privilege IAM Policy Enforcement**:
   - Limit `bedrock:InvokeModel` permissions strictly to approved ARNs (e.g., `arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude*`).
   - Use condition keys like `aws:PrincipalTag` to prevent unauthorized cross-department model access.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockLeastPrivilegeInvoke",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-*"
    }
  ]
}
```

2. **Data Guardrails & Safety Filters**:
   - Attach AWS Bedrock Guardrails to all public endpoint invocations to automatically censor PII (SSN, credit cards) and block prompt injection attempts before hitting foundation models.

3. **VPC Endpoint Network Isolation**:
   - Route all Bedrock API calls inside AWS VPCs via AWS PrivateLink (`com.amazonaws.region.bedrock-runtime`). Avoid routing model inference over public internet gateways.

## Systematic Troubleshooting Guide

| Issue Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **`AccessDeniedException` on InvokeModel** | Model access not requested or IAM role lacks permissions | `aws bedrock get-foundation-model-availability --model-identifier <ID>` | Request model access in AWS Bedrock Console under "Model Access" tab |
| **`ThrottlingException` (429 Rate Limit)** | Exceeded Provisioned Throughput or account TPM limit | `aws cloudwatch get-metric-statistics --namespace AWS/Bedrock` | Implement exponential backoff retries or purchase Provisioned Throughput |
| **`ValidationException` in Knowledge Base Search** | Vector index dimension mismatch in DynamoDB / OpenSearch | Check DynamoDB Vector Search index configuration | Re-create vector index matching embedding model dimensions (e.g. 1536 for Titan) |
| **High Latency on First Token (TTFT)** | Cold start on rarely used custom fine-tuned model | Inspect CloudWatch `InvocationLatency` metric | Warm model via scheduled ping lambda or switch to standard foundation model |

## Related tools / concepts
- [Anthropic](../providers/anthropic.md) — Creator of Claude models hosted on Bedrock.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Tool integration standard.
- [Docker](../infrastructure/docker.md) — For containerizing agentic workloads calling Bedrock.
- [DynamoDB Vector Search](../infrastructure/docker.md) — Transactional vector storage integration.

## Sources / References
- [AWS Bedrock Official Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)
- [Boto3 Bedrock Runtime Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
