#!/usr/bin/env python3
"""
Daily ABCF regulatory monitor — zero-cost by default.

Pulls the last 24h from primary + commentary sources, classifies each item, writes
a dated digest to insider-trading/digests/, and emits high-relevance alerts for the
workflow to open GitHub issues.

Provider layer (LLM_PROVIDER env)
---------------------------------
  github   (default) OpenAI SDK against GitHub Models
           (base_url https://models.inference.ai.azure.com, key = GITHUB_TOKEN,
           model gpt-4o-mini). No extra secret; needs `permissions: models: read`.
  gemini   google-generativeai, gemini-1.5-flash, key = GEMINI_API_KEY (free tier).
  groq     OpenAI SDK against https://api.groq.com/openai/v1,
           llama-3.3-70b-versatile, key = GROQ_API_KEY (free tier).
  anthropic  existing Anthropic path (paid) — kept for later.
  none     skip the LLM entirely (keyword-only classification).

Quota protection
----------------
  * A keyword pre-filter (terms from feeds.yml) gates LLM calls — only matched
    items go to the model.
  * Each item is capped (title + first 800 chars + link) and items are batched
    up to 10 per request.
  * On HTTP 429 / quota errors the run falls back to keyword-only classification
    for the remainder — it never fails the workflow.

Every item ALWAYS gets a keyword-only baseline classification (category, sector
flags, extraterritorial / UAE-GCC flag, provisional gain-seeking vs loss-avoidance
tag), so a digest is produced even with no model at all. AI output is never
treated as fact — items are flagged needs_review.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone

# scripts/ is on sys.path[0] when run as ``python scripts/abcf_monitor.py``.
from common import (  # noqa: E402
    DEFAULT_MODEL,
    DEFAULT_UA,
    extract_json,
    fetch_feed_entries,
    log,
    now_iso,
    save_json,
    set_output,
)

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

FR_AGENCIES = [
    "securities-and-exchange-commission",
    "justice-department",
    "financial-crimes-enforcement-network",  # FinCEN
    "foreign-assets-control-office",          # OFAC
]

# Fallback term list if feeds.yml has no `terms:` block.
DEFAULT_TERMS = [
    "insider trading", "10b5-1", "Section 16", "FCPA", "anti-bribery", "bribery",
    "corruption", "kickback", "loss avoidance", "disgorgement", "Section 17(a)",
    "17(a)", "material non-public", "misappropriation",
]

SEC_FEEDS = [
    "https://www.sec.gov/news/pressreleases.rss",
    "https://www.sec.gov/rss/litigation/litreleases.xml",
]
DOJ_FEEDS = [
    "https://www.justice.gov/news/rss?type=press_release",
    "https://www.justice.gov/feeds/justice-news.xml",
]
SFO_FEEDS = ["https://www.sfo.gov.uk/feed/"]

FEEDS_YML = "insider-trading/sources/feeds.yml"
DIGEST_DIR = "insider-trading/digests"
ALERTS_PATH = "abcf_daily_alerts.json"  # transient; see .gitignore

BATCH_SIZE = int(os.environ.get("ABCF_BATCH_SIZE", "10"))
LOOKBACK_DAYS = int(os.environ.get("ABCF_LOOKBACK_DAYS", "1"))

# Per-item input caps (keeps each item well under ~1,500 input tokens).
TITLE_CAP = 300
SUMMARY_CAP = 800

# Sector / nexus / fact-pattern keyword rules (keyword-only fallback).
ENERGY_KW = (
    "oil", "gas", "petroleum", "energy", "pipeline", "lng", "refin", "drilling",
    "offshore", "renewable", "solar", "wind", "utility", "power plant", "electric",
    "crude", "opec", "upstream", "midstream",
)
AI_KW = (
    "artificial intelligence", " ai ", "ai-", "machine learning", "semiconductor",
    "chip", "gpu", "compute", "data center", "datacenter", "nvidia", "cloud",
    "frontier model", "large language model", "llm",
)
UAE_GCC_KW = (
    "uae", "united arab emirates", "emirates", "dubai", "abu dhabi", "gcc",
    "gulf cooperation", "saudi", "qatar", "kuwait", "bahrain", "oman", "riyadh",
)
EXTRATERRITORIAL_KW = (
    "foreign", "cross-border", "overseas", "abroad", "extraterritorial",
    "non-u.s.", "non-us", "foreign official", "subsidiary", "jurisdiction",
)
INSIDER_KW = (
    "insider trading", "insider", "10b5-1", "10b-5", "section 16", "tipping",
    "tippee", "material non-public", "material nonpublic", "misappropriation", "mnpi",
)
BRIBERY_KW = (
    "fcpa", "foreign corrupt practices", "bribe", "bribery", "corrupt", "kickback",
    "anti-bribery", "foreign official",
)
# Loss-avoidance vs gain-seeking (provisional).
LOSS_ACTION_KW = ("sold", "sale", "sell", "hedge", "hedged", "pledge", "pledged", "gift", "gifted", "collar", "put option")
GAIN_ACTION_KW = ("bought", "buy", "purchase", "acquired", "call option", "accumulated")
AHEAD_KW = ("prior to announcement", "ahead of", "before the announcement", "pre-announcement",
            "before the public", "in advance of", "bad news", "negative news", "disappointing")


def _env_list(name):
    raw = os.environ.get(name, "").strip()
    return [u.strip() for u in raw.split(",") if u.strip()]


def load_feeds_yaml():
    try:
        import yaml
    except Exception as exc:
        log(f"PyYAML unavailable ({exc}).")
        return {}
    try:
        with open(FEEDS_YML, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except FileNotFoundError:
        log(f"{FEEDS_YML} not found.")
        return {}


def load_terms(cfg):
    terms = cfg.get("terms") if isinstance(cfg, dict) else None
    return [str(t) for t in terms] if terms else list(DEFAULT_TERMS)


# --------------------------------------------------------------------------- #
# Fetchers
# --------------------------------------------------------------------------- #

def _requests():
    try:
        import requests

        return requests
    except Exception:
        return None


def fetch_federal_register(terms, days_back):
    requests = _requests()
    if requests is None:
        log("requests unavailable — skipping Federal Register.")
        return []
    gte = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")
    seen, items = set(), []
    for term in terms:
        params = [
            ("per_page", "40"), ("order", "newest"),
            ("conditions[term]", term),
            ("conditions[publication_date][gte]", gte),
            ("fields[]", "title"), ("fields[]", "html_url"),
            ("fields[]", "publication_date"), ("fields[]", "abstract"),
            ("fields[]", "agencies"), ("fields[]", "document_number"),
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
                    "source": "Federal Register", "source_type": "federal_register",
                    "agency": agencies or "Federal Register",
                    "title": doc.get("title", ""), "link": doc.get("html_url", ""),
                    "published": doc.get("publication_date", ""),
                    "summary": (doc.get("abstract") or "")[:1200],
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
                    "source": name, "source_type": "rss", "agency": agency,
                    "title": e["title"], "link": e["link"],
                    "published": e["published"], "summary": (e.get("summary") or "")[:1200],
                }
            )
    return items


def fetch_firm_feeds(cfg, days_back):
    items = []
    for feed in (cfg.get("feeds", []) or []):
        url = feed.get("url")
        if not url:
            continue
        name = feed.get("name", url)
        got = fetch_feed_entries(url, days_back=days_back)
        log(f"  firm feed {name}: {len(got)} entrie(s)")
        for e in got:
            items.append(
                {
                    "source": name, "source_type": "law_firm",
                    "agency": feed.get("publisher", "law firm"),
                    "title": e["title"], "link": e["link"],
                    "published": e["published"], "summary": (e.get("summary") or "")[:1200],
                }
            )
    return items


def gather(cfg, terms, days_back):
    items = []
    items += fetch_federal_register(terms, days_back)
    items += fetch_rss_source("SEC", "SEC", _env_list("SEC_FEEDS") or SEC_FEEDS, days_back)
    items += fetch_rss_source("DOJ Fraud/FCPA", "DOJ", _env_list("DOJ_FEEDS") or DOJ_FEEDS, days_back)
    items += fetch_rss_source("UK SFO", "SFO", _env_list("SFO_FEEDS") or SFO_FEEDS, days_back)
    items += fetch_firm_feeds(cfg, days_back)

    seen, deduped = set(), []
    for it in items:
        key = (it.get("link") or it.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    log(f"Collected {len(deduped)} unique item(s) from all sources.")
    return deduped


# --------------------------------------------------------------------------- #
# Keyword-only classification (baseline + fallback)
# --------------------------------------------------------------------------- #

def _text_of(item):
    return f"{item.get('title','')} {item.get('summary','')}".lower()


def keyword_match(item, terms):
    low = _text_of(item)
    return any(t.lower() in low for t in terms)


def _any(low, kws):
    return any(k in low for k in kws)


def keyword_classify(item, terms):
    """Rule-based classification — always available, no network."""
    low = _text_of(item)
    # Fact-pattern signals also indicate the insider-trading category, even when
    # the literal word "insider" is absent (e.g. "sold ... ahead of bad news").
    loss_signal = _any(low, LOSS_ACTION_KW) and _any(low, AHEAD_KW)
    gain_signal = _any(low, GAIN_ACTION_KW) and _any(low, AHEAD_KW)
    insider = _any(low, INSIDER_KW) or loss_signal or gain_signal
    bribery = _any(low, BRIBERY_KW)
    if insider and not bribery:
        category = "insider-trading"
    elif bribery and not insider:
        category = "anti-bribery-corruption"
    elif insider and bribery:
        category = "insider-trading" if low.count("insider") >= 1 else "anti-bribery-corruption"
    else:
        category = "fraud-other"

    energy = _any(low, ENERGY_KW)
    ai = _any(low, AI_KW)
    uae_gcc = _any(low, UAE_GCC_KW)
    extraterritorial = _any(low, EXTRATERRITORIAL_KW)
    section_17a = "17(a)" in low or "section 17(a)" in low or "securities act section 17" in low

    fact_pattern = None
    if category == "insider-trading":
        if loss_signal and not gain_signal:
            fact_pattern = "loss-avoidance"
        elif gain_signal and not loss_signal:
            fact_pattern = "gain-seeking"
        elif _any(low, LOSS_ACTION_KW):
            fact_pattern = "loss-avoidance"

    matched = keyword_match(item, terms)
    on_topic = category in ("insider-trading", "anti-bribery-corruption")
    if matched and on_topic and (energy or ai):
        relevance = "high"
    elif matched and on_topic:
        relevance = "medium"
    else:
        relevance = "low"

    energy_relevance = (4 if relevance == "high" else 3) if energy else 0
    ai_relevance = (4 if relevance == "high" else 3) if ai else 0

    snippet = (item.get("summary") or item.get("title") or "").strip().replace("\n", " ")
    bullets = [snippet[:200]] if snippet else []

    return {
        "category": category,
        "energy_relevance": energy_relevance, "ai_relevance": ai_relevance,
        "energy": energy, "ai": ai,
        "bullets": bullets,
        "extraterritorial": extraterritorial, "uae_gcc_nexus": uae_gcc,
        "insider_fact_pattern": fact_pattern, "section_17a": section_17a,
        "relevance": relevance, "rationale": "keyword-only classification",
        "method": "keyword", "needs_review": True,
    }


# --------------------------------------------------------------------------- #
# Provider layer
# --------------------------------------------------------------------------- #

class QuotaError(Exception):
    pass


def get_provider():
    return (os.environ.get("LLM_PROVIDER") or "github").strip().lower()


def make_llm_client(provider):
    """Return (kind, client, model) or None when unavailable/none."""
    if provider == "none":
        log("LLM_PROVIDER=none — keyword-only classification.")
        return None
    if provider == "github":
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            log("GITHUB_TOKEN not set — keyword-only fallback.")
            return None
        try:
            from openai import OpenAI
        except Exception as exc:
            log(f"openai SDK unavailable ({exc}) — keyword-only fallback.")
            return None
        return ("openai", OpenAI(base_url="https://models.inference.ai.azure.com", api_key=token), "gpt-4o-mini")
    if provider == "groq":
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            log("GROQ_API_KEY not set — keyword-only fallback.")
            return None
        try:
            from openai import OpenAI
        except Exception as exc:
            log(f"openai SDK unavailable ({exc}) — keyword-only fallback.")
            return None
        return ("openai", OpenAI(base_url="https://api.groq.com/openai/v1", api_key=key), "llama-3.3-70b-versatile")
    if provider == "gemini":
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            log("GEMINI_API_KEY not set — keyword-only fallback.")
            return None
        try:
            import google.generativeai as genai
        except Exception as exc:
            log(f"google-generativeai unavailable ({exc}) — keyword-only fallback.")
            return None
        genai.configure(api_key=key)
        return ("gemini", genai.GenerativeModel("gemini-1.5-flash"), "gemini-1.5-flash")
    if provider == "anthropic":
        from common import get_client
        client = get_client()
        if client is None:
            return None
        return ("anthropic", client, DEFAULT_MODEL)
    log(f"Unknown LLM_PROVIDER '{provider}' — keyword-only fallback.")
    return None


def _is_quota_error(exc):
    code = getattr(exc, "status_code", None) or getattr(getattr(exc, "response", None), "status_code", None)
    if code == 429:
        return True
    s = str(exc).lower()
    return any(k in s for k in ("429", "rate limit", "quota", "insufficient_quota",
                                "too many requests", "resource_exhausted", "rate_limit"))


def llm_raw_call(provider_tuple, prompt):
    kind, client, model = provider_tuple
    try:
        if kind == "openai":
            resp = client.chat.completions.create(
                model=model, temperature=0, max_tokens=1600,
                messages=[
                    {"role": "system", "content": "You are a precise regulatory-news classifier. Output only JSON."},
                    {"role": "user", "content": prompt},
                ],
            )
            return resp.choices[0].message.content
        if kind == "gemini":
            resp = client.generate_content(prompt)
            return resp.text
        if kind == "anthropic":
            resp = client.messages.create(
                model=model, max_tokens=1600,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
    except Exception as exc:
        if _is_quota_error(exc):
            raise QuotaError(str(exc))
        raise
    return None


BATCH_SCHEMA = """Classify EACH numbered regulatory/enforcement news item for an
anti-bribery, corruption & fraud (ABCF) project focused on the ENERGY and AI/compute
sectors.

