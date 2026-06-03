from Interfaces import main_interface
from Logics import main_menu_option
from Utilities import clear_screen

if __name__ == "__main__":
    
    # Initialize the console terminal with a clean slate on startup
    clear_screen.clear_screen()
    
#----------------------- MAIN PROGRAM LOOP ------------------------------------------
    
    # Infinite loop to keep the Command Line Interface (CLI) application running
    while True:
        
        # Display the visual menu options to the user
        main_interface.main_menu() 
        
        # Capture user input and execute the corresponding logic/feature
        main_menu_option.handle_main_menu_option()
        
        # Clear the terminal screen before the next loop iteration to refresh the UI
        clear_screen.clear_screen()