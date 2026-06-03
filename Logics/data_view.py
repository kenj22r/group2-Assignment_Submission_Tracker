import json
import os

#----------------------------------------------------------------------------------


def data_view():
    """Reads the JSON database and prints all saved assignments to the terminal."""
    path = os.path.join("Models", "Assignments_Data.json")

   
    if os.path.exists(path):
        with open(path, "r") as f:
            assignment_data = json.load(f)
        
        # Guard Clause: Validates if the file contains actual records or an empty dictionary {}
        if assignment_data:
            
            # Formatted Output Loop: Enumerates the dictionary data to build a numbered CLI list
            for i, (k, details) in enumerate(assignment_data.items(), start=1):
                print()
                print(f"\nAssignment No: {i}")
                print()
                print(f"\tAssignment Title: {details['Title']}")
                print(f"\tSubject: {details['Subject']}")
                print(f"\tDue Date: {details['Due_Date']}")
                print(f"\tStatus: {details['Status']}")
                print(f"\tPriority: {details['Priority']}")
        else:
            print('\n\tNo item/s in storage\n')
            
    else:
        print('\n\tStorage file not found\n')