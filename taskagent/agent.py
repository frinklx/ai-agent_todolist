import json
import os
import ssl
from datetime import datetime
from typing import List, Optional
import nltk
from nltk.tokenize import word_tokenize
import parsedatetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .models import Task

# Fix NLTK SSL verification and download
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Try to download NLTK data, handle errors gracefully
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except Exception:
        # If download fails, use simple word splitting instead
        def word_tokenize(text):
            return text.split()

console = Console()
cal = parsedatetime.Calendar()

class TodoAgent:
    def __init__(self, data_file: str = None):
        self.tasks: List[Task] = []
        self.data_file = data_file or os.path.expanduser('~/.taskagent.json')
        self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]

    def _save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def _parse_date(self, text: str) -> Optional[datetime]:
        try:
            time_struct, parse_status = cal.parse(text)
            if parse_status:
                return datetime(*time_struct[:6])
        except:
            return None
        return None

    def _extract_metadata(self, description: str) -> tuple:
        tokens = word_tokenize(description.lower())
        
        priority_keywords = {
            "high": ["urgent", "important", "critical", "asap", "emergency"],
            "low": ["whenever", "someday", "eventually", "optional"],
        }
        
        priority = "medium"
        category = "general"
        due_date = None
        tags = []

        words = description.split()
        tags = [word[1:] for word in words if word.startswith('#')]
        description = ' '.join(word for word in words if not word.startswith('#'))

        for word in words:
            if word.startswith('@'):
                category = word[1:].lower()
                description = description.replace(word, '').strip()

        for word in tokens:
            for p, keywords in priority_keywords.items():
                if word in keywords:
                    priority = p
                    break

        date_indicators = ["by", "due", "on", "at", "before", "after"]
        text = description.lower()
        for indicator in date_indicators:
            if indicator in text:
                parts = text.split(indicator)
                if len(parts) > 1:
                    possible_date = parts[1].strip()
                    parsed_date = self._parse_date(possible_date)
                    if parsed_date:
                        due_date = parsed_date
                        break

        return description, priority, category, due_date, tags

    def add_task(self, description: str, priority: str = "medium") -> Task:
        description, detected_priority, category, due_date, tags = self._extract_metadata(description)
        
        if priority == "medium":
            priority = detected_priority

        task = Task(len(self.tasks) + 1, description, priority)
        task.due_date = due_date
        task.category = category
        task.tags = tags
        
        self.tasks.append(task)
        self._save_tasks()
        return task

    def add_subtask(self, task_id: int, description: str) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                subtask = {
                    "description": description,
                    "completed": False
                }
                task.subtasks.append(subtask)
                self._save_tasks()
                return True
        return False

    def add_note(self, task_id: int, note: str) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.notes += f"\n{note}" if task.notes else note
                self._save_tasks()
                return True
        return False

    def list_tasks(self, show_completed: bool = False, category: str = None, tags: List[str] = None):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Description")
        table.add_column("Due Date", justify="center")
        table.add_column("Category", justify="center")
        table.add_column("Priority", justify="center")
        table.add_column("Status", justify="center")

        for task in sorted(self.tasks, key=lambda x: (x.due_date or datetime.max, -len(x.subtasks))):
            if not show_completed and task.completed:
                continue
            
            if category and task.category != category:
                continue

            if tags and not any(tag in task.tags for tag in tags):
                continue

            status = "✓" if task.completed else "○"
            if task.subtasks:
                completed_subtasks = sum(1 for st in task.subtasks if st["completed"])
                status = f"({completed_subtasks}/{len(task.subtasks)})"

            priority_colors = {"high": "red", "medium": "yellow", "low": "green"}
            priority = task.priority
            
            due_str = ""
            if task.due_date:
                days_left = (task.due_date - datetime.now()).days
                if days_left < 0:
                    due_str = f"[red]Overdue {abs(days_left)}d[/]"
                elif days_left == 0:
                    due_str = "[red]Today[/]"
                else:
                    due_str = f"{days_left}d left"

            table.add_row(
                str(task.id),
                task.description + (" [dim]#" + " #".join(task.tags) + "[/]" if task.tags else ""),
                due_str,
                task.category,
                f"[{priority_colors.get(priority, 'white')}]{priority}[/]",
                status
            )

            if task.subtasks:
                for i, subtask in enumerate(task.subtasks, 1):
                    status = "✓" if subtask["completed"] else "○"
                    table.add_row(
                        f"└─{task.id}.{i}",
                        f"[dim]{subtask['description']}[/]",
                        "",
                        "",
                        "",
                        status
                    )

            if task.notes:
                table.add_row(
                    "",
                    f"[dim italic]{task.notes}[/]",
                    "",
                    "",
                    "",
                    ""
                )

        console.print(table)

    def complete_task(self, task_id: int, subtask_id: int = None) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                if subtask_id is not None:
                    if 1 <= subtask_id <= len(task.subtasks):
                        task.subtasks[subtask_id - 1]["completed"] = True
                    else:
                        return False
                else:
                    task.completed = True
                self._save_tasks()
                return True
        return False

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._save_tasks()

    def search_tasks(self, query: str) -> List[Task]:
        query = query.lower()
        return [
            task for task in self.tasks
            if query in task.description.lower()
            or query in task.category.lower()
            or any(query in tag.lower() for tag in task.tags)
            or query in task.notes.lower()
        ] 