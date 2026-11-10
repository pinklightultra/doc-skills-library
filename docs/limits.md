# Limits

Back to the [skill list](../README.md).

## Configuration

Two notes worth reading before you trust a result.

The default `search_command` is `grep`, not `rg`. ripgrep is faster and worth switching to if you have it, but verify it first. A missing binary does not fail loudly here: the shell writes "command not found" to stderr, the skill reads an empty result set, and an empty result set looks exactly like a clean corpus. That is the failure mode `GUARDRAILS.md` calls "absence of evidence is not evidence of absence." This library used to ship the `rg` default that causes it.

Field *names* are configured rather than field ids, because hosted trackers expose custom fields under opaque per-instance ids. A skill body carrying `customfield_10142` works in exactly one place. That id is invented for the example. Yours will differ, and nothing in a skill should be carrying it.

## What is missing

The search this library assumes is literal text search. It finds names, not topics. Ask which articles discuss authentication and it will find the ones containing the string "authentication", which is neither the same set nor a superset. Articles that cover the concept in other words are invisible to it.

That gap has consequences the reports cannot fully caveat:

- **Coverage audits undercount.** `/audit-docs-coverage` finds a topic absent when no article names it. An article covering it in different terms reads as a gap.
- **Duplicate detection is weak.** Two articles documenting the same procedure with different vocabulary do not look like duplicates.
- **`/leak-scan` is the exception, and literal matching is what it needs.** Leak scanning looks for a specific hostname, a specific customer name, a specific key shape. Semantic similarity would add false positives to the one skill that must not have them.

`semantic_search_command` exists in the config for this reason and ships empty. It is a component you supply. Skills that would benefit degrade to literal search and say so in their report.

Also missing: an evaluation of whether these skills produce better documentation than working without them.

## The audience-gating problem

`docs.audience_model` has two values, and they are not interchangeable. Which one your stack uses decides whether "internal only" is a fact or a hope.

**`reader_group`.** The backend enforces per-audience read access at request time. An article outside a reader's group is not served to them. Splitting content by audience is a real control.

**`frontmatter`.** Audience is a field on the article, honored by the build. Two build targets read the field and emit two sites. This holds until the field is wrong, the build target is misconfigured, a page is published outside the pipeline, or someone reads the source repository. There is no request-time check.

The natural fix for a mixed-audience article is to split it into an internal one and an external one. Under `frontmatter` that split is organizational. The document gets better. The exposure stays the same.

`/audience-lens` asks the question rather than assuming the answer. It reports whether a recommended split is access-enforceable on your stack or only a reorganization, and under `frontmatter` it says so. Set the key to the model you actually run. Setting it to `reader_group` because that is the model you want produces confident advice that is wrong in the direction that costs you.
