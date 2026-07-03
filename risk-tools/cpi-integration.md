# Corruption Perceptions Index (CPI) Integration

**Summary.** Transparency International's **Corruption Perceptions Index (CPI)**
is the most widely used cross-country corruption measure and a sensible *first-
pass* jurisdiction screen for ABCF risk. This file explains how to integrate CPI
into the [risk matrix](abcf-risk-matrix.md) and siting/sourcing decisions — and,
just as importantly, where CPI's limits require you to look past the score.

## What CPI is (and isn't)

- **Is:** an annual index scoring countries/territories on *perceived* public-
  sector corruption, aggregated from multiple expert and business surveys, on a
  0–100 scale (0 = highly corrupt, 100 = very clean), with a global ranking.
- **Isn't:** a measure of *experienced* corruption, of private-sector
  corruption, of a specific counterparty, or of a specific sub-national zone.
  It measures **perception**, is **national**, and **lags** real change.

Use it as a **tiering input**, never as a verdict on a transaction.

## Integrating CPI into the risk matrix

Map CPI bands to the jurisdiction axis of the [risk matrix](abcf-risk-matrix.md).
Bands are illustrative — set your own thresholds and revisit them when CPI is
republished each year:

| CPI band (illustrative) | Jurisdiction axis | Default posture |
|---|---|---|
| Upper (cleaner) | 1 — Low | Standard controls |
| Upper-middle | 2 — Moderate | Standard + reps/warranties |
| Lower-middle | 3 — Elevated | Enhanced due diligence |
| Lower (higher perceived corruption) | 4 — High | Full EDD; board sign-off; consider declining |

Then **adjust** the raw band using:
- **Sector enforcement history** — energy, infrastructure, and extractives carry
  sector risk that a general national score may understate.
- **Sub-national / zone specifics** — a special economic zone or free zone may
  diverge materially from the national score (see the UAE free zones in
  [`../frameworks/uae-gcc.md`](../frameworks/uae-gcc.md)).
- **Counterparty-specific diligence** — a clean-country counterparty with opaque
  UBO can outrank a high-CPI-risk country counterparty with transparent
  ownership. Country risk never overrides counterparty findings.

## Limits to respect

1. **Perception ≠ incidence.** A country can score poorly on perception while a
   specific, well-governed counterparty is low risk — and vice versa.
2. **Lag.** CPI moves slowly; a reform or a scandal may not yet be reflected.
3. **National granularity.** It cannot see sub-national, sectoral, or
   counterparty variation — where much real risk lives.
4. **Methodology sensitivity.** Scores derive from a changing basket of sources;
   small year-to-year moves may be noise. Watch **trends**, not single-year
   wobble.
5. **Public-sector focus.** Commercial (private-sector) bribery — squarely
   covered by the UK Bribery Act and the UAE Penal Code — is outside CPI's lens.

## Trend analysis

For monitoring, track **direction** over several years alongside the level:
- **Declining** scores in a jurisdiction where you operate → tighten controls,
  re-screen counterparties, revisit siting.
- **Improving** scores → evidence of reform, but confirm with sector and
  enforcement data before relaxing controls.
- Pair CPI trend with the [enforcement monitor](../.github/workflows/fcpa-sec-monitor.yml)
  so perception data and actual enforcement move your risk view together.

## Complementary indices

Triangulate CPI with other measures rather than relying on it alone:
- **World Bank Worldwide Governance Indicators** (Control of Corruption, Rule of
  Law) — see [`../governance-resources/multi-stakeholder-initiatives.md`](../governance-resources/multi-stakeholder-initiatives.md);
- **TRACE / Basel AML Index** and similar bribery/AML risk measures;
- **EITI** membership and validation status for extractive jurisdictions;
- **OECD Working Group on Bribery** enforcement ratings.

## Sources

- Transparency International, *Corruption Perceptions Index* (annual) — methodology note.
- World Bank, Worldwide Governance Indicators.
- Basel Institute on Governance, Basel AML Index; TRACE Bribery Risk Matrix.
- OECD Working Group on Bribery country reports.
