#!/usr/bin/env python3
"""Monitor DOJ press releases for FCPA / bribery enforcement actions.

Corrected version of the original draft:
  * uses $GITHUB_OUTPUT (not the removed ``::set-output``);
  * uses a valid, configurable model ID;
  * degrades gracefully with no API key or an unreachable feed;
  * flags every extracted item ``needs_review`` — nothing is asserted as fact.

Feed URLs are overridable via the DOJ_FEEDS env var (comma-separated) so they
can be corrected without editing code. Verify feeds against justice.gov.
"""

import os

from common import run_source_monitor, set_output

# DOJ press-release feeds. The historic /feeds/opa/justice-news.xml now 404s
# (DOJ site restructure), so several candidates are tried; the monitor uses
# whichever returns content and logs the rest. Override via DOJ_FEEDS.
DEFAULT_FEEDS = [
    "https://www.justice.gov/news/rss?type=press_release",
    "https://www.justice.gov/feeds/justice-news.xml",
    "https://www.justice.gov/opa/rss.xml",
    "https://www.justice.gov/rss.xml",
]


def main() -> None:
    feeds = [u.strip() for u in os.environ.get("DOJ_FEEDS", "").split(",") if u.strip()]
    cases = run_source_monitor(
        "DOJ", feeds or DEFAULT_FEEDS, "doj_fcpa_enforcement.json", days_back=14
    )
    set_output("has_new_cases", len(cases) > 0)
    set_output("case_count", len(cases))


if __name__ == "__main__":
    main()
