"""
Schedule.py - Individual Student Timetable Generator
Loads sample courses, faculty, and students data and generates personalized timetables for each student
"""

import os
import json
from typing import List, Dict
from dotenv import load_dotenv

from models import (
    Student, Course, Faculty, CourseType, DayOfWeek, TimeSlot, 
    TimetableSlot, StudentTimetable
)
from timetable_graph import TimetableGraph

# Default preferred days for all students (Monday to Friday, excluding weekends)
DEFAULT_PREFERRED_DAYS = [
    DayOfWeek.MONDAY, 
    DayOfWeek.TUESDAY, 
    DayOfWeek.WEDNESDAY, 
    DayOfWeek.THURSDAY, 
    DayOfWeek.FRIDAY
]

def load_sample_courses() -> List[Course]:
    """Load sample courses data"""
    courses = [
        Course(
            code="CS101",
            name="Introduction to Programming",
            credits=4,
            department="Computer Science",
            faculty_id="F001",
            hours_per_week=4,
            course_type=CourseType.CORE,
            semester=1,
            year=1,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="CS201",
            name="Data Structures",
            credits=3,
            department="Computer Science", 
            faculty_id="F001",
            hours_per_week=3,
            course_type=CourseType.CORE,
            semester=2,
            year=1,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="CS301",
            name="Algorithms",
            credits=3,
            department="Computer Science",
            faculty_id="F002",
            hours_per_week=3,
            course_type=CourseType.MAJOR,
            semester=3,
            year=2,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.FRIDAY]
        ),
        Course(
            code="CS401",
            name="Machine Learning",
            credits=4,
            department="Computer Science",
            faculty_id="F002",
            hours_per_week=4,
            course_type=CourseType.ELECTIVE,
            semester=4,
            year=2,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="MATH201",
            name="Linear Algebra",
            credits=3,
            department="Mathematics",
            faculty_id="F003",
            hours_per_week=3,
            course_type=CourseType.CORE,
            semester=2,
            year=1,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY]
        ),
        Course(
            code="MATH301",
            name="Statistics",
            credits=3,
            department="Mathematics",
            faculty_id="F003",
            hours_per_week=3,
            course_type=CourseType.MAJOR,
            semester=3,
            year=2,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="PHY101",
            name="Physics I",
            credits=4,
            department="Physics",
            faculty_id="F004",
            hours_per_week=4,
            course_type=CourseType.CORE,
            semester=1,
            year=1,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="CS501",
            name="Database Systems",
            credits=3,
            department="Computer Science",
            faculty_id="F005",
            hours_per_week=3,
            course_type=CourseType.MAJOR,
            semester=5,
            year=3,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.FRIDAY]
        ),
        Course(
            code="CS601",
            name="Software Engineering",
            credits=4,
            department="Computer Science",
            faculty_id="F005",
            hours_per_week=4,
            course_type=CourseType.MAJOR,
            semester=6,
            year=3,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="ENG101",
            name="Technical Communication",
            credits=2,
            department="English",
            faculty_id="F006",
            hours_per_week=2,
            course_type=CourseType.VALUE_ADDED,
            semester=1,
            year=1,
            preferred_days=[DayOfWeek.FRIDAY]
        ),
        Course(
            code="MAN201",
            name="Entrepreneurship",
            credits=2,
            department="Management",
            faculty_id="F007",
            hours_per_week=2,
            course_type=CourseType.SKILL_BASED,
            semester=2,
            year=1,
            preferred_days=[DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="CS701",
            name="Artificial Intelligence",
            credits=4,
            department="Computer Science",
            faculty_id="F002",
            hours_per_week=4,
            course_type=CourseType.ELECTIVE,
            semester=7,
            year=4,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="MATH401",
            name="Discrete Mathematics",
            credits=3,
            department="Mathematics",
            faculty_id="F003",
            hours_per_week=3,
            course_type=CourseType.MAJOR,
            semester=4,
            year=2,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.FRIDAY]
        )
    ]
    return courses

