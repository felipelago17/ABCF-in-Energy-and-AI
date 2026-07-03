# Red-Flag Indicators

**Summary.** A structured catalogue of the warning signs most consistently
associated with bribery, corruption, and fraud, organised by where they surface.
Red flags are **probabilistic**, not dispositive — their value is in triggering
proportionate escalation and diligence, not in proving misconduct. A single
strong flag (e.g., unresolvable beneficial ownership) can warrant blocking a
transaction; clusters of weaker flags compound.

## How to use this catalogue

1. Screen against these categories at intake and at monitoring triggers.
2. Record each flag, its evidence, and the disposition (cleared / mitigated /
   escalated / blocked).
3. Feed flags into the [risk matrix](abcf-risk-matrix.md) counterparty and
   transaction axes.
4. Treat **opacity itself** as a flag — inability to verify is a finding, not a
   neutral gap.

## 1. Beneficial-ownership opacity

- Ownership chains through **secrecy jurisdictions** with no operational rationale.
- UBO that **cannot be resolved** to any natural person, or resolves to someone
  inconsistent with the counterparty's stated principals.
- **Nominee** directors/shareholders; corporate-service-provider addresses shared
  across many unrelated entities.
- Rapid or unexplained **ownership changes** around a contract award.
- **Circular** ownership; bearer instruments; undocumented trusts.

See [`../institutional/beneficial-ownership.md`](../institutional/beneficial-ownership.md).

## 2. Politically exposed persons (PEPs) & official nexus

- A PEP (or family member / close associate) among owners, directors, or UBOs.
- A counterparty **introduced or recommended by an official** as a condition of
  the deal.
- Awards tracking to entities linked to decision-makers.
- Requests to route benefits to charities, sponsorships, or consultancies
  connected to officials.

See [`../compliance/peps.md`](../compliance/peps.md).

## 3. Third-party / intermediary warning signs

- Agent/consultant with **no verifiable track record**, staff, or premises for
  the work.
- **Commission** disproportionate to services, or success-fee-only structures at
  the state interface.
- Vague or **undocumented deliverables** ("business development", "facilitation").
- Requests for payment in **cash**, to a **third party**, or to a **third
  jurisdiction** unrelated to the work.
- **Refusal** to sign anti-corruption representations, accept audit rights, or
  disclose ownership.
- Agent engaged **only because** a particular official/customer required it.

See [`../institutional/vendor-third-party-risk.md`](../institutional/vendor-third-party-risk.md).

## 4. Related-party & self-dealing patterns

- Same natural person on **both sides** of an ostensibly arm's-length deal.
- Undisclosed relationships between counterparty owners and internal
  decision-makers.
- Terms **off-market** in the counterparty's favour without justification.
- Vendors sharing addresses, bank accounts, or signatories with each other or
  with employees.

## 5. Procurement-process irregularities

- **Sole-sourcing** or bypassed competitive process without documented basis.
- Specifications **tailored** to a predetermined winner.
- **Split invoices** to stay under approval thresholds.
- Bids that suggest **collusion** (cover pricing, rotation, identical errors).
- Contract **scope creep** or change orders inflating value post-award.
- **Pressure to close** before diligence completes.

## 6. Financial & books-and-records signals

- Payments **mischaracterised** in the books (e.g., "consulting", "marketing",
  "commissions") without support.
- **Round-sum** payments, unusual timing relative to milestones/tenders.
- Missing or **reconstructed** documentation; overrides of controls.
- Petty-cash, gifts, hospitality, and travel patterns clustering around
  officials or tenders.

The FCPA accounting provisions make these signals independently significant —
false records are a violation even without proof of the underlying bribe. See
[`../frameworks/fcpa.md`](../frameworks/fcpa.md).

## 7. Sanctions / export-control proximity (convergence flags)

- Counterparty or its UBO near an **OFAC/BIS** restricted party (incl. the 50%
  ownership rule).
- Structuring that appears designed to **obscure an end-user** of controlled
  goods (advanced compute/dual-use).
- Trans-shipment through jurisdictions with no commercial logic.

See [`../compliance/sanctions-abcf-alignment.md`](../compliance/sanctions-abcf-alignment.md).

## Escalation logic

| Situation | Default response |
|---|---|
| Single weak flag, otherwise low risk | Document, clear or monitor |
| Cluster of weak flags | Enhanced due diligence; compliance review |
| Any strong flag (unresolvable UBO, PEP official nexus, restricted-party proximity) | Escalate to senior/board; consider blocking |
| Flag unresolved after diligence | Do not proceed; escalate |

Red flags interact with the [risk matrix](abcf-risk-matrix.md) and the
[due-diligence checklists](due-diligence-checklists.md).

## Sources

- DOJ/SEC *Resource Guide to the FCPA* (2nd ed., 2020) — red flags & third parties.
- UK Bribery Act MoJ guidance — due diligence and monitoring.
- FATF guidance on red-flag indicators for money laundering / corruption.
- OFAC / BIS restricted-party frameworks (verify current lists).
