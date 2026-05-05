# Tesseract CLI

## What it is
Tesseract is an open-source Optical Character Recognition (OCR) engine. It can be used directly via the command line (CLI) to extract text from images and PDF files.

## What problem it solves
It converts images containing text (like scans or screenshots) into machine-readable text. This is a critical component for searchable document archives and automated data extraction.

## Where it fits in the stack
**Tool / Process & Understanding**. It serves as the core OCR engine for higher-level tools like OCRmyPDF and document management systems.

## Typical use cases
- Extracting text from scanned documents and images.
- Powering automated workflows that require text analysis of image-based inputs.
- Batch processing images for archival and indexing.

## Strengths
- **Language Support**: Supports over 100 languages out of the box.
- **Accuracy**: Highly accurate for clean, high-resolution scans.
- **Extensibility**: Can be trained to recognize new fonts or languages.

## Limitations
- **Format Support**: Requires external tools (like Leptonica) for many image formats and PDF processing (often handled by wrappers like OCRmyPDF).
- **Complex Layouts**: Can struggle with multi-column layouts or complex formatting without pre-processing.
- **Handwriting**: Generally not suited for handwritten text recognition.

## When to use it
- When you need a robust, open-source OCR engine for local processing.
- When you are building custom automation that needs to "read" images.

## When not to use it
- For handwritten documents (consider specialized AI models).
- When a higher-level wrapper like OCRmyPDF is available for PDF-specific tasks.

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

## CLI examples
```bash
# Extract text from an image to a text file (output_file.txt)
tesseract image.png output_file -l eng

# List available/installed languages
tesseract --list-langs

# Extract text from an image and output to standard output (stdout)
tesseract image.png stdout -l eng
```

## API examples

### Python (via pytesseract wrapper)
```python
import pytesseract
from PIL import Image

# Open an image file
img = Image.open('image.png')

# Convert image to string
text = pytesseract.image_to_string(img, lang='eng')
print(text)
```

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [OCRmyPDF](ocrmypdf.md)
- [Docling](docling.md)
- [Firecrawl](firecrawl.md)
- [PageIndex](pageindex.md)
- [RAGFlow](ragflow.md)

## Sources / References
- [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Documentation](https://tesseract-ocr.github.io/)

## Contribution Metadata
- Last reviewed: 2026-05-27
- Confidence: high
