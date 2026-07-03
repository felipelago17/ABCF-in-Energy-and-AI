#!/usr/bin/env python3
"""
Shared helpers for the ABCF enforcement-monitoring scripts.

Centralises the fixes over the original draft:
  * valid, current Anthropic model IDs (configurable via ANTHROPIC_MODEL);
  * GitHub Actions outputs via $GITHUB_OUTPUT (the deprecated ``::set-output``
    workflow command was removed by GitHub);
  * graceful degradation when ANTHROPIC_API_KEY is unset or a feed is
    unreachable — scripts log and continue with empty results instead of
    crashing the workflow;
  * robust JSON extraction from model responses.

Nothing here asserts enforcement facts. Any AI-derived output must be verified
against a primary source before it is treated as fact (see CONTRIBUTING.md).
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone

# A current, valid default model. Override with the ANTHROPIC_MODEL env var.
# Valid IDs at time of writing: claude-sonnet-5, claude-opus-4-8,
# claude-haiku-4-5-20251001, claude-fable-5.
DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

# FCPA / bribery keywords used for cheap pre-filtering before any API call.
FCPA_KEYWORDS = (
    "fcpa",
    "foreign corrupt practices",
    "bribery",
    "bribe",
    "corruption",
    "corrupt",
    "kickback",
)


def log(msg: str) -> None:
    print(msg, flush=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_output(name: str, value) -> None:
    """Write a GitHub Actions step output via $GITHUB_OUTPUT.

    Falls back to a plain print when run outside Actions so the scripts remain
    usable locally.
    """
    rendered = str(value).lower() if isinstance(value, bool) else str(value)
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as fh:
            fh.write(f"{name}={rendered}\n")
    else:
        log(f"[output] {name}={rendered}")


def anthropic_available() -> bool:
    """True only if the SDK is importable AND an API key is present."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log("ANTHROPIC_API_KEY not set — skipping AI analysis (graceful degrade).")
        return False
    try:
        import anthropic  # noqa: F401
    except Exception as exc:  # pragma: no cover - import guard
        log(f"anthropic SDK unavailable ({exc}) — skipping AI analysis.")
        return False
    return True


def get_client():
    """Return an Anthropic client, or None if unavailable."""
    if not anthropic_available():
        return None
    from anthropic import Anthropic

    return Anthropic()


def extract_json(text: str):
    """Best-effort extraction of a JSON object from a model response.

    Handles ```json fences and leading/trailing prose. Returns the parsed
    object, or None on failure.
    """
    if not text:
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    # Fall back to the first balanced {...} span.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            return None
    return None


def ask_json(client, prompt: str, max_tokens: int = 800):
    """Call the model and return a parsed JSON object, or None on any error."""
    if client is None:
        return None
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return extract_json(resp.content[0].text)
    except Exception as exc:  # pragma: no cover - network/runtime guard
        log(f"  ! model call failed: {exc}")
        return None


def fetch_feed_entries(url: str, days_back: int = 14, limit: int = 60):
    """Fetch recent entries from an RSS/Atom feed, defensively.

    Returns a list of dicts; on any error returns an empty list (the workflow
    must never be broken by a single unreachable feed).
    """
    try:
        import feedparser
    except Exception as exc:
        log(f"feedparser unavailable ({exc}) — returning no entries.")
        return []

    try:
        feed = feedparser.parse(url)
    except Exception as exc:
        log(f"Error fetching feed {url}: {exc}")
        return []

    if getattr(feed, "bozo", 0) and not getattr(feed, "entries", None):
        log(f"Feed not parseable or empty: {url}")
        return []

    cutoff = datetime.now(timezone.utc).timestamp() - days_back * 86400
    entries = []
    for entry in getattr(feed, "entries", [])[:limit]:
        parsed = entry.get("published_parsed") or entry.get("updated_parsed")
        if parsed:
            try:
                ts = datetime(*parsed[:6], tzinfo=timezone.utc).timestamp()
                if ts < cutoff:
                    continue
            except Exception:
                pass
        entries.append(
            {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", entry.get("updated", "")),
                "summary": entry.get("summary", ""),
            }
        )
    return entries


