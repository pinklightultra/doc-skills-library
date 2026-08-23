---
name: doc-turing-test
description: "Generate a plausible-but-fake release note mixed with real ones and challenge you (or a reviewer) to spot the fake: a vigilance drill against the \"reads legit but isn't accurate\" failure that erodes client trust."
user_invocable: true
---

# Doc Turing Test

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Generate a plausible-but-fake release note mixed with real ones and challenge you (or a reviewer) to spot the fake: a vigilance drill against the "reads legit but isn't accurate" failure that erodes client trust.

## When to use this

As a training and calibration exercise for yourself or reviewers, or to test whether the team's review process would actually catch a subtly wrong note. Sharpens the instinct that catches an overclaim before a reader does ([references/incident-ga-overclaim.md](../../references/incident-ga-overclaim.md)).

## Inputs

Optional: a product area or version to draw real notes from. Default: pull a few real published notes from the most recent release.

## What To Do

1. **Pull real notes.** Get several genuine published release-note items from the docs corpus for the chosen area or version.

2. **Craft one plausible fake.** Write a fabricated note that looks structurally correct and stylistically consistent but is subtly wrong: a feature that doesn't exist, a plausible-but-invented configuration setting, an overclaimed capability, or a real feature attributed to the wrong version. Make it a fair test: believable, not absurd.

3. **Present the mixed set.** Show the real notes and the fake together, unlabeled, numbered. Ask the user to identify the fake and explain their reasoning.

4. **Reveal and analyze.** Confirm which was fake. Discuss what tells gave it away, or should have. If the user was fooled, name the verification step that would have caught it: checking the source ticket, confirming the configuration setting actually exists, cross-referencing the version.

5. **Extract the lesson.** Tie the tells to real review practice: this is why you verify the source ticket, confirm the setting exists, cross-check the version. Reinforces the habits behind `/stop-and-reference`, `/steelman-this-note`, and `/leak-scan`.

## Output Format

```
## Doc Turing Test: [area], [date]

[Numbered set: N notes, one fake, unlabeled]

Which is fabricated, and why do you think so?

--- (after user answers) ---

### Reveal: #X was fake, [what was wrong]
### Tells: [what should have flagged it]
### Verification that would catch it: [the real-practice habit]
```

## Notes
- The fake must be fair: plausible and style-consistent, not obviously wrong. An easy fake teaches nothing.
- The payoff is the verification habit, not the game. Always land the "here's how you'd catch this for real" point.
- Never let a fabricated note leak into anything real. This is a closed drill only.
