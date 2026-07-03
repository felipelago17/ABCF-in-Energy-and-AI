#!/usr/bin/env python3
"""Merge newly-found candidate cases into data/enforcement_registry.json.

Deduplicates on (defendant, settlement_date). Every merged case keeps its
``needs_review`` flag until a human verifies it against a primary source.
"""

from common import case_key, load_json, log, now_iso, save_json, set_output

REGISTRY = "data/enforcement_registry.json"
SUMMARY = "enforcement_summary.json"


def main() -> None:
    registry = load_json(
        REGISTRY,
        {
            "created": now_iso(),
            "last_updated": now_iso(),
            "total_cases": 0,
            "cases": [],
            "summary_stats": {"by_agency": {}},
        },
    )
    summary = load_json(SUMMARY, {})
    new_cases = summary.get("new_cases", [])

    existing = {case_key(c) for c in registry.get("cases", []) if case_key(c)}
    added = 0
    for case in new_cases:
        key = case_key(case)
        # Skip items with no usable identity (dedupe would be meaningless).
        if not key or key in existing:
            continue
        case.setdefault("needs_review", True)
        case.setdefault("added", now_iso())
        registry["cases"].append(case)
        existing.add(key)
        added += 1
        log(f"  + registry: {case.get('defendant')}")

    registry["last_updated"] = now_iso()
    registry["total_cases"] = len(registry["cases"])
    by_agency = {}
    for c in registry["cases"]:
        ag = (c.get("agency") or "unknown").lower()
        by_agency[ag] = by_agency.get(ag, 0) + 1
    registry["summary_stats"] = {"by_agency": by_agency}

    save_json(REGISTRY, registry)
    log(f"Registry now holds {registry['total_cases']} case(s); {added} new.")
    set_output("registry_added", added)
    set_output("has_updates", added > 0)


if __name__ == "__main__":
    main()
