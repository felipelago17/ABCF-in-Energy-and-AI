#!/usr/bin/env python3
"""
Daily ABCF regulatory monitor.

Pulls the last 24h from primary and commentary sources, triages each item with
the Anthropic API, writes a dated digest to insider-trading/digests/, and emits
a list of high-relevance alerts for the workflow to open GitHub issues.

Sources
-------
  * Federal Register API   — SEC / DOJ / FinCEN / OFAC documents matching a set
                             of ABCF terms.
  * SEC RSS                — press releases + litigation releases.
  * DOJ                    — Fraud Section / FCPA press releases (best-effort
                             feed candidates; the FCPA page has no stable RSS).
  * UK SFO                 — news feed.
  * Law-firm feeds         — insider-trading/sources/feeds.yml.

Triage (per item, when ANTHROPIC_API_KEY is set)
------------------------------------------------
  * classify: anti-bribery/corruption | insider-trading | fraud/other
  * score energy-sector and AI-sector relevance (0-5 each)
  * 3-bullet summary with a citation link
  * flag extraterritorial reach and any UAE/GCC nexus
  * tag insider-trading items: gain-seeking vs loss-avoidance
  * note any Securities Act 17(a) theory pleaded in an SEC complaint

Ethos
-----
AI output is NEVER treated as fact. Every triaged item is a research lead and is
flagged needs_review; without an API key the monitor still runs and lists raw
items for manual review. It degrades gracefully — a single unreachable source
never breaks the run.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone

# scripts/ is on sys.path[0] when run as ``python scripts/abcf_monitor.py``.
from common import (  # noqa: E402
    DEFAULT_MODEL,
    DEFAULT_UA,
    ask_json,
    fetch_feed_entries,
    get_client,
    log,
    now_iso,
    save_json,
    set_output,
)

# --------------------------------------------------------------------------- #
# Configuration (overridable via environment / Actions variables)
# --------------------------------------------------------------------------- #

# Federal Register agency slugs.
FR_AGENCIES = [
    "securities-and-exchange-commission",
    "justice-department",
    "financial-crimes-enforcement-network",  # FinCEN
    "foreign-assets-control-office",          # OFAC
]

# ABCF search terms for the Federal Register.
FR_TERMS = [
    "insider trading",
    "10b5-1",
    "Section 16",
    "FCPA",
    "anti-bribery",
    "corruption",
    "loss avoidance",
    "disgorgement",
    "Section 17(a)",
]

SEC_FEEDS = [
    "https://www.sec.gov/news/pressreleases.rss",
    "https://www.sec.gov/rss/litigation/litreleases.xml",
]

# DOJ has no stable Fraud Section / FCPA RSS; probe press-release candidates.
DOJ_FEEDS = [
    "https://www.justice.gov/news/rss?type=press_release",
    "https://www.justice.gov/feeds/justice-news.xml",
]

SFO_FEEDS = [
    "https://www.sfo.gov.uk/feed/",
]

FEEDS_YML = "insider-trading/sources/feeds.yml"
DIGEST_DIR = "insider-trading/digests"
ALERTS_PATH = "abcf_daily_alerts.json"  # transient; see .gitignore

# How many items to send through the model per run (bounds cost/latency).
MAX_TRIAGE = int(os.environ.get("ABCF_MAX_TRIAGE", "40"))
# Lookback window; the cron is daily so 1 day + buffer inside the feed parser.
LOOKBACK_DAYS = int(os.environ.get("ABCF_LOOKBACK_DAYS", "1"))


def _env_list(name):
    raw = os.environ.get(name, "").strip()
    return [u.strip() for u in raw.split(",") if u.strip()]


# --------------------------------------------------------------------------- #
# Fetchers
# --------------------------------------------------------------------------- #

def _requests():
    try:
        import requests

        return requests
    except Exception:
        return None


def fetch_federal_register(days_back):
    """Return normalized Federal Register documents matching ABCF terms."""
    requests = _requests()
    if requests is None:
        log("requests unavailable — skipping Federal Register.")
        return []

    gte = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")
    seen = set()
    items = []
    for term in FR_TERMS:
        params = [
            ("per_page", "50"),
            ("order", "newest"),
            ("conditions[term]", term),
            ("conditions[publication_date][gte]", gte),
            ("fields[]", "title"),
            ("fields[]", "html_url"),
            ("fields[]", "publication_date"),
            ("fields[]", "abstract"),
            ("fields[]", "agencies"),
            ("fields[]", "document_number"),
            ("fields[]", "type"),
        ]
        for slug in FR_AGENCIES:
            params.append(("conditions[agencies][]", slug))
        try:
            resp = requests.get(
                "https://www.federalregister.gov/api/v1/documents.json",
                params=params,
                headers={"User-Agent": DEFAULT_UA, "Accept": "application/json"},
                timeout=30,
            )
            if resp.status_code != 200:
                log(f"  FR term '{term}' -> HTTP {resp.status_code}")
                continue
            data = resp.json()
        except Exception as exc:
            log(f"  FR term '{term}' error: {exc}")
            continue

        for doc in data.get("results", []) or []:
            num = doc.get("document_number") or doc.get("html_url")
            if not num or num in seen:
                continue
            seen.add(num)
            agencies = ", ".join(
                a.get("raw_name") or a.get("name") or "" for a in (doc.get("agencies") or [])
            ).strip(", ")
            items.append(
                {
                    "source": "Federal Register",
                    "source_type": "federal_register",
                    "agency": agencies or "Federal Register",
                    "title": doc.get("title", ""),
                    "link": doc.get("html_url", ""),
                    "published": doc.get("publication_date", ""),
                    "summary": (doc.get("abstract") or "")[:1200],
                    "matched_term": term,
                }
            )
    log(f"  Federal Register: {len(items)} document(s)")
    return items


def fetch_rss_source(name, agency, urls, days_back):
    items = []
    for url in urls:
        got = fetch_feed_entries(url, days_back=days_back)
        log(f"  {name}: {len(got)} recent entrie(s) from {url}")
        for e in got:
            items.append(
                {
                    "source": name,
                    "source_type": "rss",
                    "agency": agency,
                    "title": e["title"],
                    "link": e["link"],
                    "published": e["published"],
                    "summary": (e.get("summary") or "")[:1200],
                }
            )
    return items


def load_firm_feeds():
    try:
        import yaml
    except Exception as exc:
        log(f"PyYAML unavailable ({exc}) — skipping law-firm feeds.")
        return []
    try:
        with open(FEEDS_YML, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except FileNotFoundError:
        log(f"{FEEDS_YML} not found — skipping law-firm feeds.")
        return []
    return data.get("feeds", []) or []


def fetch_firm_feeds(days_back):
    items = []
    for feed in load_firm_feeds():
        url = feed.get("url")
        name = feed.get("name", url)
        if not url:
            continue
        got = fetch_feed_entries(url, days_back=days_back)
        log(f"  firm feed {name}: {len(got)} entrie(s)")
        for e in got:
            items.append(
                {
                    "source": name,
                    "source_type": "law_firm",
                    "agency": feed.get("publisher", "law firm"),
                    "title": e["title"],
                    "link": e["link"],
                    "published": e["published"],
                    "summary": (e.get("summary") or "")[:1200],
                }
            )
    return items


def gather(days_back):
    items = []
    items += fetch_federal_register(days_back)
    items += fetch_rss_source("SEC", "SEC", _env_list("SEC_FEEDS") or SEC_FEEDS, days_back)
    items += fetch_rss_source(
        "DOJ Fraud/FCPA", "DOJ", _env_list("DOJ_FEEDS") or DOJ_FEEDS, days_back
    )
    items += fetch_rss_source("UK SFO", "SFO", _env_list("SFO_FEEDS") or SFO_FEEDS, days_back)
    items += fetch_firm_feeds(days_back)

    # De-duplicate by link (falling back to title).
    seen = set()
    deduped = []
    for it in items:
        key = (it.get("link") or it.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    log(f"Collected {len(deduped)} unique item(s) from all sources.")
    return deduped


# --------------------------------------------------------------------------- #
# Triage
# --------------------------------------------------------------------------- #

TRIAGE_SCHEMA = """You are triaging a regulatory/enforcement news item for an
anti-bribery, corruption & fraud (ABCF) research project focused on the ENERGY
and AI/compute sectors.

