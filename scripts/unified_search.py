#!/usr/bin/env python3
"""
Unified Search CLI
Performs cross-source (Paperless + Obsidian) search.
Includes keyword-based ranking (BM25) for Paperless-ngx results.
"""

import os
import json
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

try:
    from pydantic import BaseModel, Field
    from rank_bm25 import BM25Okapi
except ImportError:
    print("Error: Required packages 'pydantic' and 'rank-bm25' not installed.")
    import sys
    sys.exit(1)

# Import schemas from reference implementation
# Instead of actual import which might fail due to pathing in sandbox, we define them here
# based on docs/reference-implementations/metadata-schemas/unified-search-api.py

class SearchSource(BaseModel):
    id: str
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None
    score: float = 0.0

class PaperlessSource(SearchSource):
    document_id: int
    created_at: datetime
    tags: List[str] = []
    correspondent: Optional[str] = None
    document_type: Optional[str] = None

class ObsidianSource(SearchSource):
    file_path: str
    modified_at: datetime
    folder: str
    tags: List[str] = []

class AudioSource(SearchSource):
    file_id: str
    transcribed_at: datetime
    duration_seconds: float
    model_used: str
    tags: List[str] = []

class UnifiedSearchResult(BaseModel):
    source_type: str
    data: Any # Union[PaperlessSource, ObsidianSource, AudioSource]
    relevance_score: float

class UnifiedSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[UnifiedSearchResult]
    processing_time_ms: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def load_paperless_data(export_dir: str) -> List[Dict[str, Any]]:
    """Loads exported Paperless text files for BM25 indexing."""
    export_path = Path(export_dir)
    if not export_path.exists():
        return []

    documents = []
    for txt_file in export_path.glob("*.txt"):
        try:
            # Expected filename format: {id}_{safe_title}.txt
            name_parts = txt_file.stem.split("_", 1)
            doc_id = int(name_parts[0])
            title = name_parts[1].replace("_", " ") if len(name_parts) > 1 else txt_file.stem

            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read()

            documents.append({
                "id": str(doc_id),
                "title": title,
                "content": content,
                "document_id": doc_id,
                "created_at": datetime.fromtimestamp(txt_file.stat().st_mtime, tz=timezone.utc)
            })
        except Exception:
            continue
    return documents

def search_paperless(query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[UnifiedSearchResult]:
    if not documents:
        return []

    tokenized_query = query.lower().split()
    corpus = [doc["content"].lower().split() for doc in documents]
    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(tokenized_query)

    results = []
    for i, score in enumerate(scores):
        if score != 0:
            doc = documents[i]
            # Create snippet (first 200 chars)
            snippet = doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"]

            p_source = PaperlessSource(
                id=doc["id"],
                title=doc["title"],
                url=f"http://paperless.local/documents/{doc['document_id']}",
                snippet=snippet,
                score=float(score),
                document_id=doc["document_id"],
                created_at=doc["created_at"],
                tags=[]
            )

            results.append(UnifiedSearchResult(
                source_type="paperless",
                data=p_source,
                relevance_score=float(score)
            ))

    # Sort by score descending
    results.sort(key=lambda x: x.relevance_score, reverse=True)
    return results[:top_k]

def search_obsidian_mock(query: str, top_k: int = 5) -> List[UnifiedSearchResult]:
    """Mock for Obsidian vector search."""
    # In a real implementation, this would query a vector database like ChromaDB
    # containing indexed Obsidian notes.
    return []

def load_audio_data(export_dir: str) -> List[Dict[str, Any]]:
    """Loads transcription JSON files for BM25 indexing."""
    export_path = Path(export_dir)
    if not export_path.exists():
        return []

    documents = []
    for json_file in export_path.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "full_text" in data:
                documents.append({
                    "id": data["file_id"],
                    "title": data.get("title", data["file_id"]),
                    "content": data["full_text"],
                    "file_id": data["file_id"],
                    "transcribed_at": datetime.fromisoformat(data["transcribed_at"].replace("Z", "+00:00")),
                    "duration_seconds": data["duration_seconds"],
                    "model_used": data["model_used"],
                    "tags": data.get("tags", [])
                })
        except Exception:
            continue
    return documents

def search_audio(query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[UnifiedSearchResult]:
    if not documents:
        return []

    tokenized_query = query.lower().split()
    corpus = [doc["content"].lower().split() for doc in documents]
    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(tokenized_query)

    results = []
    for i, score in enumerate(scores):
        if score != 0:
            doc = documents[i]
            snippet = doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"]

            a_source = AudioSource(
                id=doc["id"],
                title=doc["title"],
                url=f"nfs://nas/audio/{doc['file_id']}",
                snippet=snippet,
                score=float(score),
                file_id=doc["file_id"],
                transcribed_at=doc["transcribed_at"],
                duration_seconds=doc["duration_seconds"],
                model_used=doc["model_used"],
                tags=doc["tags"]
            )

            results.append(UnifiedSearchResult(
                source_type="audio",
                data=a_source,
                relevance_score=float(score)
            ))

    results.sort(key=lambda x: x.relevance_score, reverse=True)
    return results[:top_k]

def main():
    parser = argparse.ArgumentParser(description="Unified Search across Paperless, Obsidian, and Audio.")
    parser.add_argument("query", help="Search query.")
    parser.add_argument("--paperless-dir", default="./paperless_export", help="Directory with Paperless TXT exports.")
    parser.add_argument("--audio-dir", default="./audio_transcripts", help="Directory with audio transcription JSONs.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return.")
    parser.add_argument("--json", action="store_true", help="Output results as JSON.")

    args = parser.parse_args()

    start_time = time.time()

    # 1. Search Paperless
    paperless_docs = load_paperless_data(args.paperless_dir)
    paperless_results = search_paperless(args.query, paperless_docs, top_k=args.top_k)

    # 2. Search Obsidian (Mock for now)
    obsidian_results = search_obsidian_mock(args.query, top_k=args.top_k)

    # 3. Search Audio
    audio_docs = load_audio_data(args.audio_dir)
    audio_results = search_audio(args.query, audio_docs, top_k=args.top_k)

    # Combine results
    all_results = paperless_results + obsidian_results + audio_results
    all_results.sort(key=lambda x: x.relevance_score, reverse=True)
    final_results = all_results[:args.top_k]

    processing_time = int((time.time() - start_time) * 1000)

    response = UnifiedSearchResponse(
        query=args.query,
        total_results=len(final_results),
        results=final_results,
        processing_time_ms=processing_time
    )

    if args.json:
        print(response.model_dump_json(indent=2))
    else:
        print(f"Results for '{args.query}' ({len(final_results)} found in {processing_time}ms):")
        for res in final_results:
            source = res.data
            print(f"--- [{res.source_type.upper()}] {source.title} (Score: {res.relevance_score:.2f}) ---")
            if source.snippet:
                print(f"Snippet: {source.snippet}")
            if hasattr(source, 'url') and source.url:
                print(f"Link: {source.url}")
            print()

if __name__ == "__main__":
    main()
