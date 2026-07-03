#!/usr/bin/env python3
"""Aggregate per-source enforcement candidates into a summary + markdown report.

Corrected version of the original draft: valid model ID, $GITHUB_OUTPUT,
graceful degradation (no API key -> a mechanical summary rather than a crash),
and every case still flagged for human verification.
"""

from common import (
    ask_json,
    get_client,
    load_json,
    log,
    now_iso,
    save_json,
    set_output,
)

SOURCES = {
    "doj": "doj_fcpa_enforcement.json",
    "sec": "sec_fcpa_enforcement.json",
    "sfo": "uk_bribery_enforcement.json",
    "iso37001": "iso37001_updates.json",
}


def load_all():
    data = {}
    for key, path in SOURCES.items():
        blob = load_json(path, {})
        data[key] = blob.get("cases", blob.get("items", []))
    return data


def analyse(enforcement_data, client):
    """Ask the model for pattern/governance analysis; None if unavailable."""
    if client is None:
        return None
    import json

    prompt = (
        "You are analysing candidate ABCF enforcement items (unverified, "
        "AI-extracted). Identify only patterns supported by the data; do not "
        "invent specifics.\n\n"
        f"{json.dumps(enforcement_data, indent=2)[:8000]}\n\n"
        "Return ONLY valid JSON with this shape:\n"
        "{\n"
        '  "enforcement_summary": "2-3 sentence overview",\n'
        '  "key_patterns": ["..."],\n'
        '  "governance_insights": ["..."],\n'
        '  "high_risk_indicators": ["..."],\n'
        '  "recommended_focus_areas": ["..."]\n'
        "}"
    )
    return ask_json(client, prompt, max_tokens=1500)


def markdown_report(summary) -> str:
    a = summary.get("analysis") or {}
    counts = summary["cases_by_agency"]
    lines = [
        "# ABCF Enforcement Summary",
        "",
        f"**Generated:** {summary['generated']}",
        "",
        "> ⚠️ Auto-generated from AI-extracted candidates. **Every item must be "
        "verified against its primary source before it is treated as fact** "
        "(see CONTRIBUTING.md).",
        "",
        "## Overview",
        a.get("enforcement_summary", "_No AI analysis available (no API key); "
        "counts only._"),
        "",
        f"**Total candidate items:** {summary['total_cases_tracked']}",
        f"- DOJ: {counts['doj']}",
        f"- SEC: {counts['sec']}",
        f"- SFO/FCA (UK): {counts['sfo']}",
        f"- ISO 37001: {counts['iso37001']}",
        "",
    ]
    if a.get("key_patterns"):
        lines += ["## Patterns", ""]
        lines += [f"{i}. {p}" for i, p in enumerate(a["key_patterns"], 1)] + [""]
    if a.get("governance_insights"):
        lines += ["## Governance implications", ""]
        lines += [f"- {x}" for x in a["governance_insights"]] + [""]
    if a.get("high_risk_indicators"):
        lines += ["## High-risk indicators", ""]
        lines += [f"- {x}" for x in a["high_risk_indicators"]] + [""]
    if a.get("recommended_focus_areas"):
        lines += ["## Recommended focus areas", ""]
        lines += [f"{i}. {x}" for i, x in enumerate(a["recommended_focus_areas"], 1)] + [""]
    return "\n".join(lines)


def main() -> None:
    data = load_all()
    total = sum(len(v) for v in data.values())
    log(f"Loaded {total} candidate item(s) across sources.")

    # New (verification-pending) enforcement cases for issue creation:
    new_cases = []
    for key in ("doj", "sec", "sfo"):
        for c in data[key]:
            if c.get("is_enforcement") or c.get("needs_review"):
                new_cases.append(c)

    summary = {
        "generated": now_iso(),
        "total_cases_tracked": total,
        "cases_by_agency": {k: len(v) for k, v in data.items()},
        "analysis": analyse(data, get_client()),
        "new_cases": new_cases,
        "enforcement_data": data,
    }

    save_json("enforcement_summary.json", summary)
    with open("ENFORCEMENT_SUMMARY.md", "w", encoding="utf-8") as fh:
        fh.write(markdown_report(summary))

    set_output("has_updates", total > 0)
    set_output("has_new_cases", len(new_cases) > 0)
    set_output("total_cases_analyzed", total)
    log(f"Aggregated: {total} item(s), {len(new_cases)} pending verification.")


if __name__ == "__main__":
    main()
