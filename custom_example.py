from models import Course, Faculty, DayOfWeek, TimeSlot
from timetable_graph import TimetableGraph
import json

def create_custom_data():
    """Create your own course and faculty data"""
    
    # Custom Faculty - Add your faculty members here
    faculty = [
        Faculty(
            id="F001",
            name="Dr. Alice Cooper",
            department="Computer Science",
            max_hours_per_week=20,
            expertise_areas=["Python", "Web Development", "AI"]
        ),
        Faculty(
            id="F002",
            name="Prof. Bob Martinez",
            department="Mathematics", 
            max_hours_per_week=18,
            expertise_areas=["Calculus", "Statistics", "Linear Algebra"]
        ),
        # Add more faculty as needed
    ]
    
    # Custom Courses - Add your courses here
    courses = [
        Course(
            code="CS101",
            name="Python Programming",
            credits=4,
            department="Computer Science",
            faculty_id="F001",
            hours_per_week=4,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="MATH101", 
            name="Calculus I",
            credits=3,
            department="Mathematics",
            faculty_id="F002",
            hours_per_week=3,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        # Add more courses as needed
    ]
    
    return courses, faculty

def run_custom_timetable(groq_api_key: str):
    """Run timetable generation with custom data"""
    
    # Create custom data
    courses, faculty = create_custom_data()
    
    print("Creating timetable with custom data...")
    print(f"Courses: {len(courses)}")
    print(f"Faculty: {len(faculty)}")
    
    # Create and run timetable graph
    timetable_graph = TimetableGraph(groq_api_key)
    result = timetable_graph.generate_timetable(courses, faculty)
    
    return result

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if groq_api_key and groq_api_key != "your_groq_api_key_here":
        result = run_custom_timetable(groq_api_key)
        
        # Print basic results
        print(f"\nGenerated {len(result['generated_slots'])} time slots")
        print(f"Status: {result['status']}")
        
        if result["conflicts"]:
            print(f"Conflicts: {len(result['conflicts'])}")
    else:
        print("Please set GROQ_API_KEY in .env file")