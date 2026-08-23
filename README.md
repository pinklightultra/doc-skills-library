# doc-skills-library

Twenty-one Claude Code skills for working on a large documentation corpus: auditing it,
reviewing drafts before they go to customers, and catching the specific ways documentation
work goes wrong.

These are prompts, not programs. Each skill is a `SKILL.md` file that gets loaded when you
invoke it. No skill here executes, and that shapes what the rest of this README can honestly
claim: `check.py` verifies the files, not the behaviour.

## Why this exists

I write and maintain documentation for a knowledge base of roughly 1,900 articles.
The work has a recurring shape: the same review, the same audit, the same five checks before
publishing, done by hand, slightly differently each time, and occasionally skipped on the
day it mattered.

Most of these skills exist because something went wrong once. `/leak-scan` was written after
an engineering ticket pasted into a draft turned out to contain an encrypted application
secret, three internal URLs and a customer name. `/institutional-amnesia-check` exists
because a defense put in place after an incident quietly stopped running and nobody noticed
for months. The failure history is in the skill bodies deliberately, encoded as a rule rather
than a warning, because a rule survives being skim-read.

The library is a subset. The full set is 61 skills; these 21 are the ones whose logic is
about documentation rather than about one organization's tooling.

## Install

Skills live in a `skills/` directory that Claude Code reads. Copy the ones you want, and copy
the two shared files with them:

```bash
git clone https://github.com/pinklightultra/doc-skills-library
cd doc-skills-library
mkdir -p ~/.claude/skills             # cp fails, or silently mis-copies, without this
cp -r skills/leak-scan ~/.claude/skills/
cp GUARDRAILS.md ~/.claude/           # every skill links ../../GUARDRAILS.md
cp -r references ~/.claude/           # cited by 9 of the 21
```

The `mkdir` is not decoration. If `~/.claude/skills/` does not exist, `cp -r` either fails
outright or, when `~/.claude/` exists but `skills/` does not, exits 0 and copies the *contents*
of the skill directory to `~/.claude/skills/SKILL.md`. That leaves the skill uninstalled, with
no error and no directory named after it.

Do not skip the last two lines. All 21 skills inherit their safety rules by linking
`../../GUARDRAILS.md` rather than restating them, and from `~/.claude/skills/leak-scan/` that
path resolves to `~/.claude/GUARDRAILS.md`. If the file is not there the link simply dangles:
nothing errors, and the skill runs without the five rules, two of which are the ones that keep
it read-only. Note where the two shared paths land: one level *above* `skills/`, next to it
rather than inside it. `GUARDRAILS.md` at `~/.claude/skills/` is the wrong place, and it is
wrong silently.

Then configure:

```bash
cp config.example.yml config.yml   # config.yml is gitignored
```

Fill in `config.yml` before running anything. Skills reference config keys by name instead of
hardcoding paths, tracker projects or field names, so an unconfigured library will either
stop and tell you or produce a report full of gaps. It will not invent the values.

Invoke a skill by name: `/leak-scan`, `/audit-docs-coverage`, `/kb-health-sweep`.

## The skills

**Pre-publish gates.** Run before anything reaches a customer.

| Skill | What it does |
|---|---|
| `/leak-scan` | Sweeps seven leak classes: credentials, internal infrastructure, repo and code detail, employee names, customer names, ticket internals, leaky screenshots. Case-insensitive, confirms every hit in context, and Critical is an unambiguous publish blocker that also demands secret rotation. |
| `/steelman-this-note` | Reads a draft as a motivated customer looking for an advantage: availability overclaims, implied commitments, scope creep, contractual tone. Quotes the sentence, names the misread, offers a safer rewrite. |
| `/redline` | Contract-grade read for warranty words, SLA-like statements, absolute quantifiers and compliance assertions. Rates exposure High, Medium or Low. High means hold for legal. |
| `/bumpkin-test` | Reads as a competent outsider and tables every acronym, code name and assumed prerequisite with a plain-language fix. Commits to a yes, mostly or no verdict. |
| `/who-needs-to-know` | Maps a shipped change to the customers and teams actually affected. Emits two labelled drafts, INTERNAL and PUBLISHABLE. Never sends. |

