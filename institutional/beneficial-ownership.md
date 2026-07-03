# Beneficial Ownership & UBO Tracing

**Summary.** Corruption hides behind ownership opacity. The **ultimate
beneficial owner (UBO)** — the natural person who ultimately owns or controls an
entity — is the single most important fact in most ABCF risk assessments, and
the one most often deliberately obscured. Beneficial-ownership transparency is
therefore a keystone of the polycentric system: it is the *information layer*
that makes detection by every other centre (regulators, auditors, banks,
counterparties) possible.

## Why UBO is the crux

A bribe, a kickback, or a self-dealing arrangement almost always routes value to
a person hidden behind a chain of entities: a shell company, a nominee, a trust,
or a layered multi-jurisdiction structure. Without knowing the natural person at
the end of the chain you cannot tell whether a counterparty is:
- a **PEP** or the family member/associate of one (see [`../compliance/peps.md`](../compliance/peps.md));
- a **sanctioned** person hiding behind a non-listed entity (the OFAC 50% rule
  and analogous aggregation rules make UBO decisive — see
  [`../compliance/sanctions-abcf-alignment.md`](../compliance/sanctions-abcf-alignment.md));
- a **related party** to your own decision-makers (self-dealing);
- the **same person** appearing on both sides of a supposedly arm's-length deal.

Ownership opacity is not a neutral fact — it is itself a **red flag** and a cost
driver (see [`../risk-tools/red-flag-indicators.md`](../risk-tools/red-flag-indicators.md)).

## The transparency infrastructure

| Source | Jurisdiction | What it provides |
|---|---|---|
| FinCEN Beneficial Ownership registry (CTA) | USA | UBO info for many U.S. entities (access restricted) |
| People with Significant Control (PSC) register | UK | Public register of controllers of UK companies |
| EU beneficial-ownership registers | EU | Registers per AMLD (access varies post-2022 CJEU ruling) |
| EITI beneficial-ownership disclosure | Extractives | UBO of licence-holders in member countries |
| Open Ownership / OpenCorporates | Cross-border | Aggregated corporate & ownership data |

> **Access is uneven and shifting.** The U.S. Corporate Transparency Act
> established a FinCEN registry but access is restricted and its scope has been
> the subject of litigation and rule changes; the EU's public-access model was
> curtailed by a 2022 Court of Justice ruling. Treat "there is a register" as
> the start of diligence, not the end — registers vary in coverage, accuracy,
> verification, and who may query them.

## Multi-layer ownership in energy JVs

Energy joint ventures are structurally prone to opaque beneficial interest:
- **Layered SPVs** across multiple jurisdictions (often including secrecy
  jurisdictions) separate the operating asset from its ultimate owners.
- **Local-content and nominee arrangements** — sometimes legally mandated —
  can mask who really benefits.
- **Minority and carried interests** can place a hidden beneficiary in the cash
  flow without a visible control position.
- **Intermediary/agent equity** — an agent taking a stake rather than a fee can
  convert a bribe into an ownership entitlement that ordinary screening misses.

The governance response is to trace ownership to natural persons **at
onboarding and again at defined triggers** (ownership changes, new licences,
adverse media), and to treat unresolved opacity as a blocking condition, not a
residual note.

## Red-flag networks for obscured beneficial interest

Practical indicators that a structure is engineered to hide a beneficiary:
- Ownership chains passing through **secrecy jurisdictions** with no operational
  rationale;
- **Nominee** directors/shareholders and corporate-service-provider addresses
  shared across many unrelated entities;
- Ownership that **cannot be resolved** to any natural person, or that resolves
  to a person inconsistent with the counterparty's stated principals;
- **Bearer instruments**, undocumented trusts, or "management for the benefit of
  others" without disclosed beneficiaries;
- **Circularity** — entities owning each other in loops that terminate nowhere;
- Rapid, unexplained **ownership changes** just before or after a contract award.

These feed the opacity scoring in [`../risk-tools/red-flag-indicators.md`](../risk-tools/red-flag-indicators.md)
and the counterparty axis of the [risk matrix](../risk-tools/abcf-risk-matrix.md).

## UBO tracing as a polycentric function

No single actor sees the whole ownership picture: registers hold fragments,
banks hold KYC files, EITI holds extractive-licence UBO, investigative
journalists hold leak-derived data. Effective tracing **triangulates** across
these centres — which is exactly why transparency infrastructure (public
registers, EITI, open data) has outsized value: it lets every other centre do
its job. Opacity, conversely, disables the entire network at once.

## Sources

- U.S. Corporate Transparency Act (31 U.S.C. § 5336) and FinCEN beneficial-ownership rules.
- UK Persons with Significant Control (PSC) regime.
- EU Anti-Money-Laundering Directives; CJEU judgment on public register access (2022).
- FATF Recommendations 24 & 25 (beneficial ownership of legal persons and arrangements).
- EITI Standard — beneficial-ownership requirement.
