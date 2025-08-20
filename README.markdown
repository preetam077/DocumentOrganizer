# Document Organization and Summarization System

A powerful AI-powered pipeline that scans directories, processes documents of various formats, generates intelligent summaries, and organizes files into an optimal folder structure using Google's Gemini AI.

## 📁 Repository Structure

```
.
├── summarygenerator.py        # Document scanning, summarization, and metadata extraction script
├── fileorganizer.py           # AI-powered file organization script
├── llm_input.json             # Generated output (document metadata for AI)
├── processed_documents.json   # Generated output (full processing results)
├── fileorganizerkpi.json      # KPI report for file organization
├── summarygeneratorkpi.json   # KPI report for document processing
└── README.md                  # This file
```

## ✨ Features

- **Multi-Format Support**: Processes PDF, DOCX, PPTX, XLSX, images (with OCR), HTML, Markdown, and more
- **AI-Powered Summarization**: Generates contextual summaries using sentence embeddings and cosine similarity
- **Smart File Organization**: Uses Gemini AI to create logical folder structures with JSON plans and ASCII file trees
- **Metadata Extraction**: Automatically extracts titles, authors, and creation dates
- **OCR Capabilities**: Extracts text from images and scanned documents using EasyOCR or Tesseract
- **KPI Reporting**: Tracks performance metrics like processing success, error rates, and API response times

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system (optional, for OCR support)
- Google API key for Gemini AI access

### Install Dependencies

```bash
pip install docling docling-core sentence-transformers scikit-learn nltk google-generativeai easyocr pytesseract pandas
```

### API Setup

1. Get a Google API key from Google AI Studio.

2. Set the API key as an environment variable:

   **Linux/macOS**:

   ```bash
   export GOOGLE_API_KEY="your_actual_api_key_here"
   ```

   **Windows (Command Prompt)**:

   ```bash
   set GOOGLE_API_KEY="your_actual_api_key_here"
   ```

   **Windows (PowerShell)**:

   ```bash
   $env:GOOGLE_API_KEY="your_actual_api_key_here"
   ```

## 🚀 Usage

### Step 1: Process Documents

Run the document processing script to scan, extract content, and generate summaries:

```bash
python summarygenerator.py
```

This will:

- Scan the configured directory for supported documents
- Extract text and metadata using Docling and pandas (for Excel files)
- Apply OCR to images and scanned PDFs if EasyOCR or Tesseract is available
- Generate semantic embeddings and AI summaries
- Create `llm_input.json` and `processed_documents.json`
- Generate a KPI report in `summarygeneratorkpi.json`

### Step 2: Organize Files

Use the AI organization system to create an optimal folder structure:

```bash
python fileorganizer.py
```

This will:

- Analyze document summaries using Gemini AI
- Generate a JSON organization plan and ASCII file tree
- Display the proposed folder structure and file movements
- Prompt for confirmation before moving files
- Organize documents into the new structure under the configured destination
- Generate a KPI report in `fileorganizerkpi.json`

## ⚙️ Configuration

Edit these variables in the source code to match your environment:

In `summarygenerator.py`:

```python
base_path = r'C:\Users\support2\Developments'  # Change to your target directory
```

In `fileorganizer.py`:

```python
DESTINATION_ROOT = 'C:\\Users\\support2\\OrganizedDocuments1'  # Change to your desired output location
```

## 📊 Supported File Types

| Category | Formats |
| --- | --- |
| Documents | PDF, DOCX, PPTX, XLSX, HTML, ADOC, MD |
| Images | PNG, TIFF, JPEG, JPG, GIF, BMP (with OCR) |
| Audio | WAV, MP3 |

## 🔧 How It Works

1. **Directory Scanning**: Recursively searches for supported file types
2. **Content Extraction**: Uses Docling for most formats and pandas for Excel files to extract text and metadata
3. **OCR Processing**: Applies optical character recognition to images and scanned PDFs
4. **Embedding Generation**: Creates semantic embeddings using SentenceTransformers
5. **AI Summarization**: Generates summaries by selecting key sentences based on cosine similarity
6. **Organization Planning**: Gemini AI analyzes summaries to create a JSON plan and ASCII file tree
7. **File Movement**: Physically reorganizes files based on AI recommendations
8. **KPI Reporting**: Tracks metrics like success rates, processing times, and error rates for both scripts

## 📋 Output Files

- `llm_input.json`: Contains document metadata and summaries for AI analysis
- `processed_documents.json`: Includes full processing results with embeddings
- `fileorganizerkpi.json`: Performance metrics for file organization
- `summarygeneratorkpi.json`: Performance metrics for document processing

## 📊 KPI Reports

Both scripts generate detailed KPI reports to evaluate performance:

- **summarygenerator.py**:

  - Document Processing Success Rate
  - Average Processing Time per Document
  - Summary Quality Score (Average Words)
  - Error Rate
  - OCR Utilization Rate
  - Output File Integrity

- **fileorganizer.py**:

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

### Common Issues

- **Missing API Key**: Ensure `GOOGLE_API_KEY` environment variable is set
- **OCR Errors**: Install Tesseract or EasyOCR and ensure Tesseract is in your system PATH
- **Permission Denied**: Ensure write access to source and destination directories
- **Large Files**: Very large documents may require additional processing time
- **JSON Errors**: Verify `llm_input.json` is correctly formatted before running `fileorganizer.py`

### Getting Help

- Verify all dependencies are installed correctly
- Check that your Google API key has Gemini API access
- Ensure Tesseract or EasyOCR is properly installed for image processing
- Review KPI reports for detailed error insights

## 📄 License

This project is provided for educational and research purposes. Please ensure compliance with Google's API terms of service when using Gemini AI.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Submit bug reports and feature requests as issues
- Fork the repository and submit pull requests
- Suggest improvements to the documentation

**Note**: Always back up your files before running the organization script, as it will physically move your files to new locations.
