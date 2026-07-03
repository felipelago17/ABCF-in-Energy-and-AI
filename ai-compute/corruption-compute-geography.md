# Corruption & Compute Geography

**Summary.** Where you build and buy compute is now a corruption-risk decision.
The global build-out of AI data centres is driven by the availability of
**power, land, water/cooling, capital, and favourable jurisdictions** — and
several of the most attractive locations on those dimensions score poorly on
corruption-perception measures. This creates a genuine **trade-off**: diversifying
compute geography (for resilience, cost, or to avoid sanctioned suppliers) can
raise corruption exposure, and vice versa. Governance means making that trade-off
deliberately, not by accident.

## The infrastructure interfaces where bribery happens

Data-centre projects touch exactly the interfaces with the worst corruption
records:
- **Land acquisition** — assembly, zoning, and title, often involving local
  officials.
- **Power** — grid connection, generation permits, and long-term power purchase
  agreements, frequently with state utilities.
- **Water / cooling** — abstraction rights and utility connections.
- **Permitting & construction** — environmental, building, and operating permits;
  customs on imported equipment (the classic freight-forwarding bribe interface
  seen in the Panalpina-era energy cases).
- **Fiscal incentives** — tax holidays and subsidies negotiated with governments.

Each is a discretionary official decision over a high-value input — the textbook
setting for a bribe.

## The diversification trade-off

Two pressures push compute into higher-corruption-risk jurisdictions:
1. **Physical inputs** — cheap/abundant power, land, and cooling are sometimes
   found where governance is weaker.
2. **Supply-chain diversification** — avoiding sanctioned or export-restricted
   suppliers (a BIS/OFAC imperative) can route procurement and siting toward
   jurisdictions with higher CPI risk.

A governance framework must hold both objectives at once:

> Minimising **sanctions/export** exposure and minimising **corruption**
> exposure are *different* optimisation problems that can pull in opposite
> directions. Optimise them jointly, at board level, with the trade-off made
> explicit — not as two separate procurement workflows that never meet.

See [`abcf-ai-procurement.md`](abcf-ai-procurement.md) and
[`../compliance/sanctions-abcf-alignment.md`](../compliance/sanctions-abcf-alignment.md).

## Using CPI (and its limits) for siting

The Transparency International **Corruption Perceptions Index** is the standard
first-pass jurisdiction screen (see [`../risk-tools/cpi-integration.md`](../risk-tools/cpi-integration.md)).
For compute-siting decisions:
- Use CPI to **tier** candidate jurisdictions and set the required diligence
  depth and control intensity for each.
- **Do not treat CPI as deterministic.** It measures *perceptions*, lags real
  change, and is national-level — a well-governed special economic zone or a
  particular counterparty can diverge sharply from the country score.
- Combine CPI with **sector-specific** signals (energy/infrastructure permitting
  records, prior enforcement) and **counterparty-specific** diligence.

## A siting/sourcing risk workflow

1. **Screen jurisdictions** — CPI tier + sector enforcement history + sanctions/
   export posture.
2. **Map the official interfaces** the project will require (land, power,
   permits, customs, incentives) and score each for discretion and value.
3. **Resolve counterparties and intermediaries** to beneficial owners; screen
   for PEP and restricted-party status.
4. **Set controls to the joint (corruption × sanctions) risk** — enhanced
   diligence, payment controls, audit rights, and board sign-off for high-tier
   sites.
5. **Document the trade-off** — record why a higher-corruption-risk site was
   chosen and what controls offset it (defensible selection record).
6. **Monitor** — permitting-phase and operating-phase re-screening at triggers.

## The governance thesis

Compute geography is a governance-architecture problem, not just a cost or
latency problem. The right design puts the **corruption × sanctions** trade-off
in front of decision-makers with the information and controls to manage it —
exactly the polycentric, transaction-cost-informed approach this repository
advocates. See [`../institutional/polycentric-governance.md`](../institutional/polycentric-governance.md).

## Sources

- Transparency International, Corruption Perceptions Index (annual).
- BIS advanced-computing export controls; OFAC sanctions programs (verify current rules).
- FCPA infrastructure/customs precedents — see [`../case-studies/fcpa-energy.md`](../case-studies/fcpa-energy.md).
