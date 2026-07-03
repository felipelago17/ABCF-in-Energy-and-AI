# ABCF in AI Vendor Procurement

**Summary.** Large-scale AI/compute procurement — data centres, GPU/accelerator
supply, power and cooling infrastructure, cloud and "technology commitment"
deals — reproduces every classic ABCF risk factor at new scale: enormous
contract values, state and state-owned counterparties (especially in the GCC),
scarce allocated goods (compute capacity, export-licensed chips), and heavy
reliance on intermediaries. It also sits directly on top of the **export-control
and sanctions** regime for advanced computing. The corruption and sanctions
screens must therefore run together.

> ⚠️ **No "AI-vendor FCPA case" exists yet (as of 2026).** The established
> technology precedents are **enterprise-software / IT vendors** (e.g., SAP,
> 2024) and earlier software-licensing matters — not AI companies. Do not imply
> that a frontier-AI-specific FCPA resolution has occurred. The risk analysis
> here is *anticipatory*, built by analogy from the software-vendor and
> energy-infrastructure records. See
> [`../case-studies/fcpa-ai-technology.md`](../case-studies/fcpa-ai-technology.md).

## Where the bribery risk concentrates

| Deal element | ABCF risk | Why |
|---|---|---|
| Sovereign / SOE compute deals (e.g., GCC) | Foreign-official bribery | SOE staff are "foreign officials"; deals are large and political |
| Scarce allocation (compute capacity, licensed GPUs) | Bribery for access/priority | Rationed goods invite side-payments |
| Land, power, cooling, permits for data centres | Infrastructure bribery | Permitting and land acquisition are classic bribe interfaces |
| Local agents / distributors / systems integrators | Intermediary liability | Value routed through third parties (FCPA/UKBA s.7) |
| Export-licensed hardware | Sanctions/export overlap | BIS controls on advanced computing chips |

## The sanctions/export-control overlay (why AI is different)

AI/compute procurement is uniquely entangled with **export controls**:
- Advanced computing chips and certain AI-relevant items are subject to **BIS**
  restrictions (Entity List designations and end-use/end-user controls on
  advanced computing).
- A vendor or counterparty can be simultaneously an **OFAC/BIS** restricted
  party *and* a corruption risk. Choosing a counterparty to avoid one exposure
  can increase the other.

The practical rule: **run the corruption screen and the restricted-party screen
as one workflow.** A compute deal that looks clean on bribery may fail on export
controls, and a diversification choice made to avoid a sanctioned supplier may
route procurement through a higher-corruption jurisdiction. See
[`../compliance/sanctions-abcf-alignment.md`](../compliance/sanctions-abcf-alignment.md)
and [`corruption-compute-geography.md`](corruption-compute-geography.md).

## Compliance via contract design ("technology commitment agreements")

Large compute deals are increasingly structured as multi-year **technology
commitment agreements** with sovereign or SOE counterparties. Contract design is
a primary control surface:
- **Anti-corruption representations & warranties** and ongoing compliance
  covenants (see [`../compliance/board-management-certification.md`](../compliance/board-management-certification.md));
- **Audit and inspection rights** over the counterparty's use and sub-dealings;
- **Restricted-party and end-use covenants** aligning the deal with export-
  control obligations;
- **Termination and suspension rights** on adverse findings;
- **No-intermediary / disclosed-agent** clauses and payment controls.

This is the transaction-cost logic of governing relationship-specific,
high-value risk through **hybrid** structures rather than market screening
alone — see [`../institutional/transaction-cost-economics.md`](../institutional/transaction-cost-economics.md).

## Board-level governance of compute allocation & vendor selection

Because compute is scarce, strategically sensitive, and often allocated to state
or state-linked counterparties, vendor and allocation decisions belong at
**board / senior-management** level, not buried in procurement:
- documented **conflict-of-interest** and related-party checks on decision-makers;
- **beneficial-ownership** resolution of counterparties before commitment (see
  [`../institutional/beneficial-ownership.md`](../institutional/beneficial-ownership.md));
- a defensible **selection record** showing selection on merit, not influence;
- integration of allocation decisions into the **enterprise ABCF risk
  assessment** and reporting lines.

## Anticipatory red flags for AI/compute deals

- A local intermediary introduced or "recommended" by an official as a condition
  of access;
- Compute or hardware allocation contingent on a consultancy, sponsorship, or
  charitable payment;
- Counterparty ownership that resolves to a PEP or cannot be resolved at all;
- Pressure to close a sovereign deal before diligence completes;
- Structuring that routes hardware through a jurisdiction to evade export
  controls (a sanctions **and** integrity red flag).

Feed these into [`../risk-tools/red-flag-indicators.md`](../risk-tools/red-flag-indicators.md).

## Sources

- FCPA framework and technology-vendor precedents — see [`../frameworks/fcpa.md`](../frameworks/fcpa.md), [`../case-studies/fcpa-ai-technology.md`](../case-studies/fcpa-ai-technology.md).
- BIS Export Administration Regulations; advanced-computing and Entity List controls (verify current rules).
- OFAC sanctions programs and the 50 Percent Rule.
- UK Bribery Act ss. 6–7 (foreign officials; associated persons).
