# Policy: no customer names in published documentation

**Rule.** No specific customer, client, or account name appears in any published
article, release note, screenshot, or client-facing draft. Not as an example, not
as an attribution, not in a "as requested by" note, not in an image.

**Why it is absolute.** A named customer in a shared knowledge base tells every
other reader three things you did not intend to publish: who your customers are,
which of them asked for a given feature, and by implication which of them do not
have it. In a regulated industry that last inference is the expensive one.

**What to write instead.** Restructure so the customer is not the subject.

| Instead of | Write |
|---|---|
| "Added at Example Health's request" | "Added to support multi-tier appeal routing" |
| "Configured for Example Health" | "Configured per client, see the client configuration table" |
| "Example Health uses the daily batch" | "Clients on the daily batch schedule" |

**Internal versus published.** An internal notification list, a ticket, or a
distribution decision may name the account. The moment the text is destined for a
published surface, the name comes out. Skills that produce both kinds of output
(`/who-needs-to-know`) must keep the two halves separate and say which is which.

**Scanning caveat.** A case-sensitive grep is not a check. Neither is a
substring grep: real customer names collide with ordinary English words, so a
blind search-and-replace will corrupt innocent prose while a case-sensitive one
will miss the lowercase hit in a URL. Match case-insensitively, then read every
hit in context before editing it.
