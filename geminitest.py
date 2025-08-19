import json
import os
import shutil
import google.generativeai as genai

# --- Configuration ---
# It's recommended to set your API key as an environment variable for security.
# If you haven't, you can paste it here directly:
# api_key = "YOUR_GOOGLE_API_KEY"
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash') # Using a capable model for JSON output

# The root directory where you want the new folder structure to be created.
# '.' means the current directory where the script is running.
DESTINATION_ROOT = '#TheDirectyWhereYouWantToPerformAction#'

# --- Main Functions ---

def load_document_data(filepath='llm_input.json'):
    """Loads the document metadata from the specified JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{filepath}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'.")
        return None

def create_file_path_map(document_data):
    """Creates a simple mapping from filename to its full original path."""
    path_map = {}
    for doc in document_data:
        # os.path.basename extracts the filename (e.g., "report.pdf") from the full path
        filename = os.path.basename(doc['file_path'])
        path_map[filename] = doc['file_path']
    return path_map

def get_organization_plan_from_ai(document_data):
    """
    Sends document info to the AI and requests a file organization plan in JSON format.
    """
    # Prepare the input for the AI: Combine summaries with file paths
    documents_str = "\n".join([
        f"- File: {os.path.basename(doc['file_path'])}\n  Summary: {doc['summary']}\n"
        for doc in document_data
    ])

    # A more advanced prompt asking for a specific JSON output structure
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
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, Exception) as e:
        print(f"\n--- Error ---")
        print(f"Failed to get a valid JSON plan from the AI. Error: {e}")
        print("AI's raw response was:")
        print(response.text)
        return None


def execute_file_organization(plan, path_map, destination_root):
    """Creates directories and moves files based on the provided plan."""
    print("\nStarting file organization process...")
    total_files_moved = 0
    
    if not plan:
        print("Cannot proceed with an empty or invalid plan.")
        return

    for directory, filenames in plan.items():
        # Create the full path for the new directory
        new_dir_path = os.path.join(destination_root, directory)
        
        try:
            # Create the directory, including any parent directories needed.
            # exist_ok=True prevents an error if the directory already exists.
            os.makedirs(new_dir_path, exist_ok=True)
            print(f"\n[OK] Ensured directory exists: '{new_dir_path}'")
        except OSError as e:
            print(f"[ERROR] Could not create directory '{new_dir_path}'. Skipping. Error: {e}")
            continue

        for filename in filenames:
            # Find the original full path of the file
            original_path = path_map.get(filename)
            
            if not original_path:
                print(f"  [WARN] Could not find original path for '{filename}'. Skipping.")
                continue

            if not os.path.exists(original_path):
                 print(f"  [WARN] Source file does not exist at '{original_path}'. Skipping.")
                 continue

            destination_path = os.path.join(new_dir_path, filename)

            # Move the file
            try:
                shutil.move(original_path, destination_path)
                print(f"  -> Moved '{filename}' to '{new_dir_path}'")
                total_files_moved += 1
            except Exception as e:
                print(f"  [ERROR] Failed to move '{filename}'. Error: {e}")

    print(f"\n--- Organization Complete ---")
    print(f"Successfully moved {total_files_moved} files.")


# --- Main Execution ---
if __name__ == "__main__":
    # 1. Load data from llm_input.json
    all_docs = load_document_data()

    if all_docs:
        # 2. Get the organization plan from the AI
        organization_plan = get_organization_plan_from_ai(all_docs)

        if organization_plan:
            # 3. Display the plan and ask for user confirmation
            print("\n--- Proposed Organization Plan ---")
            for directory, files in organization_plan.items():
                print(f"\nFolder: {directory}")
                for f in files:
                    print(f"  - {f}")
            print("\n------------------------------------")

            # 4. Ask for confirmation
            confirm = input("Do you want to apply this organization? (yes/no): ").lower().strip()

            if confirm == 'yes':
                # 5. Create a map of filenames to their original paths
                file_path_map = create_file_path_map(all_docs)
                
                # 6. Execute the plan
                execute_file_organization(organization_plan, file_path_map, DESTINATION_ROOT)
            else:

                print("Operation cancelled by user.")
