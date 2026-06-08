import os
import httpx
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv(override=True)


def web_search(query: str, max_results: int = 5) -> str:
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return f"Error: TAVILY_API_KEY not set. Web search cannot be performed."

    try:
        client = TavilyClient(api_key=api_key)
        tavily_response = client.search(query=query, max_results=max_results)

        results = tavily_response.get("results", [])
        if not results:
            return f"No results found for query: '{query}'"

        output = ""
        for i, r in enumerate(results):
            output += f"Result {i + 1}:\n"
            output += f"Title: {r.get('title', 'N/A')}\n"
            output += f"URL: {r.get('url', 'N/A')}\n"
            output += f"Content: {r.get('content', 'N/A')}\n\n"
        
        return output.strip()

    except Exception as e:
        return f"Error searching web: {str(e)}"


def crawl_url(url: str) -> str:
    try:
        url = f"https://r.jina.ai/{url}"
        headers = {}

        api_key = os.environ.get("JINA_READER_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = httpx.get(
            url,
            timeout=15,
            headers=headers
        )

        content = response.text

        lines = content.splitlines()
        if len(content) > 15000:
            content = content[:15000] + "\n... (truncated)"

        return content

    except httpx.TimeoutException:
        return f"Error: Timeout while trying to crawl URL: {url}"
    except Exception as e:
        return f"Error crawling URL: {str(e)}"
