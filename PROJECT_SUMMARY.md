# 🎓 Agentic Timetable Generator - Project Summary

## 📁 Project Structure

```
/home/dpv/SIH/
├── .env                    # Environment variables (Groq API key)
├── requirements.txt        # Python dependencies
├── README.md              # Comprehensive documentation
├── models.py              # Pydantic data models
├── agents.py              # LLM-powered timetable agents
├── validators.py          # Conflict detection & validation
├── timetable_graph.py     # LangGraph workflow orchestration
├── main.py                # Main application with sample data
├── custom_example.py      # Template for custom data
├── demo.py                # Interactive demonstration
└── test_system.py         # Component validation tests
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Get Groq API key from https://console.groq.com/
# Add to .env file:
echo "GROQ_API_KEY=your_actual_api_key_here" > .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test Installation
```bash
python test_system.py
```

### 4. Run Demo
```bash
python demo.py
```

### 5. Generate Timetable
```bash
python main.py
```

## 🏗️ System Architecture

### Core Components

1. **Data Models (`models.py`)**
   - `Course`: Course information with credits, faculty, preferences
   - `Faculty`: Faculty details with workload limits and expertise
   - `TimetableSlot`: Individual schedule entries
   - `TimeSlot`: Time period definitions

2. **AI Agents (`agents.py`)**
   - `TimetableAgent`: Uses ChatGroq LLM for intelligent scheduling
   - Handles initial generation, conflict resolution, optimization

3. **Validation System (`validators.py`)**
   - `TimetableValidator`: Detects scheduling conflicts
   - `TimetableOptimizer`: Resolves conflicts and improves distribution

4. **Workflow Engine (`timetable_graph.py`)**
   - `TimetableGraph`: LangGraph-based orchestration
   - Manages complete pipeline: Generate → Validate → Resolve → Optimize

### Workflow Pipeline
```
Input (Courses + Faculty)
    ↓
1. Generate Initial (ChatGroq LLM)
    ↓
2. Validate Constraints
    ↓
3. Resolve Conflicts (ChatGroq LLM) ←┐
    ↓                                 │
4. Re-validate ──────────────────────┘
    ↓
5. Optimize Distribution (ChatGroq LLM)
    ↓
6. Finalize Timetable
    ↓
Output (Optimized Schedule)
```

## 🔧 Key Features

### Intelligent Scheduling
- **LLM-Powered**: Uses Groq's Mixtral model for smart decision making
- **Constraint-Aware**: Respects faculty limits, time conflicts, room availability
- **Preference-Sensitive**: Considers day/time preferences for courses and faculty

### Conflict Resolution
- **Automatic Detection**: Identifies time overlaps, overloaded faculty, room conflicts
- **Iterative Resolution**: Uses LLM to intelligently resolve conflicts
- **Workload Balancing**: Ensures fair distribution of teaching hours

### Credit Distribution
- **Load Balancing**: Distributes courses evenly across days
- **Equity Optimization**: Prevents concentration of heavy course loads
- **Flexibility**: Adapts to varying course credit weights

## 📊 Input Data Format

### Faculty Definition
```python
Faculty(
    id="F001",
    name="Dr. John Smith",
    department="Computer Science",
    max_hours_per_week=20,
    expertise_areas=["Programming", "AI"]
)
```

### Course Definition
```python
Course(
    code="CS101",
    name="Introduction to Programming",
    credits=4,
    department="Computer Science",
    faculty_id="F001",
    hours_per_week=4,
    preferred_days=[DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY]
)
```

## 📈 Output Format

### Timetable Display
```
📅 MONDAY
--------------------------------------------------
  09:00-10:00 | CS101 | Faculty: F001 (Room: R101)
  10:00-11:00 | MATH201 | Faculty: F003 (Room: R201)
  
📅 TUESDAY
--------------------------------------------------
  09:00-10:00 | CS201 | Faculty: F001 (Room: R101)
  11:00-12:00 | CS401 | Faculty: F002 (Room: R301)
```

### Faculty Workload Analysis
```
✅ Dr. John Smith (F001)
   Hours: 12.0/20
   Courses: CS101, CS201, CS301

