#!/usr/bin/env python3
"""
Student Gradebook CLI Application
Manages student courses with grades and calculates GPA
"""

import json
import os
import sys


class Gradebook:
    """Manages student courses and grades"""
    
    def __init__(self, data_file='gradebook_data.json'):
        """Initialize gradebook with persistent storage file"""
        self.data_file = data_file
        self.courses = {}
        self.load_data()
    
    def load_data(self):
        """Load gradebook data from file"""
        # Check if the data file exists before attempting to read
        if os.path.exists(self.data_file):
            try:
                # Open file in read mode and parse JSON data
                with open(self.data_file, 'r') as f:
                    self.courses = json.load(f)
                print(f"Loaded {len(self.courses)} courses from {self.data_file}")
            except (json.JSONDecodeError, IOError) as e:
                # Handle corrupted JSON or file read errors gracefully
                print(f"Error loading data: {e}")
                self.courses = {}
        else:
            # Initialize with empty gradebook if no file exists
            print("No existing gradebook data found. Starting fresh.")
    
    def save_data(self):
        """Save gradebook data to file"""
        try:
            # Open file in write mode (creates file if it doesn't exist)
            with open(self.data_file, 'w') as f:
                # Write courses dictionary as formatted JSON with 2-space indentation
                json.dump(self.courses, f, indent=2)
            print(f"Data saved to {self.data_file}")
            return True
        except IOError as e:
            # Handle file write errors (e.g., permissions, disk full)
            print(f"Error saving data: {e}")
            return False
    
    def validate_grade(self, grade):
        """Validate grade input (0.0 to 4.0 scale or letter grade)"""
        # First, try to parse the input as a numeric grade (0.0 to 4.0 scale)
        try:
            grade_val = float(grade)
            # Verify the numeric grade is within valid range
            if 0.0 <= grade_val <= 4.0:
                return True, grade_val
            else:
                return False, "Grade must be between 0.0 and 4.0"
        except ValueError:
            # If numeric parsing fails, treat input as a letter grade
            # Convert to uppercase and remove whitespace for consistency
            grade = grade.upper().strip()
            # Map letter grades to their 4.0 scale equivalents
            grade_map = {
                'A': 4.0, 'A-': 3.7,
                'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                'D+': 1.3, 'D': 1.0, 'D-': 0.7,
                'F': 0.0
            }
            # Check if the letter grade is valid and return its numeric value
            if grade in grade_map:
                return True, grade_map[grade]
            else:
                return False, "Invalid letter grade. Use A, A-, B+, B, B-, C+, C, C-, D+, D, D-, or F"
    
    def validate_credits(self, credits):
        """Validate credit hours input"""
        try:
            # Attempt to convert input to integer
            credits_val = int(credits)
            # Ensure credit value is positive (courses must have at least 1 credit)
            if credits_val > 0:
                return True, credits_val
            else:
                return False, "Credits must be a positive integer"
        except ValueError:
            # Handle non-numeric input
            return False, "Credits must be a valid number"
    
    def add_course(self, course_name, grade, credits):
        """Add a new course to the gradebook"""
        # Validate the grade input first (numeric or letter grade)
        is_valid_grade, grade_result = self.validate_grade(grade)
        if not is_valid_grade:
            # grade_result contains error message if validation failed
            print(f"Invalid grade: {grade_result}")
            return False
        
        # Validate the credit hours input (must be positive integer)
        is_valid_credits, credits_result = self.validate_credits(credits)
        if not is_valid_credits:
            # credits_result contains error message if validation failed
            print(f"Invalid credits: {credits_result}")
            return False
        
        # Prevent duplicate course entries in the gradebook
        if course_name in self.courses:
            print(f"Course '{course_name}' already exists. Use update to modify it.")
            return False
        
        # Create new course entry with validated grade and credits
        self.courses[course_name] = {
            'grade': grade_result,
            'credits': credits_result
        }
        print(f"Course '{course_name}' added successfully!")
        # Persist changes to file immediately
        self.save_data()
        return True
    
    def update_course(self, course_name, grade=None, credits=None):
        """Update an existing course"""
        # Verify the course exists before attempting to update
        if course_name not in self.courses:
            print(f"Course '{course_name}' not found.")
            return False
        
        # Track whether any changes were made
        updated = False
        
        # Update grade if provided (None means keep existing value)
        if grade is not None:
            is_valid_grade, grade_result = self.validate_grade(grade)
            if not is_valid_grade:
                print(f"Invalid grade: {grade_result}")
                return False
            # Update the grade value in the course dictionary
            self.courses[course_name]['grade'] = grade_result
            updated = True
        
        # Update credits if provided (None means keep existing value)
        if credits is not None:
            is_valid_credits, credits_result = self.validate_credits(credits)
            if not is_valid_credits:
                print(f"Invalid credits: {credits_result}")
                return False
            # Update the credits value in the course dictionary
            self.courses[course_name]['credits'] = credits_result
            updated = True
        
        # Only save and report success if at least one field was updated
        if updated:
            print(f"Course '{course_name}' updated successfully!")
            self.save_data()
            return True
        else:
            print("No changes made.")
            return False
    
    def delete_course(self, course_name):
        """Delete a course from the gradebook"""
        # Verify the course exists before attempting deletion
        if course_name not in self.courses:
            print(f"Course '{course_name}' not found.")
            return False
        
        # Remove the course from the courses dictionary
        del self.courses[course_name]
        print(f"Course '{course_name}' deleted successfully!")
        # Persist the deletion to file
        self.save_data()
        return True
    
    def view_gradebook(self):
        """Display all courses and grades"""
        # Handle empty gradebook case
        if not self.courses:
            print("\nGradebook is empty.")
            return
        
        # Print header with formatting
        print("\n" + "="*60)
        print("STUDENT GRADEBOOK")
        print("="*60)
        # Print column headers with left-aligned formatting
        print(f"{'Course Name':<30} {'Grade':<10} {'Credits':<10}")
        print("-"*60)
        
        # Iterate through courses in alphabetical order by course name
        for course_name, data in sorted(self.courses.items()):
            grade = data['grade']
            credits = data['credits']
            # Print each course with aligned columns (2 decimal places for grade)
            print(f"{course_name:<30} {grade:<10.2f} {credits:<10}")
        
        print("-"*60)
        # Calculate and display summary statistics
        gpa = self.calculate_gpa()
        # Sum up all credit hours across all courses
        total_credits = sum(course['credits'] for course in self.courses.values())
        print(f"{'Total Credits:':<30} {'':<10} {total_credits:<10}")
        print(f"{'GPA:':<30} {gpa:<10.2f}")
        print("="*60 + "\n")
    
    def calculate_gpa(self):
        """Calculate overall GPA"""
        # Return 0.0 for empty gradebook
        if not self.courses:
            return 0.0
        
        # Initialize accumulators for weighted GPA calculation
        total_grade_points = 0.0
        total_credits = 0
        
        # Calculate weighted sum of grades (grade * credits for each course)
        for course_data in self.courses.values():
            grade = course_data['grade']
            credits = course_data['credits']
            # Multiply grade by credits to get grade points for this course
            total_grade_points += grade * credits
            total_credits += credits
        
        # Prevent division by zero
        if total_credits == 0:
            return 0.0
        
        # GPA = total grade points / total credits (weighted average)
        return total_grade_points / total_credits


