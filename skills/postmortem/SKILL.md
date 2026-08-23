---
name: postmortem
description: "After an incident, generate a structured writeup (what happened, how it was caught, root cause, and the standing defense added) and file it to memory. Turns each fire into institutional learning instead of a one-time scramble."
user_invocable: true
---

# Postmortem

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

After an incident, generate a structured writeup (what happened, how it was caught, root cause, and the standing defense added) and file it to memory. Turns each fire into institutional learning instead of a one-time scramble.

## When to use this

After any incident or near-miss: a client-facing error caught (an availability overclaim, see [references/incident-ga-overclaim.md](../../references/incident-ga-overclaim.md)), a doc gap that reached a client, a broken publish, a customer-name leak. Run it while the details are fresh.

## Inputs

A short description of what happened, or the ticket/article involved. If thin, ask a few targeted questions to reconstruct the timeline.

## What To Do

1. **Reconstruct the timeline.** What was the state, what went wrong (or nearly), when/how it was noticed, who flagged it. Pull the relevant article/ticket history to ground it.

2. **Root cause, not just symptom.** Distinguish the surface event ("note implied GA") from the underlying cause ("no gate checking published notes against source-epic status"). Name the real gap.

3. **Capture the response.** What was done to contain it (e.g. unpublish-now), and what the permanent fix is (e.g. reword pending Product/legal).

4. **Name the standing defense.** What prevents recurrence: often a new or existing skill. The availability-overclaim incident motivated `/steelman-this-note` and `/redline`; a leak motivates `/leak-scan`. If no defense exists yet, recommend one (and consider `/skill-forge`).

5. **File it where the next session will read it.** Write the writeup to a durable note and index it from wherever your agent loads context at startup. A postmortem that lives only in a closed chat log is not institutional learning. Keep it factual, blameless, forward-looking.

6. **Fold the lesson back into the skill that failed.** If a skill was running and still let the incident through, edit that skill's `Notes` to record the specific wrong output it produced and encode the fix as a rule. This is the mechanism by which the library gets harder to fool over time.

## Output Format

```
## Postmortem: [incident], [date]

What happened: [timeline]
How caught: [who/what flagged it]
Root cause: [underlying gap, not just symptom]
Response: [containment + permanent fix]
Standing defense: [skill/process that prevents recurrence]
Filed: [note created]
Skill updated: [skill whose Notes now carry this lesson, or "none applicable"]
```

## Notes
- Blameless and factual: the goal is the systemic fix, not fault.
- Every incident should leave behind a defense; if it doesn't, the postmortem isn't done.
- File it durably so the next session inherits the lesson.
- Distinguish the surface event from the structural gap. "The wording was wrong" is a symptom; "nothing checked the claim against the source ticket's release state" is a cause. Only the second one can be defended against.
