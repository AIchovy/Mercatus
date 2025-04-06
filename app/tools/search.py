from typing import Any
from agents import RunContextWrapper, function_tool
from tavily import TavilyClient
from app.config import TAVILY_API_KEY


@function_tool(name_override="search_tool")
def search_tool(ctx: RunContextWrapper[Any], keyword: str) -> str:
    """Use this tool to search the web url or breif information for the given SEO keyword.

    Args:
        keyword: The keyword to search for.
    """

    client = TavilyClient(api_key=TAVILY_API_KEY)
    # invoke tavily search api
    results = client.search(keyword, max_results=5, include_answer=True,
                            include_raw_content=True, include_images=True)
    if results and "results" in results and len(results["results"]) > 0:
        return str(results["results"])
    return "No results"
