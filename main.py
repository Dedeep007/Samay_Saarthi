import os
from dotenv import load_dotenv
from models import Course, Faculty, Student, CourseType, DayOfWeek, TimeSlot
from timetable_graph import TimetableGraph
import json

def main_menu():
    """Display main menu and handle user choice"""
    while True:
        print("\n" + "="*80)
        print("🎓 SAMAY SAARTHI - INTELLIGENT TIMETABLE GENERATION SYSTEM")
        print("="*80)
        print("1. 🗓️ Generate Basic Timetable (Original System)")
        print("   • Generate timetable for all courses and faculty")
        print("   • Includes sample students data for reference")
        print("   • Saves sample data files for future use")
        print()
        print("2. 👨‍🎓 Student-Centric Timetable System (NEW)")
        print("   • Interactive student management")
        print("   • Individual course selection (Major/Minor/Electives/etc.)")
        print("   • Generate personalized timetables for each student")
        print("   • Student preferences and constraints")
        print()
        print("3. 📊 Demo Student System")
        print("   • Automated demo of student-centric features")
        print("   • Shows complete workflow with sample data")
        print("   • No user interaction required")
        print()
        print("4. ❌ Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            run_basic_timetable()
        elif choice == '2':
            run_student_system()
        elif choice == '3':
            run_student_demo()
        elif choice == '4':
            print("👋 Thank you for using Samay Saarthi!")
            print("💡 Generated files:")
            print("   • generated_timetable.json - Basic timetable output")
            print("   • sample_courses.json - Course data template")
            print("   • sample_faculty.json - Faculty data template") 
            print("   • sample_students.json - Student data template")
            print("   • student_timetables.json - Individual student timetables")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def run_basic_timetable():
    """Run the original basic timetable generation"""
    
    # Load environment variables
    load_dotenv()
    
    # Get Groq API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("❌ Please set your GROQ_API_KEY in the .env file")
        print("   Get your API key from: https://console.groq.com/")
        return
    
    # Check for debug mode (default: True)
    debug_mode = os.getenv("DEBUG_MODE", "true").lower() in ["true", "1", "yes"]
    
    try:
        # Load sample data
        courses, faculty, students = load_sample_data()
        
        print("📚 Loaded sample data:")
        print(f"   - {len(courses)} courses")
        print(f"   - {len(faculty)} faculty members")
        print(f"   - {len(students)} students")
        
        # Create timetable graph with debug mode
        timetable_graph = TimetableGraph(groq_api_key, debug=debug_mode)
        
        # Generate timetable
        result = timetable_graph.generate_timetable(courses, faculty)
        
        # Print results
        print_timetable(result)
        print_faculty_workload(result)
        print_student_summary(students)
        
        # Save sample data files
        save_sample_data_to_files(courses, faculty, students)
        
        # Save results to file
        output_file = "generated_timetable.json"
        timetable_data = {
            "status": result["status"],
            "conflicts": result["conflicts"],
            "slots": [
                {
                    "course_code": slot.course_code,
                    "faculty_id": slot.faculty_id,
                    "day": slot.day.value,
                    "time_slot": {
                        "start_time": slot.time_slot.start_time,
                        "end_time": slot.time_slot.end_time
                    },
                    "room": slot.room
                }
                for slot in result["generated_slots"]
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(timetable_data, f, indent=2)
        
        print(f"\n💾 Timetable saved to {output_file}")
        
        if debug_mode:
            print(f"\n💡 DEBUG MODE: ON (set DEBUG_MODE=false in .env to disable)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def run_student_system():
    """Run the new student-centric timetable system"""
    try:
        from interactive_student_system import InteractiveStudentSystem
        
        print("\n🎓 Starting Student-Centric Timetable System...")
        system = InteractiveStudentSystem()
        system.main_menu()
        
    except ImportError as e:
        print(f"❌ Error importing student system: {e}")
        print("Please ensure all required files are present.")
    except Exception as e:
        print(f"❌ Error running student system: {e}")

def run_student_demo():
    """Run the student system demo"""
    try:
        from student_input_demo import demo_student_system
        
        print("\n📊 Running Student System Demo...")
        demo_student_system()
        
    except ImportError as e:
        print(f"❌ Error importing demo: {e}")
        print("Please ensure student_input_demo.py is present.")
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()

def load_sample_data():
    """Load sample course, faculty, and student data"""
    
    # Sample Faculty
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
            expertise_areas=["Algorithms", "Machine Learning"]
        ),
        Faculty(
            id="F003",
            name="Dr. Mike Brown",
            department="Mathematics",
            max_hours_per_week=16,
            expertise_areas=["Linear Algebra", "Statistics"]
        ),
        Faculty(
            id="F004",
            name="Dr. Emily Davis",
            department="Physics",
            max_hours_per_week=18,
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
    
    # Sample Courses with course types
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
        )
    ]
    
    # Sample Students
    default_weekdays = [DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY, DayOfWeek.THURSDAY, DayOfWeek.FRIDAY]
    
    students = [
        Student(
            id="S001",
            name="Alice Johnson",
            email="alice.johnson@university.edu",
            semester=3,
            year=2,
            program="B.Tech Computer Science",
            major_courses=["CS301", "CS501"],
            minor_courses=["MATH301"],
            elective_courses=["CS401"],
            skill_based_courses=["MAN201"],
            value_added_courses=["ENG101"],
            max_credits_per_semester=22,
            preferred_days=default_weekdays,
            avoided_time_slots=[TimeSlot(start_time="12:00", end_time="13:00")]
        ),
        Student(
            id="S002",
            name="Bob Smith",
            email="bob.smith@university.edu",
            semester=1,
            year=1,
            program="B.Tech Computer Science",
            major_courses=["CS101"],
            minor_courses=[],
            elective_courses=[],
            skill_based_courses=["MAN201"],
            value_added_courses=["ENG101"],
            max_credits_per_semester=20,
            preferred_days=default_weekdays,
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
            elective_courses=["CS401"],
            skill_based_courses=[],
            value_added_courses=[],
            max_credits_per_semester=24,
            preferred_days=default_weekdays,
            avoided_time_slots=[]
        ),
        Student(
            id="S004",
            name="David Brown",
            email="david.brown@university.edu",
            semester=2,
            year=1,
            program="B.Tech Mechanical Engineering",
            major_courses=["CS201"],
            minor_courses=["MATH201"],
            elective_courses=[],
            skill_based_courses=["MAN201"],
            value_added_courses=["ENG101"],
            max_credits_per_semester=20,
            preferred_days=default_weekdays,
            avoided_time_slots=[TimeSlot(start_time="16:00", end_time="17:00")]
        ),
        Student(
            id="S005",
            name="Emma Wilson",
            email="emma.wilson@university.edu",
            semester=4,
            year=2,
            program="B.Tech Data Science",
            major_courses=["CS301", "MATH301"],
            minor_courses=[],
            elective_courses=["CS401"],
            skill_based_courses=[],
            value_added_courses=["ENG101"],
            max_credits_per_semester=22,
            preferred_days=default_weekdays,
            avoided_time_slots=[TimeSlot(start_time="14:00", end_time="15:00")]
        )
    ]
    
    return courses, faculty, students

def print_timetable(result):
    """Print the generated timetable in a formatted way"""
    print("\n" + "="*80)
    print("GENERATED TIMETABLE")
    print("="*80)
    
    if not result["generated_slots"]:
        print("No timetable slots generated.")
        return
    
    # Group by day
    days_schedule = {}
    for slot in result["generated_slots"]:
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
    
    # Print summary
    print(f"\n📊 SUMMARY")
    print("-" * 30)
    print(f"Total slots: {len(result['generated_slots'])}")
    print(f"Status: {result['status']}")
    
    if result["conflicts"]:
        print(f"\n⚠️ CONFLICTS ({len(result['conflicts'])})")
        print("-" * 30)
        for i, conflict in enumerate(result["conflicts"][:5], 1):
            print(f"{i}. {conflict}")
        if len(result["conflicts"]) > 5:
            print(f"   ... and {len(result['conflicts']) - 5} more conflicts")

def print_faculty_workload(result):
    """Print faculty workload analysis"""
    print("\n" + "="*60)
    print("FACULTY WORKLOAD ANALYSIS")
    print("="*60)
    
    faculty_hours = {}
    faculty_courses = {}
    
    for slot in result["generated_slots"]:
        faculty_id = slot.faculty_id
        
        # Calculate hours
        start_parts = slot.time_slot.start_time.split(":")
        end_parts = slot.time_slot.end_time.split(":")
        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
        hours = (end_minutes - start_minutes) / 60
        
        if faculty_id not in faculty_hours:
            faculty_hours[faculty_id] = 0
            faculty_courses[faculty_id] = set()
        
        faculty_hours[faculty_id] += hours
        faculty_courses[faculty_id].add(slot.course_code)
    
    # Get faculty info
    faculty_dict = {f.id: f for f in result["faculty"]}
    
    for faculty_id, total_hours in faculty_hours.items():
        faculty_info = faculty_dict.get(faculty_id, None)
        max_hours = faculty_info.max_hours_per_week if faculty_info else "Unknown"
        name = faculty_info.name if faculty_info else "Unknown"
        
        status = "✅" if isinstance(max_hours, int) and total_hours <= max_hours else "⚠️"
        
        print(f"\n{status} {name} ({faculty_id})")
        print(f"   Hours: {total_hours:.1f}/{max_hours}")
        print(f"   Courses: {', '.join(sorted(faculty_courses[faculty_id]))}")

def print_student_summary(students):
    """Print student enrollment summary"""
    print("\n" + "="*60)
    print("STUDENT ENROLLMENT SUMMARY")
    print("="*60)
    
    for student in students:
        total_courses = len(
            student.major_courses + student.minor_courses + 
            student.elective_courses + student.skill_based_courses + 
            student.value_added_courses
        )
        
        print(f"\n👨‍🎓 {student.name} ({student.id})")
        print(f"   Program: {student.program}")
        print(f"   Semester: {student.semester}, Year: {student.year}")
        print(f"   Total Courses: {total_courses}")
        print(f"   Max Credits: {student.max_credits_per_semester}")
        
        if student.major_courses:
            print(f"   Major: {', '.join(student.major_courses)}")
        if student.minor_courses:
            print(f"   Minor: {', '.join(student.minor_courses)}")
        if student.elective_courses:
            print(f"   Electives: {', '.join(student.elective_courses)}")
        if student.skill_based_courses:
            print(f"   Skill-based: {', '.join(student.skill_based_courses)}")
        if student.value_added_courses:
            print(f"   Value-added: {', '.join(student.value_added_courses)}")
        
        if student.preferred_days:
            print(f"   Preferred Days: {', '.join([day.value for day in student.preferred_days])}")
        
        if student.avoided_time_slots:
            avoided_times = [f"{slot.start_time}-{slot.end_time}" for slot in student.avoided_time_slots]
            print(f"   Avoided Times: {', '.join(avoided_times)}")

def save_sample_data_to_files(courses, faculty, students):
    """Save sample data to JSON files for future use"""
    
    # Save courses
    courses_data = {
        "courses": []
    }
    for course in courses:
        course_dict = course.dict()
        course_dict['course_type'] = course.course_type.value
        course_dict['preferred_days'] = [day.value for day in course.preferred_days]
        courses_data["courses"].append(course_dict)
    
    with open("sample_courses.json", 'w') as f:
        json.dump(courses_data, f, indent=2)
    
    # Save faculty
    faculty_data = {
        "faculty": [faculty_member.dict() for faculty_member in faculty]
    }
    
    with open("sample_faculty.json", 'w') as f:
        json.dump(faculty_data, f, indent=2)
    
    # Save students
    students_data = {
        "students": []
    }
    for student in students:
        student_dict = student.dict()
        student_dict['preferred_days'] = [day.value for day in student.preferred_days]
        student_dict['avoided_time_slots'] = [slot.dict() for slot in student.avoided_time_slots]
        students_data["students"].append(student_dict)
    
    with open("sample_students.json", 'w') as f:
        json.dump(students_data, f, indent=2)
    
    print(f"\n💾 Sample data saved to:")
    print(f"   - sample_courses.json ({len(courses)} courses)")
    print(f"   - sample_faculty.json ({len(faculty)} faculty)")
    print(f"   - sample_students.json ({len(students)} students)")

def main():
    """Main function to run the system"""
    main_menu()

if __name__ == "__main__":
    main()