def load_sample_faculty() -> List[Faculty]:
    """Load sample faculty data"""
    faculty = [
        Faculty(
            id="F001",
            name="Dr. John Smith",
            department="Computer Science",
            max_hours_per_week=20,
            expertise_areas=["Programming", "Data Structures"]
        ),
        Faculty(
            id="F002", 
            name="Dr. Sarah Johnson",
            department="Computer Science",
            max_hours_per_week=20,
            expertise_areas=["Algorithms", "Machine Learning", "AI"]
        ),
        Faculty(
            id="F003",
            name="Dr. Mike Brown",
            department="Mathematics",
            max_hours_per_week=18,
            expertise_areas=["Linear Algebra", "Statistics", "Discrete Math"]
        ),
        Faculty(
            id="F004",
            name="Dr. Emily Davis",
            department="Physics",
            max_hours_per_week=16,
            expertise_areas=["Quantum Physics", "Electronics"]
        ),
        Faculty(
            id="F005",
            name="Dr. Robert Wilson",
            department="Computer Science",
            max_hours_per_week=20,
            expertise_areas=["Database Systems", "Software Engineering"]
        ),
        Faculty(
            id="F006",
            name="Dr. Lisa Anderson",
            department="English",
            max_hours_per_week=15,
            expertise_areas=["Technical Writing", "Communication"]
        ),
        Faculty(
            id="F007",
            name="Dr. Mark Taylor",
            department="Management",
            max_hours_per_week=12,
            expertise_areas=["Entrepreneurship", "Business Strategy"]
        )
    ]
    return faculty

def load_sample_students() -> List[Student]:
    """Load sample students data"""
    students = [
        Student(
            id="S001",
            name="Alice Johnson",
            email="alice.johnson@university.edu",
            semester=3,
            year=2,
            program="B.Tech Computer Science",
            major_courses=["CS301", "MATH301"],
            minor_courses=["PHY101"],
            elective_courses=["CS401"],
            skill_based_courses=["MAN201"],
            value_added_courses=["ENG101"],
            max_credits_per_semester=22,
            preferred_days=DEFAULT_PREFERRED_DAYS,
            avoided_time_slots=[TimeSlot(start_time="12:00", end_time="13:00")]
        ),
        Student(
            id="S002",
            name="Bob Smith",
            email="bob.smith@university.edu",
            semester=1,
            year=1,
            program="B.Tech Computer Science",
            major_courses=["CS101", "PHY101"],
            minor_courses=["MATH201"],
            elective_courses=[],
            skill_based_courses=["MAN201"],
            value_added_courses=["ENG101"],
            max_credits_per_semester=20,
            preferred_days=DEFAULT_PREFERRED_DAYS,
            avoided_time_slots=[TimeSlot(start_time="09:00", end_time="10:00")]
        ),
        Student(
            id="S003",
            name="Carol Davis",
            email="carol.davis@university.edu",
            semester=5,
            year=3,
            program="B.Tech Computer Science",
            major_courses=["CS501", "CS601"],
            minor_courses=["MATH301"],
            elective_courses=["CS401", "CS701"],
            skill_based_courses=[],
            value_added_courses=[],
            max_credits_per_semester=24,
            preferred_days=DEFAULT_PREFERRED_DAYS,
            avoided_time_slots=[]
        ),
        Student(
            id="S004",
            name="David Brown",
            email="david.brown@university.edu",
            semester=2,
            year=1,
            program="B.Tech Mechanical Engineering",
            major_courses=["CS201", "MATH201"],
            minor_courses=["PHY101"],
            elective_courses=[],
            skill_based_courses=["MAN201"],
            value_added_courses=["ENG101"],
            max_credits_per_semester=20,
            preferred_days=DEFAULT_PREFERRED_DAYS,
            avoided_time_slots=[TimeSlot(start_time="16:00", end_time="17:00")]
        ),
        Student(
            id="S005",
            name="Emma Wilson",
            email="emma.wilson@university.edu",
            semester=4,
            year=2,
            program="B.Tech Data Science",
            major_courses=["CS301", "MATH301", "MATH401"],
            minor_courses=["CS201"],
            elective_courses=["CS401"],
            skill_based_courses=[],
            value_added_courses=["ENG101"],
            max_credits_per_semester=22,
            preferred_days=DEFAULT_PREFERRED_DAYS,
            avoided_time_slots=[TimeSlot(start_time="14:00", end_time="15:00")]
        ),
        Student(
            id="S006",
            name="Frank Miller",
            email="frank.miller@university.edu",
            semester=6,
            year=3,
            program="B.Tech Computer Science",
            major_courses=["CS601", "CS501"],
            minor_courses=["MATH401"],
            elective_courses=["CS701"],
            skill_based_courses=[],
            value_added_courses=["ENG101"],
            max_credits_per_semester=24,
            preferred_days=DEFAULT_PREFERRED_DAYS,
            avoided_time_slots=[TimeSlot(start_time="11:00", end_time="12:00")]
        )
    ]
    return students

