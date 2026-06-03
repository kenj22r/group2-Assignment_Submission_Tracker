import time
from Utilities import clear_screen

#-------------------------------------------------------------------------------------


def return_or_exit():
    """Terminal routing switch: Terminates process tree or yields flow back to previous menu."""
    user_input = input("Press r for return and e for exit: ").lower()
    
    if user_input == 'e':
        print("Exiting the program. Goodbye!")
        time.sleep(1)
        clear_screen.clear_screen()
        exit()
        
    elif user_input == 'r':
        clear_screen.clear_screen()
        return
    
    else:
        print("Invalid input. Please try again.")
        time.sleep(1)
        clear_screen.clear_lines_2()
        # Direct Tail Recursion: Loops back safely until a valid string matches criteria
        return return_or_exit()
        
        
#--------------------------------------------------------------------------------------


def continue_or_return():
    """Loop Control Selector: Translates interactive input strings into functional binary flags."""
    user_input = input("Press c for continue and r for return: ").lower()
    
    if user_input == 'c':
        clear_screen.clear_screen()
        return True
        
    elif user_input == 'r':
        clear_screen.clear_screen()
        return False
    
    else:
        print("Invalid input. Please try again.")
        time.sleep(1)
        clear_screen.clear_lines_2()
        return continue_or_return()
    
    
#--------------------------------------------------------------------------------------


def return_1():
    """Interactive Blocker: Freezes output state onscreen until user requests structural return."""
    user_input = input("Press r for return: ").lower()
    
    if user_input == 'r':
        clear_screen.clear_screen()
        return
    
    else:
        print("Invalid input. Please try again.")
        time.sleep(1)
        clear_screen.clear_lines_2()
        return return_1()
    
    
#--------------------------------------------------------------------------------------


def continue_or_next():
    """Context Switcher: Returns boolean flag to advance data wizard or keep current contextual stream."""
    user_input = input("Press c for continue and n for next: ").lower()
    
    if user_input == 'c':
        return True
        
    elif user_input == 'n':
        return False
    
    else:
        print("Invalid input. Please try again.")
        time.sleep(1)
        clear_screen.clear_lines_2()
        return continue_or_next()