---
name: source-backed-rfp
description: "Draft or audit RFP and capability responses using direct current documentation evidence, explicit partial support, and NO KB SOURCE for unsupported claims. Use for questionnaires, capability matrices, proposal answers, and any response where inference must not be presented as documented product support."
user_invocable: true
---

# Source-Backed RFP

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md), plus the two below, which are specific to evidence work.

Use direct evidence for every capability statement. Product architecture, a similar feature, an engineering ticket, or a plausible workflow is not proof that the requested capability is supported.

## Additional guardrails

- **Keep the two "no" answers distinct.** If the docs backend is unavailable or authentication fails, the answer is `NOT VERIFIED (NO ACCESS)`. Never convert an access failure into `NO KB SOURCE`. The first says you could not look; the second says you looked and it is not there. Collapsing them turns a broken connection into a confident negative, and a confident negative in an RFP is a statement about your product.
- **Verify audience scope before citing an article as customer-visible evidence.** Published is not the same as visible to external readers. Confirm the article's location is actually exposed to the external audience per `docs.audience_model`. Citing an internal-only article as public evidence is the same error as inventing it.

## When to use this

Any time a capability claim is going to leave the building with your name on it: an RFP response, a security or capability questionnaire, a compliance matrix, a proposal answer. Run it as the drafting method, not as a review pass afterward, because the failure mode is a plausible answer written from product knowledge and never traced to a source.

## Inputs

The questionnaire, capability matrix, or requirement list. If the source is a spreadsheet, take the whole thing rather than a sample; partial coverage in an RFP response reads as an answer.

## What To Do

1. **Parse the questions into one atomic capability per row.** A compound question ("does it support X and Y across Z?") gets split, because the honest answer is frequently different for each half and a single row forces you to pick one.
2. **Search the current corpus** using `docs.search_command`, and `docs.semantic_search_command` if you have configured one. A capability documented without its literal name will not turn up in a grep; note that as a search limitation rather than as an absence.
3. **Read the full candidate article, not a search snippet.** Snippets omit the sentence that scopes the claim, and that sentence is usually the reason the answer is PARTIAL rather than DIRECT.
4. **Record the article title, the reader URL from `docs.reader_url_template`, the relevant section, and the exact scope of support.**
5. **Classify the answer:**
   - `DIRECT`: the source explicitly answers the full question.
   - `PARTIAL`: the source supports only a stated portion. Describe the supported part and the unresolved part separately, in that order.
   - `NO KB SOURCE`: access worked, the relevant corpus was searched, and no direct source supports the claim.
   - `NOT VERIFIED (NO ACCESS)`: the evidence search could not be completed.
6. **Write only what the cited source supports.** Preserve explicit gaps for human follow-up. A visible gap gets answered by a subject matter expert; a gap smoothed over with plausible language gets signed.

## Hard rules

- Never infer support from architecture, adjacent modules, screenshots, implementation tickets, or general product knowledge.
- Do not turn a partial source into a full "Yes." This is the single most common failure, and it happens under deadline.
- Do not cite an authoring or editor URL where a reader URL is required.
- Do not include credentials, customer names, or internal-only implementation details.
- If a source is a draft, hidden, stale, or outside the external audience, say so. Do not present it as public evidence.
- This skill drafts and audits. It does not publish.

## Output Format

| Requirement | Status | Answer | Evidence | Gap or follow-up |
|---|---|---|---|---|
| [atomic capability] | DIRECT / PARTIAL / NO KB SOURCE / NOT VERIFIED (NO ACCESS) | [only what the source supports] | [title and reader URL] | [what a human must resolve] |

Finish with counts by status and a short list of questions requiring a subject matter expert or a product decision.

## Notes

- The status counts are the real deliverable for the reviewer. A response that is 60% DIRECT and 30% PARTIAL is a different document than one that is 90% DIRECT, and the person signing it should know which they have.
- If `NOT VERIFIED (NO ACCESS)` appears even once, say so at the top of the output, not only in the table. An access failure partway through a long matrix is easy to miss in a per-row column.

