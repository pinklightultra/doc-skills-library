---
name: counterfactual-doc
description: "Given a feature, write the release note for the version where it FAILS or is MISCONFIGURED: the anti-documentation. Surfaces every failure mode and support-ticket-in-waiting so you can preempt them in the real doc."
user_invocable: true
---

# Counterfactual Doc

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Given a feature, write the release note for the version where it FAILS or is MISCONFIGURED: the anti-documentation. Surfaces every failure mode and support-ticket-in-waiting so you can preempt them in the real doc.

## When to use this

While drafting a feature's real documentation, as a discovery step: imagining how it breaks reveals the caveats, prerequisites, and "known limitations" the real doc should include. Also useful for building troubleshooting content.

## Inputs

A feature, a configuration flow, or a single setting. If none, ask.

## What To Do

1. **Understand the happy path.** Pull how it is supposed to work: the article, the source ticket, the configuration source itself.

2. **Invert it and enumerate failure modes:**
   - **Misconfiguration:** wrong value, missing companion setting, wrong data type, a per-tenant enable flag left unchecked
   - **Missing prerequisites:** a dependency not enabled, a step skipped, a permission not granted
   - **Environment and timing:** cache not cleared, batch job not yet run, a mode toggle in the wrong state, a deploy that landed without a restart
   - **Edge cases:** unsupported file types, size limits, concurrency, per-tenant gaps
   - **Interaction failures:** conflicts with another feature or setting that reads the same value

3. **For each, write the anti-note:** what the user sees when it is broken, and why. This doubles as pre-written troubleshooting content, which is the actual payoff.

4. **Cross-check the support tracker.** Search support tickets for the feature using `issue_tracker.support_volume_query`. A predicted failure that has already happened is not a hypothesis, it is a documentation gap with evidence, and it outranks everything you imagined.

5. **Convert to real-doc improvements.** Translate the failure list into concrete additions for the actual documentation: prerequisites to state up front, a Known Limitations section, configuration gotchas to call out inline, a troubleshooting subsection.

## Output Format

```
## Counterfactual Doc: [feature], [date]

### Failure modes:
| If... | User sees... | Because... |
|---|---|---|
| setting value wrong | [symptom] | [cause] |

### Confirmed by support history: [tickets where this actually happened]

### Add to the real doc:
- Prerequisite: [...]
- Known limitation: [...]
- Troubleshooting: [...]
```

## Notes
- The failure fiction is a means. The deliverable is the list of real-doc improvements. If you finish with a vivid failure list and no doc changes, you did step 5 wrong.
- Support history grounds the imagination. Predicted failures that already occurred are the highest priority to document, and they are also the easiest to justify to a reviewer.
- This feeds the Known Limitations and troubleshooting sections that a happy-path draft always omits, because the author was thinking about the feature working.
