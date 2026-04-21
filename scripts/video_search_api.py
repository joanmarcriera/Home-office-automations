#!/usr/bin/env python3
"""
Video Search API Reference Implementation
Provides a FastAPI interface for searching the video collection in ChromaDB.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import os

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

app = FastAPI(title="Video Search API", description="Search interface for family video archive.")

class VideoSearchResult(BaseModel):
    id: str
    filename: str
    transcript_snippet: str
    tags: List[str]
    relevance_score: float
    processed_at: datetime
    url: Optional[str] = None

class VideoSearchResponse(BaseModel):
    query: str
    results: List[VideoSearchResult]
    total_found: int
    processing_time_ms: float

@app.get("/search", response_model=VideoSearchResponse)
async def search_videos(
    query: str = Query(..., min_length=1, description="The semantic search query."),
    limit: int = Query(5, ge=1, le=20, description="Max results to return."),
    chroma_dir: str = "./chroma_db",
    collection_name: str = "video_metadata"
):
    if not CHROMA_AVAILABLE:
        raise HTTPException(status_code=500, detail="ChromaDB package not installed on server.")

    if not os.path.exists(chroma_dir):
        # Mocking for reference purposes if DB doesn't exist
        return VideoSearchResponse(
            query=query,
            results=[
                VideoSearchResult(
                    id="mock-1",
                    filename="birthday_2024.mp4",
                    transcript_snippet="...kids playing with balloons at the birthday party...",
                    tags=["birthday", "kids"],
                    relevance_score=0.95,
                    processed_at=datetime.now(timezone.utc)
                )
            ],
            total_found=1,
            processing_time_ms=12.5
        )

    client = chromadb.PersistentClient(path=chroma_dir)
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found.")

    start_time = datetime.now()
    results = collection.query(
        query_texts=[query],
        n_results=limit
    )
    duration = (datetime.now() - start_time).total_seconds() * 1000

    video_results = []
    if results['ids']:
        for i in range(len(results['ids'][0])):
            metadata = results['metadatas'][0][i]
            video_results.append(VideoSearchResult(
                id=results['ids'][0][i],
                filename=metadata.get('filename', 'unknown'),
                transcript_snippet=results['documents'][0][i][:200] + "...",
                tags=metadata.get('tags', []),
                relevance_score=1.0 - results['distances'][0][i], # Convert distance to score
                processed_at=metadata.get('processed_at', datetime.now(timezone.utc)),
                url=metadata.get('url')
            ))

    return VideoSearchResponse(
        query=query,
        results=video_results,
        total_found=len(video_results),
        processing_time_ms=duration
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
