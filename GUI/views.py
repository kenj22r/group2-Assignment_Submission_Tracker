import customtkinter as ctk
import os
import json
import calendar
from datetime import datetime
from PIL import Image
from tkinter import messagebox

# Import external logic components for handling file read/writes and inputs
from Logics.open_and_save import save_assignment, full_path, Save_Updated_Data
from Logics.fields_input_validation import (
    Assignment_Title_Validation, 
    Subject_Validation, 
    Due_Date_Validation
)


# =====================================================================
# 1. CALENDAR PICKER COMPONENT
# =====================================================================
class CalendarPicker(ctk.CTkToplevel):
    """
    A custom pop-up window that creates a small calendar interface.
    It allows users to visually select a due date for assignments.
    """
    def __init__(self, parent, callback_target, on_close_callback=None):
        super().__init__(parent)
        
        # Save reference hooks for exchanging data and managing window reset states
        self.callback_target = callback_target
        self.on_close_callback = on_close_callback
        
        # Track the currently displayed year and month
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        # Window configuration settings
        self.overrideredirect(True)       # Removes standard OS window borders/title bar
        self.attributes("-topmost", True) # Forces the popup to stay on top
        self.title("Select Due Date")
        self.geometry("300x320")
        self.resizable(False, False)
        self.lift()                       # Bring window to front
        self.focus_force()                # Force focus onto the calendar
        
        # Grid layout configuration for header and calendar days
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # --- Calendar Navigation Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, pady=10, sticky="ew")
        
        # Button to switch to the previous month
        prev_btn = ctk.CTkButton(
            header, text="◀", width=30, 
            fg_color="#ff7b25", hover_color="#5c2a0b", corner_radius=15, 
            command=self.prev_month
        )
        prev_btn.pack(side="left", padx=15)
        
        # Label displaying the current Month Name and Year
        self.month_lbl = ctk.CTkLabel(header, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.month_lbl.pack(side="left", expand=True)
        
        # Button to switch to the next month
        next_btn = ctk.CTkButton(
            header, text="▶", width=30, 
            fg_color="#ff7b25", hover_color="#5c2a0b", corner_radius=15, 
            command=self.next_month
        )
        next_btn.pack(side="left", padx=15)
        
        # --- Days Grid Frame Container ---
        self.grid_frame = ctk.CTkFrame(self, corner_radius=12)
        self.grid_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Call method to draw calendar grids initially
        self.draw_calendar()

    def prev_month(self):
        """Moves the calendar back by one month."""
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    def next_month(self):
        """Moves the calendar forward by one month."""
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()

    def draw_calendar(self):
        """Generates and draws grid layout buttons representing days of the month."""
        # Clean up any existing buttons/labels from previous views
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        # Display month name string in top header label
        self.month_lbl.configure(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        
        # Render days-of-the-week standard label headers
        headers = ["M", "T", "W", "T", "F", "S", "S"]
        for col, day_name in enumerate(headers):
            self.grid_frame.grid_columnconfigure(col, weight=1, uniform="eq")
            lbl = ctk.CTkLabel(self.grid_frame, text=day_name, text_color="gray", font=ctk.CTkFont(size=11, weight="bold"))
            lbl.grid(row=0, column=col, pady=2)
            
        # Fetch month matrix data array from standard calendar library
        cal_matrix = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Loop through rows (weeks) and columns (days) to construct buttons
        for r_idx, week in enumerate(cal_matrix):
            self.grid_frame.grid_rowconfigure(r_idx + 1, weight=1, uniform="eq")
            for c_idx, day in enumerate(week):
                if day == 0:
                    continue  # Skip blank days outside of current month frame boundary
                    
                # Format string as YYYY-MM-DD
                date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                
                # Render standalone day button item
                day_btn = ctk.CTkButton(
                    self.grid_frame, text=str(day), width=25, height=25,
                    fg_color="#1e1e1e", text_color="white", hover_color="#3a3a3a", corner_radius=6, 
                    command=lambda d=date_str: self.date_selected(d)
                )
                day_btn.grid(row=r_idx + 1, column=c_idx, padx=2, pady=2, sticky="nsew")
        
    def destroy(self):
        """Safely clean up hook references when window is completely closed."""
        if self.on_close_callback:
            self.on_close_callback()
        super().destroy()

    def date_selected(self, date_str):
        """Sends chosen date info back to form entry and terminates widget view."""
        self.callback_target(date_str)
        self.destroy()    


# =====================================================================
# 2. SUBMIT WORK DIALOG WINDOW
# =====================================================================
class SubmitWorkDialog(ctk.CTkToplevel):
    """
    A pop-up modal view allowing users to append a digital submission link 
    or notes description to turn in an assignment.
    """
    def __init__(self, parent, assignment_key, current_data, refresh_callback):
        super().__init__(parent)
        self.assignment_key = assignment_key
        self.current_data = current_data
        self.refresh_callback = refresh_callback
        
        # Basic modal properties
        self.title(f"Submit Assignment: {current_data.get('Title')}")
        self.geometry("420x240")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        self.grab_set() # Prevents interaction with main dashboard until resolved
        
        self.grid_columnconfigure(0, weight=1)
        
        # Header text labels
        ctk.CTkLabel(self, text="🚀 Submit", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=15)
        ctk.CTkLabel(self, text="Paste your assignment submission URL link or note below:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        # URL link text input entry bar
        self.submission_entry = ctk.CTkEntry(
            self, width=380, corner_radius=10, 
            placeholder_text="e.g., Google Drive Link or Note Description"
        )
        self.submission_entry.grid(row=2, column=0, padx=20, pady=10)
        self.submission_entry.focus()
        
        # Lower control buttons arrangement layout structure
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=3, column=0, pady=15, padx=20, sticky="e")
        
        turn_in_btn = ctk.CTkButton(
            action_frame, text="🚀 Turn It In", fg_color="#64dd17", hover_color="#1b5e20", 
            text_color="white", font=ctk.CTkFont(weight="bold"), corner_radius=15, 
            command=self.confirm_submission
        )
        turn_in_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            action_frame, text="Cancel", fg_color="gray", hover_color="#1c1c1c",
            corner_radius=15, command=self.destroy
        )
        cancel_btn.pack(side="left")

    def confirm_submission(self):
        """Processes text data input, sets properties status, updates data logs and refreshes dashboard."""
        work_payload = self.submission_entry.get().strip()
        if not work_payload:
            work_payload = "Submitted successfully"
            
        # Alter local tracking dataset entries dictionary parameters
        self.current_data["Status"] = "Completed"
        self.current_data["Submission_Link"] = work_payload
        self.current_data["Submitted_At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Persist data saves to file location storage systems and clear window states
        Save_Updated_Data(self.assignment_key, self.current_data)
        self.refresh_callback()
        self.destroy()


# =====================================================================
# 3. UPDATE DETAILS DIALOG WINDOW
# =====================================================================
class UpdateDialog(ctk.CTkToplevel):
    """
    A pop-up modal interface form that enables modifying existing assignments 
    and validates changed field inputs.
    """
    def __init__(self, parent, assignment_key, current_data, refresh_callback):
        super().__init__(parent)
        self.assignment_key = assignment_key
        self.current_data = current_data
        self.refresh_callback = refresh_callback
        self.calendar_window = None
        
        # Window configurations
        self.title("Modify Tracked Assignment Details")
        self.geometry("460x460")
        self.resizable(False, False)
        self.lift()
        self.focus_force()
        self.grab_set() 
        
        self.grid_columnconfigure(1, weight=1)
        
        # Title Label Header
        ctk.CTkLabel(self, text="Update Assignment Settings", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # --- Title Input Block ---
        ctk.CTkLabel(self, text="Assignment Title:").grid(row=1, column=0, padx=20, pady=(10,0), sticky="e")
        self.title_entry = ctk.CTkEntry(self, width=220, corner_radius=10, placeholder_text="Enter assignment title")
        self.title_entry.grid(row=1, column=1, padx=20, pady=(10,0), sticky="w")
        self.title_entry.insert(0, current_data.get("Title", ""))
        
        self.title_err_lbl = ctk.CTkLabel(self, text="", text_color="#ff5757", font=ctk.CTkFont(size=11))
        self.title_err_lbl.grid(row=2, column=1, padx=20, pady=(0,5), sticky="w")
        
        # --- Subject Input Block ---
        ctk.CTkLabel(self, text="Subject:").grid(row=3, column=0, padx=20, pady=(5,0), sticky="e")
        self.subject_entry = ctk.CTkEntry(self, width=220, corner_radius=10, placeholder_text="Enter subject")
        self.subject_entry.grid(row=3, column=1, padx=20, pady=(5,0), sticky="w")
        self.subject_entry.insert(0, current_data.get("Subject", ""))
        
        self.subject_err_lbl = ctk.CTkLabel(self, text="", text_color="#ff5757", font=ctk.CTkFont(size=11))
        self.subject_err_lbl.grid(row=4, column=1, padx=20, pady=(0,5), sticky="w")
        
        # --- Due Date Calendar Input Block ---
        ctk.CTkLabel(self, text="Due Date (YYYY-MM-DD):").grid(row=5, column=0, padx=20, pady=(5,0), sticky="e")
        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.grid(row=5, column=1, padx=20, pady=(5,0), sticky="w")
        
        self.due_entry = ctk.CTkEntry(date_frame, width=140, corner_radius=10, placeholder_text="YYYY / MM / DD")
        self.due_entry.pack(side="left", padx=(0, 5))
        self.due_entry.insert(0, current_data.get("Due_Date", ""))
        
        self.cal_btn = ctk.CTkButton(
            date_frame, text="📅", width=40, fg_color="#3a3a3a", hover_color="#5c5c5c", 
            corner_radius=10, command=self.popup_calendar
        )
        self.cal_btn.pack(side="left")
        
        self.due_err_lbl = ctk.CTkLabel(self, text="", text_color="#ff5757", font=ctk.CTkFont(size=11))
        self.due_err_lbl.grid(row=6, column=1, padx=20, pady=(0,5), sticky="w")
        
        # --- Status Option Menus ---
        ctk.CTkLabel(self, text="Status:").grid(row=7, column=0, padx=20, pady=10, sticky="e")
        self.status_dropdown = ctk.CTkOptionMenu(
            self, values=["Select Status", "Not Started", "In Progress", "Completed"],
            button_color="#424242", button_hover_color="#5c5c5c", fg_color="#2d2d2d", width=220, corner_radius=10
        )
        self.status_dropdown.grid(row=7, column=1, padx=20, pady=10, sticky="w")
        self.status_dropdown.set(current_data.get("Status", "Select Status"))
        
        # --- Priority Option Menus ---
        ctk.CTkLabel(self, text="Priority:").grid(row=8, column=0, padx=20, pady=10, sticky="e")
        self.priority_dropdown = ctk.CTkOptionMenu(
            self, values=["Select Priority", "Low", "Medium", "High"],
            button_color="#424242", button_hover_color="#5c5c5c", fg_color="#2d2d2d", width=220, corner_radius=10
        )
        self.priority_dropdown.grid(row=8, column=1, padx=20, pady=10, sticky="w")
        self.priority_dropdown.set(current_data.get("Priority", "Select Priority"))
        
        # --- Control Form Lower Actions Buttons Bar ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=9, column=1, padx=20, pady=20, sticky="w")
        
        self.save_btn = ctk.CTkButton(
            btn_frame, text="Save Changes", fg_color="#fab333", text_color="#1f1f1f", 
            font=ctk.CTkFont(weight="bold"), width=100, corner_radius=15, command=self.apply_updates
        )
        self.save_btn.pack(side="left", padx=(0,10))
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame, text="Cancel", fg_color="#545454", hover_color="#6D6C6C", 
            width=100, corner_radius=15, command=self.destroy
        )
        self.cancel_btn.pack(side="left")
        
        # Standalone logging message output frame block
        self.global_status_lbl = ctk.CTkLabel(self, text="", text_color="yellow")
        self.global_status_lbl.grid(row=10, column=1, padx=20, sticky="w")

        # Simplified focus navigation system instead of inline complex lambda definitions
        self.title_entry.bind("<Return>", self.step_title)
        self.subject_entry.bind("<Return>", self.step_subject)
        self.due_entry.bind("<Return>", self.step_due)

    def popup_calendar(self):
        """Calculates precise system window overlay alignment positioning coordinates to mount calendar dropdowns."""
        if self.calendar_window is not None and self.calendar_window.winfo_exists():
            self.calendar_window.destroy()
            self.calendar_window = None
            return

        self.update_idletasks()
        
        try:
            btn_x = self.cal_btn.winfo_rootx() 
            btn_y = self.cal_btn.winfo_rooty()
            btn_height = self.cal_btn.winfo_height()
            
            # Math Offset coordinates parameters rules calculation
            spawn_x = btn_x - 240
            spawn_y = btn_y + btn_height + 5
        except Exception:
            # Safe Fallbacks alignments settings parameters defaults
            spawn_x = self.winfo_rootx() + 80
            spawn_y = self.winfo_rooty() + 200

        # Create callback targets handlers cleanly
        def handle_date(date_string):
            self.due_entry.delete(0, 'end')
            self.due_entry.insert(0, date_string)

        self.calendar_window = CalendarPicker(self, callback_target=handle_date)
        self.calendar_window.geometry(f"300x320+{spawn_x}+{spawn_y}")
        self.calendar_window.transient(self)
        self.calendar_window.lift()

    # --- Simplified Step-by-Step Validation Focus Handlers ---
    def step_title(self, event):
        val = self.title_entry.get().strip()
        is_valid, err = Assignment_Title_Validation(val)
        if not is_valid and "already exists" in err and val.lower() == self.current_data.get("Title", "").lower():
            is_valid, err = True, ""
        if not is_valid:
            self.title_err_lbl.configure(text=err)
            return
        self.title_err_lbl.configure(text="")
        self.subject_entry.focus()

    def step_subject(self, event):
        val = self.subject_entry.get().strip()
        is_valid, err = Subject_Validation(val)
        if not is_valid:
            self.subject_err_lbl.configure(text=err)
            return
        self.subject_err_lbl.configure(text="")
        self.due_entry.focus()

    def step_due(self, event):
        val = self.due_entry.get().strip()
        is_valid, err = Due_Date_Validation(val)
        if not is_valid:
            self.due_err_lbl.configure(text=err)
            return
        self.due_err_lbl.configure(text="")
        self.status_dropdown.focus()

    def apply_updates(self):
        """Gathers altered text forms inputs details data entries fields and updates JSON records safely."""
        title = self.title_entry.get().strip()
        subject = self.subject_entry.get().strip()
        due_date = self.due_entry.get().strip()
        status = self.status_dropdown.get()
        priority = self.priority_dropdown.get()
        
        # Validations processing tracks logic check pipelines
        title_ok, title_msg = Assignment_Title_Validation(title)
        if not title_ok and "already exists" in title_msg and title.lower() == self.current_data.get("Title", "").lower():
            title_ok, title_msg = True, ""
            
        sub_ok, sub_msg = Subject_Validation(subject)
        due_ok, due_msg = Due_Date_Validation(due_date)
        status_ok = (status != "Select Status")
        priority_ok = (priority != "Select Priority")
        
        self.title_err_lbl.configure(text=title_msg if not title_ok else "")
        self.subject_err_lbl.configure(text=sub_msg if not sub_ok else "")
        self.due_err_lbl.configure(text=due_msg if not due_ok else "")
        
        # Halt execution paths flow if inputs fails checks criteria validations definitions
        if not (title_ok and sub_ok and due_ok and status_ok and priority_ok):
            self.global_status_lbl.configure(text="❌ Complete all fields correctly.", text_color="#ff5757")
            return
            
        updated_dict = {
            "Title": title,
            "Subject": subject,
            "Due_Date": due_date,
            "Status": status,
            "Priority": priority,
            "Submission_Link": self.current_data.get("Submission_Link", ""),
            "Submitted_At": self.current_data.get("Submitted_At", "")
        }
        
        try:
            Save_Updated_Data(self.assignment_key, updated_dict)
            self.refresh_callback()
            self.destroy()
        except Exception as e:
            self.global_status_lbl.configure(text=f"❌ Error: {str(e)}", text_color="#ff5757")


# =====================================================================
# 4. MAIN DASHBOARD FRAME VIEW COMPONENT
# =====================================================================
class DashboardFrame(ctk.CTkFrame):
    """
    The core frame layout interface view containing the toolbar controls panels, 
    scrollable frames list container fields cards and addition forms panels canvas logs blocks.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.calendar_window = None
        
        # Initialize default interface custom text fonts parameters configurations templates sets
        self.setup_fonts()
        
        # Layout weights tracks systems
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Primary visual bounding frame board layout structural containment grids panel boards sheets
        self.main_container = ctk.CTkFrame(
            self, corner_radius=30, fg_color="#1e1e1e", border_width=1, border_color="#2b2b2b"
        )
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)
        
        # Core Header Label View Title bar anchor items details
        self.title_label = ctk.CTkLabel(
            self.main_container, text="Assignment Submission Dashboard", font=self.font_bold_lg
        )
        self.title_label.grid(row=0, column=0, pady=(30, 15), padx=90, sticky="w")
        
        # Initialize control toolbars buttons structures layouts configurations panels layers
        self.setup_control_panel()
        
        # Sub-tabs frames overlay container views canvas structures panel
        self.tabview_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.tabview_container.grid(row=2, column=0, padx=30, pady=(10, 30), sticky="nsew")
        self.tabview_container.grid_columnconfigure(0, weight=1)
        self.tabview_container.grid_rowconfigure(0, weight=1)
        
        # Build views components elements systems
        self.build_view_assignments_layout()
        self.build_add_assignment_layout()
        
        # Load dashboard assignments view states components
        self.show_view_tab()

    def setup_fonts(self):
        """Defines font family styles and mappings configurations templates standards fields."""
        font_family = "Glacial Indifference"
        
        self.font_bold_lg = ctk.CTkFont(family=font_family, size=25, weight="bold")
        self.font_bold_md = ctk.CTkFont(family=font_family, size=20, weight="bold")
        self.font_bold_sm = ctk.CTkFont(family=font_family, size=13, weight="bold")
        self.font_reg_md = ctk.CTkFont(family=font_family, size=14, weight="normal")
        self.font_reg_sm = ctk.CTkFont(family=font_family, size=12, weight="normal")

    def setup_control_panel(self):
        """Constructs top task management actions control buttons toolbar systems layout items."""
        # Simple step-by-step descriptive absolute file directory path resolution logic rules structures
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        add_icon_path = os.path.join(root_dir, "assets", "Add_icon.png")
        refresh_icon_path = os.path.join(root_dir, "assets", "Refresh_icon.png")

        try:
            self.icon_add = ctk.CTkImage(light_image=Image.open(add_icon_path), dark_image=Image.open(add_icon_path), size=(14, 14))
            self.icon_refresh = ctk.CTkImage(light_image=Image.open(refresh_icon_path), dark_image=Image.open(refresh_icon_path), size=(14, 14))
        except Exception as e:
            print(f"⚠️ Top Navbar Icon Loading Error: {e}")
            self.icon_add = None
            self.icon_refresh = None
        
        controls_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        controls_frame.grid(row=1, column=0, padx=35, pady=5, sticky="ew")
        
        # Navigation toggle switch link trigger command button panels item settings layout canvas
        self.add_nav_btn = ctk.CTkButton(
            controls_frame, text="  Add", image=self.icon_add, compound="right", 
            fg_color="#29b6f6", hover_color="#3087ba", text_color="white",
            font=self.font_bold_sm, width=100, height=36, corner_radius=18, anchor="w",
            command=self.show_add_tab
        )
        self.add_nav_btn.pack(side="left", padx=(0, 12))
        
        # Refresh operational sync updates dashboard actions button trigger parameters mapping
        self.refresh_btn = ctk.CTkButton(
            controls_frame, text="Refresh", image=self.icon_refresh, compound="right",
            fg_color="#ff7b25", hover_color="#aa4e15", text_color="white",
            font=self.font_bold_sm, width=110, height=36, corner_radius=18,
            command=self.load_assignments
        )
        self.refresh_btn.pack(side="left", padx=(0, 30))
        
        # Simplified operational filter switch handler callback workflow function routing link map
        def handle_filter_switch(value):
            self.show_view_tab()
            self.load_assignments()

        self.segment_filter = ctk.CTkSegmentedButton(
            controls_frame, values=["All", "Unsubmitted", "Submitted", "Pending"],
            font=self.font_bold_sm, selected_color="#626262", unselected_color="#1f1f1f",
            height=36, corner_radius=18, command=handle_filter_switch
        )
        self.segment_filter.pack(side="left", fill="x", expand=True)
        self.segment_filter.set("All")

    def build_view_assignments_layout(self):
        """Constructs scrollable assignment container canvas layout field sets panels frameworks logs."""
        self.view_tab_frame = ctk.CTkFrame(self.tabview_container, fg_color="transparent")
        self.view_tab_frame.grid_columnconfigure(0, weight=1)
        self.view_tab_frame.grid_rowconfigure(0, weight=1)
        
        self.scroll_container = ctk.CTkScrollableFrame(
            self.view_tab_frame, fg_color="#121212", corner_radius=24,
            scrollbar_fg_color="transparent",                
            scrollbar_button_color="#1f1f1f",               
            scrollbar_button_hover_color="#424242"          
        )
        self.scroll_container.grid(row=0, column=0, sticky="nsew")

    def build_add_assignment_layout(self):
        """Generates clear grid data entry form fields inputs sheets mapping panel containers views canvas layers."""
        self.add_tab_frame = ctk.CTkFrame(self.tabview_container, fg_color="#121212", corner_radius=24)
        self.add_tab_frame.grid_columnconfigure(0, weight=1)
        self.add_tab_frame.grid_rowconfigure(1, weight=1) 
        
        self.form_wrapper = ctk.CTkFrame(self.add_tab_frame, fg_color="transparent")
        self.form_wrapper.grid_columnconfigure(0, weight=0) 
        self.form_wrapper.grid_columnconfigure(1, weight=0) 

        # --- Return Button Action Navigator Anchor ---
        back_btn = ctk.CTkButton(
            self.add_tab_frame, text="Back to Dashboard", fg_color="#2d2d2d", hover_color="#424242",       
            text_color="White", font=self.font_bold_sm, width=160, height=34, corner_radius=17,            
            command=self.show_view_tab
        )
        back_btn.grid(row=0, column=0, columnspan=2, padx=(100, 35), pady=(30, 10), sticky="w")
        
        # --- Form Row Item: Title Form Text Field Inputs Blocks ---
        ctk.CTkLabel(self.form_wrapper, text="Assignment Title:", font=self.font_reg_md).grid(row=1, column=0, padx=(0, 15), pady=(10,0), sticky="e")
        self.title_entry = ctk.CTkEntry(self.form_wrapper, width=300, corner_radius=10, font=self.font_reg_md, placeholder_text="Enter assignment title")
        self.title_entry.grid(row=1, column=1, padx=(15, 0), pady=(10,0), sticky="w")
        
        self.title_err_lbl = ctk.CTkLabel(self.form_wrapper, text="", text_color="#ff5757", font=self.font_reg_sm)
        self.title_err_lbl.grid(row=2, column=1, padx=(15, 0), pady=(0,5), sticky="w")
        
        # --- Form Row Item: Subject Text Fields Input Forms Blocks ---
        ctk.CTkLabel(self.form_wrapper, text="Subject:", font=self.font_reg_md).grid(row=3, column=0, padx=(0, 15), pady=(5,0), sticky="e")
        self.subject_entry = ctk.CTkEntry(self.form_wrapper, width=300, corner_radius=10, font=self.font_reg_md, placeholder_text="Enter subject")
        self.subject_entry.grid(row=3, column=1, padx=(15, 0), pady=(5,0), sticky="w")
        
        self.subject_err_lbl = ctk.CTkLabel(self.form_wrapper, text="", text_color="#ff5757", font=self.font_reg_sm)
        self.subject_err_lbl.grid(row=4, column=1, padx=(15, 0), pady=(0,5), sticky="w")
        
        # --- Form Row Item: Due Date Text Input Calendars Picker Overlay Overlay ---
        ctk.CTkLabel(self.form_wrapper, text="Due Date:", font=self.font_reg_md).grid(row=5, column=0, padx=(0, 15), pady=(5,0), sticky="e")
        date_input_frame = ctk.CTkFrame(self.form_wrapper, fg_color="transparent")
        date_input_frame.grid(row=5, column=1, padx=(15, 0), pady=(5,0), sticky="w")
        
        self.due_entry = ctk.CTkEntry(date_input_frame, width=240, corner_radius=10, font=self.font_reg_md, placeholder_text="YYYY / MM / DD")
        self.due_entry.pack(side="left", padx=(0, 5))
        
        self.calendar_pop_btn = ctk.CTkButton(
            date_input_frame, text="📅", width=55, fg_color="#2d2d2d", hover_color="#5c5c5c",
            corner_radius=10, command=self.popup_add_calendar
        )
        self.calendar_pop_btn.pack(side="left")
        
        self.due_err_lbl = ctk.CTkLabel(self.form_wrapper, text="", text_color="#ff5757", font=self.font_reg_sm)
        self.due_err_lbl.grid(row=6, column=1, padx=(15, 0), pady=(0,5), sticky="w")
        
        # --- Form Row Item: Status Options and Priority Level Settings Pickers Lists ---
        ctk.CTkLabel(self.form_wrapper, text="Status & Priority:", font=self.font_reg_md).grid(row=7, column=0, padx=(0, 15), pady=10, sticky="e")
        dropdown_frame = ctk.CTkFrame(self.form_wrapper, fg_color="transparent")
        dropdown_frame.grid(row=7, column=1, padx=(15, 0), pady=10, sticky="w")
        
        self.status_dropdown = ctk.CTkOptionMenu(
            dropdown_frame, values=["None", "Not Started", "In Progress", "Completed"],
            fg_color="#2d2d2d", button_color="#424242", button_hover_color="#5c5c5c",
            dropdown_fg_color="#3a3a3a", width=160, corner_radius=10, font=self.font_reg_md
        )
        self.status_dropdown.pack(side="left", padx=(0, 10))
        self.status_dropdown.set("Select Status")
        
        self.priority_dropdown = ctk.CTkOptionMenu(
            dropdown_frame, values=["None", "Low", "Medium", "High"],
            fg_color="#2d2d2d", button_color="#424242", button_hover_color="#5c5c5c",
            dropdown_fg_color="#3a3a3a", width=160, corner_radius=10, font=self.font_reg_md
        )
        self.priority_dropdown.pack(side="left")
        self.priority_dropdown.set("Select Priority")
        
        # --- Form Submission Execution Action Buttons Controllers logs ---
        self.submit_btn = ctk.CTkButton(
            self.form_wrapper, text="Save Assignment", fg_color="#7ed957", text_color="white", 
            font=self.font_bold_sm, corner_radius=15, height=38, command=self.submit_form
        )
        self.submit_btn.grid(row=8, column=1, padx=(15, 0), pady=25, sticky="w")
        
        self.global_status_lbl = ctk.CTkLabel(self.form_wrapper, text="", text_color="#ffc107", font=self.font_reg_md)
        self.global_status_lbl.grid(row=9, column=1, padx=(15, 0), sticky="w")

        # Simplified binding event processing hooks maps loops structures tracks instead of lambdas
        self.title_entry.bind("<Return>", self.process_title_step)
        self.subject_entry.bind("<Return>", self.process_subject_step)
        self.due_entry.bind("<Return>", self.process_due_step)

        self.grid_columnconfigure(0, weight=1)
        self.form_wrapper.grid(row=1, column=0, padx=80, pady=10)
        
    def show_view_tab(self):
        """Displays primary card items view records canvas panels boards."""
        self.add_tab_frame.grid_remove()
        self.view_tab_frame.grid(row=0, column=0, sticky="nsew")
        self.load_assignments()

    def show_add_tab(self):
        """Switches frames visible views configuration to form inputs sheets entries canvas."""
        self.view_tab_frame.grid_remove()
        self.add_tab_frame.grid(row=0, column=0, sticky="nsew")

    def popup_add_calendar(self):
        """Calculates screen coordinate positioning tracking vectors overlays to dynamically pin calendars pickers boxes."""
        if self.calendar_window is not None and self.calendar_window.winfo_exists():
            self.calendar_window.destroy()
            return

        self.calendar_pop_btn.configure(fg_color="#ff7b25", text_color="white")
        
        def reset_button_state():
            self.calendar_window = None
            self.calendar_pop_btn.configure(fg_color="#2d2d2d", text_color="white")

        btn_x = self.calendar_pop_btn.winfo_rootx()
        btn_y = self.calendar_pop_btn.winfo_rooty()
        btn_height = self.calendar_pop_btn.winfo_height()

        spawn_x = btn_x - 150  
        spawn_y = btn_y + btn_height + 5  

        def append_date_to_form(date_string):
            self.due_entry.delete(0, 'end')
            self.due_entry.insert(0, date_string)

        self.calendar_window = CalendarPicker(
            self, callback_target=append_date_to_form, on_close_callback=reset_button_state
        )
        self.calendar_window.geometry(f"300x320+{spawn_x}+{spawn_y}")

    # --- Simplified Step Focus Return Input Form Handlers ---
    def process_title_step(self, event):
        val = self.title_entry.get().strip()
        is_valid, error_msg = Assignment_Title_Validation(val)
        if not is_valid:
            self.title_err_lbl.configure(text=error_msg)
            return
        self.title_err_lbl.configure(text="") 
        self.subject_entry.focus()           

    def process_subject_step(self, event):
        val = self.subject_entry.get().strip()
        is_valid, error_msg = Subject_Validation(val)
        if not is_valid:
            self.subject_err_lbl.configure(text=error_msg)
            return
        self.subject_err_lbl.configure(text="")
        self.due_entry.focus()               

    def process_due_step(self, event):
        val = self.due_entry.get().strip()
        is_valid, error_msg = Due_Date_Validation(val)
        if not is_valid:
            self.due_err_lbl.configure(text=error_msg)
            return
        self.due_err_lbl.configure(text="")
        self.status_dropdown.focus() 

    def submit_form(self):
        """Processes validated form item records inputs text strings, executing files writes routines dumps."""
        title = self.title_entry.get().strip()
        subject = self.subject_entry.get().strip()
        due_date = self.due_entry.get().strip()
        status = self.status_dropdown.get()
        priority = self.priority_dropdown.get()
        
        title_ok, title_msg = Assignment_Title_Validation(title)
        sub_ok, sub_msg = Subject_Validation(subject)
        due_ok, due_msg = Due_Date_Validation(due_date)
        status_ok = (status != "-- Select Status --")
        priority_ok = (priority != "-- Select Priority --")
        
        self.title_err_lbl.configure(text=title_msg if not title_ok else "")
        self.subject_err_lbl.configure(text=sub_msg if not sub_ok else "")
        self.due_err_lbl.configure(text=due_msg if not due_ok else "")
        
        if not (title_ok and sub_ok and due_ok and status_ok and priority_ok):
            self.global_status_lbl.configure(text="❌ All choices and inputs must be filled out completely!", text_color="#ff5757")
            return

        try:
            save_assignment(title, subject, due_date, status, priority)
            self.global_status_lbl.configure(text="✅ Assignment successfully tracked!", text_color="#28a745")
            
            # Reset fields values parameters defaults forms states mappings
            self.title_entry.delete(0, 'end')
            self.subject_entry.delete(0, 'end')
            self.due_entry.delete(0, 'end')
            self.due_entry.insert(0, "YYYY-MM-DD")
            self.status_dropdown.set("-- Select Status --")
            self.priority_dropdown.set("-- Select Priority --")
            
            self.show_view_tab()
            
        except Exception as e:
            self.global_status_lbl.configure(text=f"❌ Error during save: {str(e)}", text_color="#ff5757")

    # --- Simplified Assignment Pipeline Flows ---
    def trigger_submit_flow(self, key, info):
        SubmitWorkDialog(self, key, info, self.load_assignments)

    def trigger_unsubmit_flow(self, key, info):
        info["Status"] = "In Progress"
        info["Submission_Link"] = ""
        info["Submitted_At"] = ""
        Save_Updated_Data(key, info)
        self.load_assignments()

    def open_update_window(self, key, info):
        UpdateDialog(self, key, info, self.load_assignments)

    def trigger_card_delete(self, key):
        """Spawns the confirmation popup dialog frame before destroying dictionary items entries records values tracks."""
        def proceed_with_deletion():
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    try: 
                        data = json.load(f)
                    except Exception: 
                        data = {}
                        
                if key in data:
                    del data[key]
                    with open(full_path, "w") as f:
                        json.dump(data, f, indent=4)
                        
                self.load_assignments()

        DeleteConfirmationDialog(
            parent=self, 
            title_text="Are you absolutely sure you want to delete this assignment? This action cannot be undone.",
            callback=proceed_with_deletion
        )

    def load_assignments(self):
        """Parses local system JSON file records arrays and dynamically constructs cards frameworks wrappers lists boards."""
        # Wipe existing panel elements blocks structures loops items clean canvas frames layouts
        for widget in self.scroll_container.winfo_children():
            widget.destroy()
            
        active_filter = self.segment_filter.get()
        current_today = datetime.now().strftime("%Y-%m-%d")
        
        # Step-by-step clear absolute path loaders definitions for resources maps
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        submit_path = os.path.join(root_dir, "assets", "Submit_icon.png")
        update_path = os.path.join(root_dir, "assets", "Update_icon.png")
        delete_path = os.path.join(root_dir, "assets", "Delete_icon.png")
        
        try:
            icon_sub = ctk.CTkImage(light_image=Image.open(submit_path), dark_image=Image.open(submit_path), size=(14, 14))
            icon_upd = ctk.CTkImage(light_image=Image.open(update_path), dark_image=Image.open(update_path), size=(14, 14))
            icon_del = ctk.CTkImage(light_image=Image.open(delete_path), dark_image=Image.open(delete_path), size=(14, 14))
        except Exception as e:
            print(f"⚠️ Dynamic Icon Path Error: {e}")
            icon_sub = icon_upd = icon_del = None

        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                try: 
                    data = json.load(f)
                except Exception: 
                    data = {}
            
            if not data:
                ctk.CTkLabel(
                    self.scroll_container, text="No Assignments Found", 
                    font=self.font_reg_md, text_color="gray"
                ).pack(pady=180, padx=20)
                return

            # Maps priorities strings metrics values objects weights lists ranks
            priority_weights = {"High": 0, "Medium": 1, "Low": 2, "None": 3}
            
            # Simple understandable python standard sort routine pipeline parameters rules keys configurations
            sorted_items = sorted(
                data.items(),
                key=lambda item: priority_weights.get(item[1].get("Priority", "None"), 3)
            )
                
            card_count = 0
            for key, info in sorted_items:
                current_status = info.get("Status", "Not Started")
                due_date_raw = info.get("Due_Date", "").strip()
                priority_level = info.get("Priority", "None")
                
                is_past_due = len(due_date_raw) == 10 and due_date_raw < current_today
                
                # --- Beginner-Friendly Filter Rules Process Logs Structure ---
                if active_filter == "Submitted" and current_status != "Completed":
                    continue
                    
                elif active_filter == "Unsubmitted" and current_status == "Completed":
                    continue
                    
                elif active_filter == "Pending":
                    if current_status == "Completed" or not is_past_due:
                        continue
                
                card_count += 1
                
                # --- Readable Status Colors Logic Branching Switch ---
                if current_status == "Completed":
                    status_display = "Completed"
                    status_color = "#92ef6a"  
                elif current_status == "In Progress":
                    status_display = "In Progress"
                    status_color = "#fab333"  
                else:
                    status_display = "Not Started"
                    status_color = "#545454"  

                # --- Readable Due Date Contextual Alert Color Switching Logic ---
                if current_status == "Completed":
                    title_color = "white"
                elif due_date_raw == current_today:
                    title_color = "#ff5757"  
                    status_display += "  ⚠️ DUE TODAY"
                elif len(due_date_raw) == 10 and due_date_raw < current_today:
                    title_color = "#ff7b25"  
                    status_display += "  🚨 OVERDUE"
                else:
                    title_color = "white"

                # --- Readable Border Color Priority Mapping Switching Logic ---
                if priority_level == "High":
                    border_color = "#ff5757"       
                    priority_color = "#ff5757"
                elif priority_level == "Medium":
                    border_color = "#fab333"       
                    priority_color = "#fab333"
                elif priority_level == "Low":
                    border_color = "#29b6f6"       
                    priority_color = "#29b6f6"
                else:
                    border_color = "#2d2d2d"       
                    priority_color = "gray"

                # --- Render Standalone Card Instance Wrapper View Layout UI ---
                card = ctk.CTkFrame(self.scroll_container, corner_radius=24, fg_color="#181818", border_width=2, border_color=border_color)
                card.pack(fill="x", padx=20, pady=10, expand=True)
                
                text_frame = ctk.CTkFrame(card, fg_color="transparent")
                text_frame.pack(side="left", padx=25, pady=18)
                
                title_lbl = ctk.CTkLabel(text_frame, text=info['Title'], font=self.font_bold_md, text_color=title_color)
                title_lbl.pack(anchor="w")
                
                meta_str = f"Subject: {info['Subject']}   |   Due: {due_date_raw}"
                meta_lbl = ctk.CTkLabel(text_frame, text=meta_str, font=self.font_reg_md, text_color="dark gray")
                meta_lbl.pack(anchor="w", pady=3)
                
                status_row_container = ctk.CTkFrame(text_frame, fg_color="transparent")
                status_row_container.pack(anchor="w")
                
                progress_lbl = ctk.CTkLabel(status_row_container, text=status_display, font=self.font_bold_sm, text_color=status_color)
                progress_lbl.pack(side="left")
                
                divider_lbl = ctk.CTkLabel(status_row_container, text="   |   ", font=self.font_bold_sm, text_color="gray")
                divider_lbl.pack(side="left")
                
                priority_lbl = ctk.CTkLabel(status_row_container, text=f"Priority: {priority_level}", font=self.font_bold_sm, text_color=priority_color)
                priority_lbl.pack(side="left")
                
                # Append sub metadata logs information if task is completed
                if current_status == "Completed":
                    submission_row_container = ctk.CTkFrame(text_frame, fg_color="transparent")
                    submission_row_container.pack(anchor="w", pady=(4, 0)) 
                    
                    sub_details_str = f"🔗 {info.get('Submission_Link', 'N/A')}   |   📅 Submitted: {info.get('Submitted_At', 'N/A')}"
                    submission_lbl = ctk.CTkLabel(submission_row_container, text=sub_details_str, font=self.font_reg_sm, text_color="#92ef6a")
                    submission_lbl.pack(side="left")

                # --- Actions Controls Buttons Sub-Layout Panel Component Blocks ---
                action_frame = ctk.CTkFrame(card, fg_color="transparent")
                action_frame.pack(side="right", padx=25, pady=10)
                
                # Dynamic callback functions allocation bindings layouts routines maps rules
                if current_status != "Completed":
                    submit_btn = ctk.CTkButton(
                        action_frame, text="Submit", image=icon_sub, compound="right",
                        width=110, height=38, corner_radius=19, fg_color="#7ed957", hover_color="#30b439", 
                        text_color="white", font=self.font_bold_sm,
                        command=lambda k=key, i=info: self.trigger_submit_flow(k, i)
                    )
                    submit_btn.pack(side="left", padx=6)
                else:
                    unsubmit_btn = ctk.CTkButton(
                        action_frame, text="Unsubmit", width=110, height=38, corner_radius=19,
                        fg_color="#ff5757", text_color="white", font=self.font_bold_sm,
                        command=lambda k=key, i=info: self.trigger_unsubmit_flow(k, i)
                    )
                    unsubmit_btn.pack(side="left", padx=6)
                
                up_btn = ctk.CTkButton(
                    action_frame, text="Update", image=icon_upd, compound="right",
                    width=110, height=38, corner_radius=19, fg_color="#fab333", hover_color="#ba8625", 
                    text_color="white", font=self.font_bold_sm,
                    command=lambda k=key, i=info: self.open_update_window(k, i)
                )
                up_btn.pack(side="left", padx=6)
                
                del_btn = ctk.CTkButton(
                    action_frame, text="Delete", image=icon_del, compound="right", 
                    width=110, height=38, corner_radius=19, fg_color="#ff5757", hover_color="#d32f2f", 
                    text_color="white", font=self.font_bold_sm,
                    command=lambda k=key: self.trigger_card_delete(k)
                )
                del_btn.pack(side="left", padx=6)
                
            if card_count == 0:
                ctk.CTkLabel(
                    self.scroll_container, text=f"No {active_filter.lower()} assignments found inside this view tab configuration.", 
                    text_color="gray", font=self.font_reg_md
                ).pack(pady=40)
        else:
            ctk.CTkLabel(self.scroll_container, text="Database file missing initialization data.").pack(pady=20)


# =====================================================================
# 5. ACTION DELETE CONFIRMATION DIALOG MODAL
# =====================================================================
class DeleteConfirmationDialog(ctk.CTkToplevel):
    """
    A temporary pop-up window overlay modal constructed to double-check structural deletions 
    safely while prioritizing stack focus structures flags.
    """
    def __init__(self, parent, title_text, callback):
        super().__init__(parent)
        self.title("Confirm Action")
        self.geometry("340x180")
        self.resizable(False, False)
        
        # Stacking order flags setup configurations metrics logs tracks
        self.transient(parent)         
        self.attributes("-topmost", True) 
        self.grab_set()                
        
        self.callback = callback
        
        # Dynamic geometry calculation placement mappings systems updates routines loops
        parent.update_idletasks()
        self.update_idletasks()        
        
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        
        spawn_x = parent_x + (parent_width // 2) - (340 // 2) - 50
        spawn_y = parent_y + (parent_height // 2) - (180 // 2) - 100
        
        self.geometry(f"+{spawn_x}+{spawn_y}")

        # Core alert labels information views maps panel fields
        self.label = ctk.CTkLabel(self, text=title_text, font=parent.font_bold_sm, wraplength=300)
        self.label.pack(pady=(30, 20), padx=20)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        # Destructive Action execution confirmation workflow routing map buttons item
        self.yes_btn = ctk.CTkButton(
            btn_frame, text="Delete", fg_color="#ff5757", hover_color="#d32f2f", text_color="white",
            font=parent.font_bold_sm, width=100, height=36, corner_radius=18, command=self.confirm_action
        )
        self.yes_btn.pack(side="left", padx=10)

        # Operational retreat terminate popups actions cancel window trigger panel
        self.no_btn = ctk.CTkButton(
            btn_frame, text="Cancel", fg_color="#2d2d2d", hover_color="#424242", text_color="white",
            font=parent.font_bold_sm, width=100, height=36, corner_radius=18, command=self.destroy
        )
        self.no_btn.pack(side="left", padx=10)

    def confirm_action(self):
        """Dispatches external callback routine handles and closes popup window frame container views."""
        self.callback()  
        self.destroy()