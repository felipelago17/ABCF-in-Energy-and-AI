# UAE & GCC ABCF Compliance Framework

**Summary.** The UAE and wider GCC present a distinctive ABCF profile: a
federal criminal code that covers **both public- and private-sector bribery**,
several **financial free zones** (DIFC, ADGM) with their own regulators, large
**state-owned enterprises** (notably ADNOC) whose employees are foreign
officials under U.S./UK law, and a growing role as a hub for energy and AI/data-
centre investment. For a foreign investor the practical exposure is usually
*cumulative*: UAE law **plus** FCPA **plus** UK Bribery Act on the same facts.

> ⚠️ **Verify article numbers before relying on them.** Secondary sources cite
> the UAE Penal Code's bribery articles inconsistently. This file deliberately
> avoids asserting specific article numbers; confirm against the official
> Arabic text / official gazette or a licensed translation before quoting them.

## UAE Federal Decree-Law No. 31 of 2021 (the Penal Code)

Federal Decree-Law No. 31 of 2021 is the **UAE Penal Code** ("Crimes and
Penalties Law"), in force **2 January 2022**, replacing Federal Law No. 3 of
1987. Its bribery and corruption provisions:
- criminalise bribery of **public officials**, **foreign public officials**, and
  employees of international organisations;
- extend to **private-sector (commercial) bribery** — a notable feature that
  aligns the UAE with the UK Bribery Act's breadth and beyond the FCPA's
  public-official focus;
- reach **intermediaries and facilitators**; and
- carry imprisonment and substantial fines.

For governance design, the private-sector reach matters: it means vendor and
counterparty bribery inside the UAE is a *local criminal* risk, not only a
reputational one.

## The free-zone regulators (polycentric by construction)

The UAE hosts financial free zones with **independent** civil/commercial law and
regulators, layered on top of federal criminal law:
- **DIFC (Dubai International Financial Centre)** — regulated by the **DFSA
  (Dubai Financial Services Authority)**, with AML/CFT and conduct rules that
  bear directly on bribery-adjacent controls, PEP screening, and source-of-funds
  diligence.
- **ADGM (Abu Dhabi Global Market)** — regulated by the **FSRA (Financial
  Services Regulatory Authority)**, with an analogous common-law framework.
- **DMCC (Dubai Multi Commodities Centre)** — a large free zone hosting
  commodities and trading entities, with its own compliance expectations.

This produces a genuinely polycentric domestic landscape: federal criminal
authorities, free-zone financial regulators, and AML supervisors operate in
overlapping jurisdictions. See
[`institutional/polycentric-governance.md`](../institutional/polycentric-governance.md).

## AML / financial-crime overlay

Core anti-money-laundering obligations sit under separate federal instruments
(e.g., Federal Decree-Law No. 20 of 2018 on AML/CFT and its executive
regulations), supervised through federal bodies and the free-zone regulators.
Because bribe proceeds are laundered, AML controls (KYC, beneficial-ownership
identification, suspicious-transaction reporting, PEP screening) are a frontline
ABCF-detection layer. See
[`compliance/sanctions-abcf-alignment.md`](../compliance/sanctions-abcf-alignment.md).

## ADNOC and state-owned enterprises

ADNOC and other GCC national oil companies and sovereign investors are central
counterparties in energy and, increasingly, in compute/AI infrastructure deals.
Two governance points:
1. **Their employees are "foreign officials."** Under the FCPA and UK Bribery
   Act, employees of state-owned enterprises are typically foreign public
   officials. Ordinary commercial dealings — gifts, hospitality, sponsorships,
   agent commissions — therefore carry foreign-bribery risk that a purely
   domestic lens would miss.
2. **Their own governance and disclosure standards** create counterparty
   expectations (supplier codes, anti-corruption representations, audit rights)
   that flow down the contracting chain.

## The cumulative-exposure model

A single UAE energy or AI-infrastructure transaction can simultaneously engage:

| Regime | Trigger | See |
|---|---|---|
| UAE Penal Code (Decree-Law 31/2021) | Any bribery in/affecting the UAE, public or private | this file |
| DFSA / FSRA rules | Regulated activity in DIFC / ADGM | this file |
| UAE AML law | Handling/laundering of proceeds | [sanctions-abcf-alignment.md](../compliance/sanctions-abcf-alignment.md) |
| **FCPA** | U.S. issuer/domestic concern, USD flows, SOE counterparties | [fcpa.md](fcpa.md) |
| **UK Bribery Act** | "Part of a business" in the UK; associated persons | [uk-bribery-act.md](uk-bribery-act.md) |
| OFAC/BIS | Sanctioned counterparties, restricted tech/exports | [sanctions-abcf-alignment.md](../compliance/sanctions-abcf-alignment.md) |

The practical implication: design the compliance program to the **highest**
applicable standard across the stack, and aggregate counterparty risk across
sanctions **and** corruption frameworks simultaneously — the two share targets
more often than they diverge.

## Sources

- UAE Federal Decree-Law No. 31 of 2021 (Penal Code) — verify bribery article numbers against the official text.
- UAE Federal Decree-Law No. 20 of 2018 (AML/CFT) and executive regulations.
- DFSA Rulebook (AML module); ADGM FSRA rules; DMCC compliance requirements.
- FCPA and UK Bribery Act materials (see [fcpa.md](fcpa.md), [uk-bribery-act.md](uk-bribery-act.md)).
