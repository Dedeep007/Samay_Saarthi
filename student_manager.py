"""
Student Management System for Timetable Generation
Handles student data input, validation, and course enrollment
"""

import json
from typing import List, Dict, Optional
from models import Student, Course, CourseType, DayOfWeek, TimeSlot

class StudentManager:
    """Manages student data and course enrollment"""
    
    def __init__(self):
        self.students: List[Student] = []
        self.courses: List[Course] = []
    
    def add_student_interactive(self) -> Student:
        """Add a student through interactive input"""
        print("\n" + "="*60)
        print("ADD NEW STUDENT")
        print("="*60)
        
        # Basic information
        student_id = input("Enter Student ID: ").strip()
        name = input("Enter Student Name: ").strip()
        email = input("Enter Email: ").strip()
        semester = int(input("Enter Current Semester (1-8): ").strip())
        year = int(input("Enter Academic Year (1-4): ").strip())
        program = input("Enter Program (e.g., B.Tech CSE, M.Tech AI): ").strip()
        
        # Credit limit
        max_credits = input("Enter Max Credits per Semester (default 24): ").strip()
        max_credits = int(max_credits) if max_credits else 24
        
        # Course selections
        print(f"\n📚 COURSE SELECTION FOR {name}")
        print("-" * 40)
        
        major_courses = self._get_course_selection("Major Courses")
        minor_courses = self._get_course_selection("Minor Courses")
        elective_courses = self._get_course_selection("Elective Courses")
        skill_based_courses = self._get_course_selection("Skill-based Courses")
        value_added_courses = self._get_course_selection("Value-added Courses")
        
        # Preferences
        print(f"\n⚙️ PREFERENCES FOR {name}")
        print("-" * 40)
        
        preferred_days = self._get_day_preferences()
        avoided_time_slots = self._get_avoided_time_slots()
        
        student = Student(
            id=student_id,
            name=name,
            email=email,
            semester=semester,
            year=year,
            program=program,
            major_courses=major_courses,
            minor_courses=minor_courses,
            elective_courses=elective_courses,
            skill_based_courses=skill_based_courses,
            value_added_courses=value_added_courses,
            max_credits_per_semester=max_credits,
            preferred_days=preferred_days,
            avoided_time_slots=avoided_time_slots
        )
        
        self.students.append(student)
        print(f"\n✅ Student {name} added successfully!")
        return student
    
    def _get_course_selection(self, course_type: str) -> List[str]:
        """Get course selection for a specific type"""
        print(f"\n{course_type}:")
        courses = []
        
        while True:
            course_code = input(f"  Enter {course_type} code (or 'done' to finish): ").strip()
            if course_code.lower() == 'done':
                break
            if course_code:
                courses.append(course_code.upper())
        
        return courses
    
    def _get_day_preferences(self) -> List[DayOfWeek]:
        """Get preferred days from user"""
        print("\nPreferred Days (optional):")
        print("Available: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday")
        
        preferred_days = []
        days_input = input("Enter preferred days (comma-separated, or press Enter to skip): ").strip()
        
        if days_input:
            day_names = [day.strip().title() for day in days_input.split(',')]
            for day_name in day_names:
                try:
                    day = DayOfWeek(day_name)
                    preferred_days.append(day)
                except ValueError:
                    print(f"Warning: '{day_name}' is not a valid day")
        
        return preferred_days
    
    def _get_avoided_time_slots(self) -> List[TimeSlot]:
        """Get time slots to avoid from user"""
        print("\nTime Slots to Avoid (optional):")
        print("Format: HH:MM-HH:MM (e.g., 09:00-10:00)")
        
        avoided_slots = []
        
        while True:
            slot_input = input("Enter time slot to avoid (or 'done' to finish): ").strip()
            if slot_input.lower() == 'done':
                break
            
            if slot_input and '-' in slot_input:
                try:
                    start_time, end_time = slot_input.split('-')
                    time_slot = TimeSlot(start_time=start_time.strip(), end_time=end_time.strip())
                    avoided_slots.append(time_slot)
                except Exception as e:
                    print(f"Invalid time format: {e}")
        
        return avoided_slots
    
    def load_students_from_json(self, filepath: str) -> List[Student]:
        """Load students from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            students = []
            for student_data in data.get('students', []):
                # Convert avoided_time_slots
                avoided_slots = []
                for slot_data in student_data.get('avoided_time_slots', []):
                    avoided_slots.append(TimeSlot(**slot_data))
                
                student_data['avoided_time_slots'] = avoided_slots
                
                # Convert preferred_days
                preferred_days = []
                for day_str in student_data.get('preferred_days', []):
                    preferred_days.append(DayOfWeek(day_str))
                
                student_data['preferred_days'] = preferred_days
                
                student = Student(**student_data)
                students.append(student)
            
            self.students.extend(students)
            print(f"✅ Loaded {len(students)} students from {filepath}")
            return students
            
        except FileNotFoundError:
            print(f"❌ File {filepath} not found")
            return []
        except Exception as e:
            print(f"❌ Error loading students: {e}")
            return []
    
    def save_students_to_json(self, filepath: str):
        """Save students to JSON file"""
        try:
            data = {
                "students": []
            }
            
            for student in self.students:
                student_dict = student.dict()
                
                # Convert TimeSlot objects to dict
                student_dict['avoided_time_slots'] = [
                    slot.dict() for slot in student.avoided_time_slots
                ]
                
                # Convert DayOfWeek to string
                student_dict['preferred_days'] = [
                    day.value for day in student.preferred_days
                ]
                
                data["students"].append(student_dict)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved {len(self.students)} students to {filepath}")
            
        except Exception as e:
            print(f"❌ Error saving students: {e}")
    
    def get_student_courses(self, student: Student, available_courses: List[Course]) -> List[Course]:
        """Get all courses for a student based on their selections"""
        course_dict = {course.code: course for course in available_courses}
        student_courses = []
        
        # Collect all course codes for the student
        all_course_codes = (
            student.major_courses + 
            student.minor_courses + 
            student.elective_courses + 
            student.skill_based_courses + 
            student.value_added_courses
        )
        
        for course_code in all_course_codes:
            if course_code in course_dict:
                student_courses.append(course_dict[course_code])
            else:
                print(f"⚠️ Warning: Course {course_code} not found for student {student.name}")
        
        return student_courses
    
    def validate_student_enrollment(self, student: Student, available_courses: List[Course]) -> Dict:
        """Validate student's course enrollment"""
        student_courses = self.get_student_courses(student, available_courses)
        
        total_credits = sum(course.credits for course in student_courses)
        total_hours = sum(course.hours_per_week for course in student_courses)
        
        validation_result = {
            "student_id": student.id,
            "student_name": student.name,
            "total_courses": len(student_courses),
            "total_credits": total_credits,
            "total_hours": total_hours,
            "max_credits": student.max_credits_per_semester,
            "credits_valid": total_credits <= student.max_credits_per_semester,
            "missing_courses": [],
            "warnings": []
        }
        
        # Check for missing courses
        all_course_codes = (
            student.major_courses + 
            student.minor_courses + 
            student.elective_courses + 
            student.skill_based_courses + 
            student.value_added_courses
        )
        
        available_codes = {course.code for course in available_courses}
        missing_courses = [code for code in all_course_codes if code not in available_codes]
        validation_result["missing_courses"] = missing_courses
        
        # Add warnings
        if total_credits > student.max_credits_per_semester:
            validation_result["warnings"].append(f"Credit overload: {total_credits}/{student.max_credits_per_semester}")
        
        if missing_courses:
            validation_result["warnings"].append(f"Missing courses: {', '.join(missing_courses)}")
        
        return validation_result
    
    def print_student_summary(self, student: Student):
        """Print a summary of student information"""
        print(f"\n📋 STUDENT SUMMARY: {student.name}")
        print("-" * 50)
        print(f"ID: {student.id}")
        print(f"Email: {student.email}")
        print(f"Program: {student.program}")
        print(f"Semester: {student.semester}, Year: {student.year}")
        print(f"Max Credits: {student.max_credits_per_semester}")
        
        if student.major_courses:
            print(f"Major Courses: {', '.join(student.major_courses)}")
        if student.minor_courses:
            print(f"Minor Courses: {', '.join(student.minor_courses)}")
        if student.elective_courses:
            print(f"Electives: {', '.join(student.elective_courses)}")
        if student.skill_based_courses:
            print(f"Skill-based: {', '.join(student.skill_based_courses)}")
        if student.value_added_courses:
            print(f"Value-added: {', '.join(student.value_added_courses)}")
        
        if student.preferred_days:
            print(f"Preferred Days: {', '.join([day.value for day in student.preferred_days])}")
        
        if student.avoided_time_slots:
            avoided_times = [f"{slot.start_time}-{slot.end_time}" for slot in student.avoided_time_slots]
            print(f"Avoided Times: {', '.join(avoided_times)}")
    
    def list_all_students(self):
        """List all registered students"""
        if not self.students:
            print("No students registered.")
            return
        
        print(f"\n📚 REGISTERED STUDENTS ({len(self.students)})")
        print("="*60)
        
        for i, student in enumerate(self.students, 1):
            total_courses = len(
                student.major_courses + student.minor_courses + 
                student.elective_courses + student.skill_based_courses + 
                student.value_added_courses
            )
            print(f"{i}. {student.name} ({student.id}) - {student.program}")
            print(f"   Semester {student.semester}, {total_courses} courses")
