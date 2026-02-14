"""
Builds the final audit report in Markdown from scanner results + Mistral analysis.
"""

import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)


def build(results: dict, analysis: dict, output_path: str | Path = "AUDIT_SOCIAL_REPORT.md") -> Path:
    """
    Writes AUDIT_SOCIAL_REPORT.md: Summary, Red Flags, Market Positioning, Correlation, Data Summary.
    """
    out = Path(output_path)
    log.info("Writing report to %s (sources: %s).", out, list(results.keys()))
    sections = []

    # Title and sources
    sources = list(results.keys())
    sections.append("# Social Audit Report – Meilisearch")
    sections.append("")
    sections.append(f"**Sources used:** {', '.join(sources) or 'None'}")
    sections.append("")

    if analysis.get("error"):
        sections.append("## Analysis Error")
        sections.append("")
        sections.append(f"Mistral analysis could not be run: `{analysis['error']}`")
        sections.append("")
        sections.append("Ensure `MISTRAL_API_KEY` is set in `.env` and the API is reachable.")
        out.write_text("\n".join(sections), encoding="utf-8")
        log.warning("Report written with analysis error only: %s", out)
        return out

    # Summary
    score = analysis.get("summary_score")
    score_line = f"**Community confidence score: {score}/10**" if score is not None else "**Community confidence score:** N/A"
    sections.append("## Summary")
    sections.append("")
    sections.append(score_line)
    sections.append("")
    if analysis.get("raw"):
        summary_block = _take_until_next_section(analysis["raw"], "Summary")
        if summary_block:
            sections.append(summary_block.strip())
    sections.append("")

    # Red Flags
    sections.append("## Red Flags (Social)")
    sections.append("")
    for i, flag in enumerate(analysis.get("red_flags") or [], 1):
        sections.append(f"{i}. {flag}")
    if not analysis.get("red_flags"):
        sections.append("*None extracted.*")
    sections.append("")

    # Market positioning
    sections.append("## Market Positioning")
    sections.append("")
    mp = analysis.get("market_positioning") or ""
    sections.append(mp if mp else "*No content.*")
    sections.append("")

    # Correlation Lab vs Social
    sections.append("## Correlation Lab vs Social")
    sections.append("")
    corr = analysis.get("correlation_lab_social") or ""
    sections.append(corr if corr else "*No content.*")
    sections.append("")

    # Data summary
    sections.append("---")
    sections.append("## Data Summary")
    sections.append("")
    if "github" in results:
        g = results["github"]
        sections.append(f"- **GitHub repo:** {g.get('repo', '')}")
        sections.append(f"- **Issues matched:** {len(g.get('issues', []))}")
        sections.append(f"- **By category:** {g.get('issues_by_category', {})}")
        vm = g.get("velocity_metrics", {})
        sections.append(f"- **Velocity (avg first response):** bugs {vm.get('avg_first_response_hours_bugs')}h (n={vm.get('sample_bugs')}), other {vm.get('avg_first_response_hours_other')}h (n={vm.get('sample_other')})")
        details = g.get("velocity_sample_details") or []
        if details:
            sections.append("")
            sections.append("#### Issues used for velocity average (time to first comment)")
            sections.append("")
            for d in details:
                sections.append(f"- [#{d.get('number')}]({d.get('url', '')}) — {d.get('hours_to_first_response')}h — *{d.get('type')}* — {d.get('title', '')[:80]}")
            sections.append("")
    if "tavily" in results and results["tavily"].get("results"):
        sections.append(f"- **Tavily (web/social) results:** {len(results['tavily']['results'])}")
    if "reddit" in results and results["reddit"].get("posts"):
        sections.append(f"- **Reddit posts:** {len(results['reddit']['posts'])}")
    sections.append("")

    out.write_text("\n".join(sections), encoding="utf-8")
    log.info("Report written (%d bytes).", out.stat().st_size)
    return out


def _take_until_next_section(text: str, after: str) -> str:
    """Extract content after '## <after>' until next '##'."""
    pattern = rf"(?m)^##\s+{after}\s*\n(.*?)(?=^##\s+|\Z)"
    m = re.search(pattern, text, re.S | re.I)
    if not m:
        return ""
    block = m.group(1).strip()
    # Stop at next ##
    if "##" in block:
        block = block.split("##")[0].strip()
    return block
