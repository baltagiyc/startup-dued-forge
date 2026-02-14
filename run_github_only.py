"""
Runs the audit pipeline with GitHub only (no Tavily, no Reddit).
Same as main.py but forces SOURCES = ["github"].
Usage: uv run python run_github_only.py
"""

from main import main

if __name__ == "__main__":
    main(sources_override=["github"])
