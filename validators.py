from typing import List, Dict, Tuple
from collections import defaultdict
from models import Course, Faculty, TimetableSlot, TimeSlot, DayOfWeek, TimetableState

class TimetableValidator:
    """Validates timetable constraints and detects conflicts"""
    
    def __init__(self):
        self.conflicts = []
    
    def validate_timetable(self, slots: List[TimetableSlot], faculty: List[Faculty]) -> Tuple[bool, List[str]]:
        """Validate the entire timetable and return conflicts"""
        self.conflicts = []
        
        # Check for time conflicts
        self._check_faculty_time_conflicts(slots)
        self._check_room_conflicts(slots)
        
        # Check faculty workload
        self._check_faculty_workload(slots, faculty)
        
        # Check credit distribution
        self._check_credit_distribution(slots)
        
        return len(self.conflicts) == 0, self.conflicts
    
    def _check_faculty_time_conflicts(self, slots: List[TimetableSlot]):
        """Check if a faculty member is assigned to multiple slots at the same time"""
        faculty_schedule = defaultdict(list)
        
        for slot in slots:
            faculty_schedule[slot.faculty_id].append(slot)
        
        for faculty_id, faculty_slots in faculty_schedule.items():
            for i in range(len(faculty_slots)):
                for j in range(i + 1, len(faculty_slots)):
                    slot1, slot2 = faculty_slots[i], faculty_slots[j]
                    
                    if (slot1.day == slot2.day and 
                        slot1.time_slot.overlaps_with(slot2.time_slot)):
                        self.conflicts.append(
                            f"Faculty {faculty_id} has conflicting schedules: "
                            f"{slot1.course_code} and {slot2.course_code} on {slot1.day} "
                            f"at {slot1.time_slot.start_time}-{slot1.time_slot.end_time}"
                        )
    
    def _check_room_conflicts(self, slots: List[TimetableSlot]):
        """Check if multiple courses are scheduled in the same room at the same time"""
        room_schedule = defaultdict(list)
        
        for slot in slots:
            if slot.room:
                room_schedule[slot.room].append(slot)
        
        for room, room_slots in room_schedule.items():
            for i in range(len(room_slots)):
                for j in range(i + 1, len(room_slots)):
                    slot1, slot2 = room_slots[i], room_slots[j]
                    
                    if (slot1.day == slot2.day and 
                        slot1.time_slot.overlaps_with(slot2.time_slot)):
                        self.conflicts.append(
                            f"Room {room} has conflicting bookings: "
                            f"{slot1.course_code} and {slot2.course_code} on {slot1.day} "
                            f"at {slot1.time_slot.start_time}-{slot1.time_slot.end_time}"
                        )
    
    def _check_faculty_workload(self, slots: List[TimetableSlot], faculty: List[Faculty]):
        """Check if faculty workload exceeds maximum hours"""
        faculty_dict = {f.id: f for f in faculty}
        faculty_hours = defaultdict(int)
        
        for slot in slots:
            # Calculate hours for this slot
            start_minutes = self._time_to_minutes(slot.time_slot.start_time)
            end_minutes = self._time_to_minutes(slot.time_slot.end_time)
            hours = (end_minutes - start_minutes) / 60
            
            faculty_hours[slot.faculty_id] += hours
        
        for faculty_id, total_hours in faculty_hours.items():
            if faculty_id in faculty_dict:
                max_hours = faculty_dict[faculty_id].max_hours_per_week
                if total_hours > max_hours:
                    self.conflicts.append(
                        f"Faculty {faculty_id} is overloaded: {total_hours:.1f} hours "
                        f"(max: {max_hours} hours)"
                    )
    
    def _check_credit_distribution(self, slots: List[TimetableSlot]):
        """Check if credit distribution is balanced across days"""
        daily_slots = defaultdict(list)
        
        for slot in slots:
            daily_slots[slot.day].append(slot)
        
        slot_counts = [len(slots) for slots in daily_slots.values()]
        if slot_counts:
            avg_slots = sum(slot_counts) / len(slot_counts)
            max_deviation = max(abs(count - avg_slots) for count in slot_counts)
            
            if max_deviation > 2:  # Allow some flexibility
                # Create a proper dictionary mapping day names to slot counts
                daily_distribution = {day.value: len(slots) for day, slots in daily_slots.items()}
                self.conflicts.append(
                    f"Unbalanced credit distribution across days. "
                    f"Daily slots: {daily_distribution}"
                )
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert time string to minutes since midnight"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

class TimetableOptimizer:
    """Optimizes timetable by resolving conflicts and improving distribution"""
    
    def __init__(self):
        self.validator = TimetableValidator()
    
    def optimize_timetable(self, state: TimetableState) -> TimetableState:
        """Optimize the current timetable"""
        slots = state["generated_slots"]
        faculty = state["faculty"]
        
        # Validate current state
        is_valid, conflicts = self.validator.validate_timetable(slots, faculty)
        
        if is_valid:
            state["status"] = "optimized"
            state["conflicts"] = []
        else:
            # Try to resolve conflicts
            optimized_slots = self._resolve_conflicts(slots, conflicts, faculty)
            state["generated_slots"] = optimized_slots
            
            # Re-validate
            is_valid, remaining_conflicts = self.validator.validate_timetable(optimized_slots, faculty)
            state["conflicts"] = remaining_conflicts
            state["status"] = "optimized" if is_valid else "conflicts_remaining"
        
        return state
    
    def _resolve_conflicts(self, slots: List[TimetableSlot], conflicts: List[str], faculty: List[Faculty]) -> List[TimetableSlot]:
        """Attempt to resolve conflicts by rescheduling"""
        # This is a simplified conflict resolution
        # In a real implementation, you might use more sophisticated algorithms
        
        # For now, we'll just return the original slots
        # A more advanced implementation would:
        # 1. Identify conflicting slots
        # 2. Try alternative time slots
        # 3. Redistribute faculty assignments
        # 4. Use constraint satisfaction algorithms
        
        return slots