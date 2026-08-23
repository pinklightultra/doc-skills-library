---
name: redline
description: "Contract-grade read of an article for anything construable as an SLA, warranty, or commitment. Stricter and narrower than /steelman-this-note, oriented specifically to legal and contractual exposure. The lawyer in the room."
user_invocable: true
---

# Redline

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Contract-grade read of an article for anything construable as an SLA, warranty, or commitment. Stricter and narrower than `/steelman-this-note`, oriented specifically to legal and contractual exposure. The lawyer in the room.

## When to use this

Final gate before publishing anything a customer could treat as a promise: capability statements, timing, guarantees, API behavior contracts. Narrower and harder-edged than the steelman pass.

## Inputs

An article (slug/ID) or draft. If none, ask.

## What To Do

1. **Read as opposing counsel.** Assume every sentence may be quoted back in a dispute. What did your organization commit to, warrant, or guarantee, intentionally or not?

2. **Flag contract-risk language specifically:**
   - **Warranty words:** "guarantee", "ensure", "will always", "never fails", "fully compliant", "all cases"
   - **SLA-like statements:** specific timings, uptime, response commitments stated as fact
   - **Absolute quantifiers:** "all", "every", "any", "complete" applied to capability
   - **Forward commitments:** "will support", "is planned", "coming in vX" read as a delivery promise
   - **Compliance assertions:** claims of regulatory compliance that could bind your organization

3. **Rate exposure.** High = creates a plausible contractual obligation or warranty. Medium = loose but arguable. Low = stylistic.

4. **Propose defensible rewrites.** Replace absolutes with scoped, accurate language ("supports X" not "guarantees X"; "designed to" not "ensures"). Preserve meaning, remove the binding edge.

5. **Gate.** Any HIGH exposure on a live or about-to-publish article means recommend a hold for legal and product review. Do not soften commitment language on your own authority. Propose it.

## Output Format

```
## Redline: [article], [date]

### HIGH exposure:
- "[exact phrase]" → construable as [warranty/SLA/commitment]
  Rewrite: "[scoped version]"

### MEDIUM / LOW: ...

Gate: [clear / hold for legal review on HIGH items]
```

## Notes
- Stricter and narrower than `/steelman-this-note`: a pure legal and contractual lens. Run steelman first for the broad misread pass, then this for the binding-language pass.
- HIGH items may need legal sign-off, not just your edit.
- Absolutes are the usual culprits. Hunt "all", "always", "ensure", "guarantee", "never", and "fully" first, then read the verbs.
- A sentence can be factually true and still contractually dangerous. Accuracy is not the test here. Bindingness is.
