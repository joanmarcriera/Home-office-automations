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

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [OCRmyPDF](ocrmypdf.md)
- [Docling](docling.md)
- [Amazon Textract](https://aws.amazon.com/textract/)

## Sources / References
- [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Documentation](https://tesseract-ocr.github.io/)

## Contribution Metadata
- Last reviewed: 2026-04-06
- Confidence: high
