#!/usr/bin/env python3
"""
Student Gradebook GUI Application
A Tkinter-based GUI for managing student courses and grades
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os


class Gradebook:
    """Manages student courses and grades"""
    
    def __init__(self, data_file='gradebook.json'):
        """Initialize gradebook with persistent storage file"""
        self.data_file = data_file
        self.courses = {}
        self.load_data()
    
    def load_data(self):
        """Load gradebook data from file"""
        # Check if data file exists before attempting to read
        if os.path.exists(self.data_file):
            try:
                # Open and parse JSON data from file
                with open(self.data_file, 'r') as f:
                    self.courses = json.load(f)
            except (json.JSONDecodeError, IOError):
                # Initialize empty gradebook if file is corrupted or unreadable
                self.courses = {}
        else:
            # Start with empty gradebook if no file exists
            self.courses = {}
    
    def save_data(self):
        """Save gradebook data to file"""
        try:
            # Write courses dictionary to file in JSON format
            with open(self.data_file, 'w') as f:
                # Use 2-space indentation for readable JSON output
                json.dump(self.courses, f, indent=2)
            return True
        except IOError:
            # Return False if file write fails
            return False
    
    def validate_grade(self, grade):
        """Validate grade input (0.0 to 4.0 scale or letter grade)"""
        # Try to parse as numeric grade first (0.0 to 4.0 scale)
        try:
            grade_val = float(grade)
            # Check if numeric grade is within valid range
            if 0.0 <= grade_val <= 4.0:
                return True, grade_val
            else:
                return False, "Grade must be between 0.0 and 4.0"
        except ValueError:
            # If not numeric, treat as letter grade
            # Normalize to uppercase and remove whitespace
            grade = grade.upper().strip()
            # Define mapping from letter grades to numeric values
            grade_map = {
                'A': 4.0, 'A-': 3.7,
                'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                'D+': 1.3, 'D': 1.0, 'D-': 0.7,
                'F': 0.0
            }
            # Validate letter grade and return its numeric equivalent
            if grade in grade_map:
                return True, grade_map[grade]
            else:
                return False, "Invalid letter grade. Use A, A-, B+, B, B-, C+, C, C-, D+, D, D-, or F"
    
    def validate_credits(self, credits):
        """Validate credit hours input"""
        try:
            # Convert input to integer
            credits_val = int(credits)
            # Ensure credits is positive (must be at least 1)
            if credits_val > 0:
                return True, credits_val
            else:
                return False, "Credits must be a positive integer"
        except ValueError:
            # Handle non-numeric input
            return False, "Credits must be a valid number"
    
    def add_course(self, course_name, grade, credits):
        """Add a new course to the gradebook"""
        # Validate grade input (numeric or letter grade)
        is_valid_grade, grade_result = self.validate_grade(grade)
        if not is_valid_grade:
            # Return error message if validation fails
            return False, grade_result
        
        # Validate credit hours input (must be positive integer)
        is_valid_credits, credits_result = self.validate_credits(credits)
        if not is_valid_credits:
            return False, credits_result
        
        # Check for duplicate course names
        if course_name in self.courses:
            return False, f"Course '{course_name}' already exists. Use edit to modify it."
        
        # Create new course entry with validated values
        self.courses[course_name] = {
            'grade': grade_result,
            'credits': credits_result
        }
        # Persist changes to file
        self.save_data()
        return True, "Course added successfully!"
    
    def update_course(self, course_name, grade=None, credits=None):
        """Update an existing course"""
        # Verify course exists before updating
        if course_name not in self.courses:
            return False, f"Course '{course_name}' not found."
        
        # Track if any changes were made
        updated = False
        
        # Update grade if a new value is provided (not None or empty string)
        if grade is not None and grade != "":
            is_valid_grade, grade_result = self.validate_grade(grade)
            if not is_valid_grade:
                return False, grade_result
            # Update the grade in the course dictionary
            self.courses[course_name]['grade'] = grade_result
            updated = True
        
        # Update credits if a new value is provided (not None or empty string)
        if credits is not None and credits != "":
            is_valid_credits, credits_result = self.validate_credits(credits)
            if not is_valid_credits:
                return False, credits_result
            # Update the credits in the course dictionary
            self.courses[course_name]['credits'] = credits_result
            updated = True
        
        # Save changes only if at least one field was updated
        if updated:
            self.save_data()
            return True, "Course updated successfully!"
        else:
            return False, "No changes made."
    
    def delete_course(self, course_name):
        """Delete a course from the gradebook"""
        # Verify course exists before deletion
        if course_name not in self.courses:
            return False, f"Course '{course_name}' not found."
        
        # Remove course from dictionary
        del self.courses[course_name]
        # Persist deletion to file
        self.save_data()
        return True, "Course deleted successfully!"
    
    def calculate_gpa(self):
        """Calculate overall GPA"""
        # Return 0.0 for empty gradebook
        if not self.courses:
            return 0.0
        
        # Initialize accumulators for weighted average calculation
        total_grade_points = 0.0
        total_credits = 0
        
        # Sum up grade points (grade * credits) for all courses
        for course_data in self.courses.values():
            grade = course_data['grade']
            credits = course_data['credits']
            # Calculate grade points for this course
            total_grade_points += grade * credits
            total_credits += credits
        
        # Avoid division by zero
        if total_credits == 0:
            return 0.0
        
        # Calculate weighted GPA (total grade points / total credits)
        return total_grade_points / total_credits
    
    def get_total_credits(self):
        """Get total credit hours"""
        # Sum all credit values from all courses
        return sum(course['credits'] for course in self.courses.values())


class CourseDialog(tk.Toplevel):
    """Dialog for adding or editing a course"""
    
    def __init__(self, parent, title, course_name=None, grade=None, credits=None):
        super().__init__(parent)
        self.title(title)
        # Initialize result to None (will contain user input if OK is clicked)
        self.result = None
        
        # Make dialog modal (blocks interaction with parent window)
        self.transient(parent)
        self.grab_set()
        
        # Configure dialog background color
        self.configure(bg='#f3f4f6')
        
        # Set dialog size
        self.geometry("450x280")
        
        # Create main frame with padding for spacing
        main_frame = tk.Frame(self, bg='#f3f4f6')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create form fields with modern styling
        # Course Name field
        tk.Label(main_frame, text="Course Name:", font=('Arial', 10, 'bold'), 
                bg='#f3f4f6', fg='#1f2937').grid(row=0, column=0, sticky='w', padx=10, pady=12)
        self.course_name_entry = tk.Entry(main_frame, width=30, font=('Arial', 10),
                                          relief='solid', borderwidth=1)
        self.course_name_entry.grid(row=0, column=1, padx=10, pady=12)
        
        # Grade field
        tk.Label(main_frame, text="Grade (0.0-4.0 or A-F):", font=('Arial', 10, 'bold'),
                bg='#f3f4f6', fg='#1f2937').grid(row=1, column=0, sticky='w', padx=10, pady=12)
        self.grade_entry = tk.Entry(main_frame, width=30, font=('Arial', 10),
                                    relief='solid', borderwidth=1)
        self.grade_entry.grid(row=1, column=1, padx=10, pady=12)
        
        # Credit Hours field
        tk.Label(main_frame, text="Credit Hours:", font=('Arial', 10, 'bold'),
                bg='#f3f4f6', fg='#1f2937').grid(row=2, column=0, sticky='w', padx=10, pady=12)
        self.credits_entry = tk.Entry(main_frame, width=30, font=('Arial', 10),
                                      relief='solid', borderwidth=1)
        self.credits_entry.grid(row=2, column=1, padx=10, pady=12)
        
        # Pre-fill fields if editing an existing course
        if course_name:
            self.course_name_entry.insert(0, course_name)
            # Make course name read-only when editing (can't change course name)
            self.course_name_entry.config(state='readonly', bg='#e5e7eb')
        if grade is not None:
            self.grade_entry.insert(0, str(grade))
        if credits is not None:
            self.credits_entry.insert(0, str(credits))
        
        # Create button frame for OK and Cancel buttons
        button_frame = tk.Frame(main_frame, bg='#f3f4f6')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # OK button with modern blue styling
        ok_button = tk.Button(button_frame, text="OK", command=self.ok_clicked, 
                             width=12, font=('Arial', 10, 'bold'),
                             bg='#2563eb', fg='white', relief='flat',
                             activebackground='#1d4ed8', activeforeground='white',
                             cursor='hand2', pady=8)
        ok_button.pack(side='left', padx=5)
        
        # Cancel button with gray styling
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_clicked, 
                                 width=12, font=('Arial', 10, 'bold'),
                                 bg='#6b7280', fg='white', relief='flat',
                                 activebackground='#4b5563', activeforeground='white',
                                 cursor='hand2', pady=8)
        cancel_button.pack(side='left', padx=5)
        
        # Set focus to the first editable field
        if not course_name:
            self.course_name_entry.focus()
        else:
            self.grade_entry.focus()
    
    def ok_clicked(self):
        """Handle OK button click"""
        # Get values from input fields and remove whitespace
        course_name = self.course_name_entry.get().strip()
        grade = self.grade_entry.get().strip()
        credits = self.credits_entry.get().strip()
        
        # Validate that all required fields are filled
        if not course_name:
            messagebox.showerror("Input Error", "Course name cannot be empty.", parent=self)
            return
        
        if not grade:
            messagebox.showerror("Input Error", "Grade cannot be empty.", parent=self)
            return
        
        if not credits:
            messagebox.showerror("Input Error", "Credits cannot be empty.", parent=self)
            return
        
        # Store the result as a dictionary for easy access by caller
        self.result = {
            'course_name': course_name,
            'grade': grade,
            'credits': credits
        }
        # Close the dialog
        self.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click"""
        # Set result to None to indicate cancellation
        self.result = None
        # Close the dialog without saving
        self.destroy()


