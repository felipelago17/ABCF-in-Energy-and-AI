# Enforcement-Monitoring Automation

This repository includes an optional, self-contained automation pipeline that
sweeps primary enforcement sources on a schedule and turns candidates into
GitHub Issues for human verification. It is **assistive, not authoritative** —
consistent with the repository's rule that every item is verified against a
primary source before it is treated as fact (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

## What it does

Workflow: [`.github/workflows/fcpa-sec-monitor.yml`](../.github/workflows/fcpa-sec-monitor.yml)
(runs Mondays & Thursdays 08:00 UTC, or on demand via **Actions → Run workflow**).

```
DOJ / SEC / SFO feeds ─┐
ISO 37001 feeds ───────┼─▶ per-source monitors ─▶ aggregate ─▶ registry
guidance feeds ────────┘        (keyword filter          │        (dedupe,
                                 + optional AI            │         needs_review)
                                 extraction)              ▼
                                                  GitHub Issues
                                                (verify-first banner)
```

| Script | Role |
|---|---|
| `scripts/common.py` | Shared helpers: model config, `$GITHUB_OUTPUT`, robust JSON, graceful feed/key handling |
| `scripts/monitor_fcpa_doj.py` | DOJ feed → FCPA candidates |
| `scripts/monitor_fcpa_sec.py` | SEC feed → FCPA candidates |
| `scripts/monitor_uk_bribery_sfo.py` | SFO feed → UK Bribery Act candidates |
| `scripts/monitor_iso37001.py` | ISO 37001 news/certification items (feed-driven) |
| `scripts/aggregate_enforcement_summary.py` | Merge candidates → summary + `ENFORCEMENT_SUMMARY.md` |
| `scripts/update_enforcement_registry.py` | Dedupe-merge into `data/enforcement_registry.json` |
| `scripts/check_regulatory_guidance.py` | Guidance-feed sweep → guidance issue |

## Setup

1. **Enable the workflow** — it ships enabled; the first scheduled run needs no
   configuration and will open a human-sweep issue.
2. **Add AI triage (optional but recommended):** add an `ANTHROPIC_API_KEY`
   secret under **Settings → Secrets and variables → Actions**. Without it, the
   scripts skip AI extraction and fall back to a manual-sweep checklist issue —
   they never fail for lack of a key.
3. **Pick a model (optional):** set an `ANTHROPIC_MODEL` *variable* (default
   `claude-sonnet-5`). Valid IDs include `claude-sonnet-5`, `claude-opus-4-8`,
   `claude-haiku-4-5-20251001`.
4. **Override feeds (optional):** the default feed URLs are best-effort and
   should be verified against the source sites. Override any of them with
   repository *variables* (comma-separated):
   `DOJ_FEEDS`, `SEC_FEEDS`, `SFO_FEEDS`, `ISO37001_FEEDS`, `GUIDANCE_FEEDS`.
5. **User-Agent (usually leave default):** SEC.gov and Cloudflare-fronted sites
   (DOJ, SFO) return **HTTP 403** to requests without a descriptive
   `User-Agent`, so the monitor sends one and it is overridable via the
   `FEED_USER_AGENT` variable. If a run reports feeds returning `HTTP 403` or
   zero items, adjust this (SEC's access policy expects a UA identifying the
   caller with a contact) before assuming the URLs are wrong.

## Design guarantees

- **Never asserts facts.** Every extracted item is flagged `needs_review` and
  every auto-created issue carries a *verify-first* banner. AI output is a
  research lead, not a citation.
- **Graceful degradation.** No API key, an unreachable feed, or a missing
  dependency does not break the run — the pipeline produces valid (possibly
  empty) output and still opens a tracking issue.
- **Deduplicated.** The registry keys on `(defendant, settlement_date)` so
  re-runs don't create duplicates.
- **Corrected mechanics.** Uses `$GITHUB_OUTPUT` (not the removed `::set-output`),
  valid model IDs, and `permissions:` scoped to what each job needs.

## Running locally

```bash
pip install -r scripts/requirements.txt
export ANTHROPIC_API_KEY=...        # optional; omit to test the degraded path
export PYTHONPATH=scripts
python scripts/monitor_fcpa_doj.py
python scripts/aggregate_enforcement_summary.py
python scripts/update_enforcement_registry.py
```

Artifacts (`*_enforcement.json`, `enforcement_summary.json`, etc.) are transient
and git-ignored; only `data/enforcement_registry.json` and
`ENFORCEMENT_SUMMARY.md` are committed by the workflow.

## Relationship to the verified case studies

The registry holds **unverified leads**. Once a human confirms an item against
its primary source, it graduates into a proper, cited entry under
[`case-studies/`](../case-studies/) — with the misattribution discipline
described in [`case-studies/README.md`](../case-studies/README.md).
