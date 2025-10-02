from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from models import TimetableState, Course, Faculty, TimetableSlot, TimeSlot, DayOfWeek
from agents import TimetableAgent
from validators import TimetableValidator, TimetableOptimizer
import json

class TimetableGraph:
    """LangGraph implementation for timetable generation workflow"""
    
    def __init__(self, groq_api_key: str, debug: bool = True):
        self.agent = TimetableAgent(groq_api_key, debug=debug)
        self.validator = TimetableValidator()
        self.optimizer = TimetableOptimizer()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(TimetableState)
        
        # Add nodes
        workflow.add_node("generate_initial", self._generate_initial_timetable)
        workflow.add_node("validate", self._validate_timetable)
        workflow.add_node("resolve_conflicts", self._resolve_conflicts)
        workflow.add_node("optimize", self._optimize_timetable)
        workflow.add_node("finalize", self._finalize_timetable)
        
        # Add edges
        workflow.set_entry_point("generate_initial")
        
        workflow.add_edge("generate_initial", "validate")
        
        workflow.add_conditional_edges(
            "validate",
            self._should_resolve_conflicts,
            {
                "resolve": "resolve_conflicts",
                "optimize": "optimize",
                "finalize": "finalize"
            }
        )
        
        workflow.add_edge("resolve_conflicts", "validate")
        workflow.add_edge("optimize", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def _generate_initial_timetable(self, state: TimetableState) -> TimetableState:
        """Generate initial timetable using LLM agent"""
        print("🎯 Generating initial timetable...")
        
        courses = state["courses"]
        faculty = state["faculty"]
        
        # Default time slots and days
        available_days = [
            DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY,
            DayOfWeek.THURSDAY, DayOfWeek.FRIDAY
        ]
        available_slots = [
            TimeSlot(start_time="09:00", end_time="10:00"),
            TimeSlot(start_time="10:00", end_time="11:00"),
            TimeSlot(start_time="11:00", end_time="12:00"),
            TimeSlot(start_time="12:00", end_time="13:00"),
            TimeSlot(start_time="14:00", end_time="15:00"),
            TimeSlot(start_time="15:00", end_time="16:00"),
            TimeSlot(start_time="16:00", end_time="17:00")
        ]
        
        timetable_data = self.agent.generate_initial_timetable(
            courses, faculty, available_days, available_slots
        )
        
        # Convert to TimetableSlot objects
        slots = []
        for slot_data in timetable_data:
            try:
                slot = TimetableSlot(
                    course_code=slot_data["course_code"],
                    faculty_id=slot_data["faculty_id"],
                    day=DayOfWeek(slot_data["day"]),
                    time_slot=TimeSlot(
                        start_time=slot_data["time_slot"]["start_time"],
                        end_time=slot_data["time_slot"]["end_time"]
                    ),
                    room=slot_data.get("room")
                )
                slots.append(slot)
            except Exception as e:
                print(f"Error parsing slot: {e}")
                continue
        
        state["generated_slots"] = slots
        state["status"] = "initial_generated"
        state["iteration"] = 1
        
        print(f"✅ Generated {len(slots)} initial time slots")
        return state
    
    def _validate_timetable(self, state: TimetableState) -> TimetableState:
        """Validate current timetable for conflicts"""
        print("🔍 Validating timetable...")
        
        slots = state["generated_slots"]
        faculty = state["faculty"]
        
        is_valid, conflicts = self.validator.validate_timetable(slots, faculty)
        
        state["conflicts"] = conflicts
        
        if is_valid:
            state["status"] = "valid"
            print("✅ Timetable is valid!")
        else:
            state["status"] = "has_conflicts"
            print(f"⚠️ Found {len(conflicts)} conflicts")
            for conflict in conflicts[:3]:  # Show first 3 conflicts
                print(f"  - {conflict}")
        
        return state
    
    def _should_resolve_conflicts(self, state: TimetableState) -> str:
        """Determine next step based on validation results"""
        if state["conflicts"]:
            if state["iteration"] < 3:  # Limit iterations
                return "resolve"
            else:
                return "finalize"  # Give up after 3 attempts
        else:
            return "optimize"
    
    def _resolve_conflicts(self, state: TimetableState) -> TimetableState:
        """Resolve conflicts using LLM agent"""
        print("🔧 Resolving conflicts...")
        
        current_timetable = [
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
            for slot in state["generated_slots"]
        ]
        
        resolved_data = self.agent.resolve_conflicts(
            current_timetable, state["conflicts"], 
            state["courses"], state["faculty"]
        )
        
        # Convert back to TimetableSlot objects
        slots = []
        for slot_data in resolved_data:
            try:
                slot = TimetableSlot(
                    course_code=slot_data["course_code"],
                    faculty_id=slot_data["faculty_id"],
                    day=DayOfWeek(slot_data["day"]),
                    time_slot=TimeSlot(
                        start_time=slot_data["time_slot"]["start_time"],
                        end_time=slot_data["time_slot"]["end_time"]
                    ),
                    room=slot_data.get("room")
                )
                slots.append(slot)
            except Exception as e:
                print(f"Error parsing resolved slot: {e}")
                continue
        
        state["generated_slots"] = slots
        state["status"] = "conflicts_resolved"
        state["iteration"] += 1
        
        print(f"🔄 Resolved conflicts (iteration {state['iteration']})")
        return state
    
    def _optimize_timetable(self, state: TimetableState) -> TimetableState:
        """Optimize timetable for better distribution"""
        print("⚡ Optimizing timetable...")
        
        current_timetable = [
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
            for slot in state["generated_slots"]
        ]
        
        optimized_data = self.agent.optimize_distribution(
            current_timetable, state["courses"], state["faculty"]
        )
        
        # Convert back to TimetableSlot objects
        slots = []
        for slot_data in optimized_data:
            try:
                slot = TimetableSlot(
                    course_code=slot_data["course_code"],
                    faculty_id=slot_data["faculty_id"],
                    day=DayOfWeek(slot_data["day"]),
                    time_slot=TimeSlot(
                        start_time=slot_data["time_slot"]["start_time"],
                        end_time=slot_data["time_slot"]["end_time"]
                    ),
                    room=slot_data.get("room")
                )
                slots.append(slot)
            except Exception as e:
                print(f"Error parsing optimized slot: {e}")
                continue
        
        state["generated_slots"] = slots
        state["status"] = "optimized"
        
        print("✨ Timetable optimized!")
        return state
    
    def _finalize_timetable(self, state: TimetableState) -> TimetableState:
        """Finalize the timetable"""
        print("🎉 Finalizing timetable...")
        
        state["status"] = "finalized"
        
        print(f"Final timetable contains {len(state['generated_slots'])} slots")
        if state["conflicts"]:
            print(f"⚠️ {len(state['conflicts'])} unresolved conflicts remain")
        
        return state
    
    def generate_timetable(self, courses: List[Course], faculty: List[Faculty]) -> TimetableState:
        """Main method to generate timetable"""
        print("🚀 Starting timetable generation...")
        
        initial_state: TimetableState = {
            "courses": courses,
            "faculty": faculty,
            "generated_slots": [],
            "conflicts": [],
            "status": "initializing",
            "iteration": 0
        }
        
        result = self.graph.invoke(initial_state)
        return result