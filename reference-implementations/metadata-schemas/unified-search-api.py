from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timezone

class SearchSource(BaseModel):
    """Base class for search sources."""
    id: str
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None
    score: float = 0.0

class PaperlessSource(SearchSource):
    """Metadata for a Paperless-ngx document."""
    document_id: int
    created_at: datetime
    tags: List[str] = []
    correspondent: Optional[str] = None
    document_type: Optional[str] = None

class ObsidianSource(SearchSource):
    """Metadata for an Obsidian note."""
    file_path: str
    modified_at: datetime
    folder: str
    tags: List[str] = []

class AudioSource(SearchSource):
    """Metadata for an audio transcription."""
    file_id: str
    transcribed_at: datetime
    duration_seconds: float
    model_used: str
    tags: List[str] = []

class UnifiedSearchResult(BaseModel):
    """A single result in the unified search."""
    source_type: str = Field(..., description="Type of source: 'paperless', 'obsidian', or 'audio'")
    data: Union[PaperlessSource, ObsidianSource, AudioSource]
    relevance_score: float

class UnifiedSearchResponse(BaseModel):
    """The response from the unified search API."""
    query: str
    total_results: int
    results: List[UnifiedSearchResult]
    processing_time_ms: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

if __name__ == "__main__":
    # Example usage
    import json

    example_result = UnifiedSearchResult(
        source_type="paperless",
        relevance_score=0.95,
        data=PaperlessSource(
            id="p123",
            title="Washing Machine Manual",
            document_id=123,
            created_at=datetime(2023, 1, 1),
            tags=["Manual", "Appliance"],
            url="http://paperless.local/documents/123"
        )
    )

    response = UnifiedSearchResponse(
        query="washing machine repair",
        total_results=1,
        results=[example_result],
        processing_time_ms=45
    )

    print(response.json(indent=2))
