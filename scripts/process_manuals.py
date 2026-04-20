#!/usr/bin/env python3
"""
Process PDF manuals for local RAG storage.
Extracts text, performs section-aware chunking, and identifies metadata (manufacturer, model).
"""

import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterSplitter
import argparse
import json
import os
import re
import sys

class ManualProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def extract_text(self, pdf_path):
        """Extracts text from a PDF file using PyMuPDF."""
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            return full_text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}", file=sys.stderr)
            return ""

    def chunk_text(self, text):
        """Chunks the extracted text using LangChain splitters."""
        if not text:
            return []
        return self.splitter.split_text(text)

    def extract_metadata_from_text(self, text):
        """Heuristic-based extraction of model and manufacturer."""
        metadata = {
            "manufacturer": "Unknown",
            "model_number": "Unknown"
        }

        # Common manufacturer patterns
        manufacturers = ["Bosch", "Samsung", "LG", "Dell", "HP", "Sony", "Philips", "Siemens", "Miele", "Whirlpool", "Dyson"]
        for m in manufacturers:
            if re.search(r'\b' + re.escape(m) + r'\b', text, re.IGNORECASE):
                metadata["manufacturer"] = m
                break

        # Heuristic for model number (often Alphanumeric with dashes/slashes)
        model_match = re.search(r'Model(?:\s+(?:No|Number))?[:\s]+([A-Z0-9\-/]{3,20})', text, re.IGNORECASE)
        if model_match:
            metadata["model_number"] = model_match.group(1).strip()

        return metadata

    def process_file(self, pdf_path):
        """Processes a single PDF manual."""
        print(f"Processing: {pdf_path}")
        text = self.extract_text(pdf_path)
        if not text:
            return None

        metadata = self.extract_metadata_from_text(text[:3000]) # Scan beginning for metadata
        chunks = self.chunk_text(text)

        return {
            "source": os.path.basename(pdf_path),
            "metadata": metadata,
            "chunk_count": len(chunks),
            "chunks": chunks
        }

def main():
    parser = argparse.ArgumentParser(description="Process PDF manuals for RAG ingestion.")
    parser.add_argument("input", help="Path to a PDF file or a directory containing PDFs.")
    parser.add_argument("--output", "-o", help="Path to save the JSON output.")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size for splitting text.")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks.")

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

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
