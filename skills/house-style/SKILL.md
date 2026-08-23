---
name: house-style
description: "Apply (or check writing against) a general-purpose house style: direct, lean, structurally sound prose with no filler. This is a formatting/voice discipline skill, not a persona. It does not attempt to sound like any specific individual, and contains no personal biographical, humor, or identity content. Use it for any writing task (documentation, emails, reports, instructions) where tight, professional, non-corporate prose is wanted."
user_invocable: true
---

# House Style

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Apply (or check writing against) a general-purpose house style: direct, lean, structurally sound prose with no filler. This is a formatting/voice discipline skill, not a persona. It does not attempt to sound like any specific individual, and contains no personal biographical, humor, or identity content. Use it for any writing task (documentation, emails, reports, instructions) where tight, professional, non-corporate prose is wanted.

## When to use this

Any writing task where tight, professional, non-corporate prose is wanted: documentation, release notes, emails, reports, instructions. Also usable as a lint pass over someone else's draft. Layer domain-specific schema skills on top of it rather than duplicating these rules into them.

## Inputs

Accept either:
- Draft text to revise into house style
- Existing text to check against house style, flagging violations without rewriting (if the user wants a check, not a rewrite; ask if unclear)

## Core Rules (apply to all writing, no exceptions)

- **No em dashes, ever.** Use a comma, colon, period, or a rewritten sentence instead. Example: "The queue differs from the workflow — it requires approval" → "The queue differs from the workflow. It requires approval."
- **No filler openers.** Don't start with "This document covers..." or "In this section, we will..." Lead with the actual content. State what the thing does or is, not what the writing is about.
- **No closing summary paragraphs.** Don't restate what was just said. End when the content ends.
- **Cut hedging and throat-clearing.** No "It's worth noting that," "generally speaking," "in order to" (just "to"), "please note that." State things directly.
- **Prefer active, concrete verbs over abstract ones.** "Fixed an issue that caused X" not "There was an issue where X occurred."
- **Don't over-explain the obvious.** If a reader can infer something from context, don't spell it out. Trust the reader.
- **No corporate/marketing register.** Avoid "leverage," "seamless," "robust," "best-in-class," "empower," "unlock," "game-changing," "cutting-edge." Plain functional language beats buzzwords.
- **Vocabulary should be precise, not impressive.** Pick the exact right word for the meaning; don't reach for a fancier synonym to sound sophisticated. If an unusual word doesn't earn its place by precision, use the plain one.
- **Vary word choice: don't recycle a distinctive word or phrase across a piece.** If the same slightly-unusual word appears twice, one of those instances is probably the wrong word.

## Structural Rules

- **Step + result pattern for instructions.** Each numbered step is an action, followed by what the reader sees that confirms it worked. Two-part rhythm: "Click Save. The window closes." Not paragraphs of prose burying the action.
- **Headings over horizontal rules.** Use heading levels for section separation. Don't add decorative dividers between sections when a heading already does that job.
- **Minimal notes on obvious fields.** When documenting a field, form, or setting, explain only what needs explanation. A field named exactly what it does needs no gloss.
- **Bullets for parallel items, prose for explanation.** Don't force a list where the content is actually one continuous thought, and don't write a paragraph where a scannable list would serve the reader better.

## Phrasing Substitutions (default to the left column)

| Use | Not |
|---|---|
| "Go to X" | "Navigate to X" |
| "displays" | "opens" / "appears" (for windows, panels, screens) |
| "No impact" | "No" (for impact/effect fields) |
| a colon or period | an em dash |
| "to" | "in order to" |

## What This Skill Does NOT Do

- It does not impersonate a specific person's voice, humor, or biography. If you're looking for a personal voice-matching skill (mimicking a specific individual's writing for informal/social content), that's a separate, non-shareable tool scoped to that person's own use. This skill is deliberately generic and safe to hand to anyone.
- It does not enforce domain-specific schemas (e.g. a particular product's release-note field structure). For that, use a domain-specific skill layered on top of this one.
- It does not judge factual accuracy or technical correctness: this is a style/voice pass only.

## Output Format

If asked to revise: return the rewritten text with house style applied, then a one-line change summary by category, not a change log. For example: "removed 3 em dashes, cut a filler opener, converted two paragraphs to step+result."

If asked to check only: return the violations as a list, each quoting the offending text and naming the rule it breaks. Do not rewrite unless asked as a follow-up.

## Notes

- These rules are deliberately general-purpose so this skill can be shared with any team or used for any writing task, unlike domain-specific voice/persona tools that are scoped to one person or one product's documentation standards.
- When in doubt about a rule not listed here, default to whichever version is shorter and more direct.
