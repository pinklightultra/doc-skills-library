---
name: teach-me-back
description: "Inverts the relationship: quizzes YOU on a subsystem to surface where your own understanding is thin before you document it. You can't write clearly what you half-know."
user_invocable: true
---

# Teach Me Back

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Inverts the relationship: quizzes YOU on a subsystem to surface where your own understanding is thin before you document it. You can't write clearly what you half-know.

## When to use this

Before documenting an unfamiliar subsystem, integration, or config flow, or to pressure-test your grasp before a client call. A self-check, not a doc generator.

## Inputs

The subject to be quizzed on: a feature, an integration, a configuration flow, or a group of related settings.

## What To Do

1. **Assemble the ground truth first.** Quietly gather what is actually known about the subject: the docs corpus at `docs.corpus_root`, the issue tracker, the configuration source itself. Use `/stop-and-reference` for any term you cannot cite. The quiz has to be gradable against reality, not against plausibility.

2. **Ask progressively harder questions, one at a time:**
   - Level 1: what it does, where it lives
   - Level 2: how it's configured, what the values mean, dependencies
   - Level 3: failure modes, edge cases, interactions with other features, why it was built this way
   Wait for the user's answer before revealing or advancing.

3. **Grade honestly against the ground truth.** Confirm what's right, correct what's wrong, and (most importantly) flag what the user couldn't answer. Those gaps are the point.

4. **Summarize the thin spots.** At the end, list exactly where understanding was shaky. These are what to research before documenting.

5. **Offer the bridge.** Point to the source that fills each gap: the originating ticket, the configuration source, the article that already covers it. Run `/stop-and-reference` on any gap where you cannot name a source either.

## Output Format

```
## Teach-Me-Back: [subject], [date]

[Interactive Q&A happens here, one question at a time]

### Knowledge check summary:
Solid: [what you clearly know]
Shaky: [what needs shoring up before documenting]
Fill from: [sources for each gap]
```

## Notes
- Genuinely interactive: ask, wait, grade. Don't dump questions and answers together.
- Grade against real sources, not plausibility; the value is catching confident-but-wrong understanding.
- The output is a study list, not documentation. Writing comes after the gaps close.
