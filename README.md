# Agentic Timetable Generator

An intelligent timetable generation system using LangChain, Groq LLM, and LangGraph for creating optimal course schedules without conflicts.

## Features

- **Intelligent Scheduling**: Uses Groq LLM (ChatGroq) to generate optimal timetables
- **Conflict Resolution**: Automatically detects and resolves scheduling conflicts
- **Faculty Workload Management**: Ensures fair distribution and prevents overloading
- **Credit Distribution**: Balances course load across days
- **Graph-based Workflow**: Uses LangGraph for structured processing pipeline

## System Components

### 1. Models (`models.py`)
- **Course**: Course information with credits, faculty, and preferences
- **Faculty**: Faculty details with workload limits and expertise
- **TimetableSlot**: Individual schedule entries
- **TimeSlot**: Time period definitions

### 2. Agents (`agents.py`)
- **TimetableAgent**: LLM-powered agent for generating and optimizing schedules
- Uses ChatGroq for intelligent decision making
- Handles initial generation, conflict resolution, and optimization

### 3. Validators (`validators.py`)
- **TimetableValidator**: Checks for scheduling conflicts
- **TimetableOptimizer**: Resolves conflicts and improves distribution
- Validates faculty time conflicts, room conflicts, and workload limits

### 4. Graph Workflow (`timetable_graph.py`)
- **TimetableGraph**: LangGraph-based workflow orchestration
- Manages the complete pipeline from generation to finalization
- Iterative conflict resolution with optimization

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Groq API key:
   - Get API key from https://console.groq.com/
   - Add to `.env` file:
```
GROQ_API_KEY=your_actual_api_key_here
```

## Usage

### Basic Usage

Run the main script with sample data:
```bash
python main.py
```

### Custom Data

Modify `custom_example.py` to use your own courses and faculty:

```python
from models import Course, Faculty, DayOfWeek
from timetable_graph import TimetableGraph

# Define your faculty
faculty = [
    Faculty(
        id="F001",
        name="Dr. John Doe",
        department="Computer Science", 
        max_hours_per_week=20,
        expertise_areas=["Programming", "AI"]
    )
]

# Define your courses
courses = [
    Course(
        code="CS101",
        name="Introduction to Programming",
        credits=4,
        department="Computer Science",
        faculty_id="F001", 
        hours_per_week=4
    )
]

# Generate timetable
timetable_graph = TimetableGraph(groq_api_key)
result = timetable_graph.generate_timetable(courses, faculty)
```

## Workflow Pipeline

```
Input (Courses + Faculty)
    ↓
1. Generate Initial Timetable (LLM)
    ↓
2. Validate for Conflicts
    ↓
3. Resolve Conflicts (if any) → Back to Validate
    ↓
4. Optimize Distribution (LLM)
    ↓
5. Finalize Timetable
    ↓
Output (Optimized Schedule)
```

## Key Constraints

1. **No Faculty Conflicts**: Same faculty cannot teach multiple courses simultaneously
2. **Workload Limits**: Faculty hours don't exceed maximum weekly limit
3. **Room Conflicts**: No double-booking of rooms (if specified)
4. **Credit Balance**: Even distribution of courses across days
5. **Preference Respect**: Consider faculty and course day preferences

## Output

The system generates:
- **Formatted Timetable**: Day-wise schedule display
- **Faculty Workload Analysis**: Hours and course distribution per faculty
- **Conflict Report**: Any unresolved scheduling issues
- **JSON Export**: Machine-readable timetable data

## Example Output

```
📅 MONDAY
--------------------------------------------------
  09:00-10:00 | CS101 | Faculty: F001
  10:00-11:00 | MATH201 | Faculty: F003
  14:00-15:00 | PHY101 | Faculty: F004

📅 TUESDAY  
--------------------------------------------------
  09:00-10:00 | CS201 | Faculty: F001
  11:00-12:00 | CS401 | Faculty: F002
```

## Configuration

### Time Slots
Default time slots (modifiable in code):
- 09:00-10:00, 10:00-11:00, 11:00-12:00, 12:00-13:00
- 14:00-15:00, 15:00-16:00, 16:00-17:00

### Working Days
Default: Monday to Friday (configurable)

### LLM Model
Default: mixtral-8x7b-32768 (Groq)
- High performance for complex scheduling logic
- Can be changed in `TimetableAgent` initialization

## Advanced Features

### Custom Constraints
Extend the validator to add institution-specific rules:
```python
class CustomValidator(TimetableValidator):
    def validate_custom_rules(self, slots):
        # Add your custom validation logic
        pass
```

### Integration APIs
The system can be easily integrated into web applications:
```python
from timetable_graph import TimetableGraph

def generate_schedule_api(courses_data, faculty_data):
    # Convert data to models
    courses = [Course(**course) for course in courses_data]
    faculty = [Faculty(**f) for f in faculty_data] 
    
    # Generate timetable
    graph = TimetableGraph(api_key)
    return graph.generate_timetable(courses, faculty)
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure GROQ_API_KEY is set correctly in .env
2. **No Slots Generated**: Check if faculty IDs match between courses and faculty
3. **Too Many Conflicts**: Reduce course load or increase faculty availability
4. **Import Errors**: Ensure all dependencies are installed

### Performance Tips

- Limit courses to ~20-30 for optimal LLM performance
- Use specific day/time preferences to guide generation
- Increase faculty max_hours if schedules are too constrained

## Contributing

To extend the system:
1. Add new constraint types in `validators.py`
2. Enhance LLM prompts in `agents.py` 
3. Modify workflow in `timetable_graph.py`
4. Add new data models in `models.py`

## License

Open source - feel free to modify and adapt for your institution's needs.