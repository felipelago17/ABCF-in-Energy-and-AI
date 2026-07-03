# FCPA — U.S. Foreign Corrupt Practices Act

**Summary.** The FCPA (15 U.S.C. §§ 78dd-1 et seq., enacted 1977) has two
operative pillars: an **anti-bribery** prohibition and **accounting** (books-
and-records and internal-controls) provisions. It is jointly enforced by the
**Department of Justice** (criminal, and civil anti-bribery over domestic
concerns / foreign nationals) and the **Securities and Exchange Commission**
(civil, over issuers). Understanding the FCPA as a governance instrument means
seeing how these two agencies, plus corporate boards, auditors, and voluntary
self-disclosure incentives, form a distributed detection-and-deterrence
network.

## At a glance

| Element | Anti-bribery provisions | Accounting provisions |
|---|---|---|
| Statute | §§ 78dd-1, -2, -3 | § 78m(b) |
| Prohibits | Corrupt payments to **foreign officials** to obtain/retain business | False records; inadequate internal controls |
| Applies to | Issuers, domestic concerns, and certain persons acting in U.S. territory | **Issuers** only (SEC-registered) |
| Intent required | "Corruptly" and "willfully" (for criminal) | Knowing falsification (for criminal accounting) |
| Enforcers | DOJ (criminal), SEC (civil, issuers) | DOJ (criminal), SEC (civil) |

## The two pillars

### 1. Anti-bribery

Prohibits offering, paying, promising, or authorizing anything of value to a
**foreign official** (broadly defined — including officers/employees of
state-owned enterprises, which matters enormously in energy) to influence an
official act, secure an improper advantage, or obtain/retain business.

Key doctrines that recur in energy and technology matters:
- **Third-party liability.** Payments *through* agents, consultants,
  distributors, and JV partners are covered where the company knows — or is
  willfully blind to a high probability — that value will be passed to an
  official. Most FCPA exposure runs through intermediaries, not direct bribes.
- **State-owned enterprises.** Employees of national oil companies, sovereign
  wealth funds, and state utilities are typically "foreign officials." In the
  energy sector this sweeps in a large share of counterparties.
- **Facilitating payments exception & affirmative defenses.** A narrow
  exception exists for routine governmental action ("grease payments"), plus
  affirmative defenses for lawful-under-local-law payments and bona fide
  business expenditures. These are narrow and routinely overestimated.

### 2. Accounting (books-and-records & internal controls)

Applies to issuers. Requires (a) books and records that accurately reflect
transactions and (b) a system of internal accounting controls. These are
**strict-liability-flavored** civil hooks (no proof of bribery required for the
books-and-records charge) and are the SEC's workhorse — many resolutions rest
on accounting charges even where anti-bribery proof is harder.

## Jurisdictional reach (nexus)

The FCPA's reach is a frequent source of surprise:
- **Issuers** — any company with securities registered in the U.S. (including
  foreign issuers with ADRs), anywhere they operate.
- **Domestic concerns** — U.S. citizens, nationals, residents, and entities.
- **Territorial** — foreign persons/entities that take any act in furtherance
  of a corrupt payment while in U.S. territory (including, per DOJ practice,
  routing a wire through a U.S. correspondent bank or sending an email through
  U.S. servers).
- **Agency & conspiracy** theories extend liability to parents for subsidiary
  conduct and to co-venturers.

**UAE/GCC nexus.** A UAE-incorporated entity with no U.S. listing can still be
exposed where: it is a subsidiary or agent of a U.S. issuer; a JV includes a
U.S. domestic concern; payments touch U.S. dollars through correspondent
banking; or U.S. persons participate in authorizing conduct. See
[`frameworks/uae-gcc.md`](uae-gcc.md).

## Enforcement architecture (why it's polycentric)

FCPA enforcement does not rely on regulators finding bribes unaided. It is
engineered to *recruit* private actors into detection:
- **Voluntary self-disclosure** credit (the DOJ Corporate Enforcement Policy)
  makes coming forward materially cheaper than being caught — shifting
  detection cost onto companies and their counsel.
- **Cooperation & remediation** credit rewards internal investigation and
  control upgrades.
- **Auditors and the accounting provisions** turn financial-statement audits
  into a corruption-detection layer.
- **Monitors** (imposed in resolutions) extend oversight into the firm after
  settlement.
- **Whistleblower bounties** (SEC, via Dodd-Frank) pay insiders to report.

This is the core institutional insight of the repository: the FCPA works less
by direct policing than by **redistributing detection incentives** across a
network of boards, auditors, counsel, and insiders. See
[`institutional/polycentric-governance.md`](../institutional/polycentric-governance.md).

## Building an "Anti-Corruption Plan" (program expectations)

DOJ's *Evaluation of Corporate Compliance Programs* frames what a credible
program looks like. Practically, an Anti-Corruption Plan covers:
1. **Risk assessment** — sectoral, jurisdictional, and transaction-type risk
   (see [`risk-tools/abcf-risk-matrix.md`](../risk-tools/abcf-risk-matrix.md)).
2. **Third-party management** — risk-based due diligence, contractual
   anti-corruption reps/warranties and audit rights, ongoing monitoring
   (see [`compliance/third-party-vetting-lifecycle.md`](../compliance/third-party-vetting-lifecycle.md)).
3. **Internal controls** — approvals, gifts/hospitality/travel limits,
   political-contribution controls, books-and-records discipline.
4. **Tone from the top & board oversight** — documented, resourced, empowered.
5. **Training & communication** — role-based, tested, acknowledged.
6. **Monitoring, testing & audit** — proactive data analytics, not just
   reactive investigation.
7. **Investigation & remediation** — consistent discipline, root-cause fixes.
8. **M&A / JV integration** — pre- and post-acquisition due diligence and
   controls integration.

## Guidance & FAQ

The authoritative starting point is the DOJ/SEC *A Resource Guide to the U.S.
Foreign Corrupt Practices Act* (2nd ed., 2020), which consolidates statutory
text, hypotheticals, and declinations. Track updates to the DOJ Corporate
Enforcement Policy and the Compliance Program evaluation guidance, which are
revised more often than the statute.

## Recent enforcement (how to keep this current)

Do **not** treat any figure in this repository as a substitute for the primary
record. Log new actions via the [enforcement-tracking Issue template](../.github/ISSUE_TEMPLATE/enforcement-tracking.md)
and the [weekly monitor](../.github/workflows/fcpa-sec-monitor.yml). Worked
examples live in [`case-studies/fcpa-energy.md`](../case-studies/fcpa-energy.md)
and [`case-studies/fcpa-ai-technology.md`](../case-studies/fcpa-ai-technology.md),
each cited to primary sources.

> ⚠️ **Common misattribution.** Not every large penalty against an
> oilfield-services or technology company is an *FCPA* matter — several
> headline settlements are **sanctions** (OFAC) or **export-control** (BIS)
> resolutions. Always confirm the statute before filing a matter as FCPA. See
> [`case-studies/README.md`](../case-studies/README.md).

## Sources

- 15 U.S.C. §§ 78dd-1, 78dd-2, 78dd-3, 78m(b) (FCPA).
- DOJ & SEC, *A Resource Guide to the U.S. Foreign Corrupt Practices Act*, 2nd ed. (2020).
- DOJ, *Evaluation of Corporate Compliance Programs* (current edition).
- DOJ Corporate Enforcement and Voluntary Self-Disclosure Policy (current edition).
- SEC Office of the Whistleblower program materials (Dodd-Frank § 922).
