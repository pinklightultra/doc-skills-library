# doc-skills-library

21 public Claude Code skills for auditing a documentation corpus and reviewing drafts.

For technical writers and docs engineers who publish into a large knowledge base and need the review to happen the same way every time: the same pre-publish gates, the same corpus scores, and a report stable enough to diff next week against this week.

## Install and use

1. Clone this repo. Copy `skills/<name>/` into `~/.claude/skills/`, and copy `GUARDRAILS.md` and `references/` into `~/.claude/` so they sit one level above `skills/`.
2. Copy [`config.example.yml`](config.example.yml) to `config.yml` and set `docs.corpus_root` to your knowledge base before an audit.
3. Type `/<name>` in Claude Code, or open `skills/<name>/SKILL.md` and follow the steps with no agent.

Create `~/.claude/skills/` before the copy. If that directory is missing, `cp -r` can exit 0 and still not install the skill. `GUARDRAILS.md` has to land in `~/.claude/`, not inside `skills/`, or every skill runs without the five rules and nothing errors. The commands, and how the relative path resolves, are in [Install](docs/install.md).

## Skills

Each line is the first sentence of that skill's `description` in its `SKILL.md`. The order is the pass order: pre-publish gates, corpus health, drafting method, calibration and craft.

| Skill | Group | What it does |
|---|---|---|
| `/leak-scan` | Pre-publish | Sweep a document (or batch) for anything that should never be public: internal hostnames, credentials, encrypted-secret references, repo paths, employee names, customer names. |
| `/steelman-this-note` | Pre-publish | Adversarial reviewer that argues how a customer could misread an article to their advantage: availability overclaim, implied commitment, scope creep, contractual-sounding language. |
| `/redline` | Pre-publish | Contract-grade read of an article for anything construable as an SLA, warranty, or commitment. |
| `/bumpkin-test` | Pre-publish | Run a non-expert comprehension persona against an article and report every term, acronym, or assumption an outside reader would trip on. |
| `/who-needs-to-know` | Pre-publish | Given a change, work out which customers and teams are actually affected, using component, module, and per-customer project ticket signal, and who should be told. |
| `/audit-docs-coverage` | Corpus | Audit a documentation corpus for coverage gaps: stub articles, duplicate artifacts, empty categories, and topics with no article at all. |
| `/doc-decay-model` | Corpus | Predict which articles will go stale next, before they do. |
| `/kb-health-sweep` | Corpus | Run the recurring knowledge-base health sweep: orchestrate the corpus-scale analysis and client-safety skills into one periodic pass, and write a dated report to the configured reports directory. |
| `/institutional-amnesia-check` | Corpus | Periodically resurface old resolved incidents and ask "is this defense still in place?", guarding against fixes quietly rotting (a cron getting disabled, a rule removed, a habit lapsing) so past lessons don't silently un-learn. |
| `/audience-lens` | Corpus | Review or rewrite an article through three reader personas at once: end user, implementer, and internal support. |
| `/source-backed-rfp` | Drafting | Draft or audit RFP and capability responses using direct current documentation evidence, explicit partial support, and NO KB SOURCE for unsupported claims. |
| `/counterfactual-doc` | Drafting | Given a feature, write the release note for the version where it FAILS or is MISCONFIGURED: the anti-documentation. |
| `/house-style` | Drafting | Apply (or check writing against) a general-purpose house style: direct, lean, structurally sound prose with no filler. |
| `/objection-forecast` | Drafting | Before a customer call or release review, predict the questions and pushback a given release or document will generate, based on past support-ticket patterns and prior customer-reaction incidents, so you walk in with answers pre-loaded. |
| `/stop-and-reference` | Drafting | When you hit something you do not understand while writing configuration instructions or describing a screen (an unfamiliar setting, admin screen, field, context-menu option, feature name, or navigation path), STOP and pull the reference material instead of guessing. |
| `/doc-turing-test` | Calibration | Generate a plausible-but-fake release note mixed with real ones and challenge you (or a reviewer) to spot the fake: a vigilance drill against the "reads legit but isn't accurate" failure that erodes client trust. |
| `/teach-me-back` | Calibration | Inverts the relationship: quizzes YOU on a subsystem to surface where your own understanding is thin before you document it. |
| `/rubber-duck` | Calibration | You explain a gnarly config or problem out loud to it; it asks only clarifying questions (never answers) until you've talked yourself into the solution. |
| `/postmortem` | Calibration | After an incident, generate a structured writeup (what happened, how it was caught, root cause, and the standing defense added) and file it to memory. |
| `/skill-forge` | Calibration | A skill that proposes new skills. |
| `/verify-loop` | Calibration | Retrofit a codebase's testing setup to the verify-then-discard methodology (disposable per-change scripts, fresh browser contexts, real-state assertions, build-time enforcement) instead of a persistent test suite that rots unwatched |

## Documentation

- [Install and configure](docs/install.md). The copy commands, the two failures that can look like success, and the config keys an audit needs on day one.
- [Using the skills](docs/using.md). Severity, the order of a pre-publish pass, a corpus pass, and how to read a verdict.
- [Approach](docs/approach.md). Read-only until a human asks for a write. One guardrail file, linked rather than copied. Uncertainty gets its own label. The report is a template, so the next run can be diffed.
- [Limits of search and audience](docs/limits.md). Literal search misses topics. "Internal only" is sometimes only a field.
- [Background](docs/background.md). A knowledge base of about 1,900 articles, and the release note that was true about the engineering and false about availability.
- [Proof](docs/proof.md). What [`check.py`](check.py) checks. On this tree: 32 markdown files, 70 local links, 0 dangling. A pass means the library matches its own contract. It says nothing about whether a skill produces good output.

## Limitations

- **These are prompts.** `python check.py` is the only test here, and it is a structural check. It covers the seven properties listed in [Proof](docs/proof.md): links, frontmatter, the skill table, the guardrails pointer, the section contract, the em-dash rule, and a narrow secret scan. It exits non-zero and names what broke. A skill can pass all seven and still be ignored, misread, or applied to the wrong input. Treat every output as a draft to check, particularly the ones that produce confident tables.
- **No evaluation.** No A/B test, no measured error rate on the writing itself.
- **A model still does the work.** Every skill inherits the underlying model's failure modes, including plausible fabrication. Several skills are built to fight that.
- **Backend-shaped.** The library assumes a documentation corpus you can search locally and an issue tracker with per-component history. With neither configured, roughly half of these do nothing useful, and the ones written for that case will say so.
- **Three of the 21 do not follow the section contract** that `/skill-forge` declares: `house-style`, `verify-loop`, and `source-backed-rfp` have their own structure. `verify-loop` is also the one skill here that is not about documentation.
- **Not every skill has a machine-readable output block.** `/rubber-duck` is conversational by design, and `/house-style` and `/source-backed-rfp` use prose and a plain table. Anything you build that expects a fenced, bracketed template from every skill will miss those three.
- **The leak classes and the review dimensions come from one corpus** and one organization's incidents. They are a starting point for a similar knowledge base, not a standard.

## License

MIT. See [LICENSE](LICENSE).
