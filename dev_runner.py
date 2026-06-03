import os
import sys
import subprocess
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# =====================================================================
# CUSTOM FILE EVENT HANDLER (PROCESS LIFECYCLE MANAGEMENT)
# =====================================================================
class CodeChangeHandler(FileSystemEventHandler):
    """
    Monitors file system changes and manages the lifecycle of the target 
    application process (termination and restarts).
    """
    
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run
        self.process = None
        
        # Start the application immediately on initial execution
        self.start_app()

    def start_app(self):
        """Terminates the currently running app instance and spawns a fresh one."""
        # Clean shutdown of existing process if it's still alive
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait() 
        
        print("\n🔄 Code changed! Restarting application...")
        
        # Launch target script using the current python interpreter
        self.process = subprocess.Popen([sys.executable, self.script_to_run])

    def on_modified(self, event):
        """Triggered automatically by Watchdog on file/folder modifications."""
        # Filter: Only target Python files; ignore directory modification noise
        if not event.is_directory and event.src_path.endswith('.py'):
            
            # Debounce: Prevents double-triggering when editors fire sequential save events
            time.sleep(0.2)
            self.start_app()


# =====================================================================
# RUNNER INITIALIZATION & MAIN EVENT LOOP
# =====================================================================
if __name__ == "__main__":
    TARGET_SCRIPT = "gui_main.py" 

    print(f"👀 Watching for changes. Run your app via this runner to preview live.")
    
    event_handler = CodeChangeHandler(TARGET_SCRIPT)
    observer = Observer()
    
    # Monitor the current directory and all subdirectories recursively
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    # Keep the main thread alive to intercept user interruption (Ctrl+C)
    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping live preview watcher system...")
        observer.stop()
        
        # Ensure the spawned application process is killed on exit
        if event_handler.process and event_handler.process.poll() is None:
            event_handler.process.terminate()
            
    observer.join()