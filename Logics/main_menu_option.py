import tracker

from Utilities import clear_screen

#--------------------------------------------


def handle_main_menu_option():
    """
    Acts as the application's central traffic controller. 
    Parses user input and routes execution to the appropriate module feature.
    """
    option = input("Select an option: ")
    clear_screen.clear_screen()
    
    # Structural Pattern Matching: Evaluates user choices cleanly without heavy if-elif chains
    match option:
        
        case "1":
            tracker.add_assignment()
            
        case "2":
            tracker.view_assignments()
            
        case "3":
            tracker.update_assignment()
            
        case "4":
            tracker.delete_assignment()
            
        case "5":
            tracker.exit_program()           
            
        case _:
            # Wildcard Catch-All: Handles fallback logic for unrecognized menu inputs
            print("Invalid option.")