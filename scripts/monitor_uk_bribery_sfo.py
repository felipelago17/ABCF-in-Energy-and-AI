#!/usr/bin/env python3
"""Monitor UK SFO / FCA announcements for Bribery Act enforcement.

See monitor_fcpa_doj.py for the shared design. Feed URLs overridable via
SFO_FEEDS (comma-separated). Verify against sfo.gov.uk / fca.org.uk.
"""

import os

from common import run_source_monitor, set_output

# SFO news feed (override via SFO_FEEDS if it moves).
DEFAULT_FEEDS = [
    "https://www.sfo.gov.uk/feed/",
]


def main() -> None:
    feeds = [u.strip() for u in os.environ.get("SFO_FEEDS", "").split(",") if u.strip()]
    cases = run_source_monitor(
        "SFO", feeds or DEFAULT_FEEDS, "uk_bribery_enforcement.json", days_back=21
    )
    set_output("has_new_cases", len(cases) > 0)
    set_output("case_count", len(cases))


if __name__ == "__main__":
    main()
