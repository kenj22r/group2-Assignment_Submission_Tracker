import customtkinter as ctk
from GUI.views import DashboardFrame

class TrackerApp(ctk.CTk):
    """
    Main Application Window Engine.
    Inherits from customtkinter's CTk container to bootstrap the principal desktop GUI layer.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Assignment Submission Tracker")
        
        # Window Metrics: Defines structural size (1000x700 px) and initial monitor offset cords (+325x, +80y)
        self.geometry("1000x700+325+80")
        
        # 1. Force the window to launch in a maximized state
        #self.state('zoomed') 
        
        # Bounds Constraint: Locks minimum window parameters to safeguard responsive UI elements from clipping
        self.minsize(800, 550)
        
        # UX Engine Constants: Adapts color themes natively to host OS environments (Light/Dark matching)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Grid Topology Configurations: Distributes uniform expanding weight (1) across workspace dimensions
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Content Component Mount: Instantiates the primary visual frame view container
        self.dashboard = DashboardFrame(master=self)
        
        # Redundant Safety Setup: Re-enforces spatial canvas layout weights for grid anchors
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Render Point: Affixes dashboard element utilizing full sticky directional stretch (nsew) with standard padding bounds
        self.dashboard.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)