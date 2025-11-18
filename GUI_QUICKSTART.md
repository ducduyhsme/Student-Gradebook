# Student Gradebook GUI - Quick Start Guide

## Overview
The Student Gradebook GUI is a modern, user-friendly graphical interface for managing student courses and calculating GPA.

## Features

### 1. Main Window
- **Sortable Table**: Click any column header (Course Name, Grade, Credits) to sort
- **Search Bar**: Type to filter courses in real-time
- **Action Buttons**: Quick access to Add, Edit, Delete, and Refresh
- **Summary Panel**: Live display of Total Credits and GPA

### 2. Adding a Course
**Method 1 - Button:**
1. Click "Add Course" button in toolbar
2. Enter course name (e.g., "CS 101 - Data Structures")
3. Enter grade (0.0-4.0 or letter grade A-F)
4. Enter credit hours (positive integer)
5. Click OK

**Method 2 - Menu:**
1. Go to File → Add Course
2. Follow same steps as above

**Grade Formats Accepted:**
- Numeric: 4.0, 3.7, 3.3, 3.0, etc. (0.0 to 4.0 range)
- Letter: A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F

### 3. Editing a Course
**Method 1 - Double-click:**
1. Double-click any course in the table
2. Modify grade or credits (course name is locked)
3. Click OK

**Method 2 - Button:**
1. Select a course in the table
2. Click "Edit Course" button
3. Modify grade or credits
4. Click OK

### 4. Deleting a Course
1. Select a course in the table
2. Click "Delete Course" button
3. Confirm deletion in the dialog

### 5. Search/Filter
1. Type in the search box at the top
2. Results filter automatically as you type
3. Clear search to see all courses again

### 6. Sorting
- Click "Course Name" header to sort alphabetically
- Click "Grade" header to sort by grade
- Click "Credits" header to sort by credit hours
- Click again to reverse sort order

### 7. GPA Summary
The bottom panel always shows:
- **Total Credits**: Sum of all course credits
- **GPA**: Weighted average (grade × credits / total credits)

## Data Storage
- All data is automatically saved to `gradebook.json`
- Data loads automatically when you start the application
- No manual save required!

## Tips
- Use descriptive course names (e.g., "CS 101 - Intro to Programming")
- Search works on course names only
- Double-click is the fastest way to edit
- The original CLI app uses a different data file (`gradebook_data.json`)

## Keyboard Shortcuts
- **Double-click**: Edit selected course
- **Delete key**: (Future enhancement)
- **Ctrl+F**: (Future enhancement - focus search)

## Troubleshooting

**Problem:** GUI won't start
**Solution:** Make sure tkinter is installed:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

**Problem:** Data not saving
**Solution:** Check file permissions in the application directory

**Problem:** Invalid grade error
**Solution:** Use grades between 0.0-4.0 or valid letter grades (A, A-, B+, etc.)

## System Requirements
- Python 3.6 or higher
- tkinter (python3-tk)
- Any OS that supports Tkinter (Linux, macOS, Windows)

## Running the Application
```bash
python3 gradebook_gui.py
```

Or if executable:
```bash
./gradebook_gui.py
```

---
*For CLI version, use `gradebook.py` instead*
