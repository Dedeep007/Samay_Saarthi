#!/usr/bin/env python3
"""
Demo script for Agentic Timetable Generator
Shows the complete workflow with sample data
"""

import os
from dotenv import load_dotenv
from main import main, load_sample_data, print_timetable, print_faculty_workload
from timetable_graph import TimetableGraph

def demo_workflow():
    """Demonstrate the complete workflow"""
    
    print("🎓 AGENTIC TIMETABLE GENERATOR DEMO")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("\n❌ GROQ_API_KEY not configured!")
        print("Please follow these steps:")
        print("1. Go to https://console.groq.com/")
        print("2. Get your API key")
        print("3. Add it to .env file: GROQ_API_KEY=your_key_here")
        return False
    
    print("✅ API key configured")
    
    # Load sample data
    courses, faculty = load_sample_data()
    print(f"\n📚 Sample Data Loaded:")
    print(f"   • {len(courses)} courses")
    print(f"   • {len(faculty)} faculty members")
    
    # Show sample data
    print(f"\n👨‍🏫 Faculty Members:")
    for f in faculty[:3]:  # Show first 3
        print(f"   • {f.name} ({f.department}) - Max: {f.max_hours_per_week}h/week")
    if len(faculty) > 3:
        print(f"   ... and {len(faculty) - 3} more")
    
    print(f"\n📖 Courses:")
    for c in courses[:3]:  # Show first 3
        print(f"   • {c.code}: {c.name} ({c.credits} credits, {c.hours_per_week}h/week)")
    if len(courses) > 3:
        print(f"   ... and {len(courses) - 3} more")
    
    print("\n🚀 Starting Timetable Generation...")
    print("-" * 40)
    
    try:
        # Create and run timetable graph
        timetable_graph = TimetableGraph(groq_api_key)
        result = timetable_graph.generate_timetable(courses, faculty)
        
        # Show results
        print_timetable(result)
        print_faculty_workload(result)
        
        # Summary
        print("\n🎯 GENERATION COMPLETE!")
        print("=" * 40)
        print(f"Status: {result['status']}")
        print(f"Total slots: {len(result['generated_slots'])}")
        print(f"Conflicts: {len(result['conflicts'])}")
        print(f"Iterations: {result['iteration']}")
        
        if result['status'] == 'finalized' and not result['conflicts']:
            print("✅ Perfect timetable generated with no conflicts!")
        elif result['conflicts']:
            print(f"⚠️ Some conflicts remain - may need manual adjustment")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_architecture():
    """Show system architecture"""
    print("\n🏗️ SYSTEM ARCHITECTURE")
    print("=" * 40)
    print("""
    Input Data (Courses + Faculty)
           ↓
    ┌─────────────────────────┐
    │   LangGraph Workflow    │
    │                         │
    │  1. Generate Initial    │ ← ChatGroq LLM
    │  2. Validate            │ ← Custom Validators  
    │  3. Resolve Conflicts   │ ← ChatGroq LLM
    │  4. Optimize            │ ← ChatGroq LLM
    │  5. Finalize            │
    └─────────────────────────┘
           ↓
    Optimized Timetable Output

    Key Components:
    • Models: Pydantic data structures
    • Agents: LLM-powered scheduling logic  
    • Validators: Conflict detection & rules
    • Graph: LangGraph workflow orchestration
    """)

if __name__ == "__main__":
    show_architecture()
    success = demo_workflow()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("• Modify custom_example.py with your data")
        print("• Integrate into your application")
        print("• Extend with custom constraints")
    else:
        print("\n💡 Demo failed - check configuration and try again")