#!/usr/bin/env python3
"""
Debug demo script - Shows debug output with minimal data
"""

import os
from dotenv import load_dotenv
from models import Course, Faculty, DayOfWeek, TimeSlot
from timetable_graph import TimetableGraph

def create_minimal_test_data():
    """Create minimal test data for debugging"""
    
    # Minimal Faculty
    faculty = [
        Faculty(
            id="F001",
            name="Prof. Alice Smith",
            department="Computer Science",
            max_hours_per_week=15,
            expertise_areas=["Programming", "AI"]
        ),
        Faculty(
            id="F002",
            name="Dr. Bob Jones",
            department="Mathematics",
            max_hours_per_week=12,
            expertise_areas=["Statistics", "Algebra"]
        )
    ]
    
    # Minimal Courses
    courses = [
        Course(
            code="CS101",
            name="Intro to Programming",
            credits=3,
            department="Computer Science",
            faculty_id="F001",
            hours_per_week=3,
            preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
        ),
        Course(
            code="MATH101",
            name="Basic Statistics",
            credits=2,
            department="Mathematics",
            faculty_id="F002",
            hours_per_week=2,
            preferred_days=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
        ),
        Course(
            code="CS201",
            name="Data Structures",
            credits=3,
            department="Computer Science",
            faculty_id="F001",
            hours_per_week=3
        )
    ]
    
    return courses, faculty

def main():
    """Run debug demo"""
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("❌ Please set GROQ_API_KEY in .env file")
        return
    
    print("🐛 DEBUG DEMO - Timetable Generation with Debug Output")
    print("="*60)
    
    # Create minimal test data
    courses, faculty = create_minimal_test_data()
    
    print(f"📊 Test data: {len(courses)} courses, {len(faculty)} faculty")
    
    try:
        # Create timetable graph with debug enabled
        timetable_graph = TimetableGraph(groq_api_key, debug=True)
        
        # Generate timetable (this will show all debug output)
        result = timetable_graph.generate_timetable(courses, faculty)
        
        print(f"\n🎯 FINAL RESULT:")
        print(f"Status: {result['status']}")
        print(f"Generated slots: {len(result['generated_slots'])}")
        print(f"Conflicts: {len(result['conflicts'])}")
        
        if result['conflicts']:
            print(f"\n⚠️ Remaining conflicts:")
            for conflict in result['conflicts']:
                print(f"  - {conflict}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()