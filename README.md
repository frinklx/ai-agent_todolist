# Enhanced AI-Powered TODO List Agent

A sophisticated and practical TODO list manager with smart features and natural language processing.

## Features

- **Smart Task Creation**:
  - Natural language date parsing (e.g., "by tomorrow", "due next week")
  - Automatic priority detection from keywords
  - Category assignment using @tags (e.g., @work, @home)
  - Hashtags for easy filtering (#project, #meeting)
  
- **Task Organization**:
  - Subtasks for breaking down complex tasks
  - Notes and comments for additional context
  - Categories and tags for better organization
  - Due dates with automatic reminders
  
- **Intelligent Display**:
  - Color-coded priorities and statuses
  - Progress tracking for tasks with subtasks
  - Days remaining until due date
  - Overdue task highlighting
  
- **Powerful Management**:
  - Search across tasks, notes, and tags
  - Filter by category or tags
  - Sort by due date and priority
  - Track completion status

## Installation

1. Clone this repository
2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage Examples

1. Add a task with smart parsing:
```bash
# Task with due date, category, and tags
python todo_agent.py add "Submit report by next Friday @work #quarterly #finance"

# Task with priority keywords
python todo_agent.py add "Urgent meeting with client tomorrow @work #meeting"

# Simple task
python todo_agent.py add "Buy groceries"
```

2. Add subtasks to break down complex tasks:
```bash
python todo_agent.py subtask 1 "Research market trends"
python todo_agent.py subtask 1 "Compile data"
python todo_agent.py subtask 1 "Write executive summary"
```

3. Add notes to tasks:
```bash
python todo_agent.py note 1 "Don't forget to include Q3 projections"
```

4. List tasks with various filters:
```bash
# Show all tasks
python todo_agent.py list

# Show tasks in a specific category
python todo_agent.py list --category work

# Show tasks with specific tags
python todo_agent.py list --tags "quarterly,finance"

# Include completed tasks
python todo_agent.py list --all
```

5. Complete tasks or subtasks:
```bash
# Complete a main task
python todo_agent.py complete 1

# Complete a subtask
python todo_agent.py complete 1 --subtask 2
```

6. Search tasks:
```bash
python todo_agent.py search "meeting"
```

## Smart Features

- **Natural Language Processing**:
  - "Urgent meeting tomorrow" → High priority, due tomorrow
  - "Clean garage whenever" → Low priority
  - "Submit report by next Friday @work #project" → Due next Friday, work category, project tag

- **Automatic Organization**:
  - Tasks are automatically sorted by due date
  - Overdue tasks are highlighted in red
  - Subtask progress is displayed as a ratio (e.g., 2/5 completed)
  - Categories and tags for easy filtering

- **Visual Enhancements**:
  - Color-coded priorities (red for high, yellow for medium, green for low)
  - Clear status indicators (✓ for completed, ○ for pending)
  - Hierarchical display of subtasks
  - Inline notes and comments 