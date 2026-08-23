---
name: who-needs-to-know
description: "Given a change, work out which customers and teams are actually affected, using component, module, and per-customer project ticket signal, and who should be told. Turns \"we shipped it\" into a targeted notification list instead of a blast."
user_invocable: true
---

# Who Needs To Know

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Given a change, work out which customers and teams are actually affected, using component, module, and per-customer project ticket signal, and who should be told. Turns "we shipped it" into a targeted notification list instead of a blast.

## When to use this

After a change ships, or just before, when deciding who to notify. Especially for changes that are customer-specific, module-specific, or carry a safety dimension.

## Inputs

The change: a ticket, a feature, a setting, or a release item. If none, ask.

## What To Do

1. **Characterize the change.** Pull the ticket or feature and establish: which module or product area, which component, is it global or customer-specific, and does it link to a per-customer project?

2. **Determine affected customers and teams:**
   - If customer-specific, identify the account from the source project or ticket. An authentication change made for one account's integration is the archetype: it is invisible to everyone else and critical to one.
   - If global, note that it affects every customer on that module, and say how many that is if you can count it.
   - Cross-reference component and product area against your customer-to-module mapping, if you maintain one.

3. **Map to notification targets.** Who owns the relationship or needs the heads-up: the implementation team, the specific account owners, support. Distinguish **must tell** (a behavior change they will notice) from **FYI** (an internal improvement they will not).

4. **Draft the notification stub.** A short summary of what changed and what, if anything, the recipient must do.

5. **Split the output by destination, and label each half.** An internal notification list may name the account; that is what makes it actionable. Anything destined for a published surface may not. See [references/no-client-names.md](../../references/no-client-names.md). Never hand over one blob and leave the scrubbing decision to whoever forwards it, because they will forward it unscrubbed.

6. **Do not send.** Produce the list and the stub. Sending is a human action.

## Output Format

```
## Who Needs to Know: [change], [date]

Change: [what, which module, global vs customer-specific]

### Must notify:
- [team/owner]: because [behavior change they will see]

### FYI:
- [team]: [internal improvement]

### Notification stub (INTERNAL, may name accounts): [summary]
### Notification stub (PUBLISHABLE, names scrubbed): [summary]
```

## Notes
- Internal notification may name a customer. Published documentation may not. Keep the two stubs physically separate in the output so the distinction survives being copied.
- "Must tell" versus "FYI" matters. Blasting everyone for a minor internal fix trains the recipients to ignore the next one, which is the notification that mattered.
- Draft only. The human sends.
