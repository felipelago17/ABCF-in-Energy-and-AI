# Frontier AI & Enforcement Convergence

**Summary.** Frontier-AI supply chains sit at the intersection of three
enforcement regimes that historically operated separately: **anti-corruption**
(FCPA, UK Bribery Act), **export controls** (BIS), and **sanctions** (OFAC).
Advanced computing is simultaneously a corruption-risk good (scarce,
high-value, state-linked) and a controlled good (export-restricted, sanctions-
sensitive). This file maps how those regimes are converging on the same
transactions and what that means for governance.

> ⚠️ **Anticipatory, not retrospective.** As of 2026 there is no frontier-AI-
> specific FCPA resolution. This analysis extrapolates from adjacent records
> (technology-vendor FCPA matters such as SAP 2024; energy-infrastructure
> corruption cases; and the tightening BIS advanced-computing controls). Treat
> forward-looking statements as risk hypotheses, not established enforcement.

## Three regimes, one transaction

| Regime | Authority | Question it asks | Trigger in an AI deal |
|---|---|---|---|
| Anti-corruption | DOJ/SEC, SFO | Was value given to influence an official? | SOE counterparties; intermediaries; permits |
| Export controls | BIS | Can this item/technology go to this end-user/use? | Advanced chips, model weights, dual-use tech |
| Sanctions | OFAC | Is a blocked person involved (incl. ≥50% ownership)? | Restricted counterparties, UBO exposure |

A single sovereign compute deal can raise all three at once. Historically a
company could staff these in separate teams; convergence means a finding under
one regime frequently implies exposure under another (e.g., an intermediary
arrangement built to obscure a bribe may also obscure a restricted end-user).

## Why convergence is happening

- **The good itself is controlled and coveted.** Advanced compute is both
  export-restricted and rationed — the same scarcity that invites bribery also
  invites export-control evasion, and the same intermediaries serve both.
- **Overlapping targets.** OFAC/BIS restricted parties and high-corruption
  counterparties are frequently the *same* entities or sit in the same
  networks; UBO opacity defeats all three screens at once (see
  [`../institutional/beneficial-ownership.md`](../institutional/beneficial-ownership.md)).
- **Coordinated enforcement posture.** U.S. authorities increasingly coordinate
  corporate resolutions and credit penalties across programs; corruption and
  national-security enforcement priorities are being articulated together.

## Affiliate & end-user determination in AI consortia

Compute-sharing arrangements, AI consortia, and JV cloud/data-centre vehicles
raise hard **affiliate/end-user determination** questions that span the regimes:
- **Who is the true end-user** of exported compute (BIS)?
- **Who ultimately owns/controls** the consortium vehicle (OFAC 50% rule;
  corruption UBO)?
- **Whose conduct binds the group** (FCPA agency/parent liability; UK Bribery
  Act s.7 associated persons)?

Because the answer to one often answers the others, the diligence should be
**unified**: resolve ownership and control once, to natural persons and to
end-users, and apply the result across all three screens.

## Governance implications

1. **Unify the screen.** Run corruption, export-control, and sanctions diligence
   as one workflow keyed on a single UBO/end-user determination.
2. **Board-level ownership.** Frontier-compute deals carry cross-regime,
   bet-the-company exposure; they belong in board risk oversight (see
   [`abcf-ai-procurement.md`](abcf-ai-procurement.md)).
3. **Contract for all three.** Reps/warranties, audit rights, end-use and
   restricted-party covenants, and termination triggers should address
   corruption *and* export/sanctions in the same instrument.
4. **Monitor the convergence surface.** Track BIS advanced-computing rules,
   OFAC designations, and DOJ/SEC corporate-enforcement policy together — a
   change in one reshapes exposure under the others. Use the
   [enforcement monitor](../.github/workflows/fcpa-sec-monitor.yml).

## Sources

- FCPA framework and technology precedents — [`../frameworks/fcpa.md`](../frameworks/fcpa.md), [`../case-studies/fcpa-ai-technology.md`](../case-studies/fcpa-ai-technology.md).
- BIS Export Administration Regulations; advanced-computing / Entity List controls (verify current rules).
- OFAC sanctions programs; 50 Percent Rule guidance.
- DOJ corporate-enforcement and anti-piling-on policies.
