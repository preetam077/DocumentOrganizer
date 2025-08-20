

import os
import json
from typing import List, Dict
import pandas as pd
from docling.document_converter import DocumentConverter
from docling_core.types.doc import DoclingDocument
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import nltk
import warnings
from torch.utils.data import dataloader
from sklearn.metrics.pairwise import cosine_similarity

# Disable the specific warning
warnings.filterwarnings("ignore", 
    message=".*'pin_memory' argument is set as true but no accelerator is found.*",
    category=UserWarning,
    module=dataloader.__name__
)

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading NLTK punkt_tab resource...")
    nltk.download('punkt_tab')

# Check for OCR dependencies
try:
    import easyocr
except ImportError:
    print("Warning: easyocr not installed. Install with 'pip install docling[easyocr]' for OCR support.")
try:
    import pytesseract
except ImportError:
    print("Warning: pytesseract not installed. Install with 'pip install docling[tesseract]' and Tesseract binary for OCR support.")

# Supported file extensions
supported_extensions = {
    '.pdf', '.docx', '.pptx', '.xlsx', '.html',
    '.png', '.tiff', '.jpeg', '.jpg', '.gif', '.bmp',
    '.adoc', '.md', '.wav', '.mp3'
}

# Base directory to scan
base_path = r'PutYourDirectoryHere' #eg. C:\Users\support2\Developments

# List to hold paths of supported documents
supported_files: List[str] = []

# Step 1: Scan directory
print("Scanning for documents supported by Docling...")
for root, _, files in os.walk(base_path):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in supported_extensions:
            file_path = os.path.join(root, file)
            supported_files.append(file_path)
            print(f"Found: {file_path}")
            if ext in {'.png', '.tiff', '.jpeg', '.jpg', '.gif', '.bmp', '.pdf'}:
                print(f"  -> OCR may be applied for this file.")

print(f"\nTotal supported documents found: {len(supported_files)}")
if not supported_files:
    print("No supported documents found. Exiting.")
    exit()

# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize document converter
converter = DocumentConverter()

# Output lists
output_data: List[Dict] = []
llm_input_data: List[Dict] = []

# Function to generate summary
def generate_summary(text: str, doc_embedding: np.ndarray, max_sentences: int = 5, is_table: bool = False) -> str:
    if not text.strip():
        return "No content available for summary."
    try:
        if is_table:
            # For tabular data, create a concise summary of headers and sample rows
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if not lines:
                return "No meaningful text content extracted from table."
            # Take headers and a few rows, focusing on text content
            summary_lines = lines[:max_sentences]
            return f"Table summary: {'; '.join(summary_lines)}..."
        else:
            # Sentence-based summary for non-tabular data
            sentences = sent_tokenize(text)
            if not sentences:
                return "No sentences detected for summary."
            sentence_embeddings = embed_model.encode(sentences)
            similarities = cosine_similarity([doc_embedding], sentence_embeddings)[0]
            top_indices = np.argsort(similarities)[-max_sentences:]
            top_sentences = [sentences[i] for i in sorted(top_indices) if similarities[i] > 0.1]
            summary = " ".join(top_sentences)
            return summary if summary else "Unable to generate summary due to low similarity."
    except Exception as e:
        print(f"  -> Error generating summary: {str(e)}")
        return "Summary generation failed."

# Function to extract text from Excel using pandas
def extract_excel_text(file_path: str) -> str:
    try:
        xl = pd.ExcelFile(file_path)
        all_text = []
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Convert all cells to strings, handling NaN and other types
            df = df.astype(str).replace('nan', '').replace('', 'None')
            # Extract headers
            headers = ", ".join(df.columns.tolist())
            all_text.append(f"Sheet: {sheet_name}")
            all_text.append(f"Headers: {headers}")
            # Extract cell values (all rows, but join as comma-separated for summary)
            for _, row in df.iterrows():
                row_text = ", ".join([val for val in row if val != 'None'])
                if row_text:
                    all_text.append(row_text)
        return "\n".join(all_text)
    except Exception as e:
        print(f"  -> Error reading Excel file {file_path} with pandas: {str(e)}")
        return ""

# Process documents
print("\nProcessing supported documents...")
for file_path in supported_files:
    print(f"Processing: {file_path}")
    try:
        ext = os.path.splitext(file_path)[1].lower()
        doc_dict: Dict = {'file_path': file_path, 'file_type': ext, 'summary': "", 'embedding': []}
        llm_dict: Dict = {'file_path': file_path, 'file_type': ext, 'summary': ""}

        all_text: List[str] = []

        if ext == '.xlsx':
            # Always use pandas for .xlsx files to ensure reliable text extraction
            print(f"  -> Using pandas to extract content from {file_path}")
            excel_text = extract_excel_text(file_path)
            if excel_text:
                all_text.append(excel_text)
        else:
            # Use docling for other formats
            conv_res = converter.convert(file_path)
            if conv_res.document is not None:
                doc: DoclingDocument = conv_res.document

                # Extract metadata
                metadata = doc.model_dump().get('metadata', {})
                if isinstance(metadata, dict):
                    if 'title' in metadata:
                        doc_dict['title'] = str(metadata['title'])
                        llm_dict['title'] = str(metadata['title'])
                    if 'author' in metadata:
                        doc_dict['author'] = str(metadata['author'])
                        llm_dict['author'] = str(metadata['author'])
                    if 'creation_date' in metadata:
                        doc_dict['creation_date'] = str(metadata['creation_date'])
                        llm_dict['creation_date'] = str(metadata['creation_date'])

                # Extract text items
                all_text.extend(item.text for item in doc.texts if item.text)

                # Extract table content (only text)
                for table in doc.tables:
                    for row in table.data:
                        for cell in row:
                            cell_text = getattr(cell, 'text', str(cell)) if not isinstance(cell, str) else cell
                            if cell_text:
                                all_text.append(cell_text)

        # Join all text
        full_text = "\n".join([t for t in all_text if t]).strip()

        # Generate embedding and summary
        if full_text:
            doc_embedding = embed_model.encode(full_text)
            doc_dict['embedding'] = doc_embedding.tolist()
            summary = generate_summary(full_text, doc_embedding, is_table=(ext == '.xlsx'))
            doc_dict['summary'] = summary
            llm_dict['summary'] = summary
        else:
            doc_dict['summary'] = "No content available for summary."
            llm_dict['summary'] = "No content available for summary."

        output_data.append(doc_dict)
        llm_input_data.append(llm_dict)
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

# Save output
output_file = 'processed_documents.json' #give this file whatever name you want (this for analysis)
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"\nOutput saved to {output_file}")
except Exception as e:
    print(f"Error saving {output_file}: {str(e)}")

llm_output_file = 'llm_input.json' #give this file whatever name you want (this is fed to the AI)
try:
    with open(llm_output_file, 'w', encoding='utf-8') as f:
        json.dump(llm_input_data, f, ensure_ascii=False, indent=4)
    print(f"Output saved to {llm_output_file}")
except Exception as e:
    print(f"Error saving {llm_output_file}: {str(e)}")

print("\nProcessing complete.")
