# Student-Gradebook

A Python-based application for managing a student gradebook with both CLI and GUI interfaces, featuring data persistence, GPA calculation, and comprehensive input validation.

## Features

### GUI Application (New!)
- **Sortable Course Table**: Click column headers to sort by course name, grade, or credits
- **Search/Filter**: Real-time search to filter courses by name
- **Add/Edit Courses**: User-friendly popup dialogs for adding and editing courses
- **Delete Courses**: Delete courses with confirmation dialog
- **GPA Summary**: Live display of total credits and weighted GPA
- **Input Validation**: User-friendly error dialogs for invalid inputs
- **Persistent Storage**: Automatic save/load using `gradebook.json`

### CLI Application (Legacy)
- **Add Courses**: Add new courses with grades and credit hours
- **Update Courses**: Modify grades or credit hours for existing courses
- **Delete Courses**: Remove courses from the gradebook
- **View Gradebook**: Display all courses with grades and credits
- **GPA Calculation**: Automatically calculate weighted GPA
- **Persistent Storage**: Save and load data from JSON file
- **Input Validation**: Validates all inputs (grades, credits, course names)

## Requirements

- Python 3.6 or higher
- tkinter (python3-tk) - for GUI application

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ducduyhsme/Student-Gradebook-CLI.git
cd Student-Gradebook-CLI
```

2. Install tkinter (if not already installed):
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On Fedora
sudo dnf install python3-tkinter

# On macOS (usually pre-installed)
# No action needed

# On Windows (usually pre-installed)
# No action needed
```

3. Make scripts executable (optional):
```bash
chmod +x gradebook.py gradebook_gui.py
```

## Usage

### GUI Application (Recommended)

Run the graphical interface:
```bash
python3 gradebook_gui.py
```

Or if you made it executable:
```bash
./gradebook_gui.py
```

#### GUI Features

**Main Window:**
- View all courses in a sortable table
- Click column headers (Course Name, Grade, Credits) to sort
- See live GPA and total credits at the bottom

**Search/Filter:**
- Type in the search box to filter courses by name
- Results update in real-time

**Adding a Course:**
1. Click "Add Course" button or use File → Add Course menu
2. Enter course name, grade (0.0-4.0 or letter A-F), and credit hours
3. Click OK to save

**Editing a Course:**
1. Select a course from the table
2. Click "Edit Course" button or double-click the course
3. Modify grade or credits
4. Click OK to save

**Deleting a Course:**
1. Select a course from the table
2. Click "Delete Course" button
3. Confirm deletion in the dialog

### CLI Application (Legacy)

Run the command-line interface:
```bash
python3 gradebook.py
```

Or if you made it executable:
```bash
./gradebook.py
```

### Menu Options

1. **Add Course**: Add a new course to your gradebook
   - Enter course name
   - Enter grade (numeric 0.0-4.0 or letter grade A-F)
   - Enter credit hours (positive integer)

2. **Update Course**: Modify an existing course
   - Enter the course name to update
   - Enter new grade (or press Enter to keep current)
   - Enter new credit hours (or press Enter to keep current)

3. **Delete Course**: Remove a course from the gradebook
   - Enter course name to delete
   - Confirm deletion

4. **View Gradebook**: Display all courses with grades, credits, and current GPA

5. **Calculate GPA**: Show current GPA and total credits

6. **Exit**: Save and exit the application

### Grade Input Formats

The application accepts two grade formats:

**Numeric (4.0 scale):**
- 4.0, 3.7, 3.3, 3.0, etc.

**Letter Grades:**
- A (4.0), A- (3.7)
- B+ (3.3), B (3.0), B- (2.7)
- C+ (2.3), C (2.0), C- (1.7)
- D+ (1.3), D (1.0), D- (0.7)
- F (0.0)

### Data Storage

- **GUI Application**: Data is automatically saved to `gradebook.json`
- **CLI Application**: Data is automatically saved to `gradebook_data.json`
- Data persists between sessions
- JSON format for easy backup and transfer
- Both applications can coexist with separate data files

## Example Session

```
Welcome to Student Gradebook CLI!
============================================================

STUDENT GRADEBOOK - MAIN MENU
============================================================
1. Add Course
2. Update Course
3. Delete Course
4. View Gradebook
5. Calculate GPA
6. Exit
============================================================

Enter your choice (1-6): 1

--- Add Course ---
Enter course name: Data Structures
Enter grade (0.0-4.0 or letter grade A-F): A
Enter credit hours: 3
Course 'Data Structures' added successfully!
Data saved to gradebook_data.json

Enter your choice (1-6): 4

============================================================
STUDENT GRADEBOOK
============================================================
Course Name                    Grade      Credits   
------------------------------------------------------------
Data Structures                4.00       3         
------------------------------------------------------------
Total Credits:                            3         
GPA:                           4.00      
============================================================
```

## Input Validation

The application validates:
- **Course names**: Must not be empty
- **Grades**: Must be 0.0-4.0 or valid letter grade (A-F)
- **Credits**: Must be positive integers
- **Duplicate courses**: Prevents adding courses that already exist

## Data Structure

The gradebook uses a dictionary to store courses:
```json
{
  "Course Name": {
    "grade": 4.0,
    "credits": 3
  }
}
```

## GUI Screenshots

### Main Window
![Main Window](https://github.com/user-attachments/assets/05fe3c58-976d-4ca9-8103-1235c41dff20)

### Sorted View
![Sorted View](https://github.com/user-attachments/assets/f65b27a2-0ece-4a05-8720-19dff0c95e5d)

### Filtered Search
![Filtered Search](https://github.com/user-attachments/assets/649fe854-40ed-4d69-ad5f-4356d82bea92)

## Architecture

The application uses a modular design:
- `Gradebook` class: Core business logic for managing courses and GPA calculation
- `GradebookGUI` class: Tkinter-based graphical user interface
- `CourseDialog` class: Popup dialogs for adding/editing courses
- Persistent storage: JSON-based data persistence

## License

MIT License