class GradebookGUI:
    """Main GUI application for Student Gradebook"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Gradebook")
        self.root.geometry("900x600")
        
        # Define modern color palette for consistent UI styling
        self.colors = {
            'primary': '#2563eb',      # Modern blue for primary actions
            'primary_hover': '#1d4ed8', # Darker blue for hover state
            'secondary': '#f3f4f6',    # Light gray for backgrounds
            'accent': '#10b981',       # Green for edit actions
            'danger': '#ef4444',       # Red for delete actions
            'text': '#1f2937',         # Dark gray for text
            'text_light': '#6b7280',   # Medium gray for secondary text
            'background': '#ffffff',   # White background
            'border': '#e5e7eb'        # Light gray for borders
        }
        
        # Configure root window background
        self.root.configure(bg=self.colors['secondary'])
        
        # Initialize gradebook data model (loads existing data)
        self.gradebook = Gradebook()
        
        # Initialize search variable with trace for real-time filtering
        self.search_var = tk.StringVar()
        # Call filter_courses whenever search_var changes
        self.search_var.trace('w', self.filter_courses)
        
        # Initialize sort state variables for table sorting
        self.sort_column = None
        self.sort_reverse = False
        
        # Configure ttk widget styles for modern appearance
        self.configure_styles()
        
        # Build the GUI components
        self.create_toolbar()       # Search and action buttons
        self.create_course_table()  # Main table displaying courses
        self.create_summary_panel() # GPA summary at bottom
        
        # Load and display existing course data
        self.refresh_table()
        self.update_summary()
    
    def configure_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure Treeview header style with larger font
        style.configure("Treeview.Heading",
                       font=('Arial', 12, 'bold'),
                       background=self.colors['primary'],
                       foreground='white',
                       relief='flat',  # Remove 3D border effect
                       padding=10)     # Add padding for better spacing
        
        # Configure header hover effect (darker blue on mouseover)
        style.map("Treeview.Heading",
                 background=[('active', self.colors['primary_hover'])])
        
        # Configure Treeview body style
        style.configure("Treeview",
                       font=('Arial', 10),
                       rowheight=30,        # Taller rows for better readability
                       background='white',
                       fieldbackground='white',
                       borderwidth=1)
        
        # Configure row selection appearance (blue highlight)
        style.map('Treeview',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])
    
    def create_toolbar(self):
        """Create toolbar with search and action buttons"""
        toolbar = tk.Frame(self.root, bg=self.colors['background'], relief='flat', borderwidth=0)
        toolbar.pack(side='top', fill='x', padx=10, pady=10)
        
        # Search section on the left side
        search_frame = tk.Frame(toolbar, bg=self.colors['background'])
        search_frame.pack(side='left', padx=5)
        
        # Search label and input field
        tk.Label(search_frame, text="Search:", font=('Arial', 10), bg=self.colors['background']).pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, 
                               font=('Arial', 10), relief='solid', borderwidth=1)
        search_entry.pack(side='left', padx=5)
        
        # Action buttons section on the left (after search)
        button_frame = tk.Frame(toolbar, bg=self.colors['background'])
        button_frame.pack(side='left', padx=20)
        
        # Create action buttons with emoji icons and color coding
        # Blue for add, green for edit, red for delete, gray for refresh
        self.create_modern_button(button_frame, "➕ Add Course", self.add_course, self.colors['primary']).pack(side='left', padx=3)
        self.create_modern_button(button_frame, "✏️ Edit Course", self.edit_course, self.colors['accent']).pack(side='left', padx=3)
        self.create_modern_button(button_frame, "🗑️ Delete Course", self.delete_course, self.colors['danger']).pack(side='left', padx=3)
        self.create_modern_button(button_frame, "🔄 Refresh", self.refresh_table, self.colors['text_light']).pack(side='left', padx=3)
    
    def create_modern_button(self, parent, text, command, bg_color):
        """Create a modern styled button with hover effect"""
        button = tk.Button(parent, text=text, command=command,
                          font=('Arial', 10, 'bold'),
                          bg=bg_color,
                          fg='white',
                          activebackground=bg_color,
                          activeforeground='white',
                          relief='flat',        # Flat design (no 3D effect)
                          borderwidth=0,
                          padx=15,
                          pady=8,
                          cursor='hand2')       # Hand cursor on hover
        
        # Define hover effect functions
        def on_enter(e):
            # Darken button color when mouse enters (-20 brightness)
            button['bg'] = self.adjust_color_brightness(bg_color, -20)
        
        def on_leave(e):
            # Restore original color when mouse leaves
            button['bg'] = bg_color
        
        # Bind hover events to button
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def adjust_color_brightness(self, hex_color, amount):
        """Adjust the brightness of a hex color"""
        # Remove '#' prefix if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hex string to RGB values (base 16)
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Adjust brightness by adding/subtracting amount
        # Clamp values to valid RGB range (0-255)
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        # Convert RGB values back to hex format
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_course_table(self):
        """Create the course table with sortable columns"""
        # Frame for table with modern styling
        table_frame = tk.Frame(self.root, bg=self.colors['background'])
        table_frame.pack(side='top', fill='both', expand=True, padx=10, pady=5)
        
        # Create Treeview widget (table with tree structure capabilities)
        columns = ('course_name', 'grade', 'credits')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        
        # Define column headings with sorting functionality
        # Clicking a column header will sort the table by that column
        self.tree.heading('course_name', text='Course Name', command=lambda: self.sort_by_column('course_name'))
        self.tree.heading('grade', text='Grade', command=lambda: self.sort_by_column('grade'))
        self.tree.heading('credits', text='Credits', command=lambda: self.sort_by_column('credits'))
        
        # Define column widths for proper layout
        self.tree.column('course_name', width=400)
        self.tree.column('grade', width=150)
        self.tree.column('credits', width=150)
        
        # Add vertical scrollbar for long course lists
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar in the frame
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event to edit course
        self.tree.bind('<Double-1>', lambda e: self.edit_course())
    
    def create_summary_panel(self):
        """Create summary panel showing GPA and credits"""
        # Create colored panel at bottom of window
        summary_frame = tk.Frame(self.root, bg=self.colors['primary'], relief='flat', borderwidth=0)
        summary_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        # Add padding inside the panel
        inner_frame = tk.Frame(summary_frame, bg=self.colors['primary'])
        inner_frame.pack(fill='x', padx=20, pady=15)
        
        # Create label for total credits (left side)
        self.total_credits_label = tk.Label(inner_frame, 
                                           text="Total Credits: 0", 
                                           font=('Arial', 14, 'bold'),
                                           bg=self.colors['primary'],
                                           fg='white')
        self.total_credits_label.pack(side='left', padx=30)
        
        # Create label for GPA (left side, after credits)
        self.gpa_label = tk.Label(inner_frame, 
                                 text="GPA: 0.00", 
                                 font=('Arial', 14, 'bold'),
                                 bg=self.colors['primary'],
                                 fg='white')
        self.gpa_label.pack(side='left', padx=30)
    
    def refresh_table(self):
        """Refresh the course table"""
        # Clear all existing items from the table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get courses to display (filtered by search if applicable)
        courses = self.get_filtered_courses()
        
        # Apply sorting if a sort column is selected
        if self.sort_column:
            courses = self.sort_courses(courses)
        
        # Add each course as a row in the table
        for course_name, data in courses:
            self.tree.insert('', 'end', values=(
                course_name,
                f"{data['grade']:.2f}",  # Format grade to 2 decimal places
                data['credits']
            ))
        
        # Update the summary panel with new totals
        self.update_summary()
    
    def get_filtered_courses(self):
        """Get courses filtered by search term"""
        # Get the current search term (converted to lowercase for case-insensitive search)
        search_term = self.search_var.get().lower()
        # If no search term, return all courses
        if not search_term:
            return list(self.gradebook.courses.items())
        
        # Filter courses by checking if search term is in course name
        filtered = []
        for course_name, data in self.gradebook.courses.items():
            # Case-insensitive substring search
            if search_term in course_name.lower():
                filtered.append((course_name, data))
        return filtered
    
    def filter_courses(self, *args):
        """Filter courses based on search term"""
        # This is called automatically when search_var changes
        # Refresh the table to show filtered results
        self.refresh_table()
    
    def sort_by_column(self, column):
        """Sort table by column"""
        # If clicking the same column, toggle sort direction
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            # New column selected, sort ascending by default
            self.sort_column = column
            self.sort_reverse = False
        
        # Refresh table to apply new sort order
        self.refresh_table()
    
    def sort_courses(self, courses):
        """Sort courses by the selected column"""
        # Sort alphabetically by course name (case-insensitive)
        if self.sort_column == 'course_name':
            courses.sort(key=lambda x: x[0].lower(), reverse=self.sort_reverse)
        # Sort numerically by grade value
        elif self.sort_column == 'grade':
            courses.sort(key=lambda x: x[1]['grade'], reverse=self.sort_reverse)
        # Sort numerically by credit hours
        elif self.sort_column == 'credits':
            courses.sort(key=lambda x: x[1]['credits'], reverse=self.sort_reverse)
        return courses
    
    def update_summary(self):
        """Update GPA and credits summary"""
        # Calculate total credit hours across all courses
        total_credits = self.gradebook.get_total_credits()
        # Calculate weighted GPA
        gpa = self.gradebook.calculate_gpa()
        
        # Update the labels in the summary panel
        self.total_credits_label.config(text=f"Total Credits: {total_credits}")
        self.gpa_label.config(text=f"GPA: {gpa:.2f}")
    
    def add_course(self):
        """Show dialog to add a new course"""
        # Create and display the course dialog
        dialog = CourseDialog(self.root, "Add Course")
        # Wait for dialog to close (modal dialog blocks)
        self.root.wait_window(dialog)
        
        # Process the result if user clicked OK (result is not None)
        if dialog.result:
            # Attempt to add course with validated data
            success, message = self.gradebook.add_course(
                dialog.result['course_name'],
                dialog.result['grade'],
                dialog.result['credits']
            )
            
            # Show appropriate message based on success/failure
            if success:
                messagebox.showinfo("Success", message)
                # Refresh table to show the new course
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
    def edit_course(self):
        """Show dialog to edit selected course"""
        # Get the currently selected item in the table
        selected = self.tree.selection()
        if not selected:
            # No course selected, show warning
            messagebox.showwarning("No Selection", "Please select a course to edit.")
            return
        
        # Get course details from the selected row
        item = self.tree.item(selected[0])
        course_name = item['values'][0]
        
        # Get current values from gradebook data
        course_data = self.gradebook.courses[course_name]
        
        # Show edit dialog with pre-filled values
        dialog = CourseDialog(
            self.root, 
            "Edit Course",
            course_name=course_name,
            grade=course_data['grade'],
            credits=course_data['credits']
        )
        # Wait for dialog to close
        self.root.wait_window(dialog)
        
        # Process the result if user clicked OK
        if dialog.result:
            # Update course with new values
            success, message = self.gradebook.update_course(
                course_name,
                dialog.result['grade'],
                dialog.result['credits']
            )
            
            # Show appropriate message and refresh if successful
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
    def delete_course(self):
        """Delete selected course"""
        # Get the currently selected item in the table
        selected = self.tree.selection()
        if not selected:
            # No course selected, show warning
            messagebox.showwarning("No Selection", "Please select a course to delete.")
            return
        
        # Get course name from the selected row
        item = self.tree.item(selected[0])
        course_name = item['values'][0]
        
        # Ask user to confirm deletion (prevent accidental deletions)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{course_name}'?"):
            # User confirmed, proceed with deletion
            success, message = self.gradebook.delete_course(course_name)
            
            # Show appropriate message and refresh if successful
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
def main():
    """Main entry point"""
    # Create the root Tkinter window
    root = tk.Tk()
    # Initialize the GUI application
    app = GradebookGUI(root)
    # Start the Tkinter event loop (keeps window open and responsive)
    root.mainloop()


if __name__ == "__main__":
    main()
