"""
Orchestrator for the audit pipeline.

What this script does (in order):
  1. Loads .env and reads config (which sources: github, tavily, reddit).
  2. For each enabled source: runs the corresponding scanner (GitHub issues, Tavily search, or Reddit).
  3. Sends all collected data to Mistral to get: community score, red flags, market positioning, lab vs social correlation.
  4. Writes AUDIT_SOCIAL_REPORT.md from the analysis and data summary.
"""

import logging

from dotenv import load_dotenv

load_dotenv()

# Logs: level + time so we can follow progress
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def main() -> None:
    from config.target_meilisearch import TARGET

    sources = TARGET.get("sources", [])
    results = {}
    log.info("Sources to run: %s", sources)

    if "github" in sources:
        log.info("Starting GitHub scanner (repo + keywords from config)...")
        from core import github_scanner
        results["github"] = github_scanner.run(
            repo=TARGET["github"]["repo"],
            keywords=TARGET["github"]["keywords"],
        )
        n = len(results["github"].get("issues", []))
        log.info("GitHub done: %d issues matched (by keyword). Categories: %s", n, results["github"].get("issues_by_category"))

    if "tavily" in sources:
        log.info("Starting Tavily scanner (one search per query from config)...")
        from core import tavily_scanner
        results["tavily"] = tavily_scanner.run(queries=TARGET["tavily"]["queries"])
        n = len(results["tavily"].get("results", []))
        err = results["tavily"].get("error")
        if err:
            log.warning("Tavily finished with error: %s. Results count: %d", err, n)
        else:
            log.info("Tavily done: %d results (deduplicated by URL).", n)

    if "reddit" in sources:
        log.info("Starting Reddit scanner (PRAW)...")
        from core import reddit_scanner
        results["reddit"] = reddit_scanner.run(
            subreddits=TARGET["reddit"]["subreddits"],
            keywords=TARGET["reddit"]["keywords"],
        )
        log.info("Reddit done (stub: no PRAW data yet).")

    log.info("Running Mistral analysis (one LLM call with all data)...")
    from core import mistral_analyzer
    analysis = mistral_analyzer.run(results)
    if analysis.get("error"):
        log.error("Mistral analysis failed: %s", analysis["error"])
    else:
        log.info("Mistral done. Community score: %s/10. Red flags extracted: %d", analysis.get("summary_score"), len(analysis.get("red_flags") or []))

    log.info("Building report (Markdown)...")
    from core import report_builder
    path = report_builder.build(results, analysis)
    log.info("Report written to: %s", path.resolve())
    log.info("Pipeline finished.")


if __name__ == "__main__":
    main()
