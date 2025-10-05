"""
Student Input Demo - Shows how to use the new student-centric timetable system
This script demonstrates the comprehensive student management and individual timetable generation
"""

import os
from dotenv import load_dotenv
from models import (
    Student, Course, Faculty, CourseType, DayOfWeek, TimeSlot
)
from student_manager import StudentManager
from interactive_student_system import InteractiveStudentSystem

def demo_student_system():
    """Demonstrate the complete student system workflow"""
    
    print("🎓 STUDENT TIMETABLE SYSTEM DEMO")
    print("="*60)
    
    # Initialize the system
    system = InteractiveStudentSystem()
    
    print("\n1️⃣ Loading sample data...")
    # Load sample courses and faculty
    system.load_sample_courses()
    system.load_sample_faculty()
    
    print(f"   ✅ Loaded {len(system.courses)} courses")
    print(f"   ✅ Loaded {len(system.faculty)} faculty")
    
    print("\n2️⃣ Loading sample students...")
    # Load sample students
    system.student_manager.load_students_from_json("example_students.json")
    
    print(f"   ✅ Loaded {len(system.student_manager.students)} students")
    
    print("\n3️⃣ Validating student enrollments...")
    # Validate all student enrollments
    print("-" * 50)
    
    for student in system.student_manager.students:
        validation = system.student_manager.validate_student_enrollment(student, system.courses)
        
        status = "✅" if validation["credits_valid"] and not validation["missing_courses"] else "⚠️"
        
        print(f"{status} {validation['student_name']}")
        print(f"   Credits: {validation['total_credits']}/{validation['max_credits']}")
        print(f"   Courses: {validation['total_courses']}")
        
        if validation["warnings"]:
            for warning in validation["warnings"]:
                print(f"   ⚠️ {warning}")
    
    print("\n4️⃣ Generating individual timetables...")
    # Check if GROQ API key is available
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not set. Cannot generate timetables.")
        print("   Please set your API key in .env file to enable timetable generation.")
        print("   Get your API key from: https://console.groq.com/")
        return
    
    # Generate timetables for all students
    system.generate_timetables()
    
    print(f"\n5️⃣ Displaying generated timetables...")
    
    if system.generated_timetables:
        print(f"✅ Successfully generated {len(system.generated_timetables)} timetables")
        
        # Show timetables for first 2 students as example
        for i, timetable in enumerate(system.generated_timetables[:2]):
            system.print_student_timetable(timetable)
        
        if len(system.generated_timetables) > 2:
            print(f"\n... and {len(system.generated_timetables) - 2} more timetables")
        
        print("\n6️⃣ Exporting timetables...")
        # Export timetables to JSON
        try:
            system.export_timetables()
        except:
            # Manual export with default filename
            import json
            
            export_data = {
                "student_timetables": []
            }
            
            for timetable in system.generated_timetables:
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
            
            with open("student_timetables.json", 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✅ Exported {len(system.generated_timetables)} timetables to student_timetables.json")
    
    else:
        print("❌ No timetables were generated")
    
    print("\n7️⃣ Saving all data...")
    # Save all data
    try:
        system.save_all_data()
    except Exception as e:
        print(f"⚠️ Error saving data: {e}")
    
    print("\n🎉 DEMO COMPLETED!")
    print("="*60)
    print("✨ What was demonstrated:")
    print("   • Loading sample courses, faculty, and students")
    print("   • Validating student course enrollments")
    print("   • Generating individual timetables for each student")
    print("   • Displaying formatted timetables")
    print("   • Exporting timetables to JSON")
    print("   • Saving all data for future use")
    print("\n💡 To use the full interactive system, run:")
    print("   python interactive_student_system.py")

def demo_manual_student_creation():
    """Demonstrate manual student creation process"""
    
    print("\n" + "="*60)
    print("📝 MANUAL STUDENT CREATION DEMO")
    print("="*60)
    
    # Create a student manager
    student_manager = StudentManager()
    
    # Create a sample student manually
    student = Student(
        id="S999",
        name="Demo Student",
        email="demo@university.edu",
        semester=3,
        year=2,
        program="B.Tech Computer Science",
        major_courses=["CS301", "CS501"],
        minor_courses=["MATH301"],
        elective_courses=["CS401"],
        skill_based_courses=["MAN201"],
        value_added_courses=["ENG101"],
        max_credits_per_semester=22,
        preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY],
        avoided_time_slots=[
            TimeSlot(start_time="12:00", end_time="13:00")
        ]
    )
    
    student_manager.students.append(student)
    
    print("✅ Created demo student:")
    student_manager.print_student_summary(student)
    
    # Save to JSON
    student_manager.save_students_to_json("demo_student.json")
    
    print("\n✅ Saved demo student to demo_student.json")

