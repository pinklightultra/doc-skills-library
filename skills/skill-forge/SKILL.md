---
name: skill-forge
description: "A skill that proposes new skills. Reads recent session history and work logs, finds repeated manual sequences, and drafts the skill file for the one you keep doing by hand. Self-improving toolset."
user_invocable: true
---

# Skill Forge

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

A skill that proposes new skills. Reads recent session history and work logs, finds repeated manual sequences, and drafts the skill file for the one you keep doing by hand. Self-improving toolset.

## When to use this

Periodically, or the moment you notice you have done the same multi-step thing several times without a skill for it. This is how the library compounds instead of stagnating.

## Inputs

Optional: a time window, or a specific workflow you suspect is repetitive. Default: recent session activity plus whatever work log you keep.

## What To Do

1. **Scan for repeated sequences.** Sources: your work log, session handoff notes, and the workflows you have described out loud. Look for the same tool chain performed more than once. The canonical example: a fork, edit, publish, verify cycle run eight times by hand in a single session before anyone thought to write it down as a skill.

2. **Cross-check against the existing library.** List the current skills (one directory per skill, each holding a `SKILL.md`) and read their descriptions. Do not propose a duplicate. Propose an extension to an existing skill, or genuinely new coverage.

3. **Rank candidates by leverage:** frequency times manual effort times error-risk-if-done-by-hand. A frequent, fiddly, easy-to-botch sequence is the top candidate. A rare, easy, safe one is not worth a file, and adding it dilutes the library.

4. **Draft the skill file in the house contract.** Frontmatter is exactly three keys: `name`, `description`, `user_invocable: true`. Then, in fixed order: a Guardrails pointer to `GUARDRAILS.md`, a one-paragraph prose restatement of the description, `## When to use this`, `## Inputs`, `## What To Do` (numbered, each step bold-led with an imperative), `## Output Format`, `## Notes`.
   - **Make `Output Format` a fenced literal template with `[bracketed]` slots.** This is the highest-leverage convention in the library. It makes the skill's output diffable run over run, which is what lets an umbrella skill compute a delta across its children. A skill whose output shape is described in prose cannot be aggregated.
   - Reference config keys from `config.yml`, never literal hostnames, paths, project keys, or field ids. A skill body with a tenant value baked into it is a skill that only works on one machine.
   - Do not invent a link syntax to a private note store. If the skill needs a policy, either state the policy in the skill or put it in `references/<topic>.md` and link there.

5. **Encode the failure history.** If the new skill exists because something went wrong, say what went wrong in its `Notes` and encode the fix as a numbered rule in `What To Do`. A guardrail whose origin story has been stripped out reads as arbitrary process and gets skipped by the next person, including you.

6. **Present for approval before writing to disk.** Show the draft. Create the file only on confirmation, unless explicitly told to just build it. Never overwrite an existing skill without flagging it first.

## Output Format

```
## Skill Forge: [date]

### Proposed: /[name]
Observed: [the repeated sequence, N times]
Leverage: [frequency / effort / risk]
Draft: [the SKILL.md content]

### Also considered: [lower-ranked candidates, one line each]
```

## Notes
- Meta but real. The highest-value skills come from watching what you actually repeat, not from imagining what would be useful.
- Match the existing contract exactly so the library stays consistent and machine-diffable.
- Propose, then build on approval. Do not clutter the directory with speculative skills; an unused skill is a maintenance cost and a false signal to the next reader.
- **Keep the logic outside the skill.** If the workflow needs a script, write the script separately and have the skill tell the model to read it at runtime. A skill that embeds a remembered copy of a script's behavior will drift from the script silently, and the drift surfaces as a confidently wrong answer rather than as an error.
- Back up the skills directory as real files. Do not replace it with a symlink or junction to satisfy a sync tool: most backup utilities skip link targets by default, so the linked directory gets silently excluded from every backup and you find out when you need it.
