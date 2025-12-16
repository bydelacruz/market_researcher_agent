from duckduckgo_search import DDGS


def search_web(query: str) -> str:
    if not query:
        return "Please provide a search query"

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

        formatted_result = ""

        for result in results:
            formatted = f"""
                Title: {result["title"]}\n
                Link: {result["href"]}\n
                snippet: {result["body"]}\n
            """
            formatted_result += formatted

        return formatted_result
