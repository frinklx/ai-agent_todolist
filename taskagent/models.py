from datetime import datetime
from typing import Dict, List, Optional
from dateutil import parser

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