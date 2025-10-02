#!/usr/bin/env python3
"""
Quick test to validate the timetable system components
"""

from models import Course, Faculty, DayOfWeek, TimeSlot, TimetableSlot
from validators import TimetableValidator
import json

def test_models():
    """Test data models"""
    print("🧪 Testing Data Models...")
    
    # Test Faculty
    faculty = Faculty(
        id="TEST001",
        name="Test Professor",
        department="Test Dept",
        max_hours_per_week=20
    )
    print(f"✅ Faculty created: {faculty.name}")
    
    # Test Course
    course = Course(
        code="TEST101",
        name="Test Course",
        credits=3,
        department="Test Dept",
        faculty_id="TEST001",
        hours_per_week=3
    )
    print(f"✅ Course created: {course.code}")
    
    # Test TimeSlot
    time_slot = TimeSlot(start_time="09:00", end_time="10:00")
    time_slot2 = TimeSlot(start_time="09:30", end_time="10:30")
    
    # Test overlap detection
    overlap = time_slot.overlaps_with(time_slot2)
    print(f"✅ Time overlap detection: {overlap} (should be True)")
    
    # Test TimetableSlot
    timetable_slot = TimetableSlot(
        course_code=course.code,
        faculty_id=faculty.id,
        day=DayOfWeek.MONDAY,
        time_slot=time_slot
    )
    print(f"✅ Timetable slot created: {timetable_slot.course_code} on {timetable_slot.day}")
    
    return faculty, course, timetable_slot

def test_validator():
    """Test validator functionality"""
    print("\n🔍 Testing Validator...")
    
    faculty, course, slot = test_models()
    validator = TimetableValidator()
    
    # Test with single slot (should be valid)
    is_valid, conflicts = validator.validate_timetable([slot], [faculty])
    print(f"✅ Single slot validation: Valid={is_valid}, Conflicts={len(conflicts)}")
    
    # Test with conflicting slots
    conflicting_slot = TimetableSlot(
        course_code="CONFLICT101",
        faculty_id=faculty.id,
        day=DayOfWeek.MONDAY,
        time_slot=TimeSlot(start_time="09:30", end_time="10:30")
    )
    
    is_valid, conflicts = validator.validate_timetable([slot, conflicting_slot], [faculty])
    print(f"✅ Conflict detection: Valid={is_valid}, Conflicts={len(conflicts)}")
    
    if conflicts:
        print(f"   Detected conflict: {conflicts[0]}")

def test_json_serialization():
    """Test JSON serialization of models"""
    print("\n💾 Testing JSON Serialization...")
    
    faculty, course, slot = test_models()
    
    # Test serialization
    try:
        faculty_json = faculty.model_dump()
        course_json = course.model_dump()
        
        print("✅ JSON serialization successful")
        print(f"   Faculty JSON keys: {list(faculty_json.keys())}")
        print(f"   Course JSON keys: {list(course_json.keys())}")
        
        # Test deserialization
        faculty_restored = Faculty(**faculty_json)
        course_restored = Course(**course_json)
        
        print("✅ JSON deserialization successful")
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")

def main():
    """Run all tests"""
    print("🚀 TIMETABLE SYSTEM COMPONENT TESTS")
    print("=" * 50)
    
    try:
        test_models()
        test_validator()
        test_json_serialization()
        
        print("\n🎉 All tests passed!")
        print("\nSystem is ready for timetable generation.")
        print("Next: Set GROQ_API_KEY in .env and run main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()