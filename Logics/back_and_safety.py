import time

from Utilities import clear_screen

#------------------------------------------------------------------------------------


def input_confirmation():
    """Boilerplate input validation loop for confirming data creation/saves."""
    while True:
        
        choice = input("Are you sure you want to save this assignment? (y/n): ").lower()
        
        # State Return flags: map directly to structural flow breaks in the calling functions
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            time.sleep(1)
            # UX Optimization: targets and erases exactly the error message and the failed input line
            clear_screen.clear_lines_2()
            continue
        
            
#--------------------------------------------------------------------------------------


def delete_confirmation():
    """Boilerplate input validation loop for destructive data changes."""
    while True:
        
        choice = input("Are you sure you want to delete this assignment? (y/n): ").lower()
        
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            time.sleep(1)
            # UX Optimization: targets and erases exactly the error message and the failed input line
            clear_screen.clear_lines_2()
            continue