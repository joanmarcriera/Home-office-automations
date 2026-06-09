#!/usr/bin/env python3
"""
Paperless-ngx Tool for Home Admin Agent
Allows the agent to search and retrieve documents from Paperless-ngx.
"""

import os
import requests
from typing import List, Optional, Dict, Any, Type
from pydantic import BaseModel, Field
from agent_models import BaseHomeTool, ToolMetadata

class PaperlessSearchArgs(BaseModel):
    query: Optional[str] = Field(None, description="Search query for document content.")
    tag_id: Optional[int] = Field(None, description="Filter by tag ID.")
    correspondent_id: Optional[int] = Field(None, description="Filter by correspondent ID.")

class PaperlessUploadArgs(BaseModel):
    file_path: str = Field(..., description="Local path to the document file to upload.")
    title: Optional[str] = Field(None, description="Optional title for the document.")
    created: Optional[str] = Field(None, description="Optional creation date in ISO 8601 format.")
    tags: Optional[List[int]] = Field(None, description="Optional list of tag IDs to apply.")
    correspondent_id: Optional[int] = Field(None, description="Optional correspondent ID.")
    document_type_id: Optional[int] = Field(None, description="Optional document type ID.")

class PaperlessSearchTool(BaseHomeTool):
    """Tool for searching documents in Paperless-ngx."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="paperless_search_tool",
            description="Searches for documents in Paperless-ngx and retrieves their content snippets.",
            args_schema=PaperlessSearchArgs,
            category="knowledge"
        )

    async def run(self, query: Optional[str] = None, tag_id: Optional[int] = None, correspondent_id: Optional[int] = None) -> str:
        api_url = os.environ.get("PAPERLESS_API_URL", "http://localhost:8000/api")
        api_token = os.environ.get("PAPERLESS_API_TOKEN")

        if not api_token:
            return "Error: PAPERLESS_API_TOKEN not set in environment."

        headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }

        params = {}
        if query:
            params["query"] = query
        if tag_id:
            params["tags__id__all"] = tag_id
        if correspondent_id:
            params["correspondent__id"] = correspondent_id

        try:
            endpoint = f"{api_url.rstrip('/')}/documents/"
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            documents = data.get("results", [])

            if not documents:
                return "No documents found matching the criteria."

            formatted_docs = []
            for doc in documents[:5]:
                title = doc.get("title")
                doc_id = doc.get("id")
                content = doc.get("content", "")
                snippet = content[:200] + "..." if len(content) > 200 else content
                formatted_docs.append(f"- {title} (ID: {doc_id})\n  Snippet: {snippet}")

            result = f"Found {len(documents)} documents. Top results:\n" + "\n\n".join(formatted_docs)
            if len(documents) > 5:
                result += f"\n... and {len(documents) - 5} more."

            return result

        except requests.exceptions.RequestException as e:
            return f"Error searching Paperless-ngx: {str(e)}"

class PaperlessUploadTool(BaseHomeTool):
    """Tool for uploading documents to Paperless-ngx."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="paperless_upload_tool",
            description="Uploads a document to Paperless-ngx.",
            args_schema=PaperlessUploadArgs,
            category="automation"
        )

    async def run(self, file_path: str, title: Optional[str] = None, created: Optional[str] = None,
                  tags: Optional[List[int]] = None, correspondent_id: Optional[int] = None,
                  document_type_id: Optional[int] = None) -> str:
        api_url = os.environ.get("PAPERLESS_API_URL", "http://localhost:8000/api")
        api_token = os.environ.get("PAPERLESS_API_TOKEN")

        if not api_token:
            return "Error: PAPERLESS_API_TOKEN not set in environment."

        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"

        headers = {
            "Authorization": f"Token {api_token}"
        }

        files = {
            "document": open(file_path, "rb")
        }

        data = {}
        if title:
            data["title"] = title
        if created:
            data["created"] = created
        if correspondent_id:
            data["correspondent"] = correspondent_id
        if document_type_id:
            data["document_type"] = document_type_id
        if tags:
            data["tags"] = tags

        try:
            endpoint = f"{api_url.rstrip('/')}/documents/post_document/"
            response = requests.post(endpoint, headers=headers, files=files, data=data, timeout=30)
            response.raise_for_status()

            return f"Document uploaded successfully. Status: {response.status_code}. Response: {response.text}"

        except requests.exceptions.RequestException as e:
            return f"Error uploading to Paperless-ngx: {str(e)}"
        finally:
            files["document"].close()

if __name__ == "__main__":
    import asyncio
    async def main():
        print("Paperless tools available:")
        print(f"- {PaperlessSearchTool.get_metadata().name}: {PaperlessSearchTool.get_metadata().description}")
        print(f"- {PaperlessUploadTool.get_metadata().name}: {PaperlessUploadTool.get_metadata().description}")
    asyncio.run(main())