def get_student_courses(student: Student, all_courses: List[Course]) -> List[Course]:
    """Get all courses for a specific student"""
    course_dict = {course.code: course for course in all_courses}
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

def print_student_timetable(student_timetable: StudentTimetable):
    """Print a formatted student timetable"""
    print(f"\n" + "="*80)
    print(f"🎓 TIMETABLE FOR: {student_timetable.student_name}")
    print("="*80)
    print(f"Student ID: {student_timetable.student_id}")
    print(f"Semester: {student_timetable.semester}, Year: {student_timetable.year}")
    print(f"Total Credits: {student_timetable.total_credits}")
    print(f"Total Hours per Week: {student_timetable.total_hours}")
    
    if not student_timetable.slots:
        print("❌ No timetable slots generated.")
        return
    
    # Group by day
    days_schedule = {}
    for slot in student_timetable.slots:
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
            print("-" * 60)
            
            for slot in days_schedule[day]:
                # Get course details
                course_name = "Unknown Course"
                for course in all_courses:
                    if course.code == slot.course_code:
                        course_name = course.name
                        break
                
                room_info = f" (Room: {slot.room})" if slot.room else ""
                print(f"  {slot.time_slot.start_time}-{slot.time_slot.end_time} | "
                      f"{slot.course_code}: {course_name}")
                print(f"    Faculty: {slot.faculty_id}{room_info}")
    
    print(f"\n📊 WEEKLY SUMMARY")
    print("-" * 40)
    print(f"Total Classes: {len(student_timetable.slots)}")
    
    # Count by course type
    course_types = {}
    for slot in student_timetable.slots:
        for course in all_courses:
            if course.code == slot.course_code:
                course_type = course.course_type.value
                course_types[course_type] = course_types.get(course_type, 0) + 1
                break
    
    for course_type, count in course_types.items():
        print(f"{course_type} courses: {count}")

def validate_student_data(students: List[Student], courses: List[Course]) -> Dict:
    """Validate student enrollment data"""
    validation_summary = {
        "total_students": len(students),
        "valid_students": 0,
        "students_with_issues": 0,
        "issues": []
    }
    
    available_course_codes = {course.code for course in courses}
    
    for student in students:
        student_issues = []
        
        # Check for missing courses
        all_student_courses = (
            student.major_courses + student.minor_courses + 
            student.elective_courses + student.skill_based_courses + 
            student.value_added_courses
        )
        
        missing_courses = [code for code in all_student_courses if code not in available_course_codes]
        if missing_courses:
            student_issues.append(f"Missing courses: {', '.join(missing_courses)}")
        
        # Check credit limits
        student_courses = [course for course in courses if course.code in all_student_courses]
        total_credits = sum(course.credits for course in student_courses)
        
        if total_credits > student.max_credits_per_semester:
            student_issues.append(f"Credit overload: {total_credits}/{student.max_credits_per_semester}")
        
        if student_issues:
            validation_summary["students_with_issues"] += 1
            validation_summary["issues"].append({
                "student": f"{student.name} ({student.id})",
                "issues": student_issues
            })
        else:
            validation_summary["valid_students"] += 1
    
    return validation_summary

def save_timetables_to_json(student_timetables: List[StudentTimetable], filename: str = "student_schedules.json"):
    """Save all student timetables to JSON file"""
    export_data = {
        "generated_at": "2025-10-04",
        "total_students": len(student_timetables),
        "student_timetables": []
    }
    
    for timetable in student_timetables:
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
    
    return filename

def main():
    """Main function to generate student timetables"""
    
    print("🎓 STUDENT SCHEDULE GENERATOR")
    print("="*60)
    print("Loading sample data and generating individual timetables...")
    print("📅 Note: All students prefer weekdays (Mon-Fri) by default, excluding weekends.")
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not found in .env file")
        print("Please set your Groq API key to generate timetables.")
        print("Get your API key from: https://console.groq.com/")
        return
    
    # Load sample data
    print("\n📚 Loading sample data...")
    global all_courses, all_faculty, all_students
    all_courses = load_sample_courses()
    all_faculty = load_sample_faculty()
    all_students = load_sample_students()
    
    print(f"✅ Loaded {len(all_courses)} courses")
    print(f"✅ Loaded {len(all_faculty)} faculty members")
    print(f"✅ Loaded {len(all_students)} students")
    
    # Validate student data
    print("\n🔍 Validating student enrollment data...")
    validation = validate_student_data(all_students, all_courses)
    
    print(f"✅ {validation['valid_students']}/{validation['total_students']} students have valid enrollments")
    
    if validation['students_with_issues'] > 0:
        print(f"⚠️ {validation['students_with_issues']} students have issues:")
        for issue in validation['issues']:
            print(f"   • {issue['student']}: {', '.join(issue['issues'])}")
    
    # Initialize timetable generator
    print(f"\n🗓️ Generating individual timetables...")
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() in ["true", "1", "yes"]
    timetable_graph = TimetableGraph(groq_api_key, debug=debug_mode)
    
    generated_timetables = []
    
    # Generate timetable for each student
    for i, student in enumerate(all_students, 1):
        print(f"\n📋 Processing student {i}/{len(all_students)}: {student.name}")
        
        # Get student's courses
        student_courses = get_student_courses(student, all_courses)
        
        if not student_courses:
            print(f"   ⚠️ No valid courses found for {student.name}")
            continue
        
        print(f"   📚 Found {len(student_courses)} courses for {student.name}")
        
        # Get relevant faculty for student's courses
        faculty_ids = {course.faculty_id for course in student_courses}
        relevant_faculty = [f for f in all_faculty if f.id in faculty_ids]
        
        print(f"   👩‍🏫 Found {len(relevant_faculty)} faculty members")
        
        try:
            # Generate timetable for this student
            result = timetable_graph.generate_timetable(student_courses, relevant_faculty)
            
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
            
            generated_timetables.append(student_timetable)
            
            print(f"   ✅ Generated {len(result['generated_slots'])} time slots")
            if result["conflicts"]:
                print(f"   ⚠️ {len(result['conflicts'])} conflicts detected")
            
        except Exception as e:
            print(f"   ❌ Error generating timetable for {student.name}: {e}")
    
    # Display results
    print(f"\n🎉 TIMETABLE GENERATION COMPLETED!")
    print(f"Successfully generated timetables for {len(generated_timetables)}/{len(all_students)} students")
    
    if generated_timetables:
        print(f"\n📊 INDIVIDUAL STUDENT TIMETABLES")
        print("="*80)
        
        # Display each student's timetable
        for timetable in generated_timetables:
            print_student_timetable(timetable)
        
        # Save to JSON file
        print(f"\n💾 Saving timetables to file...")
        filename = save_timetables_to_json(generated_timetables)
        print(f"✅ Saved all timetables to {filename}")
        
        # Print summary statistics
        print(f"\n📈 SUMMARY STATISTICS")
        print("="*40)
        total_slots = sum(len(tt.slots) for tt in generated_timetables)
        total_credits = sum(tt.total_credits for tt in generated_timetables)
        total_hours = sum(tt.total_hours for tt in generated_timetables)
        
        print(f"Total time slots generated: {total_slots}")
        print(f"Total credits scheduled: {total_credits}")
        print(f"Total weekly hours: {total_hours}")
        print(f"Average slots per student: {total_slots/len(generated_timetables):.1f}")
        print(f"Average credits per student: {total_credits/len(generated_timetables):.1f}")
    
    else:
        print("❌ No timetables were successfully generated")
    
    print(f"\n🎯 NEXT STEPS")
    print("-" * 30)
    print("• Review generated timetables in student_schedules.json")
    print("• Check for any conflicts or issues")
    print("• Customize course/student data as needed")
    print("• Use interactive_student_system.py for manual management")

if __name__ == "__main__":
    main()