Respond with ONLY this JSON (no markdown), exactly N objects, SAME ORDER as items:
{"results":[
  {
    "category":"anti-bribery-corruption"|"insider-trading"|"fraud-other",
    "energy_relevance":0-5,"ai_relevance":0-5,
    "bullets":["3 short factual bullets"],
    "extraterritorial":boolean,"uae_gcc_nexus":boolean,
    "insider_fact_pattern":"gain-seeking"|"loss-avoidance"|null,
    "section_17a":boolean,
    "relevance":"high"|"medium"|"low",
    "rationale":"one short sentence"
  }
]}
Notes: loss-avoidance = pre-announcement sales, hedges, gifts, or pledges made AHEAD
of bad news to avoid a loss. section_17a = an SEC complaint pleads Securities Act
Section 17(a). Base every field ONLY on the provided text; if unknown, use
conservative defaults (false / null / "low"). Do not invent facts."""


def build_batch_prompt(batch):
    lines = [BATCH_SCHEMA, "", f"There are {len(batch)} items:", ""]
    for i, it in enumerate(batch):
        lines.append(f"--- ITEM {i} ---")
        lines.append(f"source: {it.get('source','')} ({it.get('agency','')})")
        lines.append(f"title: {it.get('title','')[:TITLE_CAP]}")
        lines.append(f"summary: {it.get('summary','')[:SUMMARY_CAP]}")
        lines.append(f"link: {it.get('link','')}")
        lines.append("")
    return "\n".join(lines)


def llm_classify_batch(provider_tuple, batch):
    """Return a list aligned to batch (dict or None). Raises QuotaError on 429/quota."""
    text = llm_raw_call(provider_tuple, build_batch_prompt(batch))
    obj = extract_json(text) if text else None
    results = obj.get("results") if isinstance(obj, dict) else (obj if isinstance(obj, list) else None)
    if not isinstance(results, list):
        return [None] * len(batch)
    return [results[i] if i < len(results) and isinstance(results[i], dict) else None for i in range(len(batch))]


def _merge_llm(base, res):
    merged = dict(base)
    for k in ("category", "energy_relevance", "ai_relevance", "bullets", "extraterritorial",
              "uae_gcc_nexus", "insider_fact_pattern", "section_17a", "relevance", "rationale"):
        if k in res and res[k] is not None:
            merged[k] = res[k]
    try:
        merged["energy"] = int(merged.get("energy_relevance", 0)) >= 1
        merged["ai"] = int(merged.get("ai_relevance", 0)) >= 1
    except (TypeError, ValueError):
        pass
    merged["method"] = "llm"
    merged["needs_review"] = True
    return merged


def is_high_relevance(t):
    if not t:
        return False
    if str(t.get("relevance", "")).lower() == "high":
        return True
    try:
        return max(int(t.get("energy_relevance", 0)), int(t.get("ai_relevance", 0))) >= 4
    except (TypeError, ValueError):
        return False


def enrich(items, terms, provider_tuple):
    # 1) keyword baseline for every item (guarantees a classification exists).
    for it in items:
        it["triage"] = keyword_classify(it, terms)
        it["_matched"] = keyword_match(it, terms)

    # 2) LLM-enrich only keyword-matched items, batched, with quota fallback.
    if provider_tuple is not None:
        matched = [it for it in items if it["_matched"]]
        log(f"LLM triage: {len(matched)} keyword-matched item(s), batches of {BATCH_SIZE}.")
        quota_hit = False
        for start in range(0, len(matched), BATCH_SIZE):
            if quota_hit:
                break
            batch = matched[start:start + BATCH_SIZE]
            try:
                results = llm_classify_batch(provider_tuple, batch)
            except QuotaError as exc:
                log(f"  ! quota/429 — keyword-only for the rest of this run ({exc}).")
                quota_hit = True
                break
            except Exception as exc:
                log(f"  ! LLM batch error ({exc}) — keeping keyword baseline for this batch.")
                continue
            for it, res in zip(batch, results):
                if res:
                    it["triage"] = _merge_llm(it["triage"], res)

    for it in items:
        it["high_relevance"] = is_high_relevance(it["triage"])
    return items


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

CATEGORY_LABELS = {
    "anti-bribery-corruption": "Anti-Bribery / Corruption",
    "insider-trading": "Insider Trading",
    "fraud-other": "Fraud / Other",
}


def render_item(item):
    t = item.get("triage") or {}
    title = item.get("title") or "(untitled)"
    link = item.get("link")
    lines = [f"#### [{title}]({link})" if link else f"#### {title}"]
    meta = f"_{item.get('source','')}"
    if item.get("agency"):
        meta += f" · {item['agency']}"
    if item.get("published"):
        meta += f" · {item['published']}"
    meta += f" · via {t.get('method','keyword')}_"
    lines.append(meta)

    badges = [f"relevance: **{t.get('relevance','low')}**",
              f"energy {t.get('energy_relevance', 0)}/5", f"AI {t.get('ai_relevance', 0)}/5"]
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
    if t.get("method") == "keyword":
        lines.append("- _Keyword-only classification — confirm against the source._")
    lines.append("")
    return "\n".join(lines)


def render_digest(date_str, items, provider, triage_active):
    highs = [i for i in items if i.get("high_relevance")]
    buckets = {"anti-bribery-corruption": [], "insider-trading": [], "fraud-other": []}
    for it in items:
        cat = (it.get("triage") or {}).get("category")
        buckets.get(cat, buckets["fraud-other"]).append(it)

    out = [f"# ABCF Daily Digest — {date_str}", ""]
    out.append(
        f"_Generated {now_iso()} · provider: **{provider}**"
        f"{' (active)' if triage_active else ' (keyword-only fallback)'} · "
        f"{len(items)} item(s), {len(highs)} high-relevance._"
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
    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    provider = get_provider()
    log(f"== ABCF daily monitor {date_str} · LLM_PROVIDER={provider} ==")

    cfg = load_feeds_yaml()
    terms = load_terms(cfg)

    items = gather(cfg, terms, LOOKBACK_DAYS)
    provider_tuple = make_llm_client(provider)
    triage_active = provider_tuple is not None
    items = enrich(items, terms, provider_tuple)

    os.makedirs(DIGEST_DIR, exist_ok=True)
    digest_path = os.path.join(DIGEST_DIR, f"{date_str}.md")
    with open(digest_path, "w", encoding="utf-8") as fh:
        fh.write(render_digest(date_str, items, provider, triage_active))
    log(f"Wrote digest -> {digest_path}")

    alerts = []
    for it in items:
        if not it.get("high_relevance"):
            continue
        t = it.get("triage") or {}
        alerts.append(
            {
                "title": it.get("title", ""), "link": it.get("link", ""),
                "source": it.get("source", ""), "agency": it.get("agency", ""),
                "category": t.get("category", "fraud-other"),
                "relevance": t.get("relevance", ""),
                "energy_relevance": t.get("energy_relevance", 0),
                "ai_relevance": t.get("ai_relevance", 0),
                "extraterritorial": bool(t.get("extraterritorial")),
                "uae_gcc_nexus": bool(t.get("uae_gcc_nexus")),
                "insider_fact_pattern": t.get("insider_fact_pattern"),
                "section_17a": bool(t.get("section_17a")),
                "method": t.get("method", "keyword"),
                "bullets": (t.get("bullets") or [])[:3],
            }
        )
    save_json(ALERTS_PATH, {"date": date_str, "provider": provider, "count": len(alerts), "alerts": alerts})
    log(f"Wrote {len(alerts)} alert(s) -> {ALERTS_PATH}")

    set_output("provider", provider)
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
