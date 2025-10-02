import os
from dotenv import load_dotenv
from models import Course, Faculty, DayOfWeek, TimeSlot
from timetable_graph import TimetableGraph
import json

def load_sample_data():
    """Load sample course and faculty data"""
    
    # Sample Faculty
    faculty = [
        Faculty(
            id="F001",
            name="Dr. John Smith",
            department="Computer Science",
            max_hours_per_week=8,
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
        )
    ]
    
    # Sample Courses
    courses = [
        Course(
            code="CS101",
            name="Introduction to Programming",
            credits=4,
            department="Computer Science",
            faculty_id="F001",
            hours_per_week=4,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="CS201",
            name="Data Structures",
            credits=3,
            department="Computer Science", 
            faculty_id="F001",
            hours_per_week=3,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="CS301",
            name="Algorithms",
            credits=3,
            department="Computer Science",
            faculty_id="F002",
            hours_per_week=3,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.FRIDAY]
        ),
        Course(
            code="CS401",
            name="Machine Learning",
            credits=4,
            department="Computer Science",
            faculty_id="F002",
            hours_per_week=4,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="MATH201",
            name="Linear Algebra",
            credits=3,
            department="Mathematics",
            faculty_id="F003",
            hours_per_week=3,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY]
        ),
        Course(
            code="MATH301",
            name="Statistics",
            credits=3,
            department="Mathematics",
            faculty_id="F003",
            hours_per_week=3,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="PHY101",
            name="Physics I",
            credits=4,
            department="Physics",
            faculty_id="F004",
            hours_per_week=4,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="CS501",
            name="Database Systems",
            credits=3,
            department="Computer Science",
            faculty_id="F005",
            hours_per_week=3,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.FRIDAY]
        ),
        Course(
            code="CS601",
            name="Software Engineering",
            credits=4,
            department="Computer Science",
            faculty_id="F005",
            hours_per_week=4,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.THURSDAY]
        )
    ]
    
    return courses, faculty

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

def main():
    """Main function to run the timetable generation"""
    
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
        courses, faculty = load_sample_data()
        
        print("📚 Loaded sample data:")
        print(f"   - {len(courses)} courses")
        print(f"   - {len(faculty)} faculty members")
        
        # Create timetable graph with debug mode
        timetable_graph = TimetableGraph(groq_api_key, debug=debug_mode)
        
        # Generate timetable
        result = timetable_graph.generate_timetable(courses, faculty)
        
        # Print results
        print_timetable(result)
        print_faculty_workload(result)
        
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

if __name__ == "__main__":
    main()