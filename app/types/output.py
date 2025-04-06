from pydantic import BaseModel


class TaskItem(BaseModel):
    task: str
    """Specific single task information"""


class UserQueryPlan(BaseModel):
    tasks: list[TaskItem]
    """Based on user input, generate a plan to guide AI in executing tasks, consisting of multiple tasks."""


class EvaluatorResult(BaseModel):
    status: str
    """Task status: completed/partially_completed/not_completed/failed"""
    
    action: str
    """Suggested action: continue_execution_plan/retry_current_task/adjust_task_plan/terminate_execution"""
    
    overall_status: str
    """Overall task completion status: in_progress/completed/needs_adjustment"""
    
    summary: str
    """Detailed explanation or summary of evaluation results"""


