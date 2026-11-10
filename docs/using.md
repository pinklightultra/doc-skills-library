# Using the skills

Back to the [skill list](../README.md).

The [README](../README.md) quotes the first sentence of each description. What follows is the rest of the rule: severity, gates, and the order to run them.

Invoke a skill by typing its name: `/leak-scan`, `/audit-docs-coverage`, `/kb-health-sweep`. The file is `skills/<name>/SKILL.md`. You can also follow that file as a checklist with no agent in the loop. The slash command is the shortcut.

**Pre-publish gates.** Run before anything reaches a customer.

| Skill | What it does |
|---|---|
| `/leak-scan` | Sweeps seven leak classes: credentials, internal infrastructure, repo and code detail, employee names, customer names, ticket internals, leaky screenshots. Case-insensitive, confirms every hit in context. Critical is a publish blocker. A real secret also needs rotation, because deleting the text does not un-publish the value. |
| `/steelman-this-note` | Reads a draft as a motivated customer looking for an advantage: availability overclaims, implied commitments, scope creep, contractual tone. Quotes the sentence, names the misread, offers a safer rewrite. High means hold for product and legal review. |
| `/redline` | Contract-grade read for warranty words, SLA-like statements, absolute quantifiers, and compliance assertions. Rates exposure High, Medium, or Low. High means hold for legal and product review. The skill proposes the rewrite and leaves the softening to that review. |
| `/bumpkin-test` | Reads as a competent outsider and tables every acronym, code name, and assumed prerequisite with a plain-language fix. Commits to a yes, mostly, or no verdict. |
| `/who-needs-to-know` | Maps a shipped change to the customers and teams actually affected. Emits two labelled drafts, INTERNAL and PUBLISHABLE. Never sends. |

**Corpus health.** Read-only analysis over the knowledge base.

| Skill | What it does |
|---|---|
| `/audit-docs-coverage` | Finds stubs, duplicate artifacts, empty categories, and absent topics, then joins the gap list to support-ticket volume for priority. Carries five hard preconditions against nested-count, stale-export, title-shape, status-code, and zero-length-fetch miscounts. |
| `/doc-decay-model` | Scores articles for predicted future staleness from version age, source-ticket churn, release touches, support velocity, and edit recency. Archive categories are exempt from the age signal. Produces a watchlist and edits nothing. The ranking is the result. The numeric score is a heuristic. |
| `/kb-health-sweep` | The scheduled umbrella. Index-freshness preflight, then safety gates, then corpus health, then the amnesia check on the slower cadence. Skips an unavailable backend and names the skip. One deduplicated list, led by the diff against the previous run. |
| `/institutional-amnesia-check` | Re-reads past incidents and verifies each defense still exists and still runs: the rule is still in the skill, the job is still firing, the gate was not quietly widened. Reports lapsed defenses against verified-active ones. |
| `/audience-lens` | Reads one article three times, as end user, implementer, and internal support. Rates each served-well, buried, or missing, and checks whether a proposed split is access-enforceable or only organizational. |

**Drafting method.** How to produce something you can defend.

| Skill | What it does |
|---|---|
| `/source-backed-rfp` | Evidence-first drafting for RFP answers and security questionnaires. Splits a compound question into atomic capabilities, reads the full article rather than the search snippet, cites title plus reader URL, and labels each row DIRECT, PARTIAL, NO KB SOURCE, or NOT VERIFIED (NO ACCESS). Does not infer support from architecture or an adjacent module. |
| `/counterfactual-doc` | Writes the inverted "how it breaks" note first, cross-checks that failure list against support tickets, then turns the survivors into prerequisites, limitations, and troubleshooting. |
| `/house-style` | A prose ruleset: no em dashes, no filler openers, no closing summaries, step plus result for instructions, a short substitution table. Runs as a rewrite or as a check-only lint. It is a voice pass, not a persona and not a fact check. |
| `/objection-forecast` | Predicts the pushback a release will draw from per-component support history, and flags any answer that would create a commitment if someone improvised it in the room. An empty ticket search is reported as no signal. |
| `/stop-and-reference` | The one skill written to be invoked unprompted, mid-task, by the model itself. When a setting, screen, field, or navigation path cannot be cited, it looks up the literal string, reads the top article, and on no hit refuses both to fabricate a value and to leave a `[CONFIRM]` placeholder. There is no separate trigger in this repo. The stop is a rule in the file. |

**Calibration and craft.** Aimed at the writer, as well as the document.

| Skill | What it does |
|---|---|
| `/doc-turing-test` | Mixes one fabricated but style-consistent release note into real ones, unlabeled, and asks you to find it. Then names the verification step that would have caught it. |
| `/teach-me-back` | Assembles ground truth, quizzes you in three escalating levels on a subsystem, grades the answers against real sources, and returns a solid, shaky, and fill-from list to close before writing. |
| `/rubber-duck` | Asks one question at a time and refuses to answer for you until you have done real work. Offers to switch to solve mode only with permission. |
| `/postmortem` | Incident writeup: timeline, root cause separated from symptom, containment separated from the permanent fix, and the named standing defense. Its last step folds the lesson into the skill that let the incident through. |
| `/skill-forge` | Mines work logs for repeated manual sequences, ranks candidates by frequency times effort times error risk, and drafts a new `SKILL.md` in this library's contract. Writes to disk only on approval. |
| `/verify-loop` | Retrofits a codebase's tests to verify-then-discard: run the suite for real before believing it, remove shared fixtures, replace decorative assertions, keep error listeners on. The one skill here that is not about documentation. It stays because the rest of the library depends on that discipline. |

## A pre-publish pass

On a draft, in this order:

1. `/leak-scan`. Critical means do not publish. A live secret means rotate it, then remove it from the draft.
2. `/steelman-this-note`. Read the High items as sentences a customer could quote back.
3. `/redline`. High means hold for legal and product review.
4. `/bumpkin-test`. Yes, mostly, or no: would a competent outsider finish the task.
5. `/house-style`, ask for a check if you want the lint and will do the rewrite yourself.
6. `/stop-and-reference`, the moment a setting, screen, field, or path is coming from memory.

`/who-needs-to-know` belongs after the change has shipped, when you are deciding who hears about it. It drafts. A person sends.

## A corpus pass

`/kb-health-sweep` is the standing battery: index freshness, then `/leak-scan`, `/steelman-this-note`, and `/redline`, then `/doc-decay-model` and `/audit-docs-coverage`, then `/institutional-amnesia-check` on the slower cadence. Pass the date in the prompt. The runtime cannot read the clock.

The report is written under `reports.output_dir` (default `./reports/kb-health`). That directory is gitignored. A real sweep contains article titles, ticket volume, and sometimes account context, and none of that belongs in this repo.

Run `/audit-docs-coverage` or `/doc-decay-model` alone when you want one question rather than the whole battery. State the denominator. "14 gaps" is not a finding. "14 gaps across the corpus" is.

## How to read a result

Treat the output as a draft you still have to check. Act on the verdict line: `BLOCKED`, `hold for legal review`, `HARD STOP`. A decay score is a sort key. `/doc-decay-model` says so in its own notes: quote the ranking, not the absolute number. For an RFP matrix, the useful line is the count by status. `/source-backed-rfp` treats that count as the deliverable, because a sheet that is mostly DIRECT is a different document from one that is mostly PARTIAL, and the person signing it needs the split.
