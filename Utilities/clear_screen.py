import os
import sys

#-----------------------------------------------------------------


def clear_screen():
    # Cross-platform environment check: handles command differences between Windows (nt) and UNIX variants
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
        
#------------------------------------------------------------------       
        
        
def clear_lines_4(count=4):
    """Removes a specific number of lines from the terminal."""
    for _ in range(count):
        # ANSI Escape Codes: \033[1A moves the cursor up one row; \033[2K erases the entire row content
        sys.stdout.write("\033[1A\033[2K")
    sys.stdout.flush()
        
        
#-------------------------------------------------------------------      
        
        
def clear_lines_3(count=3):
    """Removes a specific number of lines from the terminal."""
    for _ in range(count):
        # ANSI Escape Codes: Moves cursor up and deletes the line
        sys.stdout.write("\033[1A\033[2K")
    sys.stdout.flush()
    
    
#-------------------------------------------------------------------    
    
    
def clear_lines_2(count=2):
    """Removes a specific number of lines from the terminal."""
    for _ in range(count):
        # ANSI Escape Codes: Moves cursor up and deletes the line
        sys.stdout.write("\033[1A\033[2K")
    sys.stdout.flush()
    
    
#-------------------------------------------------------------------    
    
def clear_lines_1():
    # Single line optimization: Uses print with end="" to instantly trigger inline ANSI cleanup without adding a newline
    print("\033[1A\033[2K", end="")
    sys.stdout.flush()