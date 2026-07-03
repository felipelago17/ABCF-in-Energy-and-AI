# Vendor & Third-Party Risk

**Summary.** Third parties — agents, distributors, consultants, freight
forwarders, sub-contractors, JV partners, and vendors — are the dominant vector
for ABCF exposure. The overwhelming share of FCPA and UK Bribery Act matters run
*through* an intermediary, not through a direct corporate bribe. Managing
third-party risk is therefore the highest-leverage governance activity, and it
is where the sanctions and corruption regimes most tightly converge.

## Why third parties dominate the risk

- **Liability flows through them.** Under the FCPA, knowledge (including willful
  blindness) that value will reach an official through an intermediary is enough.
  Under UK Bribery Act **s.7**, an "associated person" bribing for the company's
  benefit makes the company liable — with only the adequate-procedures defence.
- **They sit at the state interface.** Local agents exist precisely to interact
  with governments, customs, and state-owned enterprises — the highest-risk
  counterparties.
- **They create information asymmetry.** The principal often cannot see how the
  intermediary spends its commission — the asset-specificity/opportunism problem
  from [`transaction-cost-economics.md`](transaction-cost-economics.md).

## Two convergent screens: sanctions and corruption

Third-party vetting must run **two overlapping screens** on every counterparty,
because the same entity can be both a corruption and a sanctions risk:

### Sanctions / restricted-party screening
- **OFAC** — SDN List and sectoral/consolidated lists; apply the **50% rule**
  (entities owned ≥50% by blocked persons are themselves blocked), which makes
  UBO tracing decisive (see [`beneficial-ownership.md`](beneficial-ownership.md)).
- **BIS** — the **Entity List** and related export-control restrictions
  (critical for AI/compute hardware and dual-use technology — see
  [`../ai-compute/abcf-ai-procurement.md`](../ai-compute/abcf-ai-procurement.md)).
- Other national/UN/EU/UK consolidated sanctions lists as applicable.

### Corruption / integrity screening
- **PEP status** of owners, directors, and beneficial owners (see
  [`../compliance/peps.md`](../compliance/peps.md));
- **Jurisdiction risk** (CPI and sector history — see
  [`../risk-tools/cpi-integration.md`](../risk-tools/cpi-integration.md));
- **Adverse media** and prior enforcement, debarment, or investigation;
- **Ownership opacity** and unexplained structure;
- **Relationship red flags** — how the vendor was introduced, by whom, and
  whether an official recommended them.

> Screening lists and rules cited here change frequently. Verify against the
> live primary sources at time of screening; do not rely on cached snapshots.

## Governance-network design for procurement compliance

Third-party risk is managed by *designing a network*, not by a single gate:

1. **Risk-tiering at intake.** Classify every third party by inherent risk
   (transaction value, role at the state interface, jurisdiction, ownership
   transparency). Tier drives depth — the transaction-cost calibration.
2. **Graduated due diligence.** Light-touch database screening for low-risk
   vendors; enhanced diligence (UBO tracing, source-of-wealth, site visits,
   references) for high-risk intermediaries.
3. **Contractual controls.** Anti-corruption representations & warranties,
   audit rights, right to terminate for breach, no-subcontracting-without-
   consent, and certification/training obligations. These *shift detection to
   the party with the information* — the polycentric move.
4. **Payment controls.** No cash, no payments to third jurisdictions or third
   parties, invoices matched to deliverables, approval thresholds.
5. **Ongoing monitoring.** Periodic re-screening, adverse-media monitoring,
   relationship reviews at defined triggers.
6. **Escalation & remediation.** Clear routes to block, investigate, and remove;
   documented decisions.

See [`../compliance/third-party-vetting-lifecycle.md`](../compliance/third-party-vetting-lifecycle.md)
for the operational lifecycle and [`../risk-tools/due-diligence-checklists.md`](../risk-tools/due-diligence-checklists.md)
for checklists.

## The "make vs. buy" of screening

Following [`transaction-cost-economics.md`](transaction-cost-economics.md),
organisations choose how to *govern* screening itself:
- **Buy** — third-party screening databases and diligence providers (efficient
  at scale, weaker on relationship-specific and locally-sourced risk);
- **Make** — in-house investigations and monitoring (costly, reserved for the
  highest-risk relationships);
- **Hybrid** — external data feeds plus internal analyst review and escalation
  (the common equilibrium).

The right mix is driven by portfolio risk concentration: spend the scarce
in-house investigative capacity on the small tail of high-specificity,
high-value, high-jurisdiction-risk intermediaries where expected loss is
greatest.

## Sources

- FCPA third-party liability (DOJ/SEC *Resource Guide*, 2nd ed., 2020).
- UK Bribery Act 2010, ss. 7–8 (associated persons); MoJ six principles (due diligence).
- OFAC 50 Percent Rule guidance; BIS Entity List (EAR).
- FATF Recommendations on customer due diligence and beneficial ownership.
