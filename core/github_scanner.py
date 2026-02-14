"""
GitHub scanner: fetches and filters issues from the target repo.
Only invoked when "github" is in config TARGET["sources"].
"""

import logging
import os

from github import Github

log = logging.getLogger(__name__)


def run(repo: str, keywords: dict, max_issues: int = 300) -> dict:
    """
    Fetches issues from the repo, filters by keywords, computes velocity metrics.
    Returns a dict with raw issues (title, body, labels, dates) and velocity stats.
    """
    log.info("Connecting to GitHub (token=%s)", "set" if os.getenv("GITHUB_TOKEN") else "not set")
    token = os.getenv("GITHUB_TOKEN") or None
    gh = Github(token)
    repo_obj = gh.get_repo(repo)
    log.info("Repo: %s. Fetching up to %d issues (open+closed), sorted by updated.", repo, max_issues)

    # Flatten all keywords for matching
    all_keywords = []
    for kws in keywords.values():
        all_keywords.extend(kws)

    issues_by_category: dict[str, list] = {k: [] for k in keywords}
    velocity_bug_hours: list[float] = []
    velocity_other_hours: list[float] = []
    velocity_sample_details: list[dict] = []  # List of issues used for the average

    # Cap velocity sampling: avoid 1 API call per issue (get_comments)
    max_velocity_samples = 25
    velocity_samples_done = 0

    count = 0
    for issue in repo_obj.get_issues(state="all", sort="updated"):
        if count >= max_issues:
            break
        if issue.pull_request:
            continue
        count += 1
        if count % 50 == 0:
            matched = sum(len(v) for v in issues_by_category.values())
            log.info("  Scanned %d issues so far, %d matched by keywords.", count, matched)
        text = f"{issue.title or ''} {issue.body or ''}".lower()
        for category, kws in keywords.items():
            if any(kw.lower() in text for kw in kws):
                issues_by_category[category].append({
                    "number": issue.number,
                    "title": issue.title,
                    "body": (issue.body or "")[:2000],
                    "state": issue.state,
                    "created_at": issue.created_at.isoformat() if issue.created_at else None,
                    "updated_at": issue.updated_at.isoformat() if issue.updated_at else None,
                    "labels": [l.name for l in (issue.labels or [])],
                    "url": issue.html_url,
                })
                break

        # Velocity: only on a small sample to avoid hundreds of get_comments() calls
        if velocity_samples_done < max_velocity_samples:
            try:
                comments = list(issue.get_comments())
                if comments and issue.created_at:
                    first = min(comments, key=lambda c: c.created_at)
                    delta = (first.created_at - issue.created_at).total_seconds() / 3600.0
                    delta_hours = round(delta, 1)
                    is_bug = any("bug" in (l.name or "").lower() for l in (issue.labels or []))
                    if is_bug:
                        velocity_bug_hours.append(delta)
                    else:
                        velocity_other_hours.append(delta)
                    velocity_sample_details.append({
                        "number": issue.number,
                        "title": issue.title or "(no title)",
                        "url": issue.html_url,
                        "hours_to_first_response": delta_hours,
                        "type": "bug" if is_bug else "other",
                    })
                    velocity_samples_done += 1
            except Exception:
                pass

    # Build flat list for analyzer (dedupe by issue number)
    seen = set()
    issues_flat = []
    for items in issues_by_category.values():
        for i in items:
            if i["number"] not in seen:
                seen.add(i["number"])
                issues_flat.append(i)

    def avg(hours: list[float]) -> float | None:
        return sum(hours) / len(hours) if hours else None

    velocity_metrics = {
        "avg_first_response_hours_bugs": avg(velocity_bug_hours),
        "avg_first_response_hours_other": avg(velocity_other_hours),
        "sample_bugs": len(velocity_bug_hours),
        "sample_other": len(velocity_other_hours),
    }

    by_cat = {k: len(v) for k, v in issues_by_category.items()}
    log.info("GitHub scan finished: %d issues fetched, %d matched. By category: %s. Velocity sample: %d (bugs) + %d (other).", count, len(issues_flat), by_cat, len(velocity_bug_hours), len(velocity_other_hours))
    return {
        "repo": repo,
        "issues": issues_flat,
        "issues_by_category": by_cat,
        "velocity_metrics": velocity_metrics,
        "velocity_sample_details": velocity_sample_details,
    }
