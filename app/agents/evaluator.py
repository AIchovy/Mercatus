from agents import Agent

from app.types.output import EvaluatorResult
from app.config import BASE_MODEL_NAME
from app.prompts.evaluator import dynamic_instructions


evaluator_agent = Agent(
    name="EvaluatorAgent",
    instructions=dynamic_instructions,
    model=BASE_MODEL_NAME,
    output_type=EvaluatorResult,
)
