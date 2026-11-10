# Approach

Back to the [skill list](../README.md).

Four decisions shape every skill.

**Read-only until a human asks for a write.** Audits and reviews do not edit, publish, or reorganize. When a write is requested, it follows four beats: dry run, show the diff, confirm, verify the live result. A write that returned HTTP 200 is not a write you have seen.

**One guardrail file, linked rather than copied.** All 21 skills point at [GUARDRAILS.md](../GUARDRAILS.md). In the source library, 55 of 61 skills carried their own copy, and the copies had drifted: of the 56 skills with a guardrails block, exactly one pair was identical. `check.py` fails if a skill drops the link or if the relative path does not resolve.

**Uncertainty gets its own label.** A missing backend, a 404, and a clean search are different outcomes. Skills finish the rest of the sweep and name the skip. A 404 or an auth failure is `NOT VERIFIED (NO ACCESS)`. A search that ran and found nothing is a different label: `NO KB SOURCE`, or "no signal" on the axis you queried. Neither is a clean bill of health. If a lookup for a setting, field, or path finds nothing, the skill stops. It does not emit a `[CONFIRM]` placeholder and continue. Placeholders get published.

**The report is a template, so the next run can be diffed.** Most skills end with a fenced block of `[bracketed]` slots. `/kb-health-sweep` depends on that shape. It runs the safety and corpus skills, merges them into one prioritized list, and leads with the delta against the previous report. Paths, hostnames, project keys, and field ids stay in `config.yml`, copied from [config.example.yml](../config.example.yml). A skill body that bakes in a tenant value works in exactly one place.

## Guardrails

Five rules, three error-handling idioms, and a four-beat write ritual live once in [GUARDRAILS.md](../GUARDRAILS.md). Every skill points at that file.

The five rules: default audits to read-only; gate every write behind a shown diff and a confirmation; parse JSON and HTML with a real parser; never expose credentials, tokens, customer names, PII, or PHI; resolve current paths from `config.yml` instead of trusting a path baked into a skill.

The three idioms matter more than any step list. **Degrade rather than fail**: run the rest of the sweep and record the skip. **Absence of evidence is not evidence of absence**: a 404 and a clean result get different labels. **Hard stop over a confident guess**: no `[CONFIRM]` placeholders.

Three reference files carry incident detail the skills cite: [incident-ga-overclaim.md](../references/incident-ga-overclaim.md), [no-client-names.md](../references/no-client-names.md), [pii-redaction.md](../references/pii-redaction.md). Nine of the 21 skills link at least one of them.
