# Document Organization and Summarization System

A robust AI-powered pipeline that scans directories, processes various document formats, generates intelligent summaries, and organizes files into an optimized folder structure using Google's Gemini AI.

## 📁 Repository Structure

```
.
├── summarygenerator.py        # Scans directories, extracts metadata, and generates summaries
├── fileorganizer.py           # AI-driven file organization with JSON plans and ASCII file trees
├── llm_input.json             # Generated metadata and summaries for AI analysis
├── processed_documents.json   # Full processing results with embeddings
└── README.md                  # This file
```

## ✨ Features

- **Multi-Format Support**: Processes PDF, DOCX, PPTX, XLSX, HTML, Markdown, and images (PNG, TIFF, JPEG, JPG, GIF, BMP)
- **AI-Powered Summarization**: Creates concise summaries using SentenceTransformers and cosine similarity
- **Smart File Organization**: Uses Gemini AI to propose logical folder structures based on document content
- **Metadata Extraction**: Extracts titles, authors, and creation dates where available
- **OCR Capabilities**: Supports text extraction from images and scanned PDFs using EasyOCR or Tesseract
- **KPI Tracking**: Monitors performance metrics like processing success, error rates, and API response times

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Tesseract OCR (optional, for image processing)
- Google API key for Gemini AI access

### Install Dependencies

```bash
pip install docling docling-core sentence-transformers scikit-learn nltk google-generativeai pandas
pip install docling[easyocr]  # Optional: for EasyOCR support
pip install docling[tesseract]  # Optional: for Tesseract support
```

### API Setup

1. Obtain a Google API key from Google AI Studio.
2. Set the API key as an environment variable:

   **Linux/macOS**:

   ```bash
   export GOOGLE_API_KEY="your_api_key"
   ```

   **Windows (Command Prompt)**:

   ```bash
   set GOOGLE_API_KEY="your_api_key"
   ```

   **Windows (PowerShell)**:

   ```bash
   $env:GOOGLE_API_KEY="your_api_key"
   ```

### Directory Configuration

Set the source and destination directories as environment variables:

**Linux/macOS**:

```bash
export BASE_PATH="/your/target/directory"
export DESTINATION_ROOT="/your/output/directory"
```

**Windows (Command Prompt)**:

```bash
set BASE_PATH=C:\Your\Target\Directory
set DESTINATION_ROOT=C:\Your\Output\Directory
```

**Windows (PowerShell)**:

```bash
$env:BASE_PATH="C:\Your\Target\Directory"
$env:DESTINATION_ROOT="C:\Your\Output\Directory"
```

Alternatively, edit the variables directly in the scripts:

In `summarygenerator.py`:

```python
base_path = r'C:\Users\support2\Developments'  # Set to your source directory
```

In `fileorganizer.py`:

```python
DESTINATION_ROOT = r'C:\Users\support2\OrganizedDocuments1'  # Set to your output directory
```

## 🚀 Usage

### Step 1: Process Documents

Run the summarization script to scan and process documents:

```bash
python summarygenerator.py
```

This will:
- Scan the configured directory (`BASE_PATH`) for supported files
- Extract text and metadata using Docling (for most formats) and pandas (for XLSX)
- Apply OCR to images and scanned PDFs if EasyOCR or Tesseract is installed
- Generate semantic embeddings and summaries
- Save results to `llm_input.json` (for AI organization) and `processed_documents.json` (full results with embeddings)
- Display a KPI report with metrics like processing success and error rates

### Step 2: Organize Files

Run the organization script to create an optimized folder structure:

```bash
python fileorganizer.py
```

This will:
- Load `llm_input.json` and analyze document summaries using Gemini AI
- Generate a JSON organization plan and ASCII file tree
- Display the proposed structure and prompt for confirmation
- Move files to the new structure under `DESTINATION_ROOT`
- Display a KPI report with metrics like file movement success and API response times

## 📊 Supported File Types

| Category   | Formats                            |
|------------|------------------------------------|
| Documents  | PDF, DOCX, PPTX, XLSX, HTML, ADOC, MD |
| Images     | PNG, TIFF, JPEG, JPG, GIF, BMP     |
| Audio      | WAV, MP3                           |

## 🔧 How It Works

1. **Directory Scanning**: Recursively scans for supported file types
2. **Content Extraction**: Uses Docling for most formats and pandas for Excel files
3. **OCR Processing**: Extracts text from images and scanned PDFs if OCR tools are available
4. **Embedding & Summarization**: Generates embeddings with SentenceTransformers and creates summaries based on cosine similarity
5. **AI Organization**: Gemini AI analyzes summaries to propose a logical folder structure
6. **File Movement**: Moves files to the AI-recommended structure after user confirmation
7. **KPI Reporting**: Tracks performance metrics for both processing and organization

## 📋 Output Files

- `llm_input.json`: Metadata and summaries for AI organization
- `processed_documents.json`: Full processing results, including embeddings

## 📊 KPI Reports

Both scripts generate KPI reports displayed in the console:

**summarygenerator.py**:
- Document Processing Success Rate
- Average Processing Time per Document
- Summary Quality Score (average words)
- Error Rate
- OCR Utilization Rate
- Output File Integrity

**fileorganizer.py**:
- File Organization Success Rate
- Processing Time
- AI Plan Validity Rate
- Directory Creation Success Rate
- File Path Mapping Accuracy
- Error Rate
- Input File Load Success Rate
- API Response Time
- Tokens Used

## 🐛 Troubleshooting

- **Missing API Key**: Ensure `GOOGLE_API_KEY` is set
- **OCR Issues**: Install EasyOCR or Tesseract and add Tesseract to your system PATH
- **Permission Errors**: Verify read/write access to source and destination directories
- **JSON Errors**: Check `llm_input.json` for valid formatting
- **Large Files**: Increase processing time for large documents
- **Dependencies**: Ensure all required packages are installed

For additional help, review KPI reports or check dependency configurations.

## 📄 License

Provided for educational and research purposes. Comply with Google's API terms for Gemini AI usage.

## 🤝 Contributing

- Report bugs or request features via issues
- Submit pull requests with improvements
- Suggest documentation enhancements

**⚠️ Warning**: Back up files before running `fileorganizer.py`, as it physically moves files to new locations.
