"""
Audit target: Meilisearch.
Defines which sources to call (github and/or tavily) and their parameters.
Use --sources on the CLI to choose at run time; SOURCES here is the default when no flag is passed.
"""

# Default sources when running without --sources
SOURCES = ["github"]

# --- GitHub ---
GITHUB_REPO = "meilisearch/meilisearch"

GITHUB_KEYWORDS = {
    "stabilite": [
        "panic", "unwrap()", "index corruption", "crash",
        "out of memory", "OOM",
    ],
    "souverainete": [
        "OpenAI", "privacy", "telemetry", "data leak", "sovereignty",
    ],
    "performance": [
        "p95", "slow indexing", "HNSW latency", "mmap limit",
    ],
}

# --- Tavily (multi-source: Reddit, HN, Stack Overflow, tech blogs) ---
TAVILY_QUERIES = [
    "Meilisearch vs Typesense",
    "Meilisearch vs Algolia",
    "Meilisearch vs Elasticsearch",
    "Meilisearch in production",
    "Meilisearch scaling issues",
    "Meilisearch re-indexing",
    "Meilisearch crash panic",
    "Meilisearch switch migrate away",
]

# --- Reddit (optional; stub if no PRAW credentials) ---
REDDIT_SUBREDDITS = ["selfhosted", "rust", "Search", "LanguageTechnology"]
REDDIT_KEYWORDS = {
    "comparaisons": ["Meilisearch vs Typesense", "Meilisearch vs Algolia", "Meilisearch vs Elasticsearch"],
    "feedback_production": ["Meilisearch in production", "scaling issues", "re-indexing pain"],
    "pain_points": ["switch from Meilisearch", "migrate away", "leave Meilisearch"],
}

# Export for the orchestrator
TARGET = {
    "sources": SOURCES,
    "github": {
        "repo": GITHUB_REPO,
        "keywords": GITHUB_KEYWORDS,
    },
    "tavily": {
        "queries": TAVILY_QUERIES,
    },
    "reddit": {
        "subreddits": REDDIT_SUBREDDITS,
        "keywords": REDDIT_KEYWORDS,
    },
}
