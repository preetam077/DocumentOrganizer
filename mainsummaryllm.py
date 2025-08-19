import os
import json
from typing import List, Dict
from docling.document_converter import DocumentConverter
from docling_core.types.doc import DoclingDocument
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
import warnings
from torch.utils.data import dataloader

# Disable the specific warning
warnings.filterwarnings("ignore", 
    message=".*'pin_memory' argument is set as true but no accelerator is found.*",
    category=UserWarning,
    module=dataloader.__name__
)

# Download NLTK data for sentence tokenization
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

# Define supported file extensions based on Docling's capabilities
supported_extensions = {
    '.pdf', '.docx', '.pptx', '.xlsx', '.html',
    '.png', '.tiff', '.jpeg', '.jpg', '.gif', '.bmp',
    '.adoc', '.md', '.wav', '.mp3'
}

# Base directory to scan
base_path = r'#TheDirectoryYouWantToScan#'

# List to hold paths of supported documents
supported_files: List[str] = []

# Step 1: Scan directory and print supported documents
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

# Print summary
print(f"\nTotal supported documents found: {len(supported_files)}")
if not supported_files:
    print("No supported documents found. Exiting.")
    exit()

# Step 2: Process the documents
# Load the embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the document converter (reusable)
converter = DocumentConverter()

# Lists to hold processed document data
output_data: List[Dict] = []  # For processed_documents.json
llm_input_data: List[Dict] = []  # For llm_input.json

# Function to generate a summary from text using embeddings
def generate_summary(text: str, doc_embedding: np.ndarray, max_sentences: int = 3) -> str:
    if not text.strip():
        return "No content available for summary."
    try:
        # Split text into sentences
        sentences = sent_tokenize(text)
        if not sentences:
            return "No sentences detected for summary."
        
        # Compute embeddings for each sentence
        sentence_embeddings = embed_model.encode(sentences)
        
        # Compute cosine similarity between document embedding and sentence embeddings
        similarities = cosine_similarity([doc_embedding], sentence_embeddings)[0]
        
        # Select top sentences based on similarity
        top_indices = np.argsort(similarities)[-max_sentences:]
        top_sentences = [sentences[i] for i in sorted(top_indices) if similarities[i] > 0.1]  # Filter low-similarity sentences
        
        # Combine sentences into a summary
        summary = " ".join(top_sentences)
        return summary if summary else "Unable to generate summary due to low similarity."
    except Exception as e:
        print(f"  -> Error generating summary: {str(e)}")
        return "Summary generation failed due to tokenization error."

# Process each supported file
print("\nProcessing supported documents...")
for file_path in supported_files:
    print(f"Processing: {file_path}")
    try:
        # Convert the document
        conv_res = converter.convert(file_path)
        
        # Check if conversion was successful
        if conv_res.document is not None:
            doc: DoclingDocument = conv_res.document
            
            # Create dictionaries for both JSON files
            doc_dict: Dict = {
                'file_path': file_path,
                'file_type': os.path.splitext(file_path)[1].lower(),
                'summary': "",
                'embedding': []
            }
            llm_dict: Dict = {
                'file_path': file_path,
                'file_type': os.path.splitext(file_path)[1].lower(),
                'summary': ""
            }
            
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
            
            # Extract all text for embedding and summarization
            all_text: List[str] = [item.text for item in doc.texts if item.text]
            string_cell_detected = False
            
            # Extract table content
            for table in doc.tables:
                for row in table.data:
                    for cell in row:
                        # Handle both string cells (e.g., .xlsx, some .pdf/.docx) and objects
                        cell_text = cell if isinstance(cell, str) else getattr(cell, 'text', '')
                        if isinstance(cell, str) and not string_cell_detected:
                            print(f"  -> String cells detected in tables for {file_path}")
                            string_cell_detected = True
                        if cell_text:
                            all_text.append(cell_text)
            
            # Join all text
            full_text = "\n".join([t for t in all_text if t]).strip()
            
            # Generate embedding and summary
            if full_text:
                doc_embedding = embed_model.encode(full_text)
                doc_dict['embedding'] = doc_embedding.tolist()
                summary = generate_summary(full_text, doc_embedding)
                doc_dict['summary'] = summary
                llm_dict['summary'] = summary
            else:
                doc_dict['summary'] = "No content available for summary."
                llm_dict['summary'] = "No content available for summary."
            
            # Append to output lists
            output_data.append(doc_dict)
            llm_input_data.append(llm_dict)
        else:
            print(f"Conversion failed for {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

# Save the output to two JSON files
# 1. processed_documents.json (includes embeddings)
output_file = 'processed_documents_existing.json'
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"\nOutput saved to {output_file}")
except Exception as e:
    print(f"Error saving {output_file}: {str(e)}")

# 2. llm_input.json (excludes embeddings)
llm_output_file = 'llm_input.json'
try:
    with open(llm_output_file, 'w', encoding='utf-8') as f:
        json.dump(llm_input_data, f, ensure_ascii=False, indent=4)
    print(f"Output saved to {llm_output_file}")
except Exception as e:
    print(f"Error saving {llm_output_file}: {str(e)}")


print("\nProcessing complete.")