def looks_like_fcpa(text: str) -> bool:
    low = (text or "").lower()
    return any(kw in low for kw in FCPA_KEYWORDS)


def load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: str, data) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def case_key(case: dict) -> str:
    """Stable-ish dedupe key for an enforcement case."""
    defendant = (case.get("defendant") or "").strip().lower()
    date = (case.get("settlement_date") or "").strip()
    return f"{defendant}|{date}" if defendant else ""


TRIAGE_SCHEMA_HINT = """Return ONLY valid JSON (no markdown, no prose) with exactly this shape:
{
  "is_enforcement": boolean,
  "defendant": "entity or person name, or null",
  "settlement_date": "YYYY-MM-DD or null",
  "penalty": "amount as a string incl. currency and TYPE (fine/disgorgement/forfeiture/combined), or null",
  "agency": "AGENCY_PLACEHOLDER",
  "case_type": "DPA/NPA/guilty plea/civil settlement/declination, or null",
  "statute": "FCPA anti-bribery / FCPA books-and-records / FCPA internal-controls / UK Bribery Act s.6 / s.7 / sanctions / other, or null",
  "key_facts": "1-2 factual sentences, or empty string",
  "violations": ["short list of alleged violations"],
  "sectors": ["industry sectors, e.g. energy, technology"]
}
Set is_enforcement=false if the item is not a bribery/corruption enforcement action."""


def triage_entries(entries, agency: str, client):
    """Pre-filter feed entries for FCPA/bribery relevance, then (optionally)
    use the model to extract structured details.

    Without a model client, returns pre-filtered *candidates* flagged
    ``needs_review`` so a human can complete them — never fabricated facts.
    """
    candidates = [e for e in entries if looks_like_fcpa(e["title"] + " " + e["summary"])]
    log(f"  {len(candidates)} keyword candidate(s) of {len(entries)} entries")

    results = []
    for entry in candidates:
        if client is None:
            results.append(
                {
                    "is_enforcement": None,
                    "needs_review": True,
                    "agency": agency,
                    "defendant": None,
                    "settlement_date": None,
                    "key_facts": "",
                    "source_url": entry["link"],
                    "source_title": entry["title"],
                    "source_date": entry["published"],
                }
            )
            continue

        prompt = (
            f"Analyse this {agency} press release and extract enforcement details "
            f"if it concerns a bribery/corruption action.\n\n"
            f"Title: {entry['title']}\n"
            f"Summary: {entry['summary'][:800]}\n\n"
            + TRIAGE_SCHEMA_HINT.replace("AGENCY_PLACEHOLDER", agency)
        )
        data = ask_json(client, prompt, max_tokens=600)
        if not data:
            continue
        if data.get("is_enforcement"):
            data["needs_review"] = True  # AI output is never authoritative
            data["source_url"] = entry["link"]
            data["source_title"] = entry["title"]
            data["source_date"] = entry["published"]
            data.setdefault("agency", agency)
            results.append(data)
            log(f"  ✓ candidate: {data.get('defendant') or entry['title'][:60]}")
    return results


def run_source_monitor(agency: str, feed_urls, out_path: str, days_back: int = 14):
    """End-to-end monitor for one source: fetch -> triage -> save.

    Returns the list of extracted candidate cases. Always writes ``out_path``
    (possibly with an empty list) and never raises.
    """
    log(f"== Monitoring {agency} ==")
    entries = []
    for url in feed_urls:
        got = fetch_feed_entries(url, days_back=days_back)
        log(f"  {len(got)} recent entrie(s) from {url}")
        entries.extend(got)

    client = get_client()
    cases = triage_entries(entries, agency, client)

    save_json(
        out_path,
        {"agency": agency, "timestamp": now_iso(), "total": len(cases), "cases": cases},
    )
    log(f"  saved {len(cases)} candidate(s) -> {out_path}")
    return cases
