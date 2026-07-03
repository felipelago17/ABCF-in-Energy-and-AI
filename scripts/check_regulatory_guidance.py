#!/usr/bin/env python3
"""Check configured guidance sources for new ABCF regulatory guidance.

Reads feeds from GUIDANCE_FEEDS (comma-separated). Without feeds it writes an
empty result and prompts a manual sweep — it does not fabricate guidance. When
a model is available it drafts a short (verification-pending) summary.
"""

import os

from common import (
    ask_json,
    fetch_feed_entries,
    get_client,
    log,
    looks_like_fcpa,
    now_iso,
    save_json,
    set_output,
)

GUIDANCE_KEYWORDS = (
    "guidance",
    "iso 37001",
    "iso37001",
    "compliance program",
    "fcpa",
    "bribery",
    "anti-corruption",
    "anti-bribery",
    "eiti",
    "uncac",
    "oecd",
)


def relevant(entry) -> bool:
    text = (entry["title"] + " " + entry["summary"]).lower()
    return looks_like_fcpa(text) or any(k in text for k in GUIDANCE_KEYWORDS)


def main() -> None:
    feeds = [u.strip() for u in os.environ.get("GUIDANCE_FEEDS", "").split(",") if u.strip()]
    items = []
    for url in feeds:
        for e in fetch_feed_entries(url, days_back=30):
            if relevant(e):
                items.append(
                    {
                        "title": e["title"],
                        "source_url": e["link"],
                        "source_date": e["published"],
                        "needs_review": True,
                    }
                )

    summary_md = ""
    client = get_client()
    if items and client is not None:
        import json

        data = ask_json(
            client,
            "Summarise these ABCF regulatory-guidance items in 3-5 bullet points. "
            "State only what the titles support; flag uncertainty.\n\n"
            + json.dumps(items, indent=2)[:6000],
            max_tokens=600,
        )
        if isinstance(data, dict):
            summary_md = data.get("summary", "")

    body = summary_md or (
        "New guidance candidates detected — verify each against its issuing "
        "authority before treating as fact." if items else
        "No GUIDANCE_FEEDS configured — manual sweep of DOJ/SEC, FCA/SFO, ISO, "
        "EITI, UNCAC, and OECD guidance recommended."
    )

    save_json(
        "guidance_updates.json",
        {
            "timestamp": now_iso(),
            "total": len(items),
            "items": items,
            "summary": "### Regulatory guidance sweep\n\n"
            + body
            + "\n\n> ⚠️ Auto-generated; verify against primary sources.",
        },
    )
    log(f"  saved {len(items)} guidance candidate(s) -> guidance_updates.json")
    set_output("has_updates", len(items) > 0)


if __name__ == "__main__":
    main()
