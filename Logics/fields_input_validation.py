import time
from Logics import data_match

def Assignment_Title_Validation(Assignment_Title):
    """
    Sanitizes and checks assignment titles against length limits, 
    illegal characters, reserved words, and database duplicates.
    """
    if Assignment_Title.strip() == "":
        return False, "❌ Assignment Title cannot be empty."
    if len(Assignment_Title) > 50:
        return False, "❌ Title cannot exceed 50 characters."
    
    # Character Whitelist: Restricts titles to alphanumeric characters and spaces only
    if not all(c.isalnum() or c.isspace() for c in Assignment_Title):
        return False, "❌ Title can only contain letters, numbers, and spaces."
    
    # Reserved Words Protection: Prevents conflicts with system enums
    if Assignment_Title in ["Not Started", "In Progress", "Completed"]:
        return False, "❌ Title cannot be the same as a status."
    if Assignment_Title in ["Low", "Medium", "High"]:
        return False, "❌ Title cannot be the same as a priority."
    
    # Database Uniqueness Check: Queries data module to prevent key collisions
    if data_match.data_match(Assignment_Title) == True:
        return False, "❌ Assignment Title already exists."
        
    return True, ""

def Subject_Validation(Subject):
    """Validates subject names against blank spaces, length limits, and formatting rules."""
    if Subject.strip() == "":
        return False, "❌ Subject cannot be empty."
    if len(Subject) > 50:
        return False, "❌ Subject cannot exceed 50 characters."
    if not all(c.isalnum() or c.isspace() for c in Subject):
        return False, "❌ Subject can only contain letters, numbers, and spaces."
    return True, ""

def Due_Date_Validation(Due_Date):
    """
    Uses python 'time' struct pattern matching to ensure string dates 
    can safely convert into valid ISO calendar dates.
    """
    try:
        # Strict Pattern Match: Throws a ValueError if input is not a real date or misses format tokens
        time.strptime(Due_Date, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "❌ Must be in the format YYYY-MM-DD."