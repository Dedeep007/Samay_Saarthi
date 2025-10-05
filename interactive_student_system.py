"""
Interactive Student Timetable System
Comprehensive system for managing students, courses, faculty and generating individual timetables
"""

import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

from models import (
    Student, Course, Faculty, CourseType, DayOfWeek, TimeSlot, 
    TimetableSlot, StudentTimetable
)
from student_manager import StudentManager
from timetable_graph import TimetableGraph

class InteractiveStudentSystem:
    """Main system for interactive student timetable management"""
    
    def __init__(self):
        self.student_manager = StudentManager()
        self.courses: List[Course] = []
        self.faculty: List[Faculty] = []
        self.timetable_graph: Optional[TimetableGraph] = None
        self.generated_timetables: List[StudentTimetable] = []
        
        # Load environment
        load_dotenv()
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
    def main_menu(self):
        """Main interactive menu"""
        while True:
            print("\n" + "="*70)
            print("🎓 STUDENT TIMETABLE GENERATION SYSTEM")
            print("="*70)
            print("1. 👨‍🎓 Student Management")
            print("2. 📚 Course Management")
            print("3. 👩‍🏫 Faculty Management")
            print("4. 🗓️ Generate Individual Timetables")
            print("5. 📊 View Generated Timetables")
            print("6. 💾 Save/Load Data")
            print("7. ❌ Exit")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                self.student_menu()
            elif choice == '2':
                self.course_menu()
            elif choice == '3':
                self.faculty_menu()
            elif choice == '4':
                self.generate_timetables()
            elif choice == '5':
                self.view_timetables_menu()
            elif choice == '6':
                self.data_management_menu()
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def student_menu(self):
        """Student management menu"""
        while True:
            print("\n" + "="*50)
            print("👨‍🎓 STUDENT MANAGEMENT")
            print("="*50)
            print("1. Add New Student")
            print("2. List All Students")
            print("3. View Student Details")
            print("4. Validate Student Enrollments")
            print("5. Back to Main Menu")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self.student_manager.add_student_interactive()
            elif choice == '2':
                self.student_manager.list_all_students()
            elif choice == '3':
                self.view_student_details()
            elif choice == '4':
                self.validate_all_enrollments()
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def course_menu(self):
        """Course management menu"""
        while True:
            print("\n" + "="*50)
            print("📚 COURSE MANAGEMENT")
            print("="*50)
            print("1. Add New Course")
            print("2. List All Courses")
            print("3. Load Sample Courses")
            print("4. Back to Main Menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                self.add_course_interactive()
            elif choice == '2':
                self.list_courses()
            elif choice == '3':
                self.load_sample_courses()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def faculty_menu(self):
        """Faculty management menu"""
        while True:
            print("\n" + "="*50)
            print("👩‍🏫 FACULTY MANAGEMENT")
            print("="*50)
            print("1. Add New Faculty")
            print("2. List All Faculty")
            print("3. Load Sample Faculty")
            print("4. Back to Main Menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                self.add_faculty_interactive()
            elif choice == '2':
                self.list_faculty()
            elif choice == '3':
                self.load_sample_faculty()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def add_course_interactive(self):
        """Add a course through interactive input"""
        print("\n" + "="*60)
        print("ADD NEW COURSE")
        print("="*60)
        
        code = input("Course Code: ").strip().upper()
        name = input("Course Name: ").strip()
        credits = int(input("Credits: ").strip())
        department = input("Department: ").strip()
        faculty_id = input("Faculty ID: ").strip()
        hours_per_week = int(input("Hours per Week: ").strip())
        
        print("\nCourse Type:")
        for i, course_type in enumerate(CourseType, 1):
            print(f"{i}. {course_type.value}")
        
        type_choice = int(input("Select course type (1-6): ").strip())
        course_type = list(CourseType)[type_choice - 1]
        
        semester = int(input("Semester (1-8): ").strip())
        year = int(input("Year (1-4): ").strip())
        
        course = Course(
            code=code,
            name=name,
            credits=credits,
            department=department,
            faculty_id=faculty_id,
            hours_per_week=hours_per_week,
            course_type=course_type,
            semester=semester,
            year=year
        )
        
        self.courses.append(course)
        print(f"✅ Course {code} added successfully!")
    
    def add_faculty_interactive(self):
        """Add faculty through interactive input"""
        print("\n" + "="*60)
        print("ADD NEW FACULTY")
        print("="*60)
        
        faculty_id = input("Faculty ID: ").strip()
        name = input("Faculty Name: ").strip()
        department = input("Department: ").strip()
        max_hours = int(input("Max Hours per Week (default 20): ").strip() or "20")
        
        print("\nExpertise Areas (comma-separated):")
        expertise_input = input("Enter expertise areas: ").strip()
        expertise_areas = [area.strip() for area in expertise_input.split(',')] if expertise_input else []
        
        faculty = Faculty(
            id=faculty_id,
            name=name,
            department=department,
            max_hours_per_week=max_hours,
            expertise_areas=expertise_areas
        )
        
        self.faculty.append(faculty)
        print(f"✅ Faculty {name} added successfully!")
    
    def list_courses(self):
        """List all courses"""
        if not self.courses:
            print("No courses available.")
            return
        
        print(f"\n📚 ALL COURSES ({len(self.courses)})")
        print("="*80)
        
        for course in self.courses:
            print(f"{course.code} - {course.name}")
            print(f"  Credits: {course.credits} | Type: {course.course_type.value} | Faculty: {course.faculty_id}")
            print(f"  Department: {course.department} | Hours/Week: {course.hours_per_week}")
            print()
    
    def list_faculty(self):
        """List all faculty"""
        if not self.faculty:
            print("No faculty available.")
            return
        
        print(f"\n👩‍🏫 ALL FACULTY ({len(self.faculty)})")
        print("="*70)
        
        for faculty in self.faculty:
            print(f"{faculty.id} - {faculty.name}")
            print(f"  Department: {faculty.department}")
            print(f"  Max Hours: {faculty.max_hours_per_week}/week")
            if faculty.expertise_areas:
                print(f"  Expertise: {', '.join(faculty.expertise_areas)}")
            print()
    
    def view_student_details(self):
        """View details of a specific student"""
        if not self.student_manager.students:
            print("No students registered.")
            return
        
        self.student_manager.list_all_students()
        
        try:
            choice = int(input("\nSelect student number to view details: ").strip())
            if 1 <= choice <= len(self.student_manager.students):
                student = self.student_manager.students[choice - 1]
                self.student_manager.print_student_summary(student)
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def validate_all_enrollments(self):
        """Validate all student enrollments"""
        if not self.student_manager.students:
            print("No students to validate.")
            return
        
        if not self.courses:
            print("No courses available for validation.")
            return
        
        print(f"\n🔍 VALIDATING {len(self.student_manager.students)} STUDENT ENROLLMENTS")
        print("="*70)
        
        for student in self.student_manager.students:
            validation = self.student_manager.validate_student_enrollment(student, self.courses)
            
            status = "✅" if validation["credits_valid"] and not validation["missing_courses"] else "⚠️"
            
            print(f"\n{status} {validation['student_name']} ({validation['student_id']})")
            print(f"   Credits: {validation['total_credits']}/{validation['max_credits']}")
            print(f"   Courses: {validation['total_courses']}")
            
            if validation["warnings"]:
                for warning in validation["warnings"]:
                    print(f"   ⚠️ {warning}")
    
    def generate_timetables(self):
        """Generate individual timetables for all students"""
        if not self.groq_api_key or self.groq_api_key == "your_groq_api_key_here":
            print("❌ Please set your GROQ_API_KEY in the .env file")
            return
        
        if not self.student_manager.students:
            print("❌ No students registered. Please add students first.")
            return
        
        if not self.courses:
            print("❌ No courses available. Please add courses first.")
            return
        
        if not self.faculty:
            print("❌ No faculty available. Please add faculty first.")
            return
        
        print("\n🗓️ GENERATING INDIVIDUAL STUDENT TIMETABLES")
        print("="*60)
        
        # Initialize timetable graph
        debug_mode = os.getenv("DEBUG_MODE", "true").lower() in ["true", "1", "yes"]
        self.timetable_graph = TimetableGraph(self.groq_api_key, debug=debug_mode)
        
        self.generated_timetables = []
        
        for i, student in enumerate(self.student_manager.students, 1):
            print(f"\n📋 Generating timetable for {student.name} ({i}/{len(self.student_manager.students)})")
            
            # Get student's courses
            student_courses = self.student_manager.get_student_courses(student, self.courses)
            
            if not student_courses:
                print(f"   ⚠️ No valid courses found for {student.name}")
                continue
            
            # Get relevant faculty
            faculty_ids = {course.faculty_id for course in student_courses}
            relevant_faculty = [f for f in self.faculty if f.id in faculty_ids]
            
            try:
                # Generate timetable for this student
                result = self.timetable_graph.generate_timetable(student_courses, relevant_faculty)
                
                # Create student timetable
                student_timetable = StudentTimetable(
                    student_id=student.id,
                    student_name=student.name,
                    semester=student.semester,
                    year=student.year,
                    slots=result["generated_slots"],
                    total_credits=sum(course.credits for course in student_courses),
                    total_hours=sum(course.hours_per_week for course in student_courses)
                )
                
                self.generated_timetables.append(student_timetable)
                
                print(f"   ✅ Generated {len(result['generated_slots'])} slots")
                if result["conflicts"]:
                    print(f"   ⚠️ {len(result['conflicts'])} conflicts detected")
                
            except Exception as e:
                print(f"   ❌ Error generating timetable: {e}")
        
        print(f"\n🎉 Completed! Generated timetables for {len(self.generated_timetables)} students.")
    
    def view_timetables_menu(self):
        """Menu for viewing generated timetables"""
        if not self.generated_timetables:
            print("❌ No timetables generated yet. Please generate timetables first.")
            return
        
        while True:
            print("\n" + "="*50)
            print("📊 VIEW TIMETABLES")
            print("="*50)
            print("1. View All Student Timetables")
            print("2. View Specific Student Timetable")
            print("3. Export Timetables to JSON")
            print("4. Back to Main Menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                self.view_all_timetables()
            elif choice == '2':
                self.view_specific_timetable()
            elif choice == '3':
                self.export_timetables()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def view_all_timetables(self):
        """View all generated timetables"""
        for timetable in self.generated_timetables:
            self.print_student_timetable(timetable)
    
    def view_specific_timetable(self):
        """View a specific student's timetable"""
        print(f"\n📋 SELECT STUDENT TIMETABLE")
        print("-" * 40)
        
        for i, timetable in enumerate(self.generated_timetables, 1):
            print(f"{i}. {timetable.student_name} ({timetable.student_id})")
        
        try:
            choice = int(input("\nSelect student number: ").strip())
            if 1 <= choice <= len(self.generated_timetables):
                timetable = self.generated_timetables[choice - 1]
                self.print_student_timetable(timetable)
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def print_student_timetable(self, timetable: StudentTimetable):
        """Print a formatted student timetable"""
        print(f"\n" + "="*80)
        print(f"🎓 TIMETABLE: {timetable.student_name}")
        print("="*80)
        print(f"Student ID: {timetable.student_id}")
        print(f"Semester: {timetable.semester}, Year: {timetable.year}")
        print(f"Total Credits: {timetable.total_credits}")
        print(f"Total Hours: {timetable.total_hours}")
        
        if not timetable.slots:
            print("No timetable slots generated.")
            return
        
        # Group by day
        days_schedule = {}
        for slot in timetable.slots:
            day = slot.day.value
            if day not in days_schedule:
                days_schedule[day] = []
            days_schedule[day].append(slot)
        
        # Sort slots by time within each day
        for day in days_schedule:
            days_schedule[day].sort(key=lambda x: x.time_slot.start_time)
        
        # Print schedule day by day
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in day_order:
            if day in days_schedule:
                print(f"\n📅 {day.upper()}")
                print("-" * 50)
                
                for slot in days_schedule[day]:
                    room_info = f" (Room: {slot.room})" if slot.room else ""
                    print(f"  {slot.time_slot.start_time}-{slot.time_slot.end_time} | "
                          f"{slot.course_code} | Faculty: {slot.faculty_id}{room_info}")
    
    def export_timetables(self):
        """Export all timetables to JSON"""
        if not self.generated_timetables:
            print("❌ No timetables to export.")
            return
        
        filename = input("Enter filename (default: student_timetables.json): ").strip()
        if not filename:
            filename = "student_timetables.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            export_data = {
                "student_timetables": []
            }
            
            for timetable in self.generated_timetables:
                timetable_dict = {
                    "student_id": timetable.student_id,
                    "student_name": timetable.student_name,
                    "semester": timetable.semester,
                    "year": timetable.year,
                    "total_credits": timetable.total_credits,
                    "total_hours": timetable.total_hours,
                    "slots": [
                        {
                            "course_code": slot.course_code,
                            "faculty_id": slot.faculty_id,
                            "day": slot.day.value,
                            "time_slot": {
                                "start_time": slot.time_slot.start_time,
                                "end_time": slot.time_slot.end_time
                            },
                            "room": slot.room,
                            "student_ids": slot.student_ids
                        }
                        for slot in timetable.slots
                    ]
                }
                export_data["student_timetables"].append(timetable_dict)
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✅ Exported {len(self.generated_timetables)} timetables to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting timetables: {e}")
    
    def data_management_menu(self):
        """Data save/load menu"""
        while True:
            print("\n" + "="*50)
            print("💾 DATA MANAGEMENT")
            print("="*50)
            print("1. Save All Data")
            print("2. Load All Data")
            print("3. Load Sample Data")
            print("4. Back to Main Menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                self.save_all_data()
            elif choice == '2':
                self.load_all_data()
            elif choice == '3':
                self.load_all_sample_data()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def save_all_data(self):
        """Save all data to JSON files"""
        # Save students
        self.student_manager.save_students_to_json("students_data.json")
        
        # Save courses
        self.save_courses_to_json("courses_data.json")
        
        # Save faculty
        self.save_faculty_to_json("faculty_data.json")
        
        print("✅ All data saved successfully!")
    
    def load_all_data(self):
        """Load all data from JSON files"""
        # Load students
        self.student_manager.load_students_from_json("students_data.json")
        
        # Load courses
        self.load_courses_from_json("courses_data.json")
        
        # Load faculty
        self.load_faculty_from_json("faculty_data.json")
        
        print("✅ All data loaded successfully!")
    
    def save_courses_to_json(self, filename: str):
        """Save courses to JSON file"""
        try:
            data = {
                "courses": [course.dict() for course in self.courses]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.courses)} courses to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving courses: {e}")
    
    def load_courses_from_json(self, filename: str):
        """Load courses from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            courses = []
            for course_data in data.get('courses', []):
                course = Course(**course_data)
                courses.append(course)
            
            self.courses.extend(courses)
            print(f"✅ Loaded {len(courses)} courses from {filename}")
            
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
        except Exception as e:
            print(f"❌ Error loading courses: {e}")
    
    def save_faculty_to_json(self, filename: str):
        """Save faculty to JSON file"""
        try:
            data = {
                "faculty": [faculty.dict() for faculty in self.faculty]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.faculty)} faculty to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving faculty: {e}")
    
    def load_faculty_from_json(self, filename: str):
        """Load faculty from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            faculty = []
            for faculty_data in data.get('faculty', []):
                faculty_member = Faculty(**faculty_data)
                faculty.append(faculty_member)
            
            self.faculty.extend(faculty)
            print(f"✅ Loaded {len(faculty)} faculty from {filename}")
            
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
        except Exception as e:
            print(f"❌ Error loading faculty: {e}")
    
    def load_sample_courses(self):
        """Load sample courses"""
        sample_courses = [
            Course(
                code="CS101", name="Introduction to Programming", credits=4,
                department="Computer Science", faculty_id="F001", hours_per_week=4,
                course_type=CourseType.CORE, semester=1, year=1
            ),
            Course(
                code="CS201", name="Data Structures", credits=3,
                department="Computer Science", faculty_id="F001", hours_per_week=3,
                course_type=CourseType.CORE, semester=2, year=1
            ),
            Course(
                code="CS301", name="Algorithms", credits=3,
                department="Computer Science", faculty_id="F002", hours_per_week=3,
                course_type=CourseType.MAJOR, semester=3, year=2
            ),
            Course(
                code="CS401", name="Machine Learning", credits=4,
                department="Computer Science", faculty_id="F002", hours_per_week=4,
                course_type=CourseType.ELECTIVE, semester=4, year=2
            ),
            Course(
                code="MATH201", name="Linear Algebra", credits=3,
                department="Mathematics", faculty_id="F003", hours_per_week=3,
                course_type=CourseType.CORE, semester=2, year=1
            ),
            Course(
                code="MATH301", name="Statistics", credits=3,
                department="Mathematics", faculty_id="F003", hours_per_week=3,
                course_type=CourseType.MAJOR, semester=3, year=2
            ),
            Course(
                code="PHY101", name="Physics I", credits=4,
                department="Physics", faculty_id="F004", hours_per_week=4,
                course_type=CourseType.CORE, semester=1, year=1
            ),
            Course(
                code="CS501", name="Database Systems", credits=3,
                department="Computer Science", faculty_id="F005", hours_per_week=3,
                course_type=CourseType.MAJOR, semester=5, year=3
            ),
            Course(
                code="CS601", name="Software Engineering", credits=4,
                department="Computer Science", faculty_id="F005", hours_per_week=4,
                course_type=CourseType.MAJOR, semester=6, year=3
            ),
            Course(
                code="ENG101", name="Technical Communication", credits=2,
                department="English", faculty_id="F006", hours_per_week=2,
                course_type=CourseType.VALUE_ADDED, semester=1, year=1
            ),
            Course(
                code="MAN201", name="Entrepreneurship", credits=2,
                department="Management", faculty_id="F007", hours_per_week=2,
                course_type=CourseType.SKILL_BASED, semester=2, year=1
            )
        ]
        
        self.courses.extend(sample_courses)
        print(f"✅ Loaded {len(sample_courses)} sample courses")
    
    def load_sample_faculty(self):
        """Load sample faculty"""
        sample_faculty = [
            Faculty(
                id="F001", name="Dr. John Smith", department="Computer Science",
                max_hours_per_week=20, expertise_areas=["Programming", "Data Structures"]
            ),
            Faculty(
                id="F002", name="Dr. Sarah Johnson", department="Computer Science",
                max_hours_per_week=20, expertise_areas=["Algorithms", "Machine Learning"]
            ),
            Faculty(
                id="F003", name="Dr. Mike Brown", department="Mathematics",
                max_hours_per_week=16, expertise_areas=["Linear Algebra", "Statistics"]
            ),
            Faculty(
                id="F004", name="Dr. Emily Davis", department="Physics",
                max_hours_per_week=18, expertise_areas=["Quantum Physics", "Electronics"]
            ),
            Faculty(
                id="F005", name="Dr. Robert Wilson", department="Computer Science",
                max_hours_per_week=20, expertise_areas=["Database Systems", "Software Engineering"]
            ),
            Faculty(
                id="F006", name="Dr. Lisa Anderson", department="English",
                max_hours_per_week=15, expertise_areas=["Technical Writing", "Communication"]
            ),
            Faculty(
                id="F007", name="Dr. Mark Taylor", department="Management",
                max_hours_per_week=12, expertise_areas=["Entrepreneurship", "Business Strategy"]
            )
        ]
        
        self.faculty.extend(sample_faculty)
        print(f"✅ Loaded {len(sample_faculty)} sample faculty")
    
    def load_all_sample_data(self):
        """Load all sample data"""
        self.load_sample_courses()
        self.load_sample_faculty()
        print("✅ All sample data loaded!")

def main():
    """Main function to run the interactive system"""
    system = InteractiveStudentSystem()
    system.main_menu()

if __name__ == "__main__":
    main()
