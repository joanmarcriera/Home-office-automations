#!/usr/bin/env python3
"""
Process PDF manuals for local RAG storage.
Extracts text, performs section-aware chunking, and identifies metadata (manufacturer, model).
Now includes ChromaDB integration and improved heading detection.
"""

import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

class ManualProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def extract_text_with_sections(self, pdf_path):
        """Extracts text and attempts to identify sections based on formatting."""
        sections = []
        current_section = {"title": "Introduction", "content": ""}

        try:
            doc = fitz.open(pdf_path)

            # Heuristic: find the most common font size to identify headings
            font_sizes = {}
            for page in doc:
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if b['type'] == 0: # text
                        for l in b["lines"]:
                            for s in l["spans"]:
                                size = round(s["size"])
                                font_sizes[size] = font_sizes.get(size, 0) + len(s["text"])

            if not font_sizes:
                return [{"title": "Document", "content": self.extract_text(pdf_path)}]

            common_size = max(font_sizes, key=font_sizes.get)

            for page in doc:
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if b['type'] == 0:
                        block_text = ""
                        is_heading = False

                        for l in b["lines"]:
                            for s in l["spans"]:
                                # Heading heuristic: larger than common size OR bold (flag 2^4 = 16 or similar depending on font)
                                # PyMuPDF flags: 2^0=superscript, 2^1=italic, 2^2=serif, 2^3=monospaced, 2^4=bold
                                if (s["size"] > common_size * 1.2) or (s["flags"] & 2**4):
                                    is_heading = True
                                block_text += s["text"] + " "

                        block_text = block_text.strip()
                        if not block_text:
                            continue

                        if is_heading and len(block_text) < 100: # Headings aren't usually long paragraphs
                            if current_section["content"].strip():
                                sections.append(current_section)
                            current_section = {"title": block_text, "content": ""}
                        else:
                            current_section["content"] += block_text + "\n"

            if current_section["content"].strip():
                sections.append(current_section)

            return sections
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}", file=sys.stderr)
            return []

    def extract_text(self, pdf_path):
        """Fallback: Extracts all text from a PDF file."""
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            return full_text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}", file=sys.stderr)
            return ""

    def chunk_sections(self, sections):
        """Chunks each section independently."""
        all_chunks = []
        for section in sections:
            if not section["content"].strip():
                continue
            chunks = self.splitter.split_text(section["content"])
            for i, chunk_text in enumerate(chunks):
                all_chunks.append({
                    "section": section["title"],
                    "chunk_index": i,
                    "text": chunk_text
                })
        return all_chunks

    def extract_metadata_from_text(self, text):
        """Heuristic-based extraction of model and manufacturer."""
        metadata = {
            "manufacturer": "Unknown",
            "model_number": "Unknown"
        }

        manufacturers = ["Bosch", "Samsung", "LG", "Dell", "HP", "Sony", "Philips", "Siemens", "Miele", "Whirlpool", "Dyson", "Apple", "Logitech"]
        for m in manufacturers:
            if re.search(r'\b' + re.escape(m) + r'\b', text, re.IGNORECASE):
                metadata["manufacturer"] = m
                break

        model_match = re.search(r'Model(?:\s+(?:No|Number))?[:\s]+([A-Z0-9\-/]{3,25})', text, re.IGNORECASE)
        if model_match:
            metadata["model_number"] = model_match.group(1).strip()

        return metadata

    def process_file(self, pdf_path):
        """Processes a single PDF manual."""
        print(f"Processing: {pdf_path}")
        sections = self.extract_text_with_sections(pdf_path)
        if not sections:
            return None

        # Sample start of document for metadata
        full_text_sample = "\n".join([s["content"] for s in sections[:3]])
        metadata = self.extract_metadata_from_text(full_text_sample[:5000])

        chunks = self.chunk_sections(sections)

        return {
            "source": os.path.basename(pdf_path),
            "metadata": metadata,
            "chunk_count": len(chunks),
            "chunks": chunks
        }

def store_in_chroma(results, db_dir, collection_name):
    if not CHROMA_AVAILABLE:
        print("Error: chromadb package not installed. Cannot store in Vector DB.", file=sys.stderr)
        return

    client = chromadb.PersistentClient(path=db_dir)
    collection = client.get_or_create_collection(name=collection_name)

    for doc in results:
        ids = []
        documents = []
        metadatas = []

        source = doc["source"]
        m_mfr = doc["metadata"]["manufacturer"]
        m_model = doc["metadata"]["model_number"]

        for i, chunk in enumerate(doc["chunks"]):
            chunk_id = f"{source}_{i}"
            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append({
                "source": source,
                "manufacturer": m_mfr,
                "model_number": m_model,
                "section": chunk["section"],
                "processed_at": datetime.now(timezone.utc).isoformat()
            })

        if ids:
            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            print(f"Stored {len(ids)} chunks from {source} into ChromaDB collection '{collection_name}'")

def main():
    parser = argparse.ArgumentParser(description="Process PDF manuals for RAG ingestion.")
    parser.add_argument("input", help="Path to a PDF file or a directory containing PDFs.")
    parser.add_argument("--output", "-o", help="Path to save the JSON output.")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size for splitting text.")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks.")
    parser.add_argument("--chroma-dir", help="Directory for ChromaDB persistent storage.")
    parser.add_argument("--collection", default="manuals", help="ChromaDB collection name.")

    args = parser.parse_args()

    processor = ManualProcessor(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    results = []

    if os.path.isfile(args.input):
        if args.input.lower().endswith(".pdf"):
            res = processor.process_file(args.input)
            if res:
                results.append(res)
    elif os.path.isdir(args.input):
        for root, _, files in os.walk(args.input):
            for file in files:
                if file.lower().endswith(".pdf"):
                    res = processor.process_file(os.path.join(root, file))
                    if res:
                        results.append(res)
    else:
        print(f"Error: Input path '{args.input}' not found.")
        sys.exit(1)

    if args.chroma_dir:
        store_in_chroma(results, args.chroma_dir, args.collection)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")
    elif not args.chroma_dir:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
