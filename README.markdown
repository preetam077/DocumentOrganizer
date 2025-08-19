# Document Organization and Summarization System

A powerful AI-powered pipeline that scans directories, processes documents of various formats, generates intelligent summaries, and organizes files into an optimal folder structure using Google's Gemini AI.

## 📁 Repository Structure

```
.
├── mainsummaryllm.py          # Main document processing and summarization script
├── geminitest.py              # AI-powered file organization script
├── llm_input.json             # Generated output (document metadata for AI)
├── processed_documents_existing.json  # Generated output (full processing results)
└── README.md                  # This file
```

## ✨ Features

- **Multi-Format Support**: Processes PDF, DOCX, PPTX, XLSX, images (with OCR), HTML, Markdown, and more
- **AI-Powered Summarization**: Generates contextual summaries using sentence embeddings
- **Smart File Organization**: Uses Gemini AI to create logical folder structures based on content
- **Metadata Extraction**: Automatically extracts titles, authors, and creation dates
- **OCR Capabilities**: Extracts text from images and scanned documents using Tesseract/EasyOCR

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
- Google API key for Gemini AI access

### Install Dependencies

```bash
pip install docling docling-core sentence-transformers scikit-learn nltk google-generativeai easyocr pytesseract python-dotenv
```

### API Setup

1. Get a Google API key from [Google AI Studio](https://aistudio.google.com/).
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

Run the main processing script to scan, extract content, and generate summaries:

```bash
python mainsummaryllm.py
```

This will:
- Scan the configured directory for supported documents
- Extract text and metadata from each file
- Generate embeddings and AI summaries
- Create `llm_input.json` and `processed_documents_existing.json`

### Step 2: Organize Files

Use the AI organization system to create an optimal folder structure:

```bash
python geminitest.py
```

This will:
- Analyze document summaries using Gemini AI
- Propose a logical folder structure based on content
- Prompt for confirmation before moving files
- Organize documents into the new structure

## ⚙️ Configuration

Edit these variables in the source code to match your environment:

In `mainsummaryllm.py`:
```python
base_path = r'C:\Users\support2\Developments'  # Change to your target directory
```

In `geminitest.py`:
```python
DESTINATION_ROOT = 'C:\\Users\\support2\\OrganizedDocuments'  # Change to your desired output location
```

## 📊 Supported File Types

| Category   | Formats                              |
|------------|--------------------------------------|
| Documents  | PDF, DOCX, PPTX, XLSX, HTML, ADOC, MD |
| Images     | PNG, TIFF, JPEG, JPG, GIF, BMP (with OCR) |
| Audio      | WAV, MP3                             |

## 🔧 How It Works

1. **Directory Scanning**: Recursively searches for supported file types
2. **Content Extraction**: Uses Docling library to extract text and metadata
3. **OCR Processing**: Applies optical character recognition to images
4. **Embedding Generation**: Creates semantic embeddings using SentenceTransformers
5. **AI Summarization**: Generates summaries by identifying key sentences
6. **Organization Planning**: Gemini AI analyzes content to create optimal folder structure
7. **File Movement**: Physically reorganizes files based on AI recommendations

## 📋 Output Files

- `llm_input.json`: Contains document metadata and summaries for AI analysis
- `processed_documents_existing.json`: Includes full processing results with embeddings

## 🐛 Troubleshooting

### Common Issues

- **Missing API Key**: Ensure `GOOGLE_API_KEY` environment variable is set
- **OCR Errors**: Install Tesseract OCR and ensure it's in your system PATH
- **Permission Denied**: Ensure write access to destination directories
- **Large Files**: Very large documents may require additional processing time

### Getting Help

- Verify all dependencies are installed correctly
- Check that your Google API key has Gemini API access
- Ensure Tesseract OCR is properly installed for image processing

## 📄 License

This project is provided for educational and research purposes. Please ensure compliance with Google's API terms of service when using Gemini AI.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Submit bug reports and feature requests as issues
- Fork the repository and submit pull requests
- Suggest improvements to the documentation

**Note**: Always back up your files before running the organization script, as it will physically move your files to new locations.