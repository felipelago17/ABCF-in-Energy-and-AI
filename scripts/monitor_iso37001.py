#!/usr/bin/env python3
"""Track ISO 37001 (anti-bribery management systems) news and certifications.

ISO does not publish a single machine-readable feed of new certifications, so
this monitor is intentionally conservative: if an ISO37001_FEEDS env var lists
feeds, it pulls recent items from them; otherwise it emits an empty result with
a note prompting a manual check. It never fabricates certification claims.
"""

import os

from common import fetch_feed_entries, log, now_iso, save_json, set_output


def main() -> None:
    feeds = [u.strip() for u in os.environ.get("ISO37001_FEEDS", "").split(",") if u.strip()]
    items = []
    for url in feeds:
        got = fetch_feed_entries(url, days_back=30)
        log(f"  {len(got)} recent item(s) from {url}")
        for e in got:
            items.append(
                {
                    "title": e["title"],
                    "source_url": e["link"],
                    "source_date": e["published"],
                    "needs_review": True,
                }
            )

    note = (
        "No ISO37001_FEEDS configured — manual check of ISO 37001 news and "
        "certification registers recommended." if not feeds else ""
    )
    save_json(
        "iso37001_updates.json",
        {"timestamp": now_iso(), "total": len(items), "items": items, "note": note},
    )
    log(f"  saved {len(items)} ISO 37001 item(s) -> iso37001_updates.json")
    set_output("has_updates", len(items) > 0)


if __name__ == "__main__":
    main()
