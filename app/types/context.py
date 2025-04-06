from dataclasses import dataclass

from app.types.output import TaskItem


@dataclass
class ExecutorContext():
    goal: str
    """User's goal"""
    
    tasks: list[TaskItem]
    """All tasks"""

    finished: bool
    """Whether the task is completed"""

    current_task: TaskItem
    """The task currently being executed"""

    execution_history: list[str]
    """Execution history"""
    