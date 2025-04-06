from agents import set_default_openai_api, set_tracing_disabled
from openai import AsyncOpenAI
from agents import set_default_openai_client
from app.config import BASIC_LLM_API_KEY, BASIC_LLM_URL
from app.mcps.file import file_mcp_server
from app.manager import Manager
from app.utils.logging import setup_logger
import sys

# Set up main logger
logger = setup_logger(name="main")

custom_client = AsyncOpenAI(base_url=BASIC_LLM_URL, api_key=BASIC_LLM_API_KEY)
set_default_openai_client(client=custom_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

async def main():

    try:
        logger.info("Initializing file MCP server")
        await file_mcp_server.connect()
        logger.info("File MCP server connected successfully")
          
        logger.info("Initializing manager")
        manager = Manager()
        
        query = input("Please enter your goal: ")
        logger.info(f"Executing query: {query}")
        
        result = await manager.run(query)

        logger.debug(f"Final result: {result}")
        print(result)
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
    finally:
        logger.info("Cleaning up resources...")
        await file_mcp_server.cleanup()



import asyncio
if __name__ == "__main__":
    logger.info("Starting application")
    asyncio.run(main())
    logger.info("Application ended")

