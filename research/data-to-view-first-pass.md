# Data-to-view first pass (post-v0.1.1 research note)

This note is separate from the v0.1.1 baseline interpretation experiment. It records a product workflow observation, not a validated H-AI-R effect or a human usefulness score.

## Hypothesis and disproof

When a job question is tied to source-defined measures and completeness, a data specialist and workflow specialist can establish meaning before a visual specialist chooses a view. The resulting interface should make missing data and the next inspection action clearer without changing source-of-truth values. This hypothesis would be weakened if the view still hides material gaps, displays unsupported totals, fails to refresh after source changes, or makes it harder for a person to find the answer.

## Implementation under test

The Astra H-A-I-R runtime now accepts a typed data-to-view handoff after acknowledged data and workflow meaning messages. The handoff references measures rather than copying values, records source, date, completeness, decision, presentation rationale, and missing-data treatment, and requires independent data and rendered-UI reviews. A failed review opens a repair finding. This contract makes assumptions inspectable; it does not validate the underlying data or confer authority to edit records.

The first product path is a job P&L workspace backed by existing versioned source lines and editable documented forecast inputs. The revised view recommends a table when actual economics are incomplete and a chart for a complete dated comparison. Operators can override the view, inspect source categories, expand reconciliation detail, and edit documented forecast inputs. Missing amounts stay distinct from known zero.

## Controlled observation

The current and revised interfaces were run against the same isolated copy of a job dataset. For an incomplete job with dated lines:

| Check | Current interface | Revised interface |
| --- | --- | --- |
| Default daily presentation | Chart with a numeric margin despite incomplete actuals | Table with an explicit incomplete margin state |
| View choice | No chart/table control | Recommended, chart, and table controls |
| Dominant amount label | “Actual to date” | “Known-line difference · incomplete” |
| Posted-cost source filter | Also included forecast assumptions | Only posted direct-cost categories |
| All-evidence filter | Omitted ticket forecast lines | Included ticket forecast lines |
| Forecast-assumption group | Added unlike revenue and cost measures into one total | Kept measures separate |
| Reconciliation detail | Always expanded | User-expandable disclosure |

A versioned source update in the isolated database changed the displayed value after refresh. An isolated forecast form submission persisted an explicit zero, a source reference, and a new source version. Desktop, tablet, and mobile browser checks found no page overflow or page errors in the changed Jobs views; independent scoped data and visual reviews passed after repairs. The mobile review specifically checked that forecast, known cost, and incomplete state remain visible together.

The complete-data recommended chart was checked with a **synthetic response fixture only**. The isolated dataset had no complete two-date job, so a real-data complete-chart result is **NOT_RUN**. Human answer-finding quality and time, model cost, and generalization across other products are **NOT_MEASURED**. Two independent review rounds exposed and repaired source-grouping and mobile readability defects; that is implementation repair evidence, not a comparative repair-cycle result. One automated navigation timing per condition was retained privately as a diagnostic and is too noisy to support a speed claim.

## Next falsifiable run

Use a source-supported complete job and a blinded human task to compare whether someone can find the answer and next action in each condition. Record initial quality, corrections, elapsed human task time, and actual model/tool cost for both conditions. Keep failures and the uncorrected first result. Until then, this pass establishes working plumbing and identifies a concrete incomplete-data improvement; it does not establish a benchmark advantage for H-AI-R.