def print_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("STUDENT GRADEBOOK - MAIN MENU")
    print("="*60)
    print("1. Add Course")
    print("2. Update Course")
    print("3. Delete Course")
    print("4. View Gradebook")
    print("5. Calculate GPA")
    print("6. Exit")
    print("="*60)


def main():
    """Main CLI interface"""
    # Display welcome message
    print("Welcome to Student Gradebook CLI!")
    print("="*60)
    
    # Initialize gradebook (loads existing data if available)
    gradebook = Gradebook()
    
    # Main application loop - runs until user chooses to exit
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            # Option 1: Add a new course to the gradebook
            print("\n--- Add Course ---")
            # Get course name from user
            course_name = input("Enter course name: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            
            # Get grade and credit hours from user
            grade = input("Enter grade (0.0-4.0 or letter grade A-F): ").strip()
            credits = input("Enter credit hours: ").strip()
            
            # Attempt to add course (validation happens in add_course method)
            gradebook.add_course(course_name, grade, credits)
        
        elif choice == '2':
            # Option 2: Update an existing course's information
            print("\n--- Update Course ---")
            course_name = input("Enter course name to update: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            
            # Check if course exists before proceeding
            if course_name not in gradebook.courses:
                print(f"Course '{course_name}' not found.")
                continue
            
            # Display current values to help user decide what to change
            print(f"Current grade: {gradebook.courses[course_name]['grade']}")
            print(f"Current credits: {gradebook.courses[course_name]['credits']}")
            
            # Allow user to update grade and/or credits (empty input keeps current value)
            grade_input = input("Enter new grade (or press Enter to keep current): ").strip()
            credits_input = input("Enter new credit hours (or press Enter to keep current): ").strip()
            
            # Convert empty strings to None to indicate "no change"
            grade = grade_input if grade_input else None
            credits = credits_input if credits_input else None
            
            gradebook.update_course(course_name, grade, credits)
        
        elif choice == '3':
            # Option 3: Delete a course from the gradebook
            print("\n--- Delete Course ---")
            course_name = input("Enter course name to delete: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            
            # Ask for confirmation before deleting to prevent accidental deletions
            confirm = input(f"Are you sure you want to delete '{course_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                gradebook.delete_course(course_name)
            else:
                print("Deletion cancelled.")
        
        elif choice == '4':
            # Option 4: Display all courses in formatted table with GPA
            gradebook.view_gradebook()
        
        elif choice == '5':
            # Option 5: Display only GPA and total credits (quick summary)
            gpa = gradebook.calculate_gpa()
            total_credits = sum(course['credits'] for course in gradebook.courses.values())
            print(f"\nTotal Credits: {total_credits}")
            print(f"Current GPA: {gpa:.2f}")
        
        elif choice == '6':
            # Option 6: Exit the application
            print("\nThank you for using Student Gradebook CLI!")
            print("Goodbye!")
            sys.exit(0)
        
        else:
            # Handle invalid menu choices
            print("\nInvalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
