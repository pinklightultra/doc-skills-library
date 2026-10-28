# doc-skills-library

Claude Code skills that audit, score, and lint enterprise documentation.

For technical writers and docs engineers who publish into a large knowledge base and need the review to happen the same way every time: the same pre-publish gates, the same corpus scores, and a report stable enough to diff next week against this week.

Twenty-one skills. Each one is a `SKILL.md` that Claude Code loads when you invoke it by name (`/leak-scan`). They are procedures written as prompts. [`check.py`](check.py) checks that the files on disk match the structural claims in this README.

## The problem

I write and maintain documentation for a knowledge base of roughly 1,900 articles. The work has a recurring shape: the same review, the same audit, the same checks before publishing, done by hand, slightly differently each time, and occasionally skipped on the day it mattered.

Most of these skills exist because something went wrong once. `/leak-scan` was written after an engineering ticket pasted into a draft turned out to contain an encrypted application secret, three internal URLs, and a customer name. `/institutional-amnesia-check` exists because a defense put in place after an incident quietly stopped running and nobody noticed for months. The failure history sits in the skill body as a rule, because a rule survives being skim-read.

The incident that taught the library to separate an accurate engineering note from an available product is written up in [references/incident-ga-overclaim.md](references/incident-ga-overclaim.md). A release note described an internal database upgrade in the present tense. It was true about the engineering. It was false about availability. It sat on the customer-visible knowledge base for months, and a customer arrived at a review ready to implement it.

The library is a subset. The full set is 61 skills. These 21 are the ones whose logic is about documentation, rather than about one organization's tooling.

## The approach

Four decisions shape every skill.

**Read-only until a human asks for a write.** Audits and reviews do not edit, publish, or reorganize. When a write is requested, it follows four beats: dry run, show the diff, confirm, verify the live result. A write that returned HTTP 200 is not a write you have seen.

**One guardrail file, linked rather than copied.** All 21 skills point at [GUARDRAILS.md](GUARDRAILS.md). In the source library, 55 of 61 skills carried their own copy, and the copies had drifted: of the 56 skills with a guardrails block, exactly one pair was identical. `check.py` fails if a skill drops the link or if the relative path does not resolve.

**Uncertainty gets its own label.** A missing backend, a 404, and a clean search are different outcomes. Skills finish the rest of the sweep and name the skip. A 404 or an auth failure is `NOT VERIFIED (NO ACCESS)`. A search that ran and found nothing is a different label: `NO KB SOURCE`, or "no signal" on the axis you queried. Neither is a clean bill of health. If a lookup for a setting, field, or path finds nothing, the skill stops. It does not emit a `[CONFIRM]` placeholder and continue. Placeholders get published.

**The report is a template, so the next run can be diffed.** Most skills end with a fenced block of `[bracketed]` slots. `/kb-health-sweep` depends on that shape. It runs the safety and corpus skills, merges them into one prioritized list, and leads with the delta against the previous report. Paths, hostnames, project keys, and field ids stay in `config.yml`, copied from [config.example.yml](config.example.yml). A skill body that bakes in a tenant value works in exactly one place.

## What you get

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

## How to use it

Claude Code is the terminal agent that loads a skill when you type `/name`. You also need a checkout of this repo. You do not need to edit the skills to run them. You do need to point them at your corpus before the audit skills have anything to read.

The files stand alone as procedures. Open `skills/<name>/SKILL.md` and follow the steps in the file. The severity labels and the report template are part of the skill. The slash command is one way to run them.

### Install

Skills live in a `skills/` directory Claude Code reads. Copy the ones you want, and copy the shared guardrails file and the `references/` directory with them:

```bash
git clone https://github.com/pinklightultra/doc-skills-library
cd doc-skills-library
mkdir -p ~/.claude/skills             # cp fails, or silently mis-copies, without this
cp -r skills/leak-scan ~/.claude/skills/
cp GUARDRAILS.md ~/.claude/           # every skill links ../../GUARDRAILS.md
cp -r references ~/.claude/           # cited by 9 of the 21
```

To install the set, replace the single-skill copy with `cp -r skills/* ~/.claude/skills/`. Pulling this repo later does not update `~/.claude`. Copy again after an update.

The `mkdir` is required. If `~/.claude/skills/` does not exist, `cp -r` either fails outright or, when `~/.claude/` exists and `skills/` does not, exits 0 and copies the *contents* of the skill directory to `~/.claude/skills/SKILL.md`. The skill is then uninstalled, with no error and no directory named after it.

