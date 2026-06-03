import os
import json
from Utilities import clear_screen

# Scalable relative database resolving
# Establishes a rock-solid root directory reference to prevent broken paths regardless of where execution starts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_name = os.path.join(BASE_DIR, "Models")
filename = "Assignments_Data.json"
full_path = os.path.join(folder_name, filename)

# Directory Guard: Ensures the host directory exists before firing any I/O file writing events
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def save_assignment(Assignment_Title, Subject, Due_Date, Status, Priority):
    """Parses existing records, autogenerates an incremental primary key ID, and stores the payload."""
    data = {}
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Corruption Recovery: Instantiates an empty state if JSON is unreadable or blank
                data = {}
                
    # Primary Key Generation: Extracts the trailing integer from structural keys (e.g., 'AS_ID_5' -> 5)
    existing_nums = []
    for k in data.keys():
        try:
            num = int(k.split('_')[-1])
            existing_nums.append(num)
        except (IndexError, ValueError):
            continue
            
    # Auto-Increment Engine: Calculates the next absolute ID number to avoid overwriting older records
    next_num = max(existing_nums, default=0) + 1
    new_key = f'AS_ID_{next_num}'
    
    # State update and transaction append block
    data.update({new_key: {
        "Title": Assignment_Title,
        "Subject": Subject,
        "Due_Date": Due_Date,
        "Status": Status,
        "Priority": Priority
    }})
    
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)
    
    clear_screen.clear_screen()
    print("\n  Data saved successfully")

def Save_Updated_Data(matched_key, updated_dict):
    """Performs an in-place update targeting a specific unique record key entry."""
    path = os.path.join(BASE_DIR, "Models", "Assignments_Data.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            assignment_data = json.load(f)
            
        # Target assignment modification: Maps the key directly to the newly parsed inner dictionary payload
        assignment_data[matched_key] = updated_dict
        
        with open(path, "w") as f:
            json.dump(assignment_data, f, indent=4)
        print("\n  Changes saved successfully!")
    else:
        print("Error: Database file not found during saving.")