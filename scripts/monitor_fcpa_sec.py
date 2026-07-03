#!/usr/bin/env python3
"""Monitor SEC releases for FCPA enforcement actions.

See monitor_fcpa_doj.py for the shared design. Feed URLs overridable via
SEC_FEEDS (comma-separated). Verify against sec.gov.
"""

import os

from common import run_source_monitor, set_output

# SEC press releases + litigation releases (override via SEC_FEEDS if they move).
DEFAULT_FEEDS = [
    "https://www.sec.gov/news/pressreleases.rss",
    "https://www.sec.gov/rss/litigation/litreleases.xml",
]


def main() -> None:
    feeds = [u.strip() for u in os.environ.get("SEC_FEEDS", "").split(",") if u.strip()]
    cases = run_source_monitor(
        "SEC", feeds or DEFAULT_FEEDS, "sec_fcpa_enforcement.json", days_back=14
    )
    set_output("has_new_cases", len(cases) > 0)
    set_output("case_count", len(cases))


if __name__ == "__main__":
    main()
