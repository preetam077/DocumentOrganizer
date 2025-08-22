# File Organizer with AI-Powered Document Analysis 📁🤖

This repository contains a Python-based tool for scanning, summarizing, and organizing files using AI-driven analysis. The system processes various document types, generates summaries, and proposes an optimized folder structure using the Gemini AI model. 🚀

## Features ✨
- **Document Scanning** 📜: Scans a specified directory for supported file types (e.g., PDF, DOCX, PNG, XLSX, etc.).
- **Summary Generation** ✍️: Extracts text and generates concise summaries using the `docling` library and sentence embeddings.
- **AI-Powered Organization** 🧠: Uses the Gemini AI model to analyze the current file structure and propose a logical folder hierarchy.
- **File Movement** 🚚: Moves files to new directories based on the AI-generated organization plan.
- **KPI Tracking** 📊: Monitors performance metrics like processing time, success rates, and error rates.

## Repository Structure 📂
- `summarygenerator.py` 🖨️: Scans documents, extracts text, generates summaries, and saves metadata to JSON files.
- `fileorganizer.py` 🗂️: Analyzes the current file structure using Gemini AI, proposes a new organization plan, and executes file movements.
- `requirements.txt` 📋: Lists Python dependencies.
- `.env.example` 🔑: Template for environment variables (API key, source/output paths).
- `.gitignore` 🚫: Excludes `.env` from version control.

## Prerequisites ✅
- Python 3.8+ 🐍
- Tesseract OCR binary (for `pytesseract`) 🔍:
  - Windows: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt install tesseract-ocr`
  - macOS: `brew install tesseract`
- Google API Key for Gemini AI (obtain from [Google AI Studio](https://aistudio.google.com/)) 🔐

## Installation 🛠️
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to include:
   - `GOOGLE_API_KEY` 🔑: Your Gemini AI API key.
   - `BASE_PATH` 📍: Directory to scan for documents.
   - `DESTINATION_ROOT` 🏁: Directory for organized files.

## Usage 🚀
1. Run `summarygenerator.py` to scan documents and generate summaries:
   ```bash
   python summarygenerator.py
   ```
   Outputs:
   - `processed_documents.json` 📄: Full document metadata with embeddings.
   - `llm_input.json` 📤: Simplified metadata for AI processing.
2. Run `fileorganizer.py` to analyze and reorganize files:
   ```bash
   python fileorganizer.py
   ```
   - Analyzes the current structure using Gemini AI 🧠.
   - Proposes a new folder structure and displays a file tree 🌳.
   - Prompts for confirmation before moving files.

## Example Workflow 🔄
1. Configure `.env` with your paths and API key.
2. Place documents in `BASE_PATH` (e.g., `/path/to/source/directory`) 📂.
3. Run `summarygenerator.py` to generate `llm_input.json` 📝.
4. Run `fileorganizer.py` to:
   - Analyze the current structure 🔎.
   - Propose a new organization plan 📑.
   - Move files to `DESTINATION_ROOT` (e.g., `/path/to/output/directory`) upon approval 🚚.

## KPI Reports 📈
Both scripts generate KPI reports, including:
- Success rates for document processing and file organization ✅.
- Processing times and error rates ⏱️.
- OCR utilization and summary quality metrics 📊.

## Notes ⚠️
- Ensure `BASE_PATH` and `DESTINATION_ROOT` are valid directories.
- The tool relies on the Gemini AI model; ensure a valid API key 🔐.
- OCR is optional for image-based files (e.g., PNG, PDF) and requires `easyocr` or `pytesseract` 🔍.
- Back up files before running `fileorganizer.py`, as it moves files 💾.

## License 📜
This project is licensed under the MIT License.
