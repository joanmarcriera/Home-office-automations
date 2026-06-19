# Tesseract CLI

## What it is
Tesseract is an open-source Optical Character Recognition (OCR) engine. It can be used directly via the command line (CLI) to extract text from images and PDF files. In the 2026 AI landscape, it remains the foundation for many local-first agentic ingestion pipelines.

## What problem it solves
It converts images containing text (like scans, screenshots, or legacy documents) into machine-readable text. This is a critical component for searchable document archives, automated data extraction, and providing vision-less agents with textual context from visual sources.

## Where it fits in the stack
**Tool / Process & Understanding**. It serves as the core OCR engine for higher-level tools like OCRmyPDF, Paperless-ngx, and custom document management systems.

## Typical use cases
- Extracting text from scanned documents and images for RAG ingestion.
- Powering automated workflows that require text analysis of image-based inputs.
- Batch processing images for archival and indexing in a personal knowledge base.
- Integration into edge devices for real-time text recognition.

## Strengths
- **Language Support**: Supports over 100 languages out of the box, including script-specific models.
- **Accuracy**: Highly accurate for clean, high-resolution scans and printed text.
- **Extensibility**: Can be trained to recognize new fonts, languages, or specialized character sets.
- **Privacy**: Local execution ensures sensitive documents never leave the host machine.

## Limitations
- **Format Support**: Requires external libraries (like Leptonica) for many image formats; PDF processing is usually handled by wrappers like OCRmyPDF.
- **Complex Layouts**: Can struggle with multi-column layouts, tables, or complex formatting without significant pre-processing.
- **Handwriting**: Generally not suited for handwritten text recognition; results are often poor compared to specialized transformer models.

## When to use it
- When you need a robust, open-source, and self-hostable OCR engine for local processing.
- When you are building custom automation that needs to "read" images without cloud dependencies.
- When processing high volumes of standardized documents where speed and cost are priorities.

## When not to use it
- For complex handwritten documents (consider specialized AI models like TrOCR).
- When a higher-level wrapper like OCRmyPDF is available for PDF-specific tasks.
- For high-fidelity layout preservation (consider Docling or Unstructured).

## Getting started

### Installation
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version
```

### Installing Language Data
Additional language packs can be installed via system package managers (e.g., `tesseract-ocr-fra` for French).

## CLI examples

### Basic Text Extraction
```bash
# Extract text from an image to a text file (output_file.txt)
tesseract image.png output_file -l eng
```

### Listing Available Languages
```bash
tesseract --list-langs
```

### Direct Output to Stdout
```bash
tesseract image.png stdout -l eng
```

### Creating Searchable PDFs
```bash
tesseract input.png output pdf
```

## API examples

### Python (via pytesseract wrapper)
```python
import pytesseract
from PIL import Image

# Open an image file
img = Image.open('image.png')

# Convert image to string with custom configuration
text = pytesseract.image_to_string(img, lang='eng', config='--psm 3')
print(text)
```

## Related tools / concepts
- [OCRmyPDF](ocrmypdf.md) (Standard PDF wrapper for Tesseract)
- [Docling](docling.md) (Advanced document parsing)
- [Firecrawl](firecrawl.md) (Web-to-markdown)
- [PageIndex](pageindex.md) (Visual document indexing)
- [RAGFlow](ragflow.md) (RAG with deep document understanding)
- [Paperless-ngx](../../services/paperless-ngx.md) (DMS using Tesseract)
- [Apache Tika](../../services/tika.md) (Content extraction suite)

## Sources / references
- [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [Pytesseract Python Wrapper](https://pypi.org/project/pytesseract/)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
