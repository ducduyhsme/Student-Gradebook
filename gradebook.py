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
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.courses = json.load(f)
                print(f"Loaded {len(self.courses)} courses from {self.data_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data: {e}")
                self.courses = {}
        else:
            print("No existing gradebook data found. Starting fresh.")
    
    def save_data(self):
        """Save gradebook data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.courses, f, indent=2)
            print(f"Data saved to {self.data_file}")
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
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
            print(f"Invalid grade: {grade_result}")
            return False
        
        is_valid_credits, credits_result = self.validate_credits(credits)
        if not is_valid_credits:
            print(f"Invalid credits: {credits_result}")
            return False
        
        # Check if course already exists
        if course_name in self.courses:
            print(f"Course '{course_name}' already exists. Use update to modify it.")
            return False
        
        # Add course
        self.courses[course_name] = {
            'grade': grade_result,
            'credits': credits_result
        }
        print(f"Course '{course_name}' added successfully!")
        self.save_data()
        return True
    
    def update_course(self, course_name, grade=None, credits=None):
        """Update an existing course"""
        if course_name not in self.courses:
            print(f"Course '{course_name}' not found.")
            return False
        
        updated = False
        
        if grade is not None:
            is_valid_grade, grade_result = self.validate_grade(grade)
            if not is_valid_grade:
                print(f"Invalid grade: {grade_result}")
                return False
            self.courses[course_name]['grade'] = grade_result
            updated = True
        
        if credits is not None:
            is_valid_credits, credits_result = self.validate_credits(credits)
            if not is_valid_credits:
                print(f"Invalid credits: {credits_result}")
                return False
            self.courses[course_name]['credits'] = credits_result
            updated = True
        
        if updated:
            print(f"Course '{course_name}' updated successfully!")
            self.save_data()
            return True
        else:
            print("No changes made.")
            return False
    
    def delete_course(self, course_name):
        """Delete a course from the gradebook"""
        if course_name not in self.courses:
            print(f"Course '{course_name}' not found.")
            return False
        
        del self.courses[course_name]
        print(f"Course '{course_name}' deleted successfully!")
        self.save_data()
        return True
    
    def view_gradebook(self):
        """Display all courses and grades"""
        if not self.courses:
            print("\nGradebook is empty.")
            return
        
        print("\n" + "="*60)
        print("STUDENT GRADEBOOK")
        print("="*60)
        print(f"{'Course Name':<30} {'Grade':<10} {'Credits':<10}")
        print("-"*60)
        
        for course_name, data in sorted(self.courses.items()):
            grade = data['grade']
            credits = data['credits']
            print(f"{course_name:<30} {grade:<10.2f} {credits:<10}")
        
        print("-"*60)
        gpa = self.calculate_gpa()
        total_credits = sum(course['credits'] for course in self.courses.values())
        print(f"{'Total Credits:':<30} {'':<10} {total_credits:<10}")
        print(f"{'GPA:':<30} {gpa:<10.2f}")
        print("="*60 + "\n")
    
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
    print("Welcome to Student Gradebook CLI!")
    print("="*60)
    
    gradebook = Gradebook()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            # Add Course
            print("\n--- Add Course ---")
            course_name = input("Enter course name: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            
            grade = input("Enter grade (0.0-4.0 or letter grade A-F): ").strip()
            credits = input("Enter credit hours: ").strip()
            
            gradebook.add_course(course_name, grade, credits)
        
        elif choice == '2':
            # Update Course
            print("\n--- Update Course ---")
            course_name = input("Enter course name to update: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            
            if course_name not in gradebook.courses:
                print(f"Course '{course_name}' not found.")
                continue
            
            print(f"Current grade: {gradebook.courses[course_name]['grade']}")
            print(f"Current credits: {gradebook.courses[course_name]['credits']}")
            
            grade_input = input("Enter new grade (or press Enter to keep current): ").strip()
            credits_input = input("Enter new credit hours (or press Enter to keep current): ").strip()
            
            grade = grade_input if grade_input else None
            credits = credits_input if credits_input else None
            
            gradebook.update_course(course_name, grade, credits)
        
        elif choice == '3':
            # Delete Course
            print("\n--- Delete Course ---")
            course_name = input("Enter course name to delete: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            
            confirm = input(f"Are you sure you want to delete '{course_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                gradebook.delete_course(course_name)
            else:
                print("Deletion cancelled.")
        
        elif choice == '4':
            # View Gradebook
            gradebook.view_gradebook()
        
        elif choice == '5':
            # Calculate GPA
            gpa = gradebook.calculate_gpa()
            total_credits = sum(course['credits'] for course in gradebook.courses.values())
            print(f"\nTotal Credits: {total_credits}")
            print(f"Current GPA: {gpa:.2f}")
        
        elif choice == '6':
            # Exit
            print("\nThank you for using Student Gradebook CLI!")
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
