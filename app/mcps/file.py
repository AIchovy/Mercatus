import os
from agents.mcp import MCPServer, MCPServerStdio


current_dir = os.path.dirname(os.path.abspath(__file__))
FILES_OUTPUT_DIR = os.path.join(current_dir, "..", "..", "artifacts", "files")


file_mcp_server =  MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", FILES_OUTPUT_DIR],
    }
)