**Corpus health.** Read-only analysis over the whole knowledge base.

| Skill | What it does |
|---|---|
| `/audit-docs-coverage` | Finds stubs, duplicate artifacts, empty categories and absent topics, then joins the gap list to support-ticket volume for priority. Carries five hard preconditions against nested-count, stale-export, title-shape, status-code and zero-length-fetch miscounts. |
| `/doc-decay-model` | Scores articles for *predicted future* staleness from version age, ticket churn, release touches, support velocity and edit recency. Produces a watchlist. Edits nothing. |
| `/kb-health-sweep` | The scheduled umbrella. Index-freshness preflight, then safety gates, then corpus health, then amnesia check. Skips unavailable backends and names the skip. Synthesizes one deduplicated list instead of concatenating reports, and leads with the diff against the previous run. |
| `/institutional-amnesia-check` | Re-reads past incidents and verifies each defense still exists *and still runs*: rule still present, job still firing, gate not quietly widened. Reports lapsed against verified-active. |
| `/audience-lens` | Reads one article three times, as end user, implementer and internal support. Rates each served-well, buried or missing, and checks whether a proposed split is access-enforceable or merely organizational. |

**Drafting method.** How to produce something defensible.

| Skill | What it does |
|---|---|
| `/source-backed-rfp` | Evidence-first drafting for RFP answers and security questionnaires. Split into atomic capabilities, read the full article rather than the search snippet, cite title plus reader URL, and label each DIRECT, PARTIAL, NO KB SOURCE or NOT VERIFIED (NO ACCESS). Never infers support from architecture or adjacent modules. |
| `/counterfactual-doc` | Writes the inverted "how it breaks" note first, cross-checks the failure list against real support tickets, then converts it into prerequisites, limitations and troubleshooting. |
| `/house-style` | A prose ruleset: no em dashes, no filler openers, no closing summaries, step plus result for instructions, a phrasing substitution table. Runs as a rewrite or as a check-only lint. Not a persona and not a fact check. |
| `/objection-forecast` | Predicts the pushback a release will draw, mined from per-component support history rather than imagination, and flags answers that would create a commitment if improvised. |
| `/stop-and-reference` | The only skill designed to fire unprompted mid-task. When a setting, screen, field or nav path cannot be cited, it stops, looks up the literal string, reads the top article, and on no hit refuses both to fabricate and to emit a `[CONFIRM]` placeholder. It hands the decision back. |

**Calibration and craft.** Aimed at the writer, not the document.

| Skill | What it does |
|---|---|
| `/doc-turing-test` | Mixes one fabricated but style-consistent release note into real ones, unlabeled, and asks you to find it. Then names the verification step that would have caught it. |
| `/teach-me-back` | Assembles ground truth, quizzes you in three escalating levels on a subsystem, grades against real sources, and returns a solid, shaky and fill-from list to close before writing. |
| `/rubber-duck` | Asks one question at a time and refuses to answer for you until you have done real work. Offers to switch to solve mode only with permission. |
| `/postmortem` | Incident writeup: timeline, root cause separated from symptom, containment against permanent fix, and the named standing defense. Its last step folds the lesson into whichever skill let the incident through. |
| `/skill-forge` | Mines work logs for repeated manual sequences, ranks candidates by frequency times effort times error risk, and drafts a new `SKILL.md` in this library's contract. Writes to disk only on approval. |
| `/verify-loop` | Retrofits a codebase's tests to verify-then-discard: run the suite for real before believing it, kill shared fixtures, replace decorative assertions, always-on error listeners. The one non-documentation skill here, kept because it is the discipline the rest depend on. |

## Configuration

`config.example.yml` is commented key by key. The blocks are `docs` (corpus root, search
commands, reader URL template, audience model and audience field, status map, archive
categories),
`issue_tracker` (base URL, project keys, a volume query template), `fields` (custom field
*names*, never ids, because ids differ per instance), `index` (optional local index and its
staleness threshold), `lookup` (term resolution and a pre-publish linter) and `reports`.

Two notes worth reading before you trust a result:

The default `search_command` is `grep`, not `rg`. ripgrep is faster and worth switching to if
you have it, but verify it first. A missing binary does not fail loudly here: the shell writes
"command not found" to stderr, the skill reads an empty result set, and an empty result set
looks exactly like a clean corpus. That is the failure mode `GUARDRAILS.md` calls "absence of
evidence is not evidence of absence", and the library used to ship the version that causes it.

Field *names* are configured rather than field ids because hosted trackers expose custom
fields under opaque per-instance ids. A skill body carrying `customfield_10142` is a skill
body that works in exactly one place. That id is invented for the example, which is
the point: yours will differ, and nothing here should be carrying it.

## What is missing

The search this library assumes is literal text search. It finds names, not topics. Ask it
which articles discuss authentication and it will find the ones containing the string
"authentication", which is neither the same set nor a superset. Articles covering the concept
under different words are invisible to it.

That gap has consequences the reports cannot fully caveat:

- **Coverage audits undercount.** `/audit-docs-coverage` finds a topic absent when no article
  names it. An article covering it in different terms reads as a gap.
- **Duplicate detection is weak.** Two articles documenting the same procedure with different
  vocabulary do not look like duplicates.
- **`/leak-scan` is the exception, and it is fine.** Leak scanning wants literal matching:
  you are looking for a specific hostname, a specific customer name, a specific key shape.
  Semantic similarity would add false positives to the one skill that must not have them.

`semantic_search_command` exists in the config for this reason and ships empty. It is a
component you supply. Skills that would benefit degrade to literal search and say so in their
report rather than silently narrowing their claim.

Also missing: there is no evaluation. I cannot show you a measurement that these skills
produce better documentation than not using them. What I can show is that each one encodes a
specific mistake that has already happened, which is a weaker claim honestly stated.

## The audience-gating problem

`docs.audience_model` has two values and they are not interchangeable. Which one your stack
uses determines whether "internal only" is a fact or a hope.

**`reader_group`.** The backend enforces per-audience read access at request time. An article
outside a reader's group is not served to them. Splitting content by audience is therefore a
real control.

**`frontmatter`.** Audience is a field on the article, honored by the build. Two build targets
read the field and emit two sites. This works right up until it does not: the field is wrong,
the build target is misconfigured, a page is published outside the pipeline, or someone reads
the source repository. There is no request-time check.

This matters because the natural fix for a mixed-audience article is "split it into an
internal one and an external one", and under `frontmatter` that split is organizational
rather than enforced. It makes the document better and the exposure identical.

So `/audience-lens` asks the question rather than assuming: it reports whether a recommended
split is access-enforceable on your stack or only cosmetic, and under `frontmatter` it says so
explicitly instead of implying a control you do not have. Set this key accurately. Setting it
to `reader_group` because that is what you wish you had produces confident advice that is
wrong in the one direction that costs you.

## Guardrails

Five rules, three error-handling idioms and a four-beat write ritual live once in
[GUARDRAILS.md](GUARDRAILS.md) and every skill points at it. In the library this came from,
55 of 61 skills carried their own copy of those five rules, and the copies had already
drifted apart: of the 56 skills with a guardrails block, exactly one pair was identical and
the other 54 were each a little different. So the cost was never just 55 edits. It was 55
edits plus deciding which wording was the real one.

The three idioms matter more than any step list: **degrade rather than fail** (run the rest
of the sweep, record the skip), **absence of evidence is not evidence of absence** (a 404 and
a clean result get different labels), and **hard stop over confident guess** (no `[CONFIRM]`
placeholders, because placeholders get published).

Three reference files in `references/` carry incident detail the skills cite:
`incident-ga-overclaim.md`, `no-client-names.md`, `pii-redaction.md`.

## Checks

The structural claims in this README are not assertions. They are a script:

```bash
python check.py      # standard library only, exits non-zero on any failure
```

Seven checks, each one a claim made above. Every count below is printed by the script, not
typed here from memory:

1. **Links resolve.** Every markdown link across the 26 `.md` files: 34 local links, 0
   dangling. File targets must exist. `#anchor` targets must match a real heading in the
   target file under GitHub's slug rules.
2. **Frontmatter parses.** All 21 `SKILL.md` files carry exactly `name`, `description`,
   `user_invocable`, in that order, with `name` equal to the containing directory name and
   `user_invocable` set to `true`. Hand-parsed, so the check has no dependencies.
3. **The skill table is complete.** 21 skill directories, 21 table rows, names matching. A
   skill with no row and a row with no skill both fail.
4. **Guardrails are inherited, not copied.** All 21 skills link `../../GUARDRAILS.md`, and
   that relative path resolves from each skill's own location. This is the check that catches
   the install mistake described above.
5. **The section contract holds, with three named exceptions.** The contract is read out of
   `/skill-forge`'s own body rather than restated in the script, so rewording that skill moves
   the check with it. Same for the machine-readable output block: a closed fence with
   `[bracketed]` slots, which is the property an umbrella skill needs to diff a child's output.
   Both exception sets are cross-checked against the prose below, so the script and this README
   cannot drift apart independently.
6. **No em dashes.** Exactly one exists in the repo, the counter-example inside the
   `/house-style` rule that forbids them. One anywhere else fails, and so does removing that
   one. Smart quotes fail anywhere.
7. **No secrets or tenant identifiers.** Deliberately narrow: assigned credential values, JWTs,
   AWS key ids, PEM private-key headers, internal ticket keys, tenant hostnames, and absolute
   local paths. Several skills here are *about* leak scanning, so the repo is full of the words
   "secret", "token" and "password" in prose. Every pattern therefore requires structure a
   sentence does not have. What it cannot catch is listed in a comment in the script, and it is
   a real list: a bare pasted value with no key beside it is indistinguishable from a hash.
   **It also skips `check.py` itself**, necessarily, since every pattern would otherwise report
   itself, and that makes this one file the only place in the repo an identifier can sit while
   the check still prints PASS. Not hypothetical: three real ticket keys were hardcoded in this
   script, inside the check that hunts for ticket keys, and check 7 passed the whole time. They
   are configuration now, and the file gets read by eye. Passing check 7 is not a human read, and
   `/leak-scan` exists because that read is still required.

What `check.py` cannot do is tell you whether any of these skills produces good output. It
verifies that the library is structurally sound: the files are well-formed, the
cross-references resolve, and this README describes what is actually on disk. Behaviour is a
model's behaviour, and no file scan reaches it.

## Limitations

- **These are prompts.** `python check.py` is the only test here, and it is a structural check,
  not a test suite for behaviour. It covers the seven properties listed under "Checks" above:
  links, frontmatter, the skill table, the guardrails pointer, the section contract, the
  em-dash rule, and a narrow secret scan. Run it before publishing; it exits non-zero and names
  what broke. The part that matters is the part it cannot reach. A skill can pass all seven and
  still be ignored, misread, or applied to the wrong input. Treat every output as a draft to
  check, particularly the ones that produce confident tables.
- **No evaluation, as above.** No A/B, no measured error rate.
- **A model still does the work.** Every skill inherits the underlying model's failure modes,
  including plausible fabrication. Several skills are built specifically to fight that, which
  should tell you how reliable the default is.
- **Backend-shaped.** The library assumes a documentation corpus you can search locally and an
  issue tracker with per-component history. With neither configured, roughly half of these do
  nothing useful, and the honest ones will tell you that instead of guessing.
- **Three of the 21 do not follow the section contract** that `/skill-forge` declares:
  `house-style`, `verify-loop` and `source-backed-rfp` have their own structure.
  `verify-loop` is also the one skill here that is not about documentation.
- **Not every skill has a machine-readable output block.** `/rubber-duck` is conversational
  by design, and `/house-style` and `/source-backed-rfp` use prose and a plain table. Anything
  you build that expects a fenced, bracketed template from every skill will hit those three.
- **The taxonomy of leak classes and review dimensions is empirical**, derived from one
  corpus and one organization's incidents. It is a decent starting point, not a standard.

## Background

Built while running documentation for a healthcare SaaS platform: a knowledge base of about
1,900 articles, release notes on a fortnightly cycle, and a customer-facing portal
where a mistake is visible to the people who pay for the product. The incident references are
real incidents, genericized.

## License

MIT. See [LICENSE](LICENSE).
