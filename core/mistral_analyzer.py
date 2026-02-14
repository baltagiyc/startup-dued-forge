"""
Mistral-based analysis: red flags, community score, market positioning, lab vs social correlation.
Single LLM call with all scanner data. Uses only Mistral API (via LangChain).
"""

import logging
import os
import re

from langchain_mistralai import ChatMistralAI

log = logging.getLogger(__name__)

# Lab findings from technical due diligence (for correlation)
LAB_FINDINGS = """
- Stability: Server crash (Rust panic) observed in lab.
- Sovereignty: Default routing to OpenAI; privacy/sovereignty concern.
- Performance: Strong p50 (~200ms on 10k docs) but p95 degrades at scale.
"""


def run(results: dict) -> dict:
    """
    Analyzes scanner results with Mistral. Returns structured analysis for the report.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        log.warning("MISTRAL_API_KEY not set.")
        return {
            "error": "MISTRAL_API_KEY not set",
            "summary_score": None,
            "red_flags": [],
            "market_positioning": "",
            "correlation_lab_social": "",
            "raw": "",
        }

    # Build context from GitHub and/or Tavily (multi-source: Reddit, HN, blogs)
    context_parts = []
    if "github" in results and results["github"].get("issues"):
        g = results["github"]
        context_parts.append(f"## GitHub ({g['repo']})\nIssues by category: {g.get('issues_by_category', {})}\nVelocity: avg first response (bugs) {g.get('velocity_metrics', {}).get('avg_first_response_hours_bugs')}h, (other) {g.get('velocity_metrics', {}).get('avg_first_response_hours_other')}h.\n\n### Sample issues (title + excerpt)\n")
        for i in g["issues"][:50]:
            context_parts.append(f"- #{i['number']} [{i['state']}] {i['title']}\n  {i['body'][:400]}...\n")
    if "tavily" in results and results["tavily"].get("results"):
        t = results["tavily"]
        context_parts.append("## Web / Social (Tavily: Reddit, HN, Stack Overflow, blogs)\n")
        for r in t.get("results", [])[:40]:
            context_parts.append(f"- {r.get('title', '')} | {r.get('content', '')[:400]}...\n")
    if "reddit" in results and results["reddit"].get("posts"):
        r = results["reddit"]
        context_parts.append("## Reddit (PRAW)\n")
        for p in r.get("posts", [])[:30]:
            context_parts.append(f"- {p.get('title', '')} | {p.get('body', '')[:300]}...\n")
    context = "\n".join(context_parts) or "No issue or post data available."
    log.info("Context size: %d chars (GitHub + Tavily/Reddit). Calling Mistral (mistral-large-latest)...", len(context))

    llm = ChatMistralAI(api_key=api_key, model="mistral-large-latest")
    prompt = f"""You are an analyst producing a due diligence audit report for a potential acquisition (Mistral AI / Meilisearch).

Below is community data from GitHub and/or Tavily (Reddit, HN, blogs) about Meilisearch.

Lab / technical findings from our side:
{LAB_FINDINGS}

Community data:
{context[:12000]}

Respond in the following exact format (use the section headers as given).

## Summary
- Community confidence score: X/10 (one number, 0-10)
- One short paragraph (2-3 sentences) on overall community health.

## Red Flags (Social)
List the top 5 recurring problems or concerns mentioned by developers. One line each, numbered 1. to 5.

## Market Positioning
- Strengths perceived vs Typesense and Algolia (bullet points).
- Weaknesses perceived vs Typesense and Algolia (bullet points).

## Correlation Lab vs Social
- Do the lab findings (Rust panic/crash, OpenAI/default routing, p95 degradation) appear in community reports? Yes/No or Partially for each, with one sentence evidence when possible.
"""

    try:
        msg = llm.invoke(prompt)
        raw = msg.content if hasattr(msg, "content") else str(msg)
        log.info("Mistral response received (%d chars). Parsing score and sections...", len(raw))
    except Exception as e:
        log.exception("Mistral API call failed.")
        return {
            "error": str(e),
            "summary_score": None,
            "red_flags": [],
            "market_positioning": "",
            "correlation_lab_social": "",
            "raw": "",
        }

    # Parse into structured fields for report
    summary_score = None
    m = re.search(r"confidence score:\s*(\d+(?:\.\d+)?)\s*/?\s*10", raw, re.I)
    if m:
        summary_score = float(m.group(1))

    red_flags = []
    for m in re.finditer(r"^\s*\d+\.\s*(.+?)(?=\n\s*\d+\.|\n##|\Z)", raw, re.M | re.S):
        red_flags.append(m.group(1).strip()[:500])

    return {
        "error": None,
        "summary_score": summary_score,
        "red_flags": red_flags[:5],
        "market_positioning": _extract_section(raw, "Market Positioning"),
        "correlation_lab_social": _extract_section(raw, "Correlation Lab vs Social"),
        "raw": raw,
    }


def _extract_section(text: str, title: str) -> str:
    pattern = rf"##\s+{re.escape(title)}\s*\n(.*?)(?=\n##\s+|\Z)"
    m = re.search(pattern, text, re.S | re.I)
    return m.group(1).strip()[:2000] if m else ""
