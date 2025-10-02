# 🐛 Debug Mode Documentation

## Overview
The enhanced TimetableAgent now includes comprehensive debug output that shows detailed input data analysis and formatted output tables in the command line.

## Debug Features

### 📊 Input Data Analysis
When debug mode is enabled, the system displays:

1. **Faculty Data Table**
   - ID, Name, Department
   - Maximum hours per week
   - Expertise areas

2. **Courses Data Table**
   - Course code, name, credits
   - Assigned faculty ID
   - Hours per week required
   - Preferred days
   - Department

3. **Available Time Slots**
   - All available time periods
   - Start and end times

4. **Summary Statistics**
   - Total courses and faculty
   - Course hours vs faculty capacity
   - Capacity utilization percentage
   - Available slots and days

### 📋 Output Tables
The system shows formatted timetable outputs at each stage:

1. **Initial Generation**: First LLM-generated timetable
2. **Conflict Resolution**: Timetable after resolving conflicts
3. **Optimization**: Final optimized timetable

Each output table includes:
- Day and time slots
- Course assignments
- Faculty assignments
- Room assignments (if available)
- Summary statistics

### 🤖 LLM Interaction Tracking
Debug mode tracks:
- When requests are sent to the LLM
- Response length and success/failure
- Error details if parsing fails
- Raw response preview on errors

## Enabling/Disabling Debug Mode

### Method 1: Environment Variable
```bash
# In .env file
DEBUG_MODE=true   # Enable debug output
DEBUG_MODE=false  # Disable debug output
```

### Method 2: Code Configuration
```python
from timetable_graph import TimetableGraph

# Enable debug
graph = TimetableGraph(api_key, debug=True)

# Disable debug
graph = TimetableGraph(api_key, debug=False)
```

### Method 3: Agent Level
```python
from agents import TimetableAgent

# Enable debug for agent only
agent = TimetableAgent(api_key, debug=True)

# Disable debug
agent = TimetableAgent(api_key, debug=False)
```

## Debug Output Examples

### Input Data Analysis
```
================================================================================
📊 DEBUG: INPUT DATA ANALYSIS
================================================================================

👨‍🏫 FACULTY DATA:
+------+-------------------+------------------+------------------+---------------------+
| ID   | Name              | Department       |   Max Hours/Week | Expertise           |
+======+===================+==================+==================+=====================+
| F001 | Prof. Alice Smith | Computer Science |               15 | Programming, AI     |
+------+-------------------+------------------+------------------+---------------------+

📚 COURSES DATA:
+---------+----------------------+-----------+--------------+--------------+-------------------+
| Code    | Name                 |   Credits | Faculty ID   |   Hours/Week | Preferred Days    |
+=========+======================+===========+==============+==============+===================+
| CS101   | Intro to Programming |         3 | F001         |            3 | Monday, Wednesday |
+---------+----------------------+-----------+--------------+--------------+-------------------+
```

### Output Timetable
```
================================================================================
📋 DEBUG: INITIAL TIMETABLE GENERATION
================================================================================
+-----------+-------------+----------+-----------+--------+
| Day       | Time        | Course   | Faculty   | Room   |
+===========+=============+==========+===========+========+
| Monday    | 09:00-10:00 | CS101    | F001      | R101   |
+-----------+-------------+----------+-----------+--------+
| Tuesday   | 09:00-10:00 | MATH101  | F002      | R201   |
+-----------+-------------+----------+-----------+--------+
```

### LLM Interaction
```
🤖 DEBUG: Sending request to LLM (openai/gpt-oss-20b)...
✅ DEBUG: Received LLM response (1352 characters)
```

### Conflict Resolution
```
🔧 DEBUG: Resolving 2 conflicts...
   1. Faculty F001 has conflicting schedules: CS101 and CS201 on Monday at 09:00-10:00
   2. Room R101 has conflicting bookings: CS101 and MATH101 on Monday at 09:00-10:00
✅ DEBUG: Received conflict resolution response
```

## Performance Impact

- **Debug ON**: Slightly slower due to table formatting and console output
- **Debug OFF**: Minimal overhead, production-ready performance
- **Memory**: Negligible additional memory usage
- **Network**: No impact on LLM API calls

## Best Practices

### Development
- Keep debug mode **ON** during development
- Use debug output to understand LLM decisions
- Monitor capacity utilization in summary statistics

### Production
- Set debug mode **OFF** for production deployments
- Enable debug temporarily for troubleshooting
- Use log files instead of console output for production debugging

### Troubleshooting
1. **No output tables**: Check if `tabulate` package is installed
2. **Malformed tables**: Verify input data structure
3. **Missing debug output**: Ensure `debug=True` is set correctly
4. **LLM errors**: Check raw response in debug output

## Files Modified for Debug Support

1. **`agents.py`**: Added debug methods and output formatting
2. **`timetable_graph.py`**: Added debug parameter passing
3. **`main.py`**: Added debug mode configuration
4. **`requirements.txt`**: Added `tabulate` dependency
5. **`.env`**: Added `DEBUG_MODE` environment variable

## Debug Demo Scripts

- **`debug_demo.py`**: Minimal example showing debug output
- **`test_system.py`**: Component testing with validation
- **`main.py`**: Full system with sample data

Run any of these to see debug output in action:
```bash
python debug_demo.py    # Minimal example
python main.py          # Full system
python test_system.py   # Component tests
```