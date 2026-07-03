# Contributing to ABCF Governance

Thank you for helping build a rigorous, well-sourced resource on anti-bribery,
corruption, and fraud (ABCF) prevention. This is a *living* repository:
regulatory landscapes move, enforcement priorities shift, and standards are
revised. Contributions that keep the material accurate and current are as
valuable as new frameworks.

## Ground rules

1. **Cite primary sources.** Enforcement facts (amounts, dates, statutes,
   authorities) must be traceable to a primary source — a DOJ or SEC press
   release, an SEC administrative order, an SFO announcement, a court filing,
   or the text of a statute/standard. Secondary reporting is fine for context
   but should not be the sole basis for a factual claim.
2. **No legal advice.** Everything here is educational. Do not phrase content
   as advice to a specific reader ("you should…"); phrase it as analysis
   ("organizations subject to Section 7 typically…").
3. **Separate fact from analysis.** When you interpret or editorialize, make it
   clear which sentences are established fact and which are the repository's
   analytical framing.
4. **Prefer durable framing.** Favor structural analysis (incentives, network
   design, transaction costs) over point-in-time data that will age quickly.
   When you must cite point-in-time data, date it and link the source.

## What we welcome

- **Regulatory updates** — new enforcement actions, agency guidance, revised
  standards (ISO 37001 revisions, EITI Standard updates, UNCAC review reports).
- **Case analysis** — governance-network readings of major FCPA, UK Bribery
  Act, or ISO 37001 matters. Use the existing case-study structure.
- **Framework improvements** — better risk matrices, sectoral checklists,
  institutional case studies, red-flag taxonomies.
- **Corrections** — if you find a wrong figure, date, or statute, open an Issue
  or PR. Corrections are high priority.
- **Translations & localization** — ABCF frameworks adapted for non-English
  jurisdictions, with source citations in the original language.

## What we do *not* accept

- **Confidential or proprietary information** — client-specific assessments,
  non-public settlements or investigations, proprietary tools.
- **Legal advice** — this repository is informational, not counsel; no
  situation- or jurisdiction-specific opinions.
- **Vendor promotion** — no marketing of compliance software/services, no
  affiliate links.
- **Unsubstantiated claims** — enforcement facts must cite a primary source;
  no speculation about open investigations.
- **Harmful content** — no instructions for committing bribery, laundering, or
  evading detection.

## How to contribute

### Issues
Use the Issue templates:
- **Enforcement tracking** — log a new enforcement action (with the analytical
  fields for governance-network and transaction-cost reading).
- **Regulatory guidance & standards update** — track guidance, standards
  revisions, and ISO 37001 developments.
- **Framework request** — propose a new framework, checklist, or risk tool.
- **Case submission / correction** — propose a new case study or correct an
  existing one.

Note: an [automated monitor](docs/AUTOMATION.md) may open `needs-verification`
enforcement issues. These are **unverified leads** — confirm each against its
primary source before it graduates into a cited `case-studies/` entry.

### Labels
- **Authority:** `doj`, `sec`, `fca`, `sfo`, `dfsa`
- **Type:** `enforcement-monitoring`, `guidance`, `regulatory-update`, `needs-verification`, `automated`
- **Sector:** `energy`, `technology`, `finance`, `defense`, `infrastructure`
- **Framework:** `polycentric-governance`, `transaction-cost-analysis`, `institutional-analysis`, `governance`
- **Activity:** `case-study`, `framework`, `research`

### Pull requests
1. Fork and branch from the default branch. Use a descriptive branch name
   (e.g. `case/rolls-royce-dpa-update`, `fix/schlumberger-statute`).
2. Keep PRs focused — one framework, one case, or one correction per PR where
   practical.
3. Follow the file conventions below.
4. In the PR description, list your primary sources.

## File conventions

- **Format:** GitHub-flavored Markdown. One `# H1` title per file.
- **Structure:** Every framework/case file opens with a short **Summary** and,
  where relevant, an **At a glance** table.
- **Sourcing:** Put a **Sources** section at the foot of any file that makes
  factual claims. Link to primary sources.
- **Dates:** Use ISO format (YYYY-MM-DD) or "Month YYYY". Never rely on relative
  time ("recently", "last year").
- **Money:** State the currency and whether a figure is a total, a U.S.
  portion, disgorgement, a penalty, or a combined global resolution — these are
  routinely conflated in secondary reporting.
- **Uncertainty:** If you cannot verify something, write "unverified" and say
  what you checked. Do not guess.

## Accuracy over completeness

A smaller, correct repository beats a large, wrong one. When in doubt, mark a
claim as unverified and open an Issue rather than asserting it. The
[case-studies README](case-studies/README.md) lists commonly-misattributed
matters — please help keep that list current.

## Attribution & credit

Contributors are credited by contribution type and, where offered, linked to a
GitHub profile or professional affiliation. Say in your PR how you'd like to be
credited (or if you'd prefer not to be).

## Code of conduct

Be constructive and precise. Assume good faith. Disagreements about
interpretation are expected in a governance repository — resolve them with
sources, not volume.
