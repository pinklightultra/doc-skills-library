---
name: steelman-this-note
description: "Adversarial reviewer that argues how a customer could misread an article to their advantage: availability overclaim, implied commitment, scope creep, contractual-sounding language. A pre-mortem for client-facing docs, built from a real published overclaim."
user_invocable: true
---

# Steelman This Note

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Adversarial reviewer that argues how a customer could misread an article to their advantage: availability overclaim, implied commitment, scope creep, contractual-sounding language. A pre-mortem for client-facing docs, built from a real published overclaim ([references/incident-ga-overclaim.md](../../references/incident-ga-overclaim.md)).

## When to use this

Before publishing anything client-facing where the wording could be held against your organization: release notes, configuration articles, API docs, anything describing capability or timing. Run it as the last gate, after the content is otherwise final.

## Inputs

An article (slug/ID) or draft text. If none, ask.

## What To Do

1. **Read like an adversarial customer.** Assume a reader motivated to interpret the text in the way most favorable to them and least favorable to you. What could they claim this promised?

2. **Hunt specific risk classes:**
   - **Availability or readiness overclaim:** implies something is released, supported, or production-ready when it is internal, in progress, or gated behind a flag. This is the failure the skill was written for.
   - **Implied commitment:** future-tense or roadmap language a customer could read as a delivery promise ("will support", "coming", "planned")
   - **Scope creep:** describes a capability more broadly than what actually shipped, inviting "but the docs said it does X"
   - **Contractual tone:** words like "guarantee", "ensure", "all", "always", "fully" that overpromise
   - **Customer-specific leakage:** naming one customer implies every other reader gets the same thing. See [references/no-client-names.md](../../references/no-client-names.md)
   - **Security disclosure:** naming patched vulnerabilities, unpatched ones, or internal infrastructure

3. **For each risk, write the misread.** State the exact sentence, then "a client could argue this means ___," then the safer rewrite.

4. **Severity-rank.** High = could create a commitment/liability or GA misrepresentation. Low = merely loose wording.

5. **Recommend a gate.** If any HIGH risk lands on a live or about-to-publish article, recommend holding it pending product and legal review. Do not reword availability or commitment language on your own authority. Propose, don't impose: a claim a customer may already have relied upon is not a wording problem an author fixes alone.

## Output Format

```
## Steelman: [article], [date]

### HIGH: [sentence]
Misread: a client could argue this means [X].
Safer: "[rewrite]"

### MEDIUM / LOW: ...

Gate: [clear to publish / hold for product and legal review on HIGH items]
```

## Notes
- This is deliberately paranoid. That is the point. The human decides what is real risk versus acceptable risk.
- Availability and commitment wording changes may need product and legal sign-off, not just your edit.
- This deep-reads a single note before publish. Pair it with `/redline` for the narrower contractual lens, and `/objection-forecast` for what a customer will ask about it in a meeting.
- Present tense is itself a claim. "Supports X", "will support X", and "has been built to support X" are three different promises, and at publish time usually only one of them is true.
