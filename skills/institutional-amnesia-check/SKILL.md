---
name: institutional-amnesia-check
description: "Periodically resurface old resolved incidents and ask \"is this defense still in place?\", guarding against fixes quietly rotting (a cron getting disabled, a rule removed, a habit lapsing) so past lessons don't silently un-learn."
user_invocable: true
---

# Institutional Amnesia Check

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Periodically resurface old resolved incidents and ask "is this defense still in place?", guarding against fixes quietly rotting (a cron getting disabled, a rule removed, a habit lapsing) so past lessons don't silently un-learn.

## When to use this

Periodically (good cron candidate, low frequency: monthly/quarterly). The meta-guard: makes sure the defenses built after past incidents are still active.

## Inputs

None required. Optionally a specific past incident to re-check.

## What To Do

1. **Gather past incidents and their defenses.** Read the incident writeups (start with [references/incident-ga-overclaim.md](../../references/incident-ga-overclaim.md)) and any `/postmortem` outputs. Ideally each names a standing defense: a skill, a scheduled job, a checklist habit, a rule. Older writeups predate that convention and won't have a structured "defense" field. **If none is named, infer the applicable guard from the incident class** rather than guessing blindly: availability or capability overclaim → `/steelman-this-note` + `/redline`; secret or PII leak → `/leak-scan`; doc drifted from its source → `/doc-decay-model`; reader couldn't follow it → `/bumpkin-test`. If no guard runs automatically for that incident class, mark it "lacking a defense". That is a finding, not a blank.

2. **Verify each defense still exists and runs:**
   - Is the skill still present in the skills directory, and does its body still contain the specific rule the incident added? A skill can survive while the one line that mattered gets edited out.
   - If it was meant to run on a schedule, is that job still configured and firing? Check the scheduler, and check for evidence of a recent run, not just a config entry.
   - If it was a process or habit (e.g. "always run `/leak-scan` before publish"), is there evidence it is still happening?
   - Was any rule or gate quietly removed, widened, or bypassed? A guard that was relaxed to let one edge case through is a lapsed guard.

3. **Flag lapsed defenses.** A defense that's been disabled, deleted, or fallen out of practice is a re-opened vulnerability: the lesson is un-learning.

4. **Recommend reinstatement.** For each lapse, what to restore and how.

5. **Confirm the still-solid ones.** Positive confirmation matters: "these 6 defenses verified active" is reassuring and real.

## Output Format

```
## Institutional Amnesia Check: [date]

### Lapsed (reinstate):
- [incident] → defense [X] is [disabled/deleted/not running], restore by [...]

### Still active (verified):
- [incident] → [defense] confirmed present/running

### New incidents lacking a defense: [any postmortem with no standing guard]
```

## Notes
- This guards the guards: the highest-leverage low-frequency check.
- Positive confirmation of active defenses is valuable output, not filler.
- If a past incident never got a defense, flag it and suggest `/postmortem` + `/skill-forge`.
