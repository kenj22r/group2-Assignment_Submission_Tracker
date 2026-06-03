# Assignment Submission Tracker


Members:
Client: Ma. Nicole R. Paguipo
Project Manager: Cielo Mercy D. Dinola
Developer 1: Kenj T. Rabi
Developer 2: Aleza Mae M. Abrillo
QA Tester: Janelle E. Caharop


## 📝 System Description
An assignment tracking system built in Python designed to help students and instructors manage academic workloads. It provides a modular desktop application (GUI) and a command-line interface (CLI) for managing, validating, and auditing academic assignments. The application separates processing, structured local JSON state persistence, and responsive UI layers cleanly across distinct software modules to ensure reliability and performance.

### 🏗️ Project Architecture
The codebase follows a decoupled micro-package structure separating state/logic from execution interfaces:
* **`GUI/`**: Built on CustomTkinter; handles window geometries, responsive grid topologies, and high-level view mounts.
* **`Interfaces/`**: Manages pure visual presentation structures for terminal interactions.
* **`Logics/`**: Central engineering core. Coordinates transaction flows, field-level data validation rules, custom input debouncing, and search index matches.
* **`Models/`**: Handles localized serialization and file I/O operations with a JSON-flatfile database.
* **`Utilities/`**: Exposes utility functions managing shell layout mechanics and ANSI string cleanups.

---

## ✨ Features (CRUD)
The system fully implements **CRUD (Create, Read, Update, Delete)** data persistence through the following core technical capabilities:

* **Create (Add Assignments):** Generates new assignment items backed by a relational auto-increment primary key algorithm (`AS_ID_X`). It isolates trailing integers, queries the absolute maximal boundary dynamically, and auto-generates consecutive records.
* **Read (View & Search):** Computes and parses output data into clear views. Includes a normalized title search engine (`data_match.py`) to easily find specific assignments.
* **Update (Modify Records):** Updates assignment fields safely. All string inputs go through comprehensive verification filters before data serialization:
  * Alphanumeric checking to prevent script injections.
  * Hard boundary length constraint verification (max 50 characters).
  * System-reserved word filters to eliminate duplicate object states.
  * Calendar validation tracking strings using structured time mapping checks (`time.strptime(val, "%Y-%m-%d")`).
* **Delete (Remove Records):** Features clean data deletion logic routines (`clear_and_delete.py`) accompanied by secondary user confirmation sub-loops to prevent accidental data loss.
* **Crash Recovery & Native Visual Cleanups:** Structural file parsing errors (e.g., `json.JSONDecodeError`) automatically fall back onto empty map states without system crashes. Inline terminal rewrites utilize raw ANSI string streams to backstep lines and wipe text buffers instantly without screen flickering.

---

## 🚀 Instructions on How to Run the System

### 1. Prerequisites
* **Python 3.10+** installed on your system.
* **Pip** (Python package environment manager).

### 2. Installation
1. Clone or extract the project workspace folder locally.
2. Open a command terminal inside the project root directory.
3. Install the required external dependencies by running:
   ```bash
   pip install customtkinter watchdog

--

## 📂 Project Directory Structure

Here is how the project files are organized. The code is strictly broken down by concern to keep it maintainable:

```text
Assignment_Submission_Tracker_G2_V.3/
├── Assets/                        # Visual elements and styling assets
│   ├── Add_icon.png
│   ├── Delete_icon.png
│   ├── Page_icon.png
│   ├── Refresh_icon.png
│   ├── Submit_icon.png
│   ├── Update_icon.png
│   └── GlacialIndifference-*.otf   # Custom application fonts
├── GUI/                           # Graphical User Interface layer
│   ├── app_window.py              # Main CustomTkinter window setup
│   └── views.py                   # Layout panels and dashboard frames
├── Interfaces/                    # Command Line Interface layout layouts
│   └── main_interface.py          # Static menus rendered in terminal view
├── Logics/                        # Core backend computations & mechanics
│   ├── back_and_safety.py         # Secondary user confirmation sub-loops
│   ├── clear_and_delete.py        # Logic routines for erasing file data
│   ├── data_match.py              # Normalized title search engine 
│   ├── data_view.py               # Parsing logic for output tables
│   ├── fields_input_validation.py # Sanitization & validation rules
│   ├── main_menu_option.py        # Case router for terminal selections
│   ├── navigation.py              # Terminal break/loop flag managers
│   └── open_and_save.py           # Auto-increment engines and file operations
├── Models/                        # Data Persistence State Storage
│   └── Assignments_Data.json      # Structured local JSON database
├── Utilities/                     # Cross-platform helper functions
│   └── clear_screen.py            # ANSI escape codes for screen cleaning
├── main.py                        # Entry point for the CLI program
├── gui_main.py                    # Entry point for the Desktop GUI program
└── dev_runner.py                  # Live-reload utility script (hot-reloader)   
