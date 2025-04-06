from agents import Agent, RunContextWrapper, WebSearchTool
from agents.model_settings import ModelSettings

from app.tools.browser import browser_use_tool
from app.tools.search import search_tool
from app.tools.file import file_tool
from app.types.context import ExecutorContext
from app.prompts.executor import dynamic_instructions


executor_agent = Agent(
    name="ExecutorAgent",
    instructions=dynamic_instructions,
    tools=[search_tool, browser_use_tool, file_tool],
    model_settings=ModelSettings(tool_choice="required"),
)