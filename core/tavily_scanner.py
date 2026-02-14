"""
Tavily scanner: multi-source social search (Reddit, HN, Stack Overflow, tech blogs).
No OAuth, single API key. Only invoked when "tavily" is in config TARGET["sources"].
"""

import logging
import os

from tavily import TavilyClient

log = logging.getLogger(__name__)


def run(queries: list[str], max_results_per_query: int = 8) -> dict:
    """
    Runs Tavily search for each query. Aggregates results (title, content, url), dedupes by URL.
    Returns a dict: results["tavily"]["results"] for the analyzer.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        log.warning("TAVILY_API_KEY not set. Skipping Tavily.")
        return {
            "results": [],
            "error": "TAVILY_API_KEY not set",
            "queries": queries,
        }

    log.info("Tavily: %d queries, max %d results per query.", len(queries), max_results_per_query)
    client = TavilyClient(api_key=api_key)
    all_results: list[dict] = []
    seen_urls: set[str] = set()

    for i, q in enumerate(queries):
        try:
            response = client.search(
                query=q,
                max_results=max_results_per_query,
                search_depth="basic",
                include_raw_content=False,
            )
            new = 0
            for r in response.get("results", []):
                url = r.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append({
                        "title": r.get("title", ""),
                        "content": r.get("content", ""),
                        "url": url,
                    })
                    new += 1
            log.info("  [%d/%d] %s -> %d new results (%d total).", i + 1, len(queries), q[:50], new, len(all_results))
        except Exception as e:
            log.warning("  [%d/%d] Query failed: %s", i + 1, len(queries), e)

    log.info("Tavily finished: %d total results (deduplicated).", len(all_results))
    return {
        "results": all_results,
        "error": None,
        "queries": queries,
    }
