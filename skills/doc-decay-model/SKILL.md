---
name: doc-decay-model
description: "Predict which articles will go stale next, before they do. Scores every article by version age, source-ticket churn, how many releases touched its feature, and support-ticket velocity against it, producing a \"these will rot first\" watchlist for proactive maintenance."
user_invocable: true
---

# Doc Decay Model

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Predict which articles will go stale next, before they do. Scores every article by version age, source-ticket churn, how many releases touched its feature, and support-ticket velocity against it, producing a "these will rot first" watchlist for proactive maintenance.

## When to use this

Periodically (a good scheduled-job candidate), or when planning a maintenance sprint. This predicts future rot. It does not find already-broken articles; that is a different pass.

## Inputs

Optional scope (version, category). Default: every published article in the corpus at `docs.corpus_root`.

## What To Do

1. **Gather published articles and metadata.** For each: title, slug, category path, last-modified timestamp, and the source ticket named in the article's own metadata (`fields.source_ticket`).

2. **Classify the article's category first.** Categories listed in `docs.archive_categories` document frozen past releases. For those, being old is **correct**, not decay. Exempt the version-age signal entirely and score them on churn, support velocity, and publish state only. Living configuration and feature articles get the full model. Do this before scoring anything, not as a filter afterward.

3. **Compute decay signals per article:**
   - **Version age:** how many releases since the documented version. Older means higher risk. SUPPRESS for archive categories per step 2.
   - **Source-ticket churn:** count of recent engineering tickets touching the same feature or epic, from `issue_tracker.dev_project`. Active development means the doc is probably already drifting.
   - **Release touch count:** how many releases have modified this feature area.
   - **Support velocity:** recent support-ticket volume mentioning the feature. High volume means the feature is either in flux or confusing, and both predict doc changes.
   - **Time since last edit:** a stale last-modified date on an actively developed feature is the clearest red flag in the model.
   - **Unpublished but churning:** a draft or unpublished article whose topic is actively changing. This is a stale draft on a moving target, and it is worse than a stale published article because nobody is looking at it. Flag it explicitly.
   - **Live but incomplete:** an article carrying an unresolved placeholder or a pending value from an open defect. Accurate today, guaranteed to change. Score it up.

4. **Score and rank.** Combine into a decay risk score. Weight active-development churn, support velocity, and unpublished-but-churning highest. Those predict imminent inaccuracy far better than age does.

5. **Produce a watchlist.** Highest risk first, with the reason each item scored high, so maintenance effort goes where rot is coming rather than where it already arrived.

6. **Do not edit.** This predicts and prioritizes. The human schedules the review.

## Output Format

```
## Doc Decay Model: [scope], [date]

### Highest risk (review soon):
| Article | Decay score | Drivers |
|---|---|---|
| [slug] | 8.5 | 8 releases behind, 4 active dev tickets, 11 support mentions |

### Watchlist (monitor): ...
### Stable: N articles low risk.
### Archive categories excluded from age scoring: [list]
```

## Notes
- Predictive, not diagnostic. This tells you what is about to break, not what is already broken.
- Churn and support velocity beat raw age. A four-year-old stable article may be perfectly fine, while a three-month-old one under active development is already rotting.
- The scores are heuristics. The **ranking** is the output; the absolute numbers are not meaningful and should not be quoted as if they were.
- **Archive categories: age is not decay.** An old release note is supposed to be old. This rule exists because naive age-weighting once buried the two articles that actually mattered under six frozen historical notes that scored higher purely for being older. If your top of watchlist is all archive content, step 2 did not run.
