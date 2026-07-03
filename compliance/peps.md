# Politically Exposed Persons (PEPs)

**Summary.** A **politically exposed person** is an individual entrusted with a
prominent public function — and, by extension, their **family members** and
**close associates**. PEP status does not imply wrongdoing; it signals *elevated
corruption and bribery risk* because such persons have the access and influence
that bribery seeks to buy, and are more likely to be the ultimate beneficiaries
of corrupt arrangements. PEP screening is a core ABCF and AML control and a
counterparty-axis input to the [risk matrix](../risk-tools/abcf-risk-matrix.md).

## Definition (FATF-aligned)

The FATF framework distinguishes:
- **Foreign PEPs** — entrusted with prominent public functions by a *foreign*
  country (heads of state/government, senior politicians, senior government/
  judicial/military officials, senior executives of state-owned enterprises,
  important political-party officials).
- **Domestic PEPs** — the same, in the home country.
- **International-organisation PEPs** — senior management of international
  organisations.

Crucially, the category extends beyond the individual to:
- **Family members** — spouses/partners, children and their spouses, parents.
- **Close associates** — persons with close business or beneficial-ownership
  relationships, including those holding assets on a PEP's behalf.

For ABCF, the **beneficial-ownership link is decisive**: a PEP hidden behind a
corporate structure is exactly the risk UBO tracing exists to surface (see
[`../institutional/beneficial-ownership.md`](../institutional/beneficial-ownership.md)).

## Why PEP status maps to bribery risk

- SOE senior executives are both **PEPs** and, under the FCPA/UK Bribery Act,
  **foreign officials** — so PEP screening and foreign-bribery screening cover
  the same people.
- Bribery frequently routes value to a PEP's **family or associate**, not the
  official directly — which is why the extended definition matters.
- A PEP as **beneficial owner** of a counterparty or intermediary is a strong
  red flag (see [`../risk-tools/red-flag-indicators.md`](../risk-tools/red-flag-indicators.md)).

## Screening sources

PEP status is identified through commercial PEP databases and jurisdiction-
specific sources. Note that, unlike sanctions lists, there is no single official
global PEP "list" — screening relies on aggregated data and judgement:
- Commercial PEP/adverse-media data providers.
- Jurisdiction-specific disclosures (e.g., DFSA and other regulators' guidance;
  asset-declaration regimes where public).
- EITI beneficial-ownership disclosures in extractive sectors.

> Because PEP data is aggregated and judgement-based, **document the basis** for
> a PEP determination (or clearance), and re-screen at monitoring triggers — a
> counterparty's owner can *become* a PEP after onboarding.

## Enhanced scrutiny — risk-based, not binary

PEP identification triggers **enhanced due diligence**, calibrated to the role
and the transaction (see the
[EDD checklist](../risk-tools/due-diligence-checklists.md)):
- Establish **source of wealth and source of funds**.
- Map the **official nexus** — does the PEP influence the award, permit, or
  counterparty selection at issue?
- Obtain **senior-management/board approval** for high-risk PEP relationships.
- Apply **ongoing monitoring** at a heightened cadence.

Risk is highest where a PEP with authority over the relevant decision is also a
beneficial owner of, or benefits from, the counterparty — that combination
should default to **escalate or decline**.

## PEPs and the convergence with sanctions

PEP screening sits alongside sanctions screening in a single counterparty
workflow: some PEPs are also sanctioned persons, and both defeat detection when
UBO is opaque. Run them together — see
[`sanctions-abcf-alignment.md`](sanctions-abcf-alignment.md).

## Sources

- FATF Recommendations 12 & 22 and FATF Guidance on Politically Exposed Persons (Recs 12 & 22).
- DFSA and other jurisdiction-specific PEP/AML guidance (see [`../frameworks/uae-gcc.md`](../frameworks/uae-gcc.md)).
- FCPA "foreign official" scope, incl. SOE employees — [`../frameworks/fcpa.md`](../frameworks/fcpa.md).
