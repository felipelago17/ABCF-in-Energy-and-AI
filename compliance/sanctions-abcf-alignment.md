# Sanctions & ABCF Alignment

**Summary.** Sanctions/export-control compliance and anti-bribery compliance are
usually run by different teams under different laws — but on the ground they
target **overlapping people, entities, and transactions**, and they fail for the
**same reason**: ownership opacity. This file explains the convergence and argues
for a **single, unified counterparty-risk workflow** that screens for corruption
and restricted-party exposure at once.

## Two regimes, converging targets

| | Sanctions / export controls | Anti-bribery (ABCF) |
|---|---|---|
| Authorities (US) | OFAC, BIS | DOJ, SEC |
| Authorities (UK/UAE) | OFSI; UK/EU regimes; UAE measures | SFO/FCA; UAE Penal Code |
| Core question | Is a **blocked/restricted** party involved? | Was value given to influence an **official**? |
| Decisive fact | **Beneficial ownership / control** (e.g., OFAC 50% rule) | **Beneficial ownership / official nexus** |
| Common failure | Opaque UBO hides a blocked person | Opaque UBO hides a PEP/official beneficiary |

The right-hand and left-hand columns share the **same decisive fact** —
who ultimately owns and controls the counterparty — which is why UBO tracing is
the keystone control for both (see
[`../institutional/beneficial-ownership.md`](../institutional/beneficial-ownership.md)).

## Where they overlap in practice

- **Same entities/networks.** OFAC/BIS restricted parties and high-corruption
  counterparties frequently sit in the same networks or are the same entities.
- **Same intermediaries.** An agent structured to obscure a bribe can also
  obscure a restricted end-user of controlled goods.
- **Same aggregation problem.** Sanctions rules aggregate ownership (the OFAC
  **50% rule**; analogous end-user/end-use analysis under the EAR); corruption
  diligence aggregates beneficial interest to find hidden PEPs. Both require
  resolving ownership to natural persons.
- **Same convergence surface in AI/compute.** Advanced-computing deals engage
  BIS export controls, OFAC sanctions, *and* FCPA/UK Bribery Act simultaneously
  — see [`../ai-compute/frontier-ai-enforcement.md`](../ai-compute/frontier-ai-enforcement.md).

## Cumulative risk profiles

A single transaction can carry additive exposure across regimes and
jurisdictions:

| Layer | Trigger |
|---|---|
| OFAC (US sanctions) | Blocked person; ≥50% ownership; US-nexus dealings |
| BIS (US export controls) | Entity List; controlled item/end-use/end-user |
| FCPA | US issuer/domestic concern; USD flows; SOE counterparties |
| UK Bribery Act | UK business nexus; associated persons (s.7) |
| UAE Penal Code | Bribery (public or private) in/affecting the UAE |

**Design to the highest applicable standard, and aggregate risk across
sanctions *and* corruption frameworks together** — not in separate silos that
each see only half the counterparty.

## The unified workflow

1. **One counterparty record.** Resolve identity and **beneficial ownership to
   natural persons** once (see [beneficial-ownership.md](../institutional/beneficial-ownership.md)).
2. **One screen, all lists.** Run OFAC (incl. 50% rule), BIS Entity List, other
   sanctions lists, **and** PEP/adverse-media/debarment against that record.
3. **One risk rating.** Feed both outputs into the
   [risk matrix](../risk-tools/abcf-risk-matrix.md) — a restricted-party
   proximity *or* a corruption red flag can carry the rating.
4. **One decision & record.** Single documented disposition covering both
   exposures; escalate on either.
5. **One monitoring cadence.** Re-screen for sanctions changes and corruption
   signals on the same schedule and triggers.

## Enforcement convergence

Authorities increasingly coordinate: US **anti-piling-on** policy credits
penalties across programs, and corporate resolutions now routinely span
corruption *and* sanctions/export findings (the Weatherford 2013 resolution
spanned DOJ, SEC, OFAC, and BIS — see
[`../case-studies/fcpa-energy.md`](../case-studies/fcpa-energy.md)). Treating the
regimes as one workflow mirrors how they are increasingly enforced.

## Sources

- OFAC 50 Percent Rule guidance; SDN and consolidated lists.
- BIS Export Administration Regulations; Entity List.
- FCPA and UK Bribery Act frameworks — [`../frameworks/fcpa.md`](../frameworks/fcpa.md), [`../frameworks/uk-bribery-act.md`](../frameworks/uk-bribery-act.md).
- DOJ anti-piling-on / coordination-of-corporate-resolution-penalties policy.
- FATF Recommendations on beneficial ownership and targeted financial sanctions.