Return ONLY valid JSON (no markdown, no prose) with exactly this shape:
{
  "category": "anti-bribery-corruption" | "insider-trading" | "fraud-other",
  "energy_relevance": 0-5 integer (relevance to energy-sector issuers),
  "ai_relevance": 0-5 integer (relevance to AI/compute-sector issuers),
  "bullets": ["3 short factual bullets summarizing the item"],
  "extraterritorial": boolean (does it assert reach over conduct/parties abroad?),
  "uae_gcc_nexus": boolean (any UAE or GCC connection?),
  "insider_fact_pattern": "gain-seeking" | "loss-avoidance" | null
      (only for insider-trading items; loss-avoidance = pre-announcement sales,
       hedges, gifts, or pledges made AHEAD OF bad news to avoid a loss),
  "section_17a": boolean (does an SEC complaint plead Securities Act Section 17(a)?),
  "relevance": "high" | "medium" | "low" (overall relevance to the project),
  "rationale": "one short sentence"
}
Base every field ONLY on the provided title/summary; if unknown, use a
conservative default (false / null / "low"). Do not invent facts."""


def triage_item(client, item):
    prompt = (
        f"{TRIAGE_SCHEMA}\n\n"
        f"SOURCE: {item['source']} ({item.get('agency','')})\n"
        f"TITLE: {item['title']}\n"
        f"SUMMARY: {item['summary'][:900]}\n"
        f"LINK: {item['link']}\n"
    )
    data = ask_json(client, prompt, max_tokens=600)
    if not data:
        return None
    data["needs_review"] = True  # AI output is never authoritative
    return data


def is_high_relevance(triage):
    if not triage:
        return False
    if str(triage.get("relevance", "")).lower() == "high":
        return True
    try:
        return max(int(triage.get("energy_relevance", 0)), int(triage.get("ai_relevance", 0))) >= 4
    except (TypeError, ValueError):
        return False


CATEGORY_LABELS = {
    "anti-bribery-corruption": "Anti-Bribery / Corruption",
    "insider-trading": "Insider Trading",
    "fraud-other": "Fraud / Other",
}


def enrich(items, client):
    triaged = []
    for i, item in enumerate(items):
        if client is not None and i < MAX_TRIAGE:
            t = triage_item(client, item)
            item["triage"] = t
            item["high_relevance"] = is_high_relevance(t)
        else:
            if client is not None:
                log(f"  (triage cap {MAX_TRIAGE} reached — {item['title'][:50]} left raw)")
            item["triage"] = None
            item["high_relevance"] = False
        triaged.append(item)
    return triaged


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def render_item(item):
    t = item.get("triage")
    lines = []
    title = item["title"] or "(untitled)"
    link = item["link"]
    lines.append(f"#### [{title}]({link})" if link else f"#### {title}")
    meta = f"_{item['source']}"
    if item.get("agency"):
        meta += f" · {item['agency']}"
    if item.get("published"):
        meta += f" · {item['published']}"
    meta += "_"
    lines.append(meta)

    if t:
        badges = []
        if t.get("relevance"):
            badges.append(f"relevance: **{t['relevance']}**")
        badges.append(f"energy {t.get('energy_relevance', 0)}/5")
        badges.append(f"AI {t.get('ai_relevance', 0)}/5")
        if t.get("extraterritorial"):
            badges.append("🌍 extraterritorial")
        if t.get("uae_gcc_nexus"):
            badges.append("🇦🇪 UAE/GCC nexus")
        if t.get("insider_fact_pattern"):
            badges.append(f"pattern: **{t['insider_fact_pattern']}**")
        if t.get("section_17a"):
            badges.append("§17(a)")
        lines.append(" · ".join(badges))
        for b in (t.get("bullets") or [])[:3]:
            lines.append(f"- {b}")
        if t.get("rationale"):
            lines.append(f"\n> {t['rationale']}")
    else:
        snippet = (item.get("summary") or "").strip().replace("\n", " ")
        if snippet:
            lines.append(f"- {snippet[:280]}")
        lines.append("- _Not triaged (no API key or triage cap) — review manually._")
    lines.append("")
    return "\n".join(lines)


def render_digest(date_str, items, triage_enabled):
    total = len(items)
    highs = [i for i in items if i.get("high_relevance")]
    buckets = {"anti-bribery-corruption": [], "insider-trading": [], "fraud-other": [], "untriaged": []}
    for it in items:
        t = it.get("triage")
        cat = (t or {}).get("category") if t else None
        target = cat if cat in buckets and cat != "untriaged" else "untriaged"
        buckets[target].append(it)

    out = []
    out.append(f"# ABCF Daily Digest — {date_str}")
    out.append("")
    out.append(
        f"_Generated {now_iso()}. {total} item(s) across all sources; "
        f"{len(highs)} high-relevance._"
    )
    if not triage_enabled:
        out.append("")
        out.append(
            "> ⚠️ **AI triage disabled** (no `ANTHROPIC_API_KEY`). Items below are "
            "raw and unclassified — for manual review only."
        )
    out.append("")
    out.append(
        "> Digest items are research leads, not findings. Confirm every "
        "classification against the linked primary source (see CONTRIBUTING.md)."
    )
    out.append("")

    if highs:
        out.append("## 🔺 High-relevance alerts")
        out.append("")
        for it in highs:
            out.append(render_item(it))

    for cat in ("anti-bribery-corruption", "insider-trading", "fraud-other"):
        group = buckets[cat]
        out.append(f"## {CATEGORY_LABELS[cat]} ({len(group)})")
        out.append("")
        if not group:
            out.append("_No items._\n")
            continue
        for it in group:
            out.append(render_item(it))

    if buckets["untriaged"]:
        out.append(f"## Untriaged ({len(buckets['untriaged'])})")
        out.append("")
        for it in buckets["untriaged"]:
            out.append(render_item(it))

    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log(f"== ABCF daily monitor {date_str} (model default: {DEFAULT_MODEL}) ==")

    items = gather(LOOKBACK_DAYS)
    client = get_client()  # None if no key / SDK — logs its own reason
    triage_enabled = client is not None
    items = enrich(items, client)

    # Digest
    os.makedirs(DIGEST_DIR, exist_ok=True)
    digest_path = os.path.join(DIGEST_DIR, f"{date_str}.md")
    with open(digest_path, "w", encoding="utf-8") as fh:
        fh.write(render_digest(date_str, items, triage_enabled))
    log(f"Wrote digest -> {digest_path}")

    # Alerts (high-relevance) for the workflow to open issues.
    alerts = []
    for it in items:
        if not it.get("high_relevance"):
            continue
        t = it.get("triage") or {}
        alerts.append(
            {
                "title": it["title"],
                "link": it["link"],
                "source": it["source"],
                "agency": it.get("agency", ""),
                "category": t.get("category", "fraud-other"),
                "relevance": t.get("relevance", ""),
                "energy_relevance": t.get("energy_relevance", 0),
                "ai_relevance": t.get("ai_relevance", 0),
                "extraterritorial": bool(t.get("extraterritorial")),
                "uae_gcc_nexus": bool(t.get("uae_gcc_nexus")),
                "insider_fact_pattern": t.get("insider_fact_pattern"),
                "section_17a": bool(t.get("section_17a")),
                "bullets": (t.get("bullets") or [])[:3],
            }
        )
    save_json(ALERTS_PATH, {"date": date_str, "count": len(alerts), "alerts": alerts})
    log(f"Wrote {len(alerts)} alert(s) -> {ALERTS_PATH}")

    set_output("digest_path", digest_path)
    set_output("digest_date", date_str)
    set_output("alert_count", len(alerts))
    set_output("has_alerts", bool(alerts))
    set_output("item_count", len(items))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never hard-fail the workflow
        log(f"FATAL (soft): {exc}")
        set_output("has_alerts", False)
        set_output("alert_count", 0)
        sys.exit(0)
