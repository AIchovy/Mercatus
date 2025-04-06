**Directory Structure**
# app: app Directory
- code main directory

## agent: Agent Directory
Responsibilities:

- The agent directory contains the core logic of AI agents, including decision-making and tool usage.

## llm: Large Language Model Directory
Responsibilities:

- The llm directory handles integration with large language models (LLMs), including LLM calls, prompt formatting, and response processing.

## tool: Tools Directory
Responsibilities:

- The tool directory contains various tools available to the agent, such as web search, database queries, etc.

## prompt: Prompts Directory
Responsibilities:

- The prompt directory includes prompt templates and related functions sent to the LLM to guide its behavior.

## mcp: Mcp Directory
Responsibilities:

- The mcp directory includes mcp servers define.

**Design Principles & Guidelines**

- The framework follows a modular, extensible, and reusable design.

**Coding Standards**

- Use descriptive naming, add comments, and adhere to Python coding standards (e.g., PEP 8).