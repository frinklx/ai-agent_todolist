import click
from rich import print as rprint
from rich.panel import Panel
from .agent import TodoAgent

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