from GUI.app_window import TrackerApp

if __name__ == "__main__":
    # Initialize the main GUI window instance
    app = TrackerApp()
    
    # Start the Tkinter event loop to keep the window open and responsive
    app.mainloop()