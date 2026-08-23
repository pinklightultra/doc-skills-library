---
name: audience-lens
description: "Review or rewrite an article through three reader personas at once: end user, implementer, and internal support. Shows where one doc is trying to serve three masters and failing. Surfaces the \"this is really three articles\" problem."
user_invocable: true
---

# Audience Lens

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Review or rewrite an article through three reader personas at once: end user, implementer, and internal support. Shows where one doc is trying to serve three masters and failing. Surfaces the "this is really three articles" problem.

## When to use this

When an article feels overloaded, or before publishing something that spans user-facing behavior AND configuration AND internal troubleshooting. The typical trigger is a feature that shipped on three surfaces at once (a UI, a partner portal, an API) and got one article covering all three.

## Inputs

An article (slug or id) or draft. If none, ask.

## What To Do

1. **Read three times, one persona each:**
   - **End user / administrator:** wants to know what the feature does and how to use it. Does not care about configuration internals.
   - **Implementer:** wants the configuration: setting names, allowed values, the ordered steps, the dependencies.
   - **Internal support:** wants failure modes, edge cases, and the detail that makes a ticket diagnosable.

2. **For each persona, assess:** is the information they need present? Is it buried under information for the other two? Would they have to wade through material irrelevant to them to reach it?

3. **Diagnose the tension.** If the article serves all three poorly by mixing them, say so. Recommend either (a) restructure with clear per-audience sections, or (b) split into linked articles: a feature overview plus a configuration article is the usual shape.

4. **Recommend, with the split or restructure sketch.** If splitting, name the resulting articles and say what goes in each. If restructuring, give the section order that separates the audiences cleanly.

5. **Check that the split is enforceable on your backend before recommending it as a safety measure.** Separating internal-support detail into its own article only protects it if your stack can actually restrict who reads that article. On a per-audience read-access backend it can. On a static site it cannot: see the audience-gating note in the README. If `docs.audience_model` is `frontmatter`, present the split as an organizational improvement and say plainly that it is not an access control.

## Output Format

```
## Audience Lens: [article], [date]

### End user: [served well / buried / missing], [note]
### Implementer: [...]
### Internal support: [...]

### Verdict: [single article works / restructure / split]
### If split: [Article 1: X] + [Article 2: Y], linked
### Enforceable: [yes, backend gates by audience / no, build-time only]
```

## Notes
- Not every article needs all three audiences. A pure configuration article can legitimately serve implementers only. Flag over-serving as well as under-serving; an article padded with end-user context an implementer will skip is also failing.
- The "overview plus linked configuration article" pattern is the default recommendation, because it lets each half be written at its own altitude.
- Pairs with `/bumpkin-test` for comprehension and `/house-style` for voice.