Do not skip the last two copies. All 21 skills inherit their safety rules by linking `../../GUARDRAILS.md` rather than restating them. From `~/.claude/skills/leak-scan/` that path resolves to `~/.claude/GUARDRAILS.md`. A missing file leaves a dangling link: nothing errors, and the skill runs without the five rules, including the two that keep it read-only. `GUARDRAILS.md` and `references/` sit one level above `skills/`, beside it. `~/.claude/skills/GUARDRAILS.md` is the wrong place, and it is wrong silently.

The same shape applies wherever you install. The skill file has to land at `<root>/skills/<name>/SKILL.md`, with `GUARDRAILS.md` and `references/` at `<root>/`. For the commands above, `<root>` is `~/.claude`.

### Configure

```bash
cp config.example.yml config.yml   # config.yml is gitignored
```

Fill in `config.yml` before running a corpus skill. Skills reference config keys by name. An unconfigured library stops and tells you, or it produces a report full of gaps. It will not invent the values.

The keys a documentation set actually needs on day one:

- `docs.corpus_root`: a local checkout or an export of the knowledge base.
- `docs.search_command`: literal search. The default is `grep`, because it is present everywhere.
- `docs.reader_url_template`: the URL a reader would open, so citations are not authoring links.
- `docs.audience_model` and `docs.audience_field`: how this stack decides who can read an article. Set this wrong and `/audience-lens` will recommend a control you do not have. See [The audience-gating problem](#the-audience-gating-problem).
- `issue_tracker`: base URL, project keys, and the support-volume query, if you want gap lists ordered by what readers already asked.

`config.example.yml` comments every key. Two of those comments point at sections below: literal search under [What is missing](#what-is-missing), and audience under [The audience-gating problem](#the-audience-gating-problem).

### A pre-publish pass

On a draft, in this order:

1. `/leak-scan`. Critical means do not publish. A live secret means rotate it, then remove it from the draft.
2. `/steelman-this-note`. Read the High items as sentences a customer could quote back.
3. `/redline`. High means hold for legal and product review.
4. `/bumpkin-test`. Yes, mostly, or no: would a competent outsider finish the task.
5. `/house-style`, ask for a check if you want the lint and will do the rewrite yourself.
6. `/stop-and-reference`, the moment a setting, screen, field, or path is coming from memory.

`/who-needs-to-know` belongs after the change has shipped, when you are deciding who hears about it. It drafts. A person sends.

### A corpus pass

`/kb-health-sweep` is the standing battery: index freshness, then `/leak-scan`, `/steelman-this-note`, and `/redline`, then `/doc-decay-model` and `/audit-docs-coverage`, then `/institutional-amnesia-check` on the slower cadence. Pass the date in the prompt. The runtime cannot read the clock.

The report is written under `reports.output_dir` (default `./reports/kb-health`). That directory is gitignored. A real sweep contains article titles, ticket volume, and sometimes account context, and none of that belongs in this repo.

Run `/audit-docs-coverage` or `/doc-decay-model` alone when you want one question rather than the whole battery. State the denominator. "14 gaps" is not a finding. "14 gaps across the corpus" is.

### How to read a result

Treat the output as a draft you still have to check. Act on the verdict line: `BLOCKED`, `hold for legal review`, `HARD STOP`. A decay score is a sort key. `/doc-decay-model` says so in its own notes: quote the ranking, not the absolute number. For an RFP matrix, the useful line is the count by status. `/source-backed-rfp` treats that count as the deliverable, because a sheet that is mostly DIRECT is a different document from one that is mostly PARTIAL, and the person signing it needs the split.

## Proof

### Structural check

```bash
python check.py      # standard library only, exits non-zero on any failure
```

Seven checks. Each one is a claim this README makes. The counts below are what the script prints on this tree, not figures typed from memory:

1. **Links resolve.** 26 markdown files, 47 local links, 0 dangling. File targets must exist. An `#anchor` must match a real heading in the target file under GitHub's slug rules.
2. **Frontmatter parses.** All 21 `SKILL.md` files carry exactly `name`, `description`, `user_invocable`, in that order, with `name` equal to the directory name and `user_invocable` set to `true`. The parser is hand-rolled, so the check has no dependencies.
3. **The skill table is complete.** 21 skill directories, 21 table rows, names matching. A skill with no row, or a row with no skill, fails.
4. **Guardrails are inherited, not copied.** All 21 skills link `../../GUARDRAILS.md`, and that relative path resolves from each skill's own location. This is the check that catches the install mistake above.
5. **The section contract holds, with three named exceptions.** The contract is read out of `/skill-forge` rather than restated in the script: `## When to use this`, `## Inputs`, `## What To Do`, `## Output Format`, `## Notes`. The machine-readable output block is a closed fence with `[bracketed]` slots, which is what an umbrella skill needs in order to diff a child. Both exception sets are cross-checked against the Limitations list, so the script and this README cannot drift apart on their own.
6. **No em dashes.** Exactly one exists in the repo, the counter-example inside the `/house-style` rule that forbids them. One anywhere else fails, and so does removing that one. Smart quotes fail anywhere.
7. **No secrets or tenant identifiers.** Deliberately narrow: assigned credential values, JWTs, AWS key ids, PEM private-key headers, internal ticket keys, tenant hostnames, and absolute local paths. The repo is full of the words "secret", "token", and "password" because several skills are about leak scanning. Every pattern therefore requires structure a sentence does not have. **The scan skips `check.py` itself**, because the patterns would otherwise report themselves. That file is the only place an identifier can sit while the check still prints PASS. Three real ticket keys were hardcoded there once, inside the check that hunts for ticket keys, and check 7 passed the whole time. They are configuration now. Passing check 7 is not a human read. `/leak-scan` exists because that read is still required.

What `check.py` cannot do is tell you whether any skill produces good output. It verifies that the library is structurally sound: the files are well-formed, the cross-references resolve, and this README describes what is on disk.

### Continuous integration

Two workflows run that same script on push, pull request, and manual dispatch to `main` and `master`.

- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) is the cross-platform run: ubuntu, windows, and macos, each on Python 3.10, 3.11, and 3.12.
- [`.github/workflows/check.yml`](.github/workflows/check.yml) is a single Ubuntu job on Python 3.11.

There is no behavioral test suite. The workflows show that a clean runner still agrees with this README. They do not show that a model followed a skill.

### Report shape

Filled-in sweep reports are not in the repo. `reports/` is gitignored on purpose. What is in the repo is the template each skill fills. This is the `## Output Format` block from [`skills/leak-scan/SKILL.md`](skills/leak-scan/SKILL.md#output-format), slots included:

```
## Leak Scan: [target], [date]

### CRITICAL (do not publish):
- [exact text]: [secret/PHI], REMOVE + [rotate if real]

### HIGH / MEDIUM:
- [exact text]: [class], [scrub to: ...]

Verdict: [clear to publish / BLOCKED on N critical items]
```

The same pattern, with different slots, is the output section of the skills `/kb-health-sweep` aggregates. Three skills do not use a fenced template. They are named under Limitations.

## Why this matters for tech writing

A documentation set of this size is a pipeline. The failure worth designing for is a gate that ran last month and did not run this month, a count that looked clean because the export was stale, or a sentence that was true about the engineering and false about availability. These skills make that pipeline explicit: the same checks, the same severity labels, the same report slots, and a diff against the previous run so a regression is the first line of the report.

That is the part of the work that can be made consistent, and the part that can be compared across articles and across weeks, without inventing a quality score nobody collected. Coverage priority joined to ticket volume, a decay ranking, and an RFP counted out as DIRECT, PARTIAL, NO KB SOURCE, and NOT VERIFIED are the comparisons the skills actually emit. `check.py` measures a narrower thing, and measures it for real: whether this library still matches its own contract. There is no study here of whether the skills produce better documentation than doing the work without them. Each skill encodes a mistake that already happened. That is the claim the files support.

## Configuration

Two notes worth reading before you trust a result.

The default `search_command` is `grep`, not `rg`. ripgrep is faster and worth switching to if you have it, but verify it first. A missing binary does not fail loudly here: the shell writes "command not found" to stderr, the skill reads an empty result set, and an empty result set looks exactly like a clean corpus. That is the failure mode `GUARDRAILS.md` calls "absence of evidence is not evidence of absence." This library used to ship the `rg` default that causes it.

Field *names* are configured rather than field ids, because hosted trackers expose custom fields under opaque per-instance ids. A skill body carrying `customfield_10142` works in exactly one place. That id is invented for the example. Yours will differ, and nothing in a skill should be carrying it.

## What is missing

The search this library assumes is literal text search. It finds names, not topics. Ask which articles discuss authentication and it will find the ones containing the string "authentication", which is neither the same set nor a superset. Articles that cover the concept in other words are invisible to it.

That gap has consequences the reports cannot fully caveat:

- **Coverage audits undercount.** `/audit-docs-coverage` finds a topic absent when no article names it. An article covering it in different terms reads as a gap.
- **Duplicate detection is weak.** Two articles documenting the same procedure with different vocabulary do not look like duplicates.
- **`/leak-scan` is the exception, and literal matching is what it needs.** Leak scanning looks for a specific hostname, a specific customer name, a specific key shape. Semantic similarity would add false positives to the one skill that must not have them.

`semantic_search_command` exists in the config for this reason and ships empty. It is a component you supply. Skills that would benefit degrade to literal search and say so in their report.

Also missing: an evaluation of whether these skills produce better documentation than working without them.

## The audience-gating problem

`docs.audience_model` has two values, and they are not interchangeable. Which one your stack uses decides whether "internal only" is a fact or a hope.

**`reader_group`.** The backend enforces per-audience read access at request time. An article outside a reader's group is not served to them. Splitting content by audience is a real control.

**`frontmatter`.** Audience is a field on the article, honored by the build. Two build targets read the field and emit two sites. This holds until the field is wrong, the build target is misconfigured, a page is published outside the pipeline, or someone reads the source repository. There is no request-time check.

The natural fix for a mixed-audience article is to split it into an internal one and an external one. Under `frontmatter` that split is organizational. The document gets better. The exposure stays the same.

`/audience-lens` asks the question rather than assuming the answer. It reports whether a recommended split is access-enforceable on your stack or only a reorganization, and under `frontmatter` it says so. Set the key to the model you actually run. Setting it to `reader_group` because that is the model you want produces confident advice that is wrong in the direction that costs you.

## Guardrails

Five rules, three error-handling idioms, and a four-beat write ritual live once in [GUARDRAILS.md](GUARDRAILS.md). Every skill points at that file.

The five rules: default audits to read-only; gate every write behind a shown diff and a confirmation; parse JSON and HTML with a real parser; never expose credentials, tokens, customer names, PII, or PHI; resolve current paths from `config.yml` instead of trusting a path baked into a skill.

The three idioms matter more than any step list. **Degrade rather than fail**: run the rest of the sweep and record the skip. **Absence of evidence is not evidence of absence**: a 404 and a clean result get different labels. **Hard stop over a confident guess**: no `[CONFIRM]` placeholders.

Three reference files carry incident detail the skills cite: [incident-ga-overclaim.md](references/incident-ga-overclaim.md), [no-client-names.md](references/no-client-names.md), [pii-redaction.md](references/pii-redaction.md). Nine of the 21 skills link at least one of them.

## Limitations

- **These are prompts.** `python check.py` is the only test here, and it is a structural check. It covers the seven properties listed under Proof: links, frontmatter, the skill table, the guardrails pointer, the section contract, the em-dash rule, and a narrow secret scan. It exits non-zero and names what broke. A skill can pass all seven and still be ignored, misread, or applied to the wrong input. Treat every output as a draft to check, particularly the ones that produce confident tables.
- **No evaluation.** No A/B test, no measured error rate on the writing itself.
- **A model still does the work.** Every skill inherits the underlying model's failure modes, including plausible fabrication. Several skills are built to fight that.
- **Backend-shaped.** The library assumes a documentation corpus you can search locally and an issue tracker with per-component history. With neither configured, roughly half of these do nothing useful, and the ones written for that case will say so.
- **Three of the 21 do not follow the section contract** that `/skill-forge` declares: `house-style`, `verify-loop`, and `source-backed-rfp` have their own structure. `verify-loop` is also the one skill here that is not about documentation.
- **Not every skill has a machine-readable output block.** `/rubber-duck` is conversational by design, and `/house-style` and `/source-backed-rfp` use prose and a plain table. Anything you build that expects a fenced, bracketed template from every skill will miss those three.
- **The leak classes and the review dimensions come from one corpus** and one organization's incidents. They are a starting point for a similar knowledge base, not a standard.

## Background

Built while running documentation for a healthcare SaaS platform: a knowledge base of about 1,900 articles, release notes on a fortnightly cycle, and a customer-facing portal where a mistake is visible to the people who pay for the product. The incident references are real incidents, genericized.

## License

MIT. See [LICENSE](LICENSE).
