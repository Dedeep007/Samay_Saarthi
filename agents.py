import os
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
import json
from tabulate import tabulate
from models import Course, Faculty, TimetableSlot, TimeSlot, DayOfWeek
from dotenv import load_dotenv

load_dotenv()

class TimetableAgent:
    """Agent that uses LLM to generate timetable suggestions"""

    def __init__(self, api_key: str = os.getenv("GROQ_API_KEY"), model_name: str = "deepseek-r1-distill-llama-70b", debug: bool = True):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model_name,
            temperature=0.1
        )
        self.debug = debug
        
        self.system_prompt = """You are an expert timetable scheduler. Your task is to create optimal course schedules 
        that avoid conflicts and ensure fair distribution of workload.

        Key constraints to follow:
        1. No faculty member should have overlapping time slots
        2. Respect faculty maximum hours per week
        3. Distribute courses evenly across days
        4. Consider course credit weights
        5. Avoid room conflicts if rooms are specified

        Always respond with valid JSON containing the timetable slots."""

    def _debug_print_input_data(self, courses: List[Course], faculty: List[Faculty], 
                              available_days: List[DayOfWeek], available_slots: List[TimeSlot]):
        """Print formatted input data for debugging"""
        if not self.debug:
            return
            
        print("\n" + "="*80)
        print("📊 DEBUG: INPUT DATA ANALYSIS")
        print("="*80)
        
        # Faculty table
        print("\n👨‍🏫 FACULTY DATA:")
        faculty_data = []
        for f in faculty:
            faculty_data.append([
                f.id,
                f.name,
                f.department,
                f.max_hours_per_week,
                ", ".join(f.expertise_areas) if f.expertise_areas else "N/A"
            ])
        
        faculty_headers = ["ID", "Name", "Department", "Max Hours/Week", "Expertise"]
        print(tabulate(faculty_data, headers=faculty_headers, tablefmt="grid"))
        
        # Courses table
        print("\n📚 COURSES DATA:")
        courses_data = []
        for c in courses:
            preferred_days = ", ".join([day.value for day in c.preferred_days]) if c.preferred_days else "Any"
            courses_data.append([
                c.code,
                c.name,
                c.credits,
                c.faculty_id,
                c.hours_per_week,
                preferred_days,
                c.department
            ])
        
        courses_headers = ["Code", "Name", "Credits", "Faculty ID", "Hours/Week", "Preferred Days", "Department"]
        print(tabulate(courses_data, headers=courses_headers, tablefmt="grid"))
        
        # Available time slots
        print(f"\n⏰ AVAILABLE TIME SLOTS:")
        slots_data = []
        for slot in available_slots:
            slots_data.append([slot.start_time, slot.end_time])
        
        slots_headers = ["Start Time", "End Time"]
        print(tabulate(slots_data, headers=slots_headers, tablefmt="grid"))
        
        # Available days
        print(f"\n📅 AVAILABLE DAYS: {', '.join([day.value for day in available_days])}")
        
        # Summary statistics
        print(f"\n📈 SUMMARY STATISTICS:")
        total_course_hours = sum(c.hours_per_week for c in courses)
        total_faculty_capacity = sum(f.max_hours_per_week for f in faculty)
        
        stats_data = [
            ["Total Courses", len(courses)],
            ["Total Faculty", len(faculty)],
            ["Total Course Hours/Week", total_course_hours],
            ["Total Faculty Capacity/Week", total_faculty_capacity],
            ["Capacity Utilization", f"{(total_course_hours/total_faculty_capacity)*100:.1f}%" if total_faculty_capacity > 0 else "N/A"],
            ["Available Time Slots", len(available_slots)],
            ["Available Days", len(available_days)]
        ]
        
        print(tabulate(stats_data, headers=["Metric", "Value"], tablefmt="grid"))

    def _debug_print_output_table(self, timetable_data: List[Dict[str, Any]], title: str = "GENERATED TIMETABLE"):
        """Print formatted output timetable for debugging"""
        if not self.debug or not timetable_data:
            return
            
        print(f"\n" + "="*80)
        print(f"📋 DEBUG: {title}")
        print("="*80)
        
        # Group by day for better visualization
        day_groups = {}
        for slot in timetable_data:
            day = slot.get('day', 'Unknown')
            if day not in day_groups:
                day_groups[day] = []
            day_groups[day].append(slot)
        
        # Sort days in order
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        all_slots_data = []
        for day in day_order:
            if day in day_groups:
                # Sort slots by start time
                day_slots = sorted(day_groups[day], key=lambda x: x.get('time_slot', {}).get('start_time', '00:00'))
                
                for slot in day_slots:
                    time_slot = slot.get('time_slot', {})
                    all_slots_data.append([
                        day,
                        f"{time_slot.get('start_time', 'N/A')}-{time_slot.get('end_time', 'N/A')}",
                        slot.get('course_code', 'N/A'),
                        slot.get('faculty_id', 'N/A'),
                        slot.get('room', 'N/A')
                    ])
        
        headers = ["Day", "Time", "Course", "Faculty", "Room"]
        print(tabulate(all_slots_data, headers=headers, tablefmt="grid"))
        
        # Summary statistics
        print(f"\n📊 TIMETABLE STATISTICS:")
        stats = self._calculate_timetable_stats(timetable_data)
        stats_data = [
            ["Total Slots", stats['total_slots']],
            ["Unique Courses", stats['unique_courses']],
            ["Unique Faculty", stats['unique_faculty']],
            ["Days with Classes", stats['days_with_classes']],
            ["Average Slots per Day", f"{stats['avg_slots_per_day']:.1f}"]
        ]
        
        print(tabulate(stats_data, headers=["Metric", "Value"], tablefmt="grid"))

    def _calculate_timetable_stats(self, timetable_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics for the timetable"""
        if not timetable_data:
            return {
                'total_slots': 0,
                'unique_courses': 0,
                'unique_faculty': 0,
                'days_with_classes': 0,
                'avg_slots_per_day': 0
            }
        
        courses = set(slot.get('course_code') for slot in timetable_data if slot.get('course_code'))
        faculty = set(slot.get('faculty_id') for slot in timetable_data if slot.get('faculty_id'))
        days = set(slot.get('day') for slot in timetable_data if slot.get('day'))
        
        return {
            'total_slots': len(timetable_data),
            'unique_courses': len(courses),
            'unique_faculty': len(faculty),
            'days_with_classes': len(days),
            'avg_slots_per_day': len(timetable_data) / len(days) if days else 0
        }

    def generate_initial_timetable(self, courses: List[Course], faculty: List[Faculty], 
                                 available_days: List[DayOfWeek], available_slots: List[TimeSlot]) -> List[Dict[str, Any]]:
        """Generate initial timetable using LLM"""
        
        # Debug: Print input data
        self._debug_print_input_data(courses, faculty, available_days, available_slots)
        
        courses_data = [course.model_dump() for course in courses]
        faculty_data = [f.model_dump() for f in faculty]
        
        if self.debug:
            print(f"\n🤖 DEBUG: Sending request to LLM ({self.llm.model_name})...")
        
        prompt = f"""
        Generate a weekly timetable for the following courses and faculty:

        Courses:
        {json.dumps(courses_data, indent=2)}

        Faculty:
        {json.dumps(faculty_data, indent=2)}

        Available Days: {[day.value for day in available_days]}
        Available Time Slots: {[{'start': slot.start_time, 'end': slot.end_time} for slot in available_slots]}

        Create a timetable that:
        1. Assigns each course to appropriate time slots based on hours_per_week
        2. Ensures no faculty conflicts
        3. Distributes workload evenly
        4. Respects faculty preferences if any

        Respond with a JSON array of timetable slots in this format:
        [
            {{
                "course_code": "CS101",
                "faculty_id": "F001",
                "day": "Monday",
                "time_slot": {{"start_time": "09:00", "end_time": "10:00"}},
                "room": "R101"
            }}
        ]
        """

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        
        if self.debug:
            print(f"✅ DEBUG: Received LLM response ({len(response.content)} characters)")
        
        try:
            # Extract JSON from response
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1]
            else:
                json_str = content
            
            timetable_data = json.loads(json_str.strip())
            
            # Debug: Print output table
            self._debug_print_output_table(timetable_data, "INITIAL TIMETABLE GENERATION")
            
            return timetable_data
        except Exception as e:
            if self.debug:
                print(f"❌ DEBUG: Error parsing LLM response: {e}")
                print(f"Raw response: {response.content[:500]}...")
            print(f"Error parsing LLM response: {e}")
            return []

    def resolve_conflicts(self, current_timetable: List[Dict[str, Any]], 
                         conflicts: List[str], courses: List[Course], 
                         faculty: List[Faculty]) -> List[Dict[str, Any]]:
        """Use LLM to resolve timetable conflicts"""
        
        if self.debug:
            print(f"\n🔧 DEBUG: Resolving {len(conflicts)} conflicts...")
            for i, conflict in enumerate(conflicts[:3], 1):
                print(f"   {i}. {conflict}")
            if len(conflicts) > 3:
                print(f"   ... and {len(conflicts) - 3} more conflicts")
        
        prompt = f"""
        The current timetable has the following conflicts:
        {json.dumps(conflicts, indent=2)}

        Current timetable:
        {json.dumps(current_timetable, indent=2)}

        Courses info:
        {json.dumps([course.model_dump() for course in courses], indent=2)}

        Faculty info:
        {json.dumps([f.model_dump() for f in faculty], indent=2)}

        Please modify the timetable to resolve these conflicts while maintaining:
        1. All course requirements
        2. Faculty workload limits
        3. No time overlaps for same faculty/room
        4. Balanced distribution across days

        Respond with the corrected timetable in the same JSON format.
        """

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        
        if self.debug:
            print(f"✅ DEBUG: Received conflict resolution response")
        
        try:
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1]
            else:
                json_str = content
            
            resolved_timetable = json.loads(json_str.strip())
            
            # Debug: Print resolved timetable
            self._debug_print_output_table(resolved_timetable, "CONFLICT RESOLUTION RESULT")
            
            return resolved_timetable
        except Exception as e:
            if self.debug:
                print(f"❌ DEBUG: Error parsing conflict resolution response: {e}")
            print(f"Error parsing conflict resolution response: {e}")
            return current_timetable

    def optimize_distribution(self, timetable: List[Dict[str, Any]], 
                            courses: List[Course], faculty: List[Faculty]) -> List[Dict[str, Any]]:
        """Use LLM to optimize course distribution for better balance"""
        
        if self.debug:
            print(f"\n⚡ DEBUG: Optimizing timetable distribution...")
        
        prompt = f"""
        Optimize the following timetable for better distribution and efficiency:

        Current timetable:
        {json.dumps(timetable, indent=2)}

        Courses info:
        {json.dumps([course.model_dump() for course in courses], indent=2)}

        Faculty info:
        {json.dumps([f.model_dump() for f in faculty], indent=2)}

        Optimization goals:
        1. Even distribution of courses across days
        2. Optimal faculty utilization
        3. Minimize gaps in schedule
        4. Consider course credit weights for balanced learning load

        Respond with the optimized timetable in JSON format.
        """

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        
        if self.debug:
            print(f"✅ DEBUG: Received optimization response")
        
        try:
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1]
            else:
                json_str = content
            
            optimized_timetable = json.loads(json_str.strip())
            
            # Debug: Print optimized timetable
            self._debug_print_output_table(optimized_timetable, "OPTIMIZATION RESULT")
            
            return optimized_timetable
        except Exception as e:
            if self.debug:
                print(f"❌ DEBUG: Error parsing optimization response: {e}")
            print(f"Error parsing optimization response: {e}")
            return timetable