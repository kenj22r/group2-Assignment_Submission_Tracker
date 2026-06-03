import time

from Utilities import clear_screen
from Logics import navigation, data_match, open_and_save, data_view, back_and_safety, fields_input_validation, clear_and_delete

#--------------------------------------------------------------------------------------------------------------------

def add_assignment():
    """Handles the wizard-style data insertion for a new assignment record."""
    while True:
        while True:
            # Grouped Input Validation: Loops internally until all individual field inputs pass validation rules
            while True:
                Assignment_Title = input("Enter the Assignment Title: ")
                if fields_input_validation.Assignment_Title_Validation(Assignment_Title) == False:
                    continue
                break
                
            while True:
                Subject = input("Enter the Subject: ")
                if fields_input_validation.Subject_Validation(Subject) == False:    
                    continue
                break
                
            while True:    
                Due_Date = input("Enter the Due Date (YYYY-MM-DD): ")
                if fields_input_validation.Due_Date_Validation(Due_Date) == False:
                    continue
                break
                
            while True:    
                Status = input("Enter the Status (Not Started, In Progress, Completed): ")
                if fields_input_validation.Status_Validation(Status) == False:
                    continue
                break
                
            while True:
                Priority = input("Enter the Priority (Low, Medium, High): ")
                if fields_input_validation.Priority_Validation(Priority) == False:
                    continue
                break

            # Core Confirmation Check before data commit
            print()
            confirmation = back_and_safety.input_confirmation()    
            if confirmation == True:
                break
            if confirmation == False:
                clear_screen.clear_screen()
                continue
        
        # IO Commit: Writes validated dataset to database/file
        open_and_save.save_assignment(Assignment_Title, Subject, Due_Date, Status, Priority)
        print()
        
        # Navigation Flag: Controls flow to either run the insertion loop again or exit to main menu
        choice = navigation.continue_or_return()
        if choice == False:
            break
        if choice == True:
            clear_screen.clear_screen()
            continue
        
#-------------------------------------------------------------------------------------- 
    
def update_assignment():
    """Queries an existing record, presents defaults, updates fields, and writes back updates."""
    while True:
        while True:
            data_view.data_view()
            print("\n")
        
            Search_Query = input("Enter the name of the assignment to update: ")
            match_result = data_match.data_match_2(Search_Query)
            
            if match_result:
                matched_key, current_details = match_result
                clear_screen.clear_screen()
                
                while True:    
                    # Field Inline Updates: Displays original value in template string. 
                    # Status '100' indicates blank fallback to original value.
                    while True:
                        current_title = current_details.get("Title", "")
                        New_Title = input(f"Title ({current_title}): ").strip()
                        validation_status = fields_input_validation.New_Title_Input_Validation(New_Title)
                        if validation_status == 100:
                            Updated_Title = current_title
                            break
                        if validation_status == True:
                            Updated_Title = New_Title
                            break
                        if validation_status == False:
                            continue
                        
                    while True:
                        current_subject = current_details.get("Subject", "")
                        new_subject = input(f"Subject ({current_subject}): ").strip()
                        validation_status = fields_input_validation.New_Subject_Input_Validation(new_subject)
                        if validation_status == 100:
                            Updated_Subject = current_subject
                            break
                        if validation_status == True:
                            Updated_Subject = new_subject
                            break
                        if validation_status == False:
                            continue
                        
                    while True:
                        current_due_date = current_details.get("Due_Date", "")
                        new_due_date = input(f"Due Date ({current_due_date}): ").strip()
                        validation_status = fields_input_validation.New_Due_Date_Input_Validation(new_due_date)
                        if validation_status == 100:
                            Updated_Due_Date = current_due_date
                            break
                        if validation_status == True:
                            Updated_Due_Date = new_due_date
                            break
                        if validation_status == False:
                            continue    
                        
                    while True:
                        current_status = current_details.get("Status", "")
                        new_status = input(f"Status ({current_status}): ").strip()
                        validation_status = fields_input_validation.New_Status_Input_Validation(new_status)
                        if validation_status == 100:
                            Updated_Status = current_status
                            break
                        if validation_status == True:
                            Updated_Status = new_status
                            break
                        if validation_status == False:
                            continue
                        
                    while True:
                        current_priority = current_details.get("Priority", "")
                        new_priority = input(f"Priority ({current_priority}): ").strip()
                        validation_status = fields_input_validation.New_Priority_Input_Validation(new_priority)
                        if validation_status == 100:
                            Updated_Priority = current_priority
                            break
                        if validation_status == True:
                            Updated_Priority = new_priority
                            break
                        if validation_status == False:
                            continue
                    
                    # Package dictionary payload for updating
                    final_updated_data = {
                        "Title": Updated_Title,
                        "Subject": Updated_Subject,
                        "Due_Date": Updated_Due_Date,
                        "Status": Updated_Status,
                        "Priority": Updated_Priority
                    }
                    
                    print()
                    confirmation = back_and_safety.input_confirmation()    
                    if confirmation == True:
                        break
                    if confirmation == False:
                        clear_screen.clear_screen()
                        continue
                
            # Query Not Found Routine
            if not match_result:
                choice = navigation.continue_or_return()
                if choice == False:
                    return choice 
                if choice == True:
                    clear_screen.clear_screen()
                    continue
            else:
                break
    
        # Save payload to specific matched record key identifier
        clear_screen.clear_screen()
        open_and_save.Save_Updated_Data(matched_key, final_updated_data)
        print()
        
        choice = navigation.continue_or_return()
        if choice == False:
            break
        if choice == True:
            clear_screen.clear_screen()
            continue
    
