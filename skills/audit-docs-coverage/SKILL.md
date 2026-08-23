---
name: audit-docs-coverage
description: "Audit a documentation corpus for coverage gaps: stub articles, duplicate artifacts, empty categories, and topics with no article at all. Cross-references support-ticket volume so the gap list is ordered by what readers actually need, not by what is easiest to count."
user_invocable: true
---

# Audit Docs Coverage

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Audit the documentation corpus at `docs.corpus_root` for coverage gaps: stub articles, duplicate artifacts, empty categories, and topics with no article at all. Cross-reference support-ticket volume so the gap list is ordered by what readers actually need.

## When to use this

Periodically, before planning a documentation quarter, or when someone asks "what are we missing?" and you need an answer with a denominator instead of an anecdote.

## Inputs

Optional scope (version, category subtree). Default: the whole corpus at `docs.corpus_root`.

## What To Do

### Critical precondition: do this before anything else

This skill has a documented failure mode, and the precondition exists because of it. An early version of this audit **undercounted articles in nested categories and reported empty-category gaps that did not exist.** That wrong report was presented as authoritative before anyone caught it.

The cause: in a hosted knowledge base, a category tree is frequently reference-based rather than a real nested structure. A category node can report `article_count: 0` while its child categories hold hundreds of articles. A single-level read of the node believes the zero.

Rules, no exceptions:

1. **Fetch the full tree, then count recursively.** Write a `count_all(node)` that descends into every child-category collection and sums at every level. Never trust a single node's own count field.
2. **Check the age of any cached export before using it.** If you are reading a saved export rather than a live fetch, check its timestamp against `index.max_age_days`. If it is older, tell the user and ask whether to refresh first. A stale export has previously reported stub articles that had already been deleted, which invalidated every downstream number in the report.
3. **Enumerate by category path, never by title shape.** Inferring an article's section from its title pattern misclassifies at scale. Walk the actual tree.
4. **Resolve the status codes from config, and enumerate all of them.** Set `docs.status_map` for your backend. Hosted knowledge bases use opaque integer codes, **more than one code commonly means "published,"** and an incomplete legend silently drops live articles from the count. An early version of this legend omitted the most common published state and would have reported most of the live corpus as unpublished. Classify every article you touch by this field. Never assume "exists" means "published."
5. **Count zero-length results and re-fetch them.** A throttled or failed request can return an error object that a naive loop records as a real article with no content. Those look identical to genuine stubs. Count them separately, re-fetch until the residual is zero, and report the residual if it is not.

### Step 1: Pull the full category and article tree

Fetch the whole tree for the version under audit. Expect a large payload that exceeds inline output limits and has to be written to a file. Read it back with the recursive counting approach above.

### Step 2: Classify every article

For every article, record: title, full category breadcrumb (not just the immediate parent), status resolved through `docs.status_map`, and its audience per `docs.audience_field`. Internal-only articles must not count toward client-facing gap totals, and must not be silently dropped either; report them as their own line.

Produce a scorecard:
```
Total client-facing articles: N
  Published: N (X%)
  Stubs: N (X%)
  Duplicate artifacts: N (X%)
Internal-only articles: N (excluded from client-facing totals)
Zero-length fetch residual: N, [0 expected; if not 0, the numbers above are low]
```

### Step 3: Identify stub clusters

Group stubs by category. Flag any category where stubs are a large share of that category's total content. These are "structured but never written" sections, and they are worth calling out as a cluster rather than as a long list of individual stubs, because the fix is one writing project rather than N.

### Step 4: Cross-reference support-ticket volume (optional, high value)

For prioritization rather than a raw gap count, query `issue_tracker.support_volume_query` for volume by topic or product area over a recent window, then match ticket-heavy topics against the gap list. A topic with **high ticket volume and a documentation gap** is a far stronger priority signal than a stub nobody has ever asked about. Report ticket counts per gap area alongside the stub counts so the reader can see the join.

### Step 5: Check for completely-absent topics

Some gaps have no stub at all: no article, no placeholder, nothing. These cannot show up in a stub count, so they need a different method. Either (a) cross-reference against a known feature or initiative list that says what articles should exist, or (b) use the support signal from Step 4 to surface topics with real reader questions and zero matching content. Report these separately from stubs. "Missing entirely" is a different and usually more urgent problem than "stub exists but unwritten."

## Output Format

```
## Docs Coverage Audit: [date]

### Scorecard
[totals as in Step 2]

### Stub Clusters (structured but unwritten)
- [Category path]: N stubs, [what is missing]

### Completely Absent Topics
- [Topic]: no article or stub found, [evidence: ticket volume / expected-article list]

### Support Signal Cross-Reference (if run)
- [Topic]: N tickets in [window], [gap severity: stub / absent / thin]

### Priority Order
1. [highest combined severity and ticket volume]
2. ...

### Method notes
Counted recursively: [yes]. Source: [live fetch / export dated X]. Status legend: [from config].
```

## Notes

- The recursive-counting rule exists because that exact mistake already happened and produced a wrong report that was believed. Do not skip the precondition to save time; the precondition **is** the skill.
- Read-only. Do not publish or create content here. Findings feed separate write work.
- If a prior audit report exists, read the most recent one first and ask whether the user wants a fresh audit or a delta against it. Re-running from scratch against a recent authoritative report wastes the effort and, worse, produces two documents that disagree.
- Always state the denominator. "14 gaps" means nothing; "14 gaps across 1,904 articles" is a finding.
