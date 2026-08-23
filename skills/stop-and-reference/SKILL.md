---
name: stop-and-reference
description: When you hit something you do not understand while writing configuration instructions or describing a screen (an unfamiliar setting, admin screen, field, context-menu option, feature name, or navigation path), STOP and pull the reference material instead of guessing. Invoke the moment uncertainty appears, before you write the instruction.
user_invocable: true
---

# Stop And Reference

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Guessing at configuration is the failure this prevents. Every time a configuration detail turns out wrong, it traces back to proceeding on an assumption instead of checking the source. This skill is the hard stop. It is the one skill in the library designed to be invoked unprompted, mid-task, by the model itself.

## When to use this

Invoke the instant any of these becomes true, without waiting to be asked:

- A setting name, message constant, feature flag, or permission key whose source you cannot cite
- An admin screen, tab, grid, column, or context-menu option you are describing from memory rather than from a document or a screenshot in front of you
- A field's exact name, its allowed values, or its behavior that you are about to state without a source
- A navigation path (`Admin > X > Y`) you are not certain of
- A ticket number destined for an article's metadata table
- Anything a reviewer could reasonably ask "where did that come from?" about

If you notice the uncertainty, stop. Noticing is the whole skill; the lookup is the easy part.

## Inputs

The exact term you are unsure about. Not a paraphrase of it: the literal string as it appears in the product, because that is what the corpus indexes.

## What To Do

1. **Run the configured lookup against the exact term.** Use `lookup.reference_command` with the term as its final argument. If no lookup command is configured, fall back to `docs.search_command` over `docs.corpus_root`, and additionally query the issue tracker at `issue_tracker.base_url` when you need the originating ticket. If your organization migrated trackers, query the legacy instance at `issue_tracker.legacy_base_url` too; pre-migration history does not appear in the current one, and its absence there is not evidence it does not exist.

2. **Read the full top-ranked article, not the search snippet.** Confirm the specific value, screen, or field against the article body. A snippet can match on the term while the surrounding sentence scopes or contradicts the value you were about to write.

3. **If the lookup finds the source:** cite it, use the real value, continue. The uncertainty is resolved and you may proceed.

4. **If the lookup finds nothing: hard stop.**
   - Do NOT fabricate a value, a field name, or a navigation path.
   - Do NOT emit a `[CONFIRM]` placeholder and keep going. Placeholders get published. This is the specific failure the rule exists to prevent.
   - Present what you searched, where, and what you did or did not find. Hand the decision to the human and wait.
   - Remember that an empty result and a failed lookup are different outcomes. If the lookup itself errored, say so; "not found" is a claim about the corpus, and you have not earned it.

5. **Lint the draft before it is published.** Run `lookup.lint_command` over the drafted section if you have one configured. It should flag every setting code, every ticket reference, and every unresolved placeholder, and verify each setting against the corpus so an invented code surfaces as unverified rather than as plausible. Nothing carrying an unverified value or an unresolved placeholder is publishable. Fix it or ask.

6. **Record what you resolved.** When a term gets traced to a source, write the mapping down wherever your lookup caches its results. The second time you need it should cost nothing, and the cache is also a record of which terms are hard to find, which is a documentation gap in itself.

## Output Format

```
## Stop And Reference: [term]

Searched: [corpus / tracker / legacy tracker], [command or query used]
Found: [article title and reader URL, or "no hit"]
Confirmed value: [the exact value, field name, or nav path from the source]

Status: [RESOLVED, proceeding / HARD STOP, need your call]
If stopped: [what is missing, and what would resolve it]
```

## Notes
- Never state a configuration value, setting code, navigation path, or field behavior you cannot trace to a source you just checked. Not one you remember checking. One you just checked.
- The discipline is asymmetric on purpose: a false stop costs a few seconds of the human's attention, and a false proceed costs a wrong value in a published article that a customer configures their system against.
- This works best with a runtime twin. If you also run automated capture or generation tooling, wire the same lookup into it so an unrecognized label triggers the same stop mid-run rather than being silently labelled from context.
- Absence of a hit is not absence of the thing. Some values live only in a per-version inventory that your lookup may not cover. Say which sources you searched, so the human knows which one to check next.