⚠️ Dr. Sarah Johnson (F002)  
   Hours: 22.0/20 (OVERLOADED)
   Courses: CS401, CS501
```

## 🎯 Use Cases

### Educational Institutions
- **Universities**: Course scheduling for departments
- **Schools**: Class timetable generation
- **Training Centers**: Workshop and session planning

### Corporate Training
- **Employee Training**: Skill development program scheduling
- **Conference Planning**: Multi-track event organization
- **Resource Management**: Meeting room and trainer allocation

## 🔧 Customization Options

### Time Slots
```python
# Default slots (modifiable in code)
time_slots = [
    TimeSlot(start_time="09:00", end_time="10:00"),
    TimeSlot(start_time="10:00", end_time="11:00"),
    # ... add more as needed
]
```

### Working Days
```python
# Default: Monday-Friday (configurable)
working_days = [
    DayOfWeek.MONDAY,
    DayOfWeek.TUESDAY,
    DayOfWeek.WEDNESDAY,
    DayOfWeek.THURSDAY,
    DayOfWeek.FRIDAY
]
```

### LLM Configuration
```python
# Change model in TimetableAgent initialization
agent = TimetableAgent(
    api_key=groq_api_key,
    model_name="mixtral-8x7b-32768"  # or other Groq models
)
```

## 📋 Validation Rules

### Hard Constraints (Must be satisfied)
1. ❌ **No Faculty Conflicts**: Same faculty cannot teach multiple courses simultaneously
2. ❌ **Room Conflicts**: No double-booking of rooms
3. ❌ **Workload Limits**: Faculty hours cannot exceed maximum weekly limit

### Soft Constraints (Optimized)
1. ⚖️ **Credit Balance**: Even distribution of courses across days
2. 📅 **Preference Respect**: Honor faculty and course day/time preferences
3. 🎯 **Gap Minimization**: Reduce gaps in daily schedules

## 🚨 Common Issues & Solutions

### Issue: No timetable generated
**Solution**: Check faculty IDs match between courses and faculty data

### Issue: Too many conflicts
**Solution**: 
- Increase faculty max_hours_per_week
- Reduce course hours_per_week
- Add more available time slots

### Issue: API errors
**Solution**: Verify GROQ_API_KEY in .env file

## 🔮 Future Enhancements

### Advanced Features
- **Multi-campus Support**: Handle multiple locations
- **Resource Constraints**: Include room capacity, equipment requirements
- **Student Preferences**: Factor in student availability and preferences
- **Holiday Integration**: Automatic handling of holidays and breaks

### Technical Improvements
- **Web Interface**: Flask/FastAPI-based GUI
- **Database Integration**: PostgreSQL/MySQL backend
- **Real-time Updates**: Live conflict resolution and updates
- **Export Options**: PDF, Excel, Calendar format exports

## 📞 Support & Development

### Extending the System
1. **Custom Constraints**: Add new validation rules in `validators.py`
2. **Enhanced Prompts**: Improve LLM instructions in `agents.py`
3. **New Workflows**: Modify pipeline in `timetable_graph.py`
4. **Data Models**: Extend structures in `models.py`

### Integration Examples
```python
# REST API Integration
from timetable_graph import TimetableGraph

def generate_schedule_api(request_data):
    courses = [Course(**c) for c in request_data['courses']]
    faculty = [Faculty(**f) for f in request_data['faculty']]
    
    graph = TimetableGraph(api_key)
    result = graph.generate_timetable(courses, faculty)
    
    return {
        'timetable': result['generated_slots'],
        'status': result['status'],
        'conflicts': result['conflicts']
    }
```

## 🎉 Success Metrics

- ✅ **Zero Conflicts**: Perfect timetables with no scheduling issues
- ⚖️ **Balanced Workload**: Fair distribution of teaching hours
- 📊 **Optimal Distribution**: Even spread of courses across days
- 🎯 **Preference Satisfaction**: Maximum respect for stated preferences

---

**Built with**: LangChain, Groq LLM, LangGraph, Pydantic
**Status**: Production Ready
**License**: Open Source