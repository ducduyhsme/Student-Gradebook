# Student-Gradebook-CLI

A Python-based command-line application for managing a student gradebook with support for data persistence, GPA calculation, and comprehensive input validation.

## Features

- **Add Courses**: Add new courses with grades and credit hours
- **Update Courses**: Modify grades or credit hours for existing courses
- **Delete Courses**: Remove courses from the gradebook
- **View Gradebook**: Display all courses with grades and credits
- **GPA Calculation**: Automatically calculate weighted GPA
- **Persistent Storage**: Save and load data from JSON file
- **Input Validation**: Validates all inputs (grades, credits, course names)

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ducduyhsme/Student-Gradebook-CLI.git
cd Student-Gradebook-CLI
```

2. Make the script executable (optional):
```bash
chmod +x gradebook.py
```

## Usage

Run the application:
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

- All data is automatically saved to `gradebook_data.json`
- Data persists between sessions
- JSON format for easy backup and transfer

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

## License

MIT License