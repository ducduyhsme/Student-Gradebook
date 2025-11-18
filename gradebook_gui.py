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
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.courses = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.courses = {}
        else:
            self.courses = {}
    
    def save_data(self):
        """Save gradebook data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.courses, f, indent=2)
            return True
        except IOError:
            return False
    
    def validate_grade(self, grade):
        """Validate grade input (0.0 to 4.0 scale or letter grade)"""
        # Accept numeric grades (0.0 to 4.0)
        try:
            grade_val = float(grade)
            if 0.0 <= grade_val <= 4.0:
                return True, grade_val
            else:
                return False, "Grade must be between 0.0 and 4.0"
        except ValueError:
            # Accept letter grades
            grade = grade.upper().strip()
            grade_map = {
                'A': 4.0, 'A-': 3.7,
                'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                'D+': 1.3, 'D': 1.0, 'D-': 0.7,
                'F': 0.0
            }
            if grade in grade_map:
                return True, grade_map[grade]
            else:
                return False, "Invalid letter grade. Use A, A-, B+, B, B-, C+, C, C-, D+, D, D-, or F"
    
    def validate_credits(self, credits):
        """Validate credit hours input"""
        try:
            credits_val = int(credits)
            if credits_val > 0:
                return True, credits_val
            else:
                return False, "Credits must be a positive integer"
        except ValueError:
            return False, "Credits must be a valid number"
    
    def add_course(self, course_name, grade, credits):
        """Add a new course to the gradebook"""
        # Validate inputs
        is_valid_grade, grade_result = self.validate_grade(grade)
        if not is_valid_grade:
            return False, grade_result
        
        is_valid_credits, credits_result = self.validate_credits(credits)
        if not is_valid_credits:
            return False, credits_result
        
        # Check if course already exists
        if course_name in self.courses:
            return False, f"Course '{course_name}' already exists. Use edit to modify it."
        
        # Add course
        self.courses[course_name] = {
            'grade': grade_result,
            'credits': credits_result
        }
        self.save_data()
        return True, "Course added successfully!"
    
    def update_course(self, course_name, grade=None, credits=None):
        """Update an existing course"""
        if course_name not in self.courses:
            return False, f"Course '{course_name}' not found."
        
        updated = False
        
        if grade is not None and grade != "":
            is_valid_grade, grade_result = self.validate_grade(grade)
            if not is_valid_grade:
                return False, grade_result
            self.courses[course_name]['grade'] = grade_result
            updated = True
        
        if credits is not None and credits != "":
            is_valid_credits, credits_result = self.validate_credits(credits)
            if not is_valid_credits:
                return False, credits_result
            self.courses[course_name]['credits'] = credits_result
            updated = True
        
        if updated:
            self.save_data()
            return True, "Course updated successfully!"
        else:
            return False, "No changes made."
    
    def delete_course(self, course_name):
        """Delete a course from the gradebook"""
        if course_name not in self.courses:
            return False, f"Course '{course_name}' not found."
        
        del self.courses[course_name]
        self.save_data()
        return True, "Course deleted successfully!"
    
    def calculate_gpa(self):
        """Calculate overall GPA"""
        if not self.courses:
            return 0.0
        
        total_grade_points = 0.0
        total_credits = 0
        
        for course_data in self.courses.values():
            grade = course_data['grade']
            credits = course_data['credits']
            total_grade_points += grade * credits
            total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return total_grade_points / total_credits
    
    def get_total_credits(self):
        """Get total credit hours"""
        return sum(course['credits'] for course in self.courses.values())


class CourseDialog(tk.Toplevel):
    """Dialog for adding or editing a course"""
    
    def __init__(self, parent, title, course_name=None, grade=None, credits=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.geometry("400x250")
        
        # Create form fields
        tk.Label(self, text="Course Name:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.course_name_entry = tk.Entry(self, width=30)
        self.course_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Grade (0.0-4.0 or A-F):").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.grade_entry = tk.Entry(self, width=30)
        self.grade_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Credit Hours:").grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.credits_entry = tk.Entry(self, width=30)
        self.credits_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Pre-fill if editing
        if course_name:
            self.course_name_entry.insert(0, course_name)
            self.course_name_entry.config(state='readonly')
        if grade is not None:
            self.grade_entry.insert(0, str(grade))
        if credits is not None:
            self.credits_entry.insert(0, str(credits))
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="OK", command=self.ok_clicked, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel_clicked, width=10).pack(side='left', padx=5)
        
        # Focus on first field
        if not course_name:
            self.course_name_entry.focus()
        else:
            self.grade_entry.focus()
    
    def ok_clicked(self):
        """Handle OK button click"""
        course_name = self.course_name_entry.get().strip()
        grade = self.grade_entry.get().strip()
        credits = self.credits_entry.get().strip()
        
        if not course_name:
            messagebox.showerror("Input Error", "Course name cannot be empty.", parent=self)
            return
        
        if not grade:
            messagebox.showerror("Input Error", "Grade cannot be empty.", parent=self)
            return
        
        if not credits:
            messagebox.showerror("Input Error", "Credits cannot be empty.", parent=self)
            return
        
        self.result = {
            'course_name': course_name,
            'grade': grade,
            'credits': credits
        }
        self.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.result = None
        self.destroy()


class GradebookGUI:
    """Main GUI application for Student Gradebook"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Gradebook")
        self.root.geometry("900x600")
        
        # Initialize gradebook
        self.gradebook = Gradebook()
        
        # Search variable
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_courses)
        
        # Sort state
        self.sort_column = None
        self.sort_reverse = False
        
        # Create GUI components
        self.create_menu()
        self.create_toolbar()
        self.create_course_table()
        self.create_summary_panel()
        
        # Load initial data
        self.refresh_table()
        self.update_summary()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Course", command=self.add_course)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Edit Course", command=self.edit_course)
        edit_menu.add_command(label="Delete Course", command=self.delete_course)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create toolbar with search and action buttons"""
        toolbar = tk.Frame(self.root, relief='raised', borderwidth=1)
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        # Search section
        tk.Label(toolbar, text="Search:").pack(side='left', padx=5)
        search_entry = tk.Entry(toolbar, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Action buttons
        tk.Button(toolbar, text="Add Course", command=self.add_course).pack(side='left', padx=5)
        tk.Button(toolbar, text="Edit Course", command=self.edit_course).pack(side='left', padx=5)
        tk.Button(toolbar, text="Delete Course", command=self.delete_course).pack(side='left', padx=5)
        tk.Button(toolbar, text="Refresh", command=self.refresh_table).pack(side='left', padx=5)
    
    def create_course_table(self):
        """Create the course table with sortable columns"""
        # Frame for table
        table_frame = tk.Frame(self.root)
        table_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        
        # Create Treeview
        columns = ('course_name', 'grade', 'credits')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        
        # Define column headings with sorting
        self.tree.heading('course_name', text='Course Name', command=lambda: self.sort_by_column('course_name'))
        self.tree.heading('grade', text='Grade', command=lambda: self.sort_by_column('grade'))
        self.tree.heading('credits', text='Credits', command=lambda: self.sort_by_column('credits'))
        
        # Define column widths
        self.tree.column('course_name', width=400)
        self.tree.column('grade', width=150)
        self.tree.column('credits', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_course())
    
    def create_summary_panel(self):
        """Create summary panel showing GPA and credits"""
        summary_frame = tk.Frame(self.root, relief='sunken', borderwidth=2)
        summary_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        # Create labels
        self.total_credits_label = tk.Label(summary_frame, text="Total Credits: 0", font=('Arial', 12, 'bold'))
        self.total_credits_label.pack(side='left', padx=20, pady=10)
        
        self.gpa_label = tk.Label(summary_frame, text="GPA: 0.00", font=('Arial', 12, 'bold'))
        self.gpa_label.pack(side='left', padx=20, pady=10)
    
    def refresh_table(self):
        """Refresh the course table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get courses to display
        courses = self.get_filtered_courses()
        
        # Sort if needed
        if self.sort_column:
            courses = self.sort_courses(courses)
        
        # Add courses to table
        for course_name, data in courses:
            self.tree.insert('', 'end', values=(
                course_name,
                f"{data['grade']:.2f}",
                data['credits']
            ))
        
        self.update_summary()
    
    def get_filtered_courses(self):
        """Get courses filtered by search term"""
        search_term = self.search_var.get().lower()
        if not search_term:
            return list(self.gradebook.courses.items())
        
        filtered = []
        for course_name, data in self.gradebook.courses.items():
            if search_term in course_name.lower():
                filtered.append((course_name, data))
        return filtered
    
    def filter_courses(self, *args):
        """Filter courses based on search term"""
        self.refresh_table()
    
    def sort_by_column(self, column):
        """Sort table by column"""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        self.refresh_table()
    
    def sort_courses(self, courses):
        """Sort courses by the selected column"""
        if self.sort_column == 'course_name':
            courses.sort(key=lambda x: x[0].lower(), reverse=self.sort_reverse)
        elif self.sort_column == 'grade':
            courses.sort(key=lambda x: x[1]['grade'], reverse=self.sort_reverse)
        elif self.sort_column == 'credits':
            courses.sort(key=lambda x: x[1]['credits'], reverse=self.sort_reverse)
        return courses
    
    def update_summary(self):
        """Update GPA and credits summary"""
        total_credits = self.gradebook.get_total_credits()
        gpa = self.gradebook.calculate_gpa()
        
        self.total_credits_label.config(text=f"Total Credits: {total_credits}")
        self.gpa_label.config(text=f"GPA: {gpa:.2f}")
    
    def add_course(self):
        """Show dialog to add a new course"""
        dialog = CourseDialog(self.root, "Add Course")
        self.root.wait_window(dialog)
        
        if dialog.result:
            success, message = self.gradebook.add_course(
                dialog.result['course_name'],
                dialog.result['grade'],
                dialog.result['credits']
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
    def edit_course(self):
        """Show dialog to edit selected course"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a course to edit.")
            return
        
        # Get selected course
        item = self.tree.item(selected[0])
        course_name = item['values'][0]
        
        # Get current values
        course_data = self.gradebook.courses[course_name]
        
        # Show edit dialog
        dialog = CourseDialog(
            self.root, 
            "Edit Course",
            course_name=course_name,
            grade=course_data['grade'],
            credits=course_data['credits']
        )
        self.root.wait_window(dialog)
        
        if dialog.result:
            success, message = self.gradebook.update_course(
                course_name,
                dialog.result['grade'],
                dialog.result['credits']
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
    def delete_course(self):
        """Delete selected course"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a course to delete.")
            return
        
        # Get selected course
        item = self.tree.item(selected[0])
        course_name = item['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{course_name}'?"):
            success, message = self.gradebook.delete_course(course_name)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Student Gradebook GUI
Version 2.0

A graphical application for managing student courses and calculating GPA.

Features:
• Sortable course table
• Search and filter courses
• Add, edit, and delete courses
• GPA calculation
• Persistent storage

Developed with Python and Tkinter"""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GradebookGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
