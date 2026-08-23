---
name: objection-forecast
description: "Before a customer call or release review, predict the questions and pushback a given release or document will generate, based on past support-ticket patterns and prior customer-reaction incidents, so you walk in with answers pre-loaded. Built from a real caught-us-off-guard meeting."
user_invocable: true
---

# Objection Forecast

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Before a customer call or release review, predict the questions and pushback a given release or document will generate, based on past support-ticket patterns and prior customer-reaction incidents, so you walk in with answers pre-loaded. Built from a real caught-us-off-guard meeting ([references/incident-ga-overclaim.md](../../references/incident-ga-overclaim.md)).

## When to use this

Ahead of a client-facing meeting, a customer review session, or a release announcement. Turns "we got blindsided by implementation questions" into "we anticipated them."

## Inputs

The subject: a release, an article, or a topic going to a meeting. Optionally the audience.

## What To Do

1. **Understand what is being presented.** Pull the release note or article content. Identify the claims, the new capabilities, and anything ambiguous or availability-adjacent.

2. **Mine past reaction patterns:**
   - Support tickets on the same feature. What did customers actually get confused by, or push on? Use `issue_tracker.support_volume_query` from config and **query per feature or component, not by the release name.** Searching free text for a release name returns deploy and scheduling noise instead of signal, which reads as "no concerns found" when in fact you searched the wrong axis.
   - Prior incidents. Read your own postmortems; the useful pattern is usually "customers asked implementation questions about something that was not implemented yet."
   - Known customer hot buttons: implementation timing, readiness, configuration burden, cost, migration effort.

3. **Generate likely objections and questions, ranked by likelihood:**
   - Implementation and timing ("when can WE have this, is it actually released?")
   - Scope ("does this cover our use case X?")
   - Configuration burden ("what do we have to do?")
   - Risk and compliance ("does this affect our compliance posture?")
   - The awkward one: anything the doc overclaims or leaves ambiguous that a sharp customer would probe

4. **Pre-load answers.** For each predicted question, draft a defensible answer. Flag any question whose honest answer is "not released" or "not committed," so it gets a prepared, sign-off-safe response instead of an improvised one.

5. **Flag the traps.** Explicitly call out questions where an off-the-cuff answer would create a commitment. A verbal timeline given in a meeting is as binding, in practice, as a written one.

## Output Format

```
## Objection Forecast: [subject], [audience], [date]

### Likely questions (ranked):
1. [question], likelihood: high
   Prepared answer: [...]
   TRAP: [if answering wrong creates a commitment or an availability overclaim]

### Walk-in summary: [the 2-3 things to be ready for]
```

## Notes
- The point is no surprises. A predicted question with a prepared, sign-off-safe answer is the goal.
- Availability and commitment answers may need pre-clearance. Flag those before the meeting, not during it.
- Ground predictions in real support history, not imagination. A question a customer already asked is worth ten you invented.
- If the support-ticket search returns nothing, say "no support signal found" and note which axis you searched. Do not report it as "no objections expected." An empty query result is a fact about your query.
