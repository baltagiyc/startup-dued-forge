"""
Audit target: Meilisearch.
Defines which sources to call (github and/or tavily) and their parameters.
Only sources listed in SOURCES are called.
"""

# Sources to use. Options: "github", "tavily", or both.
# Tavily = multi-source (Reddit, HN, Stack Overflow, blogs) with one API key — no OAuth.
# Examples:
#   SOURCES = ["github"]            → GitHub only
#   SOURCES = ["tavily"]             → Tavily only (social/web)
#   SOURCES = ["github", "tavily"]   → both
SOURCES = ["github", "tavily"]

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
}
