# ABCF Risk Matrix

**Summary.** A structured, repeatable way to score bribery/corruption/fraud risk
for a transaction or counterparty and to map the score to a proportionate
control response. The matrix operationalises the transaction-cost principle that
control intensity should track expected loss (see
[`../institutional/transaction-cost-economics.md`](../institutional/transaction-cost-economics.md)).
It is a **starting template** — calibrate the weights and thresholds to your
sector and risk appetite.

## Three scoring axes

Score each axis, combine into an inherent-risk rating, then apply mitigation to
reach a residual rating.

### Axis 1 — Jurisdiction risk

| Score | Signal (illustrative) |
|---|---|
| 1 — Low | CPI top tier; strong rule of law; no recent sector enforcement |
| 2 — Moderate | Mid CPI; some enforcement history |
| 3 — Elevated | Lower CPI; weak institutions; sector corruption history |
| 4 — High | Bottom-tier CPI; systemic corruption; sanctions/conflict exposure |

Draw jurisdiction scores from CPI plus sector-specific enforcement history — see
[`cpi-integration.md`](cpi-integration.md). Remember CPI is national and
perception-based; adjust for the specific counterparty and sub-jurisdiction.

### Axis 2 — Transaction-type risk

| Score | Transaction type (illustrative) |
|---|---|
| 1 — Low | Arm's-length purchase of standard goods, private counterparty, low value |
| 2 — Moderate | Ongoing services; modest value; limited official interface |
| 3 — Elevated | Government/SOE contract; licences/permits; use of intermediaries |
| 4 — High | Large government/SOE contract *via intermediary*; JV with state party; M&A into high-risk market; rationed/allocated goods |

State and state-owned-enterprise counterparties raise the score because their
staff are "foreign officials" under the FCPA/UK Bribery Act.

### Axis 3 — Counterparty risk

| Score | Signal (illustrative) |
|---|---|
| 1 — Low | Transparent ownership; no PEP; clean record; established entity |
| 2 — Moderate | Some opacity; minor adverse media; newer entity |
| 3 — Elevated | PEP linkage; multi-layer ownership; unresolved diligence items |
| 4 — High | Unresolvable UBO; PEP beneficial owner; prior enforcement/debarment; restricted-party proximity |

Counterparty scoring depends on resolving beneficial ownership — see
[`../institutional/beneficial-ownership.md`](../institutional/beneficial-ownership.md)
and the red-flag catalogue in [`red-flag-indicators.md`](red-flag-indicators.md).

## Combining scores

A simple, transparent default: **inherent risk = max(axis scores)**, escalated
one tier if two or more axes are ≥3. Rationale: ABCF risk is *conjunctive* — a
single high axis (e.g., unresolvable UBO) can carry the whole transaction, so a
simple average would mask it. Document whichever rule you adopt.

| Inherent rating | Condition (default rule) |
|---|---|
| **Low** | all axes = 1 |
| **Moderate** | max axis = 2 |
| **Elevated** | max axis = 3 |
| **High** | any axis = 4, or ≥2 axes at 3 |

## Mitigation by tier

| Tier | Control response | Sign-off |
|---|---|---|
| **Low** | Standard database screening; standard terms | Business owner |
| **Moderate** | Screening + anti-corruption reps/warranties; periodic re-screen | Compliance review |
| **Elevated** | Enhanced due diligence (UBO tracing, adverse media, references); audit rights; payment controls; training/certification | Compliance sign-off |
| **High** | Full EDD + source-of-wealth; independent verification; hybrid oversight (monitoring, co-approval); board/senior-management approval; consider declining | Board / senior management |

Residual risk = inherent risk after mitigation. If residual remains **High**
with unresolved items (especially unresolvable UBO or a PEP beneficial owner
with an official nexus), the default posture is **decline or escalate**, not
proceed-with-a-note.

## Worked example (illustrative)

> Large services contract with a national oil company, won through a locally-
> introduced agent, in a bottom-tier-CPI jurisdiction, agent ownership routed
> through a secrecy jurisdiction.
>
> - Jurisdiction: **4** · Transaction type: **4** (SOE + intermediary) ·
>   Counterparty: **4** (opaque UBO) → **Inherent: High**.
> - Mitigation: resolve agent UBO to natural persons; source-of-wealth on the
>   agent; independent references; anti-corruption reps + audit rights; no
>   payments to third parties/jurisdictions; board sign-off. If UBO cannot be
>   resolved → **decline**.

## Using the matrix well

- **Score at intake and re-score at triggers** (ownership change, new licence,
  adverse media, value increase).
- **Keep the record.** The score, evidence, and mitigation decision are the
  defensible selection record regulators and boards will want.
- **Calibrate, don't copy.** Weights and thresholds are illustrative; tune them
  to your sector's loss experience and risk appetite.

## Sources

- DOJ, *Evaluation of Corporate Compliance Programs* (risk-based approach).
- DOJ/SEC *Resource Guide* (2nd ed., 2020) — risk assessment and third parties.
- UK Bribery Act MoJ guidance — proportionate procedures & risk assessment.
- Transparency International CPI — see [cpi-integration.md](cpi-integration.md).
