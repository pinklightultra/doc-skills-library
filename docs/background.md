# Background

Back to the [skill list](../README.md).

## The problem

I write and maintain documentation for a knowledge base of roughly 1,900 articles. The work has a recurring shape: the same review, the same audit, the same checks before publishing, done by hand, slightly differently each time, and occasionally skipped on the day it mattered.

Most of these skills exist because something went wrong once. `/leak-scan` was written after an engineering ticket pasted into a draft turned out to contain an encrypted application secret, three internal URLs, and a customer name. `/institutional-amnesia-check` exists because a defense put in place after an incident quietly stopped running and nobody noticed for months. The failure history sits in the skill body as a rule, because a rule survives being skim-read.

The incident that taught the library to separate an accurate engineering note from an available product is written up in [references/incident-ga-overclaim.md](../references/incident-ga-overclaim.md). A release note described an internal database upgrade in the present tense. It was true about the engineering. It was false about availability. It sat on the customer-visible knowledge base for months, and a customer arrived at a review ready to implement it.

The library is a subset. The full set is 61 skills. These 21 are the ones whose logic is about documentation, rather than about one organization's tooling.

## Why this matters for tech writing

A documentation set of this size is a pipeline. The failure worth designing for is a gate that ran last month and did not run this month, a count that looked clean because the export was stale, or a sentence that was true about the engineering and false about availability. These skills make that pipeline explicit: the same checks, the same severity labels, the same report slots, and a diff against the previous run so a regression is the first line of the report.

That is the part of the work that can be made consistent, and the part that can be compared across articles and across weeks, without inventing a quality score nobody collected. Coverage priority joined to ticket volume, a decay ranking, and an RFP counted out as DIRECT, PARTIAL, NO KB SOURCE, and NOT VERIFIED are the comparisons the skills actually emit. `check.py` measures a narrower thing, and measures it for real: whether this library still matches its own contract. There is no study here of whether the skills produce better documentation than doing the work without them. Each skill encodes a mistake that already happened. That is the claim the files support.

## Where it was built

Built while running documentation for a healthcare SaaS platform: a knowledge base of about 1,900 articles, release notes on a fortnightly cycle, and a customer-facing portal where a mistake is visible to the people who pay for the product. The incident references are real incidents, genericized.
