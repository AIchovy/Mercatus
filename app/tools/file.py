from typing import Any
from agents import Agent
from app.config import BASE_MODEL_NAME
from app.mcps.file import file_mcp_server

agent_mcp = Agent(
    name="FileMcpAgentTool",
    model=BASE_MODEL_NAME,
    instructions="Use the tools to read the filesystem and write to the filesystem.",
    mcp_servers=[file_mcp_server],
)
file_tool = agent_mcp.as_tool(
    tool_name="file_tool",
    tool_description="Use the tools to read the filesystem and write to the filesystem.",
)
