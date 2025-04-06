from agents import Agent

from app.config import BASE_MODEL_NAME
from app.types.output import UserQueryPlan
from app.prompts.planner import PROMPT

planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model=BASE_MODEL_NAME,
    output_type=UserQueryPlan,
)
