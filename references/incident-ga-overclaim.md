# Incident: the availability overclaim

This is the incident several skills in this library were written in response to.
It is recorded here, de-identified, because a guardrail whose origin story has
been stripped out reads like arbitrary process and gets skipped.

## What happened

A release note described a platform-infrastructure upgrade (a database engine
version bump) in the present tense, as a shipped and supported capability. The
underlying work was real but internal: it had not been released to customers, and
no timeline had been committed. The note was published to the customer-visible
knowledge base and sat there for months.

A customer read it, reasonably concluded the capability was available to them,
and arrived at a scheduled review meeting with implementation questions. Nobody
on the documentation or product side was prepared for those questions, because
nobody had noticed the note said what it said.

## Root cause

Not "someone wrote it badly." The gap was structural: **nothing checked a
published note's claim against the release state of its source ticket.** A note
could describe internal work in shipped-capability language and pass every review
gate, because every gate was checking prose quality, not claim/state agreement.

The secondary cause is subtler and worth naming. The note was accurate about the
*engineering*. It was wrong about the *availability*. Those are different
assertions and the writing did not distinguish them.

## Response

Unpublish immediately, then reword under product and legal review rather than
unilaterally. A customer-facing claim that may already have been relied upon is
not a wording problem an author fixes alone.

## Standing defenses

- **`/steelman-this-note`** deep-reads a single note pre-publish, asking what a
  motivated reader could argue it promised.
- **`/redline`** applies the narrower contractual lens: warranty words, absolute
  quantifiers, forward commitments.
- **`/objection-forecast`** predicts the meeting questions a release will
  generate, so an availability question gets a prepared answer rather than an
  improvised one.
- **`/postmortem`** exists so the next incident also leaves a defense behind.

## The transferable lesson

Present tense is a claim about availability, not just about code. "Supports X"
and "will support X" and "has been built to support X" are three different
promises, and only one of them is usually true at publish time.
