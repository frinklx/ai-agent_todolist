import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import subprocess

def install_packages():
    print("Installing required packages...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    from rich.panel import Panel
    from rich.markdown import Markdown
    import nltk
    from nltk.tokenize import word_tokenize
    import parsedatetime
    from dateutil import parser
    from dateutil.relativedelta import relativedelta
except ImportError:
    install_packages()
    import click
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    from rich.panel import Panel
    from rich.markdown import Markdown
    import nltk
    from nltk.tokenize import word_tokenize
    import parsedatetime
    from dateutil import parser
    from dateutil.relativedelta import relativedelta

# Download required NLTK data
nltk.download('punkt', quiet=True)

console = Console()
cal = parsedatetime.Calendar()

class Task:
    def __init__(self, id: int, description: str, priority: str = "medium"):
        self.id = id
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self.completed = False
        self.due_date: Optional[datetime] = None
        self.category: str = "general"
        self.notes: str = ""
        self.subtasks: List[Dict] = []
        self.tags: List[str] = []

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "category": self.category,
            "notes": self.notes,
            "subtasks": self.subtasks,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            data.get("id", 0),
            data.get("description", ""),
            data.get("priority", "medium")
        )
        task.created_at = parser.parse(data.get("created_at", datetime.now().isoformat()))
        task.completed = data.get("completed", False)
        task.due_date = parser.parse(data.get("due_date")) if data.get("due_date") else None
        task.category = data.get("category", "general")
        task.notes = data.get("notes", "")
        task.subtasks = data.get("subtasks", [])
        task.tags = data.get("tags", [])
        return task

class TodoAgent:
    def __init__(self):
        self.tasks: List[Task] = []
        self.data_file = 'tasks.json'
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
        
        # Priority detection
        priority_keywords = {
            "high": ["urgent", "important", "critical", "asap", "emergency"],
            "low": ["whenever", "someday", "eventually", "optional"],
        }
        
        priority = "medium"
        category = "general"
        due_date = None
        tags = []

        # Extract hashtags
        words = description.split()
        tags = [word[1:] for word in words if word.startswith('#')]
        
        # Remove hashtags from description
        description = ' '.join(word for word in words if not word.startswith('#'))

        # Check for category indicators (e.g., @work, @home)
        for word in words:
            if word.startswith('@'):
                category = word[1:].lower()
                description = description.replace(word, '').strip()

        # Priority detection
        for word in tokens:
            for p, keywords in priority_keywords.items():
                if word in keywords:
                    priority = p
                    break

        # Date detection - look for common date patterns
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
        
        # Use detected priority unless explicitly specified
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

            # Show subtasks if any
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

            # Show notes if any
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

@click.group()
def cli():
    """Enhanced AI-powered TODO list manager"""
    pass

@cli.command()
@click.argument('description')
@click.option('--priority', '-p', default='medium', type=click.Choice(['low', 'medium', 'high']))
def add(description, priority):
    """Add a new task with smart parsing of dates, categories, and tags"""
    agent = TodoAgent()
    task = agent.add_task(description, priority)
    rprint(f"[green]Added task:[/] {task.description}")
    if task.due_date:
        rprint(f"[blue]Due date:[/] {task.due_date.strftime('%Y-%m-%d %H:%M')}")
    if task.tags:
        rprint(f"[yellow]Tags:[/] #{' #'.join(task.tags)}")

@cli.command()
@click.argument('task_id', type=int)
@click.argument('description')
def subtask(task_id, description):
    """Add a subtask to an existing task"""
    agent = TodoAgent()
    if agent.add_subtask(task_id, description):
        rprint(f"[green]Added subtask to task {task_id}[/]")
    else:
        rprint(f"[red]Task {task_id} not found![/]")

@cli.command()
@click.argument('task_id', type=int)
@click.argument('note')
def note(task_id, note):
    """Add a note to an existing task"""
    agent = TodoAgent()
    if agent.add_note(task_id, note):
        rprint(f"[green]Added note to task {task_id}[/]")
    else:
        rprint(f"[red]Task {task_id} not found![/]")

@cli.command()
@click.option('--all', '-a', is_flag=True, help='Show completed tasks')
@click.option('--category', '-c', help='Filter by category')
@click.option('--tags', '-t', help='Filter by tags (comma-separated)')
def list(all, category, tags):
    """List tasks with optional filters"""
    agent = TodoAgent()
    tags_list = tags.split(',') if tags else None
    agent.list_tasks(show_completed=all, category=category, tags=tags_list)

@cli.command()
@click.argument('task_id', type=int)
@click.option('--subtask', '-s', type=int, help='Subtask ID to complete')
def complete(task_id, subtask):
    """Mark a task or subtask as completed"""
    agent = TodoAgent()
    if agent.complete_task(task_id, subtask):
        if subtask:
            rprint(f"[green]Marked subtask {subtask} of task {task_id} as completed![/]")
        else:
            rprint(f"[green]Marked task {task_id} as completed![/]")
    else:
        rprint(f"[red]Task or subtask not found![/]")

@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """Delete a task"""
    agent = TodoAgent()
    agent.delete_task(task_id)
    rprint(f"[yellow]Deleted task {task_id}[/]")

@cli.command()
@click.argument('query')
def search(query):
    """Search tasks by description, category, tags, or notes"""
    agent = TodoAgent()
    results = agent.search_tasks(query)
    if results:
        rprint(f"[green]Found {len(results)} matching tasks:[/]")
        for task in results:
            rprint(Panel(f"[bold]#{task.id}[/] {task.description}"))
    else:
        rprint("[yellow]No matching tasks found.[/]")

if __name__ == '__main__':
    cli() 