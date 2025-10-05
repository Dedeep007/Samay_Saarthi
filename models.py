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

class CourseType(str, Enum):
    MAJOR = "Major"
    MINOR = "Minor"
    ELECTIVE = "Elective"
    SKILL_BASED = "Skill-based"
    VALUE_ADDED = "Value-added"
    CORE = "Core"

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
    course_type: CourseType = CourseType.CORE
    semester: int = 1
    year: int = 1
    preferred_days: List[DayOfWeek] = []
    preferred_time_slots: List[TimeSlot] = []
    prerequisites: List[str] = []

class Student(BaseModel):
    id: str
    name: str
    email: str
    semester: int
    year: int
    program: str  # e.g., "B.Tech CSE", "M.Tech AI"
    major_courses: List[str] = []  # Course codes for major courses
    minor_courses: List[str] = []  # Course codes for minor courses
    elective_courses: List[str] = []  # Course codes for electives
    skill_based_courses: List[str] = []  # Course codes for skill-based courses
    value_added_courses: List[str] = []  # Course codes for value-added courses
    max_credits_per_semester: int = 24
    preferred_days: List[DayOfWeek] = []
    avoided_time_slots: List[TimeSlot] = []  # Time slots student wants to avoid

class TimetableSlot(BaseModel):
    course_code: str
    faculty_id: str
    day: DayOfWeek
    time_slot: TimeSlot
    room: Optional[str] = None
    student_ids: List[str] = []  # Students enrolled in this slot

class StudentTimetable(BaseModel):
    student_id: str
    student_name: str
    semester: int
    year: int
    slots: List[TimetableSlot] = []
    total_credits: int = 0
    total_hours: int = 0

class TimetableState(TypedDict):
    courses: List[Course]
    faculty: List[Faculty]
    students: List[Student]
    generated_slots: List[TimetableSlot]
    student_timetables: List[StudentTimetable]
    conflicts: List[str]
    status: str
    iteration: int

class TimetableRequest(BaseModel):
    courses: List[Course]
    faculty: List[Faculty]
    students: List[Student] = []
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