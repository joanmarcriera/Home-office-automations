# OCRmyPDF

## What it is
OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched. It uses the Tesseract OCR engine and is highly configurable for various languages and document types.

## What problem it solves
Makes scanned PDF documents searchable and indexable by adding a hidden text layer, which is essential for document management systems like Paperless-ngx.

## Where it fits in the stack
**Infrastructure**. Serves as the OCR processing layer for the document management pipeline, typically used alongside Paperless-ngx.

## Typical use cases
- Adding searchable text layers to scanned PDFs for Paperless-ngx ingestion
- Batch processing scanned documents for archival and indexing
- Preparing documents for full-text search in document management systems

## Strengths
- Produces high-quality OCR output using the Tesseract engine
- Supports multiple languages and configurable processing options
- Preserves the original PDF structure while adding the text layer

## Limitations
- OCR quality depends on scan quality and document complexity
- Processing large batches can be CPU-intensive
- Tesseract may struggle with handwritten text or unusual fonts

## When to use it
- When you need to make scanned PDFs searchable in a document management system
- When batch-processing scanned documents for archival

## When not to use it
- When documents are already digital-native PDFs with embedded text
- When you need OCR for non-PDF formats (use Tesseract directly or other tools)

## Related tools / concepts
- [Tesseract CLI](https://github.com/tesseract-ocr/tesseract)
- [Amazon Textract](https://aws.amazon.com/textract/)

## Sources / references
- [GitHub Repository](https://github.com/ocrmypdf/OCRmyPDF)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