def show_system_features():
    """Show the key features of the new student system"""
    
    print("\n" + "="*70)
    print("🌟 NEW STUDENT TIMETABLE SYSTEM FEATURES")
    print("="*70)
    
    features = [
        "👨‍🎓 **Individual Student Management**",
        "   • Student profiles with personal details",
        "   • Program and semester tracking",
        "   • Email and contact information",
        "",
        "📚 **Flexible Course Selection**",
        "   • Major courses (core program courses)",
        "   • Minor courses (secondary specialization)",
        "   • Elective courses (optional choices)",
        "   • Skill-based courses (practical skills)",
        "   • Value-added courses (additional certifications)",
        "",
        "⚙️ **Student Preferences**",
        "   • Preferred days of the week",
        "   • Time slots to avoid",
        "   • Maximum credit limits per semester",
        "",
        "🗓️ **Individual Timetable Generation**",
        "   • Personalized timetables for each student",
        "   • Considers student's enrolled courses only",
        "   • Respects student preferences and constraints",
        "   • Handles different course combinations",
        "",
        "📊 **Comprehensive Validation**",
        "   • Credit limit validation",
        "   • Course availability checking",
        "   • Prerequisite validation (future feature)",
        "   • Conflict detection and resolution",
        "",
        "💾 **Data Management**",
        "   • JSON import/export for all data",
        "   • Persistent storage of student information",
        "   • Backup and restore capabilities",
        "   • Sample data for quick testing",
        "",
        "🎯 **Interactive Interface**",
        "   • Step-by-step student registration",
        "   • Menu-driven course selection",
        "   • Real-time validation feedback",
        "   • Formatted timetable display"
    ]
    
    for feature in features:
        print(feature)
    
    print("\n" + "="*70)
    print("🚀 USAGE SCENARIOS")
    print("="*70)
    
    scenarios = [
        "🎓 **Individual Student Registration**",
        "   Use when: Registering new students with their course choices",
        "   Benefit: Personalized academic planning",
        "",
        "📚 **Course Planning & Validation**", 
        "   Use when: Planning semester course loads",
        "   Benefit: Avoid credit overloads and conflicts",
        "",
        "🗓️ **Personal Timetable Generation**",
        "   Use when: Creating individual class schedules",
        "   Benefit: Optimized schedules respecting preferences",
        "",
        "📊 **Academic Tracking**",
        "   Use when: Monitoring student progress",
        "   Benefit: Track credits, courses, and requirements",
        "",
        "🏫 **Institution Management**",
        "   Use when: Managing multiple students and programs",
        "   Benefit: Centralized student and course management"
    ]
    
    for scenario in scenarios:
        print(scenario)

def main():
    """Main demo function"""
    
    print("🎓 COMPREHENSIVE STUDENT TIMETABLE SYSTEM")
    print("="*60)
    print("This demo shows the enhanced system that handles:")
    print("• Individual student details and preferences")
    print("• Multiple course types (Major, Minor, Electives, etc.)")
    print("• Personalized timetable generation")
    print("• Complete data management")
    
    # Show system features
    show_system_features()
    
    # Run the main demo
    demo_student_system()
    
    # Show manual student creation
    demo_manual_student_creation()
    
    print("\n" + "="*70)
    print("🎯 NEXT STEPS")
    print("="*70)
    print("1. Set up your GROQ_API_KEY in .env file")
    print("2. Run 'python interactive_student_system.py' for full interface")
    print("3. Customize course types and student fields as needed")
    print("4. Integrate with your institution's existing systems")
    print("5. Add web interface for easier access")

if __name__ == "__main__":
    main()
