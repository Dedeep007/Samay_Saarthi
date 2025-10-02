from typing import Dict, List, Optional, TypedDict
from pydantic import BaseModel
from enum import Enum

class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class TimeSlot(BaseModel):
    start_time: str  # Format: "HH:MM"
    end_time: str    # Format: "HH:MM"
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this time slot overlaps with another"""
        start1 = self._time_to_minutes(self.start_time)
        end1 = self._time_to_minutes(self.end_time)
        start2 = self._time_to_minutes(other.start_time)
        end2 = self._time_to_minutes(other.end_time)
        
        return not (end1 <= start2 or end2 <= start1)
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert time string to minutes since midnight"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

class Faculty(BaseModel):
    id: str
    name: str
    department: str
    max_hours_per_week: int = 20
    expertise_areas: List[str] = []

class Course(BaseModel):
    code: str
    name: str
    credits: int
    department: str
    faculty_id: str
    hours_per_week: int
    preferred_days: List[DayOfWeek] = []
    preferred_time_slots: List[TimeSlot] = []
    prerequisites: List[str] = []

class TimetableSlot(BaseModel):
    course_code: str
    faculty_id: str
    day: DayOfWeek
    time_slot: TimeSlot
    room: Optional[str] = None

class TimetableState(TypedDict):
    courses: List[Course]
    faculty: List[Faculty]
    generated_slots: List[TimetableSlot]
    conflicts: List[str]
    status: str
    iteration: int

class TimetableRequest(BaseModel):
    courses: List[Course]
    faculty: List[Faculty]
    working_days: List[DayOfWeek] = [
        DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY,
        DayOfWeek.THURSDAY, DayOfWeek.FRIDAY
    ]
    time_slots: List[TimeSlot] = [
        TimeSlot(start_time="09:00", end_time="10:00"),
        TimeSlot(start_time="10:00", end_time="11:00"),
        TimeSlot(start_time="11:00", end_time="12:00"),
        TimeSlot(start_time="12:00", end_time="13:00"),
        TimeSlot(start_time="14:00", end_time="15:00"),
        TimeSlot(start_time="15:00", end_time="16:00"),
        TimeSlot(start_time="16:00", end_time="17:00")
    ]