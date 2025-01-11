# TaskAgent - Smart CLI Task Manager

A powerful, AI-enhanced command-line task manager that understands natural language, automatically organizes your tasks, and makes task management a breeze.

## ✨ Key Features

### 🧠 Smart Task Creation
- **Natural Language Understanding**
  ```bash
  taskagent add "Call mom tomorrow morning"  # Automatically sets due date
  taskagent add "Urgent meeting with client"  # Sets high priority
  taskagent add "Clean garage whenever"  # Sets low priority
  ```

- **Smart Categorization**
  ```bash
  taskagent add "Submit report @work #project #q4"  # Adds to work category with tags
  taskagent add "Buy groceries @home #shopping"     # Adds to home category
  ```

### 📊 Task Organization
- **Subtasks for Complex Projects**
  ```bash
  taskagent add "Launch website @work #project"
  taskagent subtask 1 "Design homepage"
  taskagent subtask 1 "Set up hosting"
  taskagent subtask 1 "Deploy site"
  ```

- **Notes and Context**
  ```bash
  taskagent note 1 "Include mobile responsive design"
  taskagent note 1 "Use AWS for hosting"
  ```

### 🔍 Smart Filtering and Search
- **Category Filtering**
  ```bash
  taskagent list --category work
  taskagent list --category home
  ```

- **Tag-based Filtering**
  ```bash
  taskagent list --tags "project,urgent"
  ```

- **Full-text Search**
  ```bash
  taskagent search "website"  # Searches in descriptions, notes, and tags
  ```

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone [your-repo-url]
cd taskagent

# Install the package
pip install -e .
```

### Basic Usage

1. **Adding Tasks**
   ```bash
   # Simple task
   taskagent add "Buy groceries"

   # Task with due date and category
   taskagent add "Submit report by next Friday @work"

   # Task with priority, category, and tags
   taskagent add "Urgent client meeting tomorrow @work #client #important"
   ```

2. **Viewing Tasks**
   ```bash
   # List all active tasks
   taskagent list

   # Include completed tasks
   taskagent list --all

   # Filter by category
   taskagent list --category work

   # Filter by tags
   taskagent list --tags "client,important"
   ```

3. **Managing Tasks**
   ```bash
   # Complete a task
   taskagent complete 1

   # Complete a subtask
   taskagent complete 1 --subtask 2

   # Delete a task
   taskagent delete 1
   ```

## 🎨 Smart Features Explained

### Priority Detection
TaskAgent automatically detects priority from your language:
- **High Priority**: "urgent", "important", "critical", "asap", "emergency"
- **Medium Priority**: (default)
- **Low Priority**: "whenever", "someday", "eventually", "optional"

### Date Parsing
Understands various date formats:
- "tomorrow"
- "next Friday"
- "in 3 days"
- "next week"
- "by end of month"

### Categories and Tags
- **Categories**: Use `@category` (e.g., @work, @home, @personal)
- **Tags**: Use `#tag` (e.g., #project, #urgent, #meeting)

### Visual Indicators
- 🔴 High priority tasks in red
- 🟡 Medium priority tasks in yellow
- 🟢 Low priority tasks in green
- ✓ Completed tasks
- ○ Pending tasks
- (2/5) Progress indicator for tasks with subtasks

## 📁 Data Storage
- Tasks are stored in `~/.taskagent.json`
- Human-readable JSON format
- Automatic backup before modifications

## 💡 Pro Tips

1. **Efficient Task Creation**
   ```bash
   # Combine multiple features in one command
   taskagent add "Urgent presentation for client by tomorrow @work #client #presentation"
   ```

2. **Task Organization**
   ```bash
   # Group related tasks with tags
   taskagent add "Research competitors @work #marketanalysis #q4"
   taskagent add "Create presentation @work #marketanalysis #q4"
   
   # View all related tasks
   taskagent list --tags "marketanalysis"
   ```

3. **Task Progress Tracking**
   ```bash
   # Break down big tasks into subtasks
   taskagent add "Website redesign @work #project"
   taskagent subtask 1 "Wireframes"
   taskagent subtask 1 "Design mockups"
   taskagent subtask 1 "Implementation"
   
   # Track progress
   taskagent complete 1 --subtask 1
   ```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
MIT License - feel free to use this in your own projects! 