# Insider Trading

Research module within the ABCF (anti-bribery, corruption & fraud) governance
framework, focused on **insider trading** as it intersects the framework's
energy- and AI-sector remit. It pairs a doctrinal reference with a daily
regulatory monitor that surfaces new SEC / DOJ / FinCEN / OFAC and UK activity.

> **Not legal advice.** Everything here is educational. Case figures, holdings,
> and statutory readings are cited to primary or secondary sources and should be
> confirmed against those sources before being relied on. Automated digest items
> are research leads, not findings.

## Layout

| Path | Contents |
|---|---|
| [`sources/`](sources/) | `feeds.yml` — the law-firm and commentary feeds the daily monitor polls. |
| [`digests/`](digests/) | Dated `YYYY-MM-DD.md` digests produced by the monitor. |
| [`case-law/`](case-law/) | Curated case and scholarship entries on insider-trading remedies. |

## Core Concepts

### The loss-avoidance doctrine

Following Stephen M. Bainbridge, *Insider Trading Law and Policy* (2d ed.)
§C.1, the operative insight is that **"profit" from insider trading includes
avoiding a loss.** An insider who trades on material non-public information
(MNPI) to *escape* an impending decline is treated, for liability and remedy
purposes, no differently from one who trades to *capture* a gain. Courts treat
trading to avoid a loss as **legally indistinguishable** from trading for gain:
the wrong is the exploitation of the informational asymmetry, not the arithmetic
sign of the trader's account statement.

**Worked example (per §C.1).** An insider holding stock at **$10/share** learns
of undisclosed bad news and sells before the announcement. The news breaks and
the price falls to **$5/share**. The insider realized no "gain" in the ordinary
sense — but avoided a **$5/share loss**, and that avoided loss is the measure of
liability:

- it is the base for **disgorgement** (the insider must give up the loss
  avoided, not merely gains made); and
- it is the base for the **civil penalty of up to three times** that amount
  under **Securities Exchange Act § 21A** (the ITSFEA treble-penalty provision),
  i.e. the penalty can reach up to **3 × the profit gained _or loss avoided_**.

The doctrinal significance is that the remedy provisions are drafted in the
disjunctive — **"profit gained or loss avoided"** — precisely so that a
defensive, loss-avoiding sale cannot escape the disgorgement-and-penalty regime
by pointing out that no positive profit was booked. See § 21A(a)(2) (penalty
pegged to "the profit gained or loss avoided as a result of such unlawful
purchase, sale, or communication").

### Why loss-avoidance matters to this framework

- **Fact-pattern tagging.** The daily monitor tags each insider-trading item as
  **gain-seeking** or **loss-avoidance**. Loss-avoidance fact patterns —
  *pre-announcement sales, hedges, gifts, and pledges made ahead of bad news* —
  are historically the most common classical-theory scenario (see
  [Steinberg & Ramirez](case-law/steinberg-ramirez-neglected-weapon.md)) yet are
  easy to overlook because the trader "only" broke even.
- **Remedy measurement.** Because disgorgement and § 21A penalties attach to the
  loss avoided, correctly identifying a defensive trade changes the *size* of the
  exposure, not just its existence. See
  [*SEC v. Antar*](case-law/sec-v-antar.md) (disgorgement reaches both profits
  made and losses avoided).
- **Section 17(a) theories.** The monitor also flags SEC complaints that plead
  **Securities Act § 17(a)** (including negligence-based **§ 17(a)(2)/(3)**
  theories), which lower the scienter bar relative to Exchange Act
  § 10(b)/Rule 10b-5 and are increasingly used in insider-trading and
  fraud matters.

## Daily monitor

A GitHub Actions workflow
([`.github/workflows/abcf-daily-monitor.yml`](../.github/workflows/abcf-daily-monitor.yml))
runs every day at **04:00 UTC (08:00 Gulf Standard Time)** and executes
[`scripts/abcf_monitor.py`](../scripts/abcf_monitor.py). It:

1. pulls the last 24h from the **Federal Register API** (SEC, DOJ, FinCEN, OFAC),
   **SEC** press-release and litigation-release RSS, the **DOJ Fraud
   Section / FCPA** page, **UK SFO** news, and the law-firm feeds in
   [`sources/feeds.yml`](sources/feeds.yml);
2. triages each item through a **configurable LLM provider** (default: Groq's
   free tier, at zero cost) — classifying it as **anti-bribery/corruption**,
   **insider trading**, or **fraud/other**; scoring energy- and AI-sector
   relevance; summarizing it in three bullets with a citation link; flagging
   **extraterritorial reach** or a **UAE/GCC nexus**; tagging insider-trading
   items **gain-seeking** vs **loss-avoidance**; and noting any **§ 17(a)**
   theory in an SEC complaint;
3. writes a dated digest to [`digests/`](digests/); and
4. opens a GitHub issue labeled **`abcf-alert`** for any high-relevance item.

A **keyword pre-filter** (the `terms:` list in [`sources/feeds.yml`](sources/feeds.yml))
gates the LLM: only matched items are sent to the model, in batches, so free-tier
quotas last. Every item also gets a **keyword-only baseline** classification, so a
digest is produced even with no model at all.

## Running for free

The monitor is **zero-cost by default**. Pick a provider with the `LLM_PROVIDER`
env var in the workflow's `env:` block
([`.github/workflows/abcf-daily-monitor.yml`](../.github/workflows/abcf-daily-monitor.yml)),
or override a single run via **Run workflow → provider** (workflow_dispatch input).

| `LLM_PROVIDER` | Backend / model | Secret needed | Free-tier notes |
|---|---|---|---|
| **`groq`** (default) | `llama-3.3-70b-versatile` via the OpenAI SDK | **`GROQ_API_KEY`** (free — [console.groq.com](https://console.groq.com)) | Groq free tier: generous per-minute/day request + token limits. |
| `gemini` | Google `gemini-1.5-flash` (`google-generativeai`) | **`GEMINI_API_KEY`** (free — [aistudio.google.com](https://aistudio.google.com)) | Google AI Studio free tier (~15 req/min, ~1,500 req/day at time of writing). |
| `github` | GitHub Models — `openai/gpt-4o-mini` via the OpenAI SDK | None (built-in `GITHUB_TOKEN`, `permissions: models: read`) | ⚠️ **Being retired by GitHub** — returns HTTP 410. Kept selectable but no longer usable for LLM triage. |
| `anthropic` | Claude (`ANTHROPIC_MODEL`, default `claude-sonnet-5`) | **`ANTHROPIC_API_KEY`** | **Paid** — requires Console credits/billing. Kept for later. |
| `none` | — (keyword-only) | None | Always free; rule-based classification only, no LLM. |

**How to switch:** edit `LLM_PROVIDER` in the workflow `env:` block (or set an
`LLM_PROVIDER` **Actions variable**, or use the manual-run input). For `groq` /
`gemini` / `anthropic`, add the corresponding **repository secret** under
Settings → Secrets and variables → **Actions**. `none` needs **no secret at all**.

**Verify a provider works:** run the workflow manually with **selftest = true**
(and the provider of your choice) — it classifies built-in fixtures through the
provider and logs whether each was handled by the model (`method: llm`) or the
keyword fallback, without writing a digest.

**Quota safety:** the monitor caps each item's input (title + first 800 chars +
link), batches up to 10 items per request, and on an **HTTP 429 / quota error**
logs it and falls back to keyword-only classification for the rest of the run —
it never fails the workflow. Free-tier limits change over time; check each
provider's current limits if runs start getting throttled.