#--------------------------------------------------------------------------------------    
    
def view_assignments():
    """Renders table interface directly from global dataset state."""
    data_view.data_view()
    print("\n")
    navigation.return_1()
    
#--------------------------------------------------------------------------------------

def delete_assignment():
    """Branch logic routing user requests into separate contextual deletion services."""
    while True:
        clear_screen.clear_screen()
        choice = input("Press S to delete a specific assignment or C to clear all assignments: ").lower()
        
        # Strategy branch routing
        if choice == 'c':
            clear_and_delete.clear_all()
            break
        elif choice == 's':
            while True:
                clear_and_delete.delete_specific()
                nav_out = navigation.continue_or_return()
                
                if nav_out == True:
                    continue
                if nav_out == False:
                    Flag_out = True  # Break sequence indicator flag
                    break
        else:
            print("Invalid input. Please try again.")
            time.sleep(1)
            clear_screen.clear_screen()
            continue
        
        if Flag_out is True:
            break

#--------------------------------------------------------------------------------------

def search_assignment():
    """Mock/Placeholder entry point for assignment search logic."""
    input_assignment = input("Enter the name of the assignment to search: ")
    print(f"Assignment '{input_assignment}' found!\n")
    navigation.return_or_exit()
    
#--------------------------------------------------------------------------------------

def save_data():
    """Mock/Placeholder event trigger confirming database commits."""
    print("Data saved successfully!\n")
    navigation.return_or_exit()
    
#--------------------------------------------------------------------------------------

def exit_program():
    """Intercepts execution loop to safely shut down shell operations."""
    while True:
        user_input = input("Are you sure you want to exit? (y/n): ").lower()
        
        if user_input == 'y':
            clear_screen.clear_screen()
            print("Exiting the program. Goodbye!")
            time.sleep(1)
            clear_screen.clear_screen()
            exit()
        elif user_input == 'n':
            clear_screen.clear_screen()
            break
        else:
            # Handles bad input by clearing standard logs and running recursion
            clear_screen.clear_lines_3()
            print("Invalid input. Please try again.")
            time.sleep(1)
            clear_screen.clear_lines_3()
            exit_program()