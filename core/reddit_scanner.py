"""
Reddit scanner: extracts posts/comments by subreddits and keywords.
Only invoked when "reddit" is in config TARGET["sources"].
"""

def run(subreddits: list[str], keywords: dict) -> dict:
    """
    Scans subreddits by keywords.
    Returns a dict with raw posts/comments (no LLM here).
    """
    # TODO: PRAW
    return {
        "subreddits": subreddits,
        "posts": [],
        "comments": [],
    }
