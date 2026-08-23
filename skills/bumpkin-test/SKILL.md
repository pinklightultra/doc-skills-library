---
name: bumpkin-test
description: "Run a non-expert comprehension persona against an article and report every term, acronym, or assumption an outside reader would trip on. Makes a one-off jargon audit into a repeatable button."
user_invocable: true
---

# Bumpkin Test

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Run a non-expert comprehension persona against an article and report every term, acronym, or assumption an outside reader would trip on. Makes a one-off jargon audit into a repeatable button.

## When to use this

Before publishing any client-facing article, when you want to know whether a competent outsider with no internal context could actually follow it. This is pure comprehension: pair it with `/house-style` for voice and `/audience-lens` for structure.

## Inputs

An article (slug or id) or pasted draft text. If none, ask.

## What To Do

1. **Read as a smart outsider.** Adopt the persona: a competent business user in the customer's industry who does NOT know your internals, code names, ticket systems, or undocumented acronyms. Not stupid, just uninitiated. The distinction matters, because flagging genuinely standard domain terms wastes the reviewer's attention and trains them to ignore the report.

2. **Flag every comprehension snag:**
   - Unexpanded acronyms and initialisms, on first use
   - Internal jargon, code names, module nicknames, repository or system names that leaked in
   - Assumed prior knowledge ("as configured in the usual way") with no referent
   - Undefined field or screen names presented as if familiar
   - Steps that skip a prerequisite a newcomer would not know to do
   - Customer names or internal team names. These are comprehension snags **and** policy violations, so flag them doubly. See [references/no-client-names.md](../../references/no-client-names.md)

3. **Rate overall readability.** Would the persona complete the task, or understand the feature, unaided? Yes / mostly / no. Commit to one of the three rather than hedging.

4. **Propose fixes, not just flags.** For each snag, give the plain-language replacement or the definition to add. Keep proposals in house voice per `/house-style`: lean, no em dashes.

5. **Optionally maintain a glossary.** If a term recurs across articles, note it as a candidate for a shared glossary entry rather than redefining it inline in every article. Inline redefinition is how a corpus ends up with four different definitions of the same term.

## Output Format

```
## Bumpkin Test: [article], [date]

Readability: [Yes / Mostly / No], [one-line verdict]

### Snags (N):
| Term / spot | Problem | Fix |
|---|---|---|
| "the ARB step" | acronym, never defined | expand on first use, then use the short form |
| "the usual queue setup" | assumes prior knowledge | link to the queue configuration article, or state the steps |

### Glossary candidates: [recurring terms worth a shared entry]
```

## Notes
- The persona is uninitiated, not unintelligent. Do not flag standard terms of art in the customer's own industry; they know their domain, they don't know your product.
- Customer names and internal system names are both comprehension snags and policy violations. Flag them with priority.
- This checks understanding, not correctness. An article can be perfectly comprehensible and completely wrong. Pair with `/stop-and-reference` for factual grounding.
