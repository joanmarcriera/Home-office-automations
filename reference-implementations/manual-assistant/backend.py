from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
from datetime import datetime, timezone

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

app = FastAPI(title="Manual Assistant Troubleshooting Backend")

class QueryRequest(BaseModel):
    query: str
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    top_k: int = 5

class SearchResult(BaseModel):
    text: str
    metadata: Dict[str, Any]
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SearchResult]

# Mock Vector DB initialization
def get_chroma_client():
    db_dir = os.environ.get("CHROMA_DB_DIR", "./chroma_db")
    if not CHROMA_AVAILABLE:
        return None
    return chromadb.PersistentClient(path=db_dir)

@app.get("/health")
async def health_check():
    return {"status": "ok", "chroma_available": CHROMA_AVAILABLE}

@app.post("/ask", response_model=ChatResponse)
async def ask_manual(request: QueryRequest):
    """
    Performs hybrid search (vector + simple keyword filter) and returns an answer.
    In a real implementation, this would call an LLM with the retrieved context.
    """
    if not CHROMA_AVAILABLE:
        raise HTTPException(status_code=500, detail="ChromaDB not available")

    client = get_chroma_client()
    collection_name = os.environ.get("CHROMA_COLLECTION", "manuals")

    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")

    # Construct metadata filter if provided
    where_clause = {}
    if request.manufacturer:
        where_clause["manufacturer"] = request.manufacturer
    if request.model_number:
        where_clause["model_number"] = request.model_number

    # Vector Search
    results = collection.query(
        query_texts=[request.query],
        n_results=request.top_k,
        where=where_clause if where_clause else None
    )

    search_results = []
    if results['documents']:
        for i in range(len(results['documents'][0])):
            search_results.append(SearchResult(
                text=results['documents'][0][i],
                metadata=results['metadatas'][0][i],
                score=results['distances'][0][i] if 'distances' in results else 0.0
            ))

    # Hybrid logic: If keyword search was needed, we would implement it here
    # and merge with vector results. For now, we rely on Chroma's vector search.

    # LLM Orchestration Mock
    # context = "\n---\n".join([r.text for r in search_results])
    # answer = call_llm(system_prompt, f"Context: {context}\n\nQuestion: {request.query}")

    answer = f"Based on the retrieved {len(search_results)} sections from the manual, here is the information for '{request.query}'..."
    if not search_results:
        answer = "I couldn't find any relevant information in the manuals for your query."

    return ChatResponse(
        answer=answer,
        sources=search_results
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
