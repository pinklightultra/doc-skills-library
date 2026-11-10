# Proof

Back to the [skill list](../README.md).

## Structural check

```bash
python check.py      # standard library only, exits non-zero on any failure
```

Seven checks. The README carries the skill table, the Limitations exceptions, and the link count. This page is the rest of the claim. The counts below are what the script prints on this tree, not figures typed from memory:

1. **Links resolve.** 32 markdown files, 70 local links, 0 dangling. File targets must exist. An `#anchor` must match a real heading in the target file under GitHub's slug rules. Flat `docs/*.md` pages are included. `corpus/` and `reports/`, and anything nested under `docs/`, are not. That is where a corpus and a sweep go, and neither is part of this count.
2. **Frontmatter parses.** All 21 `SKILL.md` files carry exactly `name`, `description`, `user_invocable`, in that order, with `name` equal to the directory name and `user_invocable` set to `true`. The parser is hand-rolled, so the check has no dependencies.
3. **The skill table is complete.** 21 skill directories, 21 table rows, names matching. A skill with no row, or a row with no skill, fails. The check reads the table in [README.md](../README.md) only.
4. **Guardrails are inherited, not copied.** All 21 skills link `../../GUARDRAILS.md`, and that relative path resolves from each skill's own location. This is the check that catches the install mistake in [Install](install.md).
5. **The section contract holds, with three named exceptions.** The contract is read out of `/skill-forge` rather than restated in the script: `## When to use this`, `## Inputs`, `## What To Do`, `## Output Format`, `## Notes`. The machine-readable output block is a closed fence with `[bracketed]` slots, which is what an umbrella skill needs in order to diff a child. Both exception sets are cross-checked against the [Limitations](../README.md#limitations) list, so the script and the README cannot drift apart on their own.
6. **No em dashes.** Exactly one exists in the repo, the counter-example inside the `/house-style` rule that forbids them. One anywhere else fails, and so does removing that one. Smart quotes fail anywhere. The scan includes these pages. It does not include a corpus you dropped under `corpus/` or in a subdirectory of `docs/`.
7. **No secrets or tenant identifiers.** Deliberately narrow: assigned credential values, JWTs, AWS key ids, PEM private-key headers, internal ticket keys, tenant hostnames, and absolute local paths. The repo is full of the words "secret", "token", and "password" because several skills are about leak scanning. Every pattern therefore requires structure a sentence does not have. **The scan skips `check.py` itself**, because the patterns would otherwise report themselves. That file is the only place an identifier can sit while the check still prints PASS. Three real ticket keys were hardcoded there once, inside the check that hunts for ticket keys, and check 7 passed the whole time. They are configuration now. Passing check 7 is not a human read. `/leak-scan` exists because that read is still required.

What [`check.py`](../check.py) cannot do is tell you whether any skill produces good output. It verifies that the library is structurally sound: the files are well-formed, the cross-references resolve, and the README describes what is on disk.

## Continuous integration

Two workflows run that same script on push, pull request, and manual dispatch to `main` and `master`.

- [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) is the cross-platform run: ubuntu, windows, and macos, each on Python 3.10, 3.11, and 3.12.
- [`.github/workflows/check.yml`](../.github/workflows/check.yml) is a single Ubuntu job on Python 3.11.

There is no behavioral test suite. The workflows show that a clean runner still agrees with the README and with this page. They do not show that a model followed a skill.

## Report shape

Filled-in sweep reports are not in the repo. `reports/` is gitignored on purpose. What is in the repo is the template each skill fills. This is the `## Output Format` block from [`skills/leak-scan/SKILL.md`](../skills/leak-scan/SKILL.md#output-format), slots included:

```
## Leak Scan: [target], [date]

### CRITICAL (do not publish):
- [exact text]: [secret/PHI], REMOVE + [rotate if real]

### HIGH / MEDIUM:
- [exact text]: [class], [scrub to: ...]

Verdict: [clear to publish / BLOCKED on N critical items]
```

The same pattern, with different slots, is the output section of the skills `/kb-health-sweep` aggregates. Three skills do not use a fenced template. They are named in the README under [Limitations](../README.md#limitations).
