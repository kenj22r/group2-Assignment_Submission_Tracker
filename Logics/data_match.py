import json
import os

#----------------------------------------------------------------------------------


def data_match(Assignment_Title):
    """Boolean Existence Check: Fast validation to see if a record title exists."""
    found = False
    path = os.path.join("Models", "Assignments_Data.json")

    if os.path.exists(path):
        with open(path, "r") as f:
            assignment_data = json.load(f)

        for k, details in assignment_data.items():
            # Normalized Matching Logic: Strips spaces and forces lowercase to eliminate formatting mismatches
            if Assignment_Title.lower().replace(" ", "") == details['Title'].lower().replace(" ", ""):             
                found = True
                return True
    else:
        return False

    if not found:
        return False
    
    
#-------------------------------------------------------------------------------------


def data_match_2(Search_Query):
    """Data Retrieval Search: Fetches both the structural key and its corresponding entry payload."""
    path = os.path.join("Models", "Assignments_Data.json")
    
    if not os.path.exists(path):
        print("Error: Database file does not exist.")
        return None
        
    with open(path, "r") as f:
        assignment_data = json.load(f)
        
    # Linear Scan: Iterates through the database looking for a normalized string match
    matched_key = None
    for key, details in assignment_data.items():
        if Search_Query.lower().replace(" ", "") == details.get('Title', '').lower().replace(" ", ""):
            matched_key = key
            break
            
    if not matched_key:
        print("\n-----------------------------------------------")
        print(f"No assignment found matching: '{Search_Query}'")
        print("-----------------------------------------------\n")
        return None
        
    # Extraction Block: Returns a tuple containing the database ID and the values dictionary
    Current_Details = assignment_data[matched_key]
    return matched_key, Current_Details