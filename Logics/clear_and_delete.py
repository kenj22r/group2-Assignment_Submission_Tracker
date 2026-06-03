import os
import json
import time

from Utilities.clear_screen import clear_screen
from Logics import navigation
from Utilities import clear_screen
from Logics import back_and_safety
from Logics import data_view

#--------------------------------------------------------------------------------------


def clear_all():
    """Destructive operation that resets the database file back to an empty JSON object."""
    clear_screen.clear_screen()   
        
    while True:    
        choice = input('Are you sure you want to clear all your data? (y/n): ').lower()
        
        if choice == 'y':
            path = os.path.join("Models", "Assignments_Data.json")
            
            # Wipe storage: Overwrites file context entirely with an empty dictionary format {}
            with open(path, "w") as f:
                json.dump({}, f, indent=4) 

            clear_screen.clear_screen()
            print('Storage has been cleared!')
            break
            
        if choice == 'n':
            navigation.return_1()
            
        else:
            print('Wrong input!')
            time.sleep(1)
            clear_screen.clear_lines_2()
            continue
        
        
#--------------------------------------------------------------------------------------


def delete_specific():
    """Locates a single assignment entry by its title property and removes it from state."""
    clear_screen.clear_screen()
    path = os.path.join("Models", "Assignments_Data.json")
          
    while True:
        data_view.data_view()
        print("\n")
    
        target = input("Enter the name of the assignment to delete: ").strip().lower()
        
        # File Read & Exception Management
        data = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("Error: Database file is corrupted.")
                    break
        
        # Linear Search Algorithm: matches case-insensitive string input against 'Title' nested properties
        key_to_delete = None
        for k, details in data.items():
            if details['Title'].lower() == target:
                key_to_delete = k
                break
        
        # Element removal logic
        if key_to_delete:
            print(f"\n---------------------------------\nAssignment '{target}' found.\n---------------------------------\n")
            delete_confirmed = back_and_safety.delete_confirmation()
            
            if delete_confirmed:
                # Modifies runtime dictionary state, then overwrites database changes to local disk
                del data[key_to_delete]
                with open(path, "w") as f:
                    json.dump(data, f, indent=4)       
                
                clear_screen.clear_screen()
                print(f"Assignment '{target}' deleted successfully!\n")
                break
            else:
                clear_screen.clear_screen()
                print("Deletion canceled.")
                break
        else:
            print(f"\n---------------------------------\nAssignment '{target}' not found.\n---------------------------------\n")
            break