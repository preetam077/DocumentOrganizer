import json
import os
import shutil
import google.generativeai as genai
import time
from collections import defaultdict

# --- Configuration ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

DESTINATION_ROOT = '#TheDirectyWhereYouWantToPerformAction#' #eg. C:\\Users\\Goku\\OrganizedDocuments

# KPI tracking variables
start_time = time.time()
files_moved = 0
total_files_in_plan = 0
dirs_created = 0
total_dirs_in_plan = 0
valid_path_mappings = 0
total_filenames_in_plan = 0
errors_encountered = 0
json_load_success = False
ai_plan_valid = False
api_response_time = 0.0
tokens_used = 0

# --- Main Functions ---

def load_document_data(filepath='llm_input.json'):
    """Loads the document metadata from the specified JSON file."""
    global json_load_success, errors_encountered
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json_load_success = True
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{filepath}' not found.")
        errors_encountered += 1
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'.")
        errors_encountered += 1
        return None

def create_file_path_map(document_data):
    """Creates a simple mapping from filename to its full original path."""
    path_map = {}
    for doc in document_data:
        filename = os.path.basename(doc['file_path'])
        path_map[filename] = doc['file_path']
    return path_map

def get_organization_plan_from_ai(document_data):
    """Sends document info to the AI and requests a file organization plan in JSON format."""
    global ai_plan_valid, errors_encountered, api_response_time, tokens_used
    documents_str = "\n".join([
        f"- File: {os.path.basename(doc['file_path'])}\n  Summary: {doc['summary']}\n"
        for doc in document_data
    ])

    prompt = f"""
    You are an expert file organization assistant. Your task is to organize the files listed below into a logical folder structure.

    Analyze the following file summaries and create a file tree plan. The plan should group files by project, year, topic, or other relevant criteria.

    **File Information:**
    {documents_str}

    **Instructions:**
    Respond ONLY with a valid JSON object. Do not include any text, explanations, or markdown formatting before or after the JSON block.
    The JSON object should be a dictionary where:
    - Each key is the proposed new directory path (e.g., "Case_Studies/2020_Grimmen_Vegetation").
    - Each value is a list of the filenames (e.g., ["Case Study_Cutting Vegetation_2020.docx", "Fassade nach Cutting.png"]) that should be moved into that directory.

    Example of desired output format:
    {{
      "Case_Studies/2018_Cadolzburg_Degradation": [
        "Case Study_Cadolzburg_v1.docx",
        "ZAE_Modulliste.pdf"
      ],
      "Case_Studies/2019_Umrath_Performance": [
        "Plant Performance Report.docx",
        "Plant Performance Report_2019-08-16.docx",
        "Use case Umrath.xlsx"
      ]
    }}
    """

    print("Asking the AI to generate an organization plan... (This may take a moment)")
    try:
        start_api_time = time.time()
        response = model.generate_content(prompt)
        api_response_time = time.time() - start_api_time
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        plan = json.loads(cleaned_response)
        ai_plan_valid = True
        # Estimate tokens (fallback if API metadata unavailable)
        # Rough estimate: 1 token ≈ 4 characters in English text
        input_tokens = len(prompt) // 4
        output_tokens = len(cleaned_response) // 4
        tokens_used = input_tokens + output_tokens
        # Note: If API provides token counts (e.g., response.usage_metadata), use that instead:
        # tokens_used = response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else tokens_used
        return plan
    except (json.JSONDecodeError, Exception) as e:
        print(f"\n--- Error ---")
        print(f"Failed to get a valid JSON plan from the AI. Error: {e}")
        print("AI's raw response was:")
        print(response.text)
        errors_encountered += 1
        return None

def execute_file_organization(plan, path_map, destination_root):
    """Creates directories and moves files based on the provided plan."""
    global files_moved, total_files_in_plan, dirs_created, total_dirs_in_plan
    global valid_path_mappings, total_filenames_in_plan, errors_encountered
    print("\nStarting file organization process...")
    
    if not plan:
        print("Cannot proceed with an empty or invalid plan.")
        errors_encountered += 1
        return

    total_dirs_in_plan = len(plan)
    for directory, filenames in plan.items():
        new_dir_path = os.path.join(destination_root, directory)
        total_filenames_in_plan += len(filenames)
        
        try:
            os.makedirs(new_dir_path, exist_ok=True)
            print(f"\n[OK] Ensured directory exists: '{new_dir_path}'")
            dirs_created += 1
        except OSError as e:
            print(f"[ERROR] Could not create directory '{new_dir_path}'. Skipping. Error: {e}")
            errors_encountered += 1
            continue

        for filename in filenames:
            original_path = path_map.get(filename)
            
            if not original_path:
                print(f"  [WARN] Could not find original path for '{filename}'. Skipping.")
                errors_encountered += 1
                continue

            if not os.path.exists(original_path):
                print(f"  [WARN] Source file does not exist at '{original_path}'. Skipping.")
                errors_encountered += 1
                continue

            valid_path_mappings += 1
            destination_path = os.path.join(new_dir_path, filename)

            try:
                shutil.move(original_path, destination_path)
                print(f"  -> Moved '{filename}' to '{new_dir_path}'")
                files_moved += 1
            except Exception as e:
                print(f"  [ERROR] Failed to move '{filename}'. Error: {e}")
                errors_encountered += 1

    total_files_in_plan += sum(len(files) for files in plan.values())

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Load data from llm_inputexcelkpi.json
    all_docs = load_document_data()

    if all_docs:
        # 2. Get the organization plan from the AI
        organization_plan = get_organization_plan_from_ai(all_docs)

        if organization_plan:
            # 3. Create a map of filenames to their original paths
            file_path_map = create_file_path_map(all_docs)

            # 4. Display the plan and file move information
            print("\n--- Proposed Organization Plan ---")
            for directory, files in organization_plan.items():
                print(f"\nFolder: {directory}")
                for f in files:
                    original_path = file_path_map.get(f, "Not found")
                    destination_path = os.path.join(DESTINATION_ROOT, directory, f)
                    print(f"  File: {f}")
                    print(f"    From: {original_path}")
                    print(f"    To: {destination_path}")
            print("\n------------------------------------")

            # 5. Ask for confirmation
            confirm = input("Do you want to apply this organization? (yes/no): ").lower().strip()

            if confirm == 'yes':
                # 6. Execute the plan
                execute_file_organization(organization_plan, file_path_map, DESTINATION_ROOT)
            else:
                print("Operation cancelled by user.")

    # Calculate KPIs
    total_processing_time = time.time() - start_time
    kpi_report = {
        "file_organization_success_rate": (files_moved / total_files_in_plan * 100) if total_files_in_plan else 0.0,
        "processing_time_seconds": total_processing_time,
        "ai_plan_validity_rate": 100.0 if ai_plan_valid else 0.0,
        "directory_creation_success_rate": (dirs_created / total_dirs_in_plan * 100) if total_dirs_in_plan else 0.0,
        "file_path_mapping_accuracy": (valid_path_mappings / total_filenames_in_plan * 100) if total_filenames_in_plan else 0.0,
        "error_rate": (errors_encountered / (total_filenames_in_plan + total_dirs_in_plan) * 100) if (total_filenames_in_plan + total_dirs_in_plan) else 0.0,
        "input_file_load_success_rate": 100.0 if json_load_success else 0.0,
        "api_response_time_seconds": api_response_time,
        "tokens_used": tokens_used
    }

    # Save KPI report
    kpi_output_file = 'fileorganizerkpi.json'
    try:
        with open(kpi_output_file, 'w', encoding='utf-8') as f:
            json.dump(kpi_report, f, ensure_ascii=False, indent=4)
        print(f"\nKPI report saved to {kpi_output_file}")
    except Exception as e:
        print(f"Error saving {kpi_output_file}: {str(e)}")

    # Print KPI report
    print("\n=== KPI Report ===")
    print(f"File Organization Success Rate: {kpi_report['file_organization_success_rate']:.2f}%")
    print(f"Processing Time: {kpi_report['processing_time_seconds']:.2f} seconds")
    print(f"AI Plan Validity Rate: {kpi_report['ai_plan_validity_rate']:.2f}%")
    print(f"Directory Creation Success Rate: {kpi_report['directory_creation_success_rate']:.2f}%")
    print(f"File Path Mapping Accuracy: {kpi_report['file_path_mapping_accuracy']:.2f}%")
    print(f"Error Rate: {kpi_report['error_rate']:.2f}%")
    print(f"Input File Load Success Rate: {kpi_report['input_file_load_success_rate']:.2f}%")
    print(f"API Response Time: {kpi_report['api_response_time_seconds']:.2f} seconds")
    print(f"Tokens Used: {kpi_report['tokens_used']}")
    print("=================\n")

    print("Processing complete.")
