---
name: leak-scan
description: "Sweep a document (or batch) for anything that should never be public: internal hostnames, credentials, encrypted-secret references, repo paths, employee names, customer names. Catches secrets before they cross from a ticket into a doc. Written after a single engineering ticket, pasted into a draft, turned out to contain an encrypted application secret, three internal URLs, and a customer name."
user_invocable: true
---

# Leak Scan

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Sweep a document (or batch) for anything that should never be public: internal hostnames, credentials, encrypted-secret references, repo paths, employee names, customer names. Catches secrets before they cross from a ticket into a doc. Written after a single engineering ticket, pasted into a draft, turned out to contain an encrypted application secret, three internal URLs, and a customer name.

## When to use this

Before publishing ANY article, especially one drafted from an engineering ticket or an internal wiki page, where internal detail lurks. A hard safety gate.

## Inputs

An article (slug or id), draft text, or a batch or category. If none, ask.

## What To Do

1. **Scan for each leak class:**
   - **Credentials and secrets:** encrypted-value wrappers such as `ENC(...)`, client secrets, API keys, bearer tokens, passwords, private keys, `clientId` / `clientSecret` pairs, connection strings
   - **Internal infrastructure:** internal hostnames and any host not on the public docs domain, environment-suffixed names (`*-qa`, `*-uat`, `*-internal`), IP addresses, ports, cloud account ids, resource ARNs, database connection detail
   - **Repo and code detail:** repository names, source file paths, fully-qualified class names, package structure, build artifact names
   - **People:** employee names, internal team member names, reviewer names left in a comment
   - **Customers:** any specific customer or account name. See [references/no-client-names.md](../../references/no-client-names.md)
   - **Ticket internals:** raw internal tracker keys presented to a customer, links to internal-only tickets or wiki pages
   - **Images:** screenshots showing any of the above, or unredacted record data. See [references/pii-redaction.md](../../references/pii-redaction.md)

2. **Match case-insensitively, then read every hit in context.** A case-sensitive sweep has produced a false all-clear before: the banned term appeared lowercased inside a URL. Equally, do not blind-replace, because customer and vendor names collide with ordinary words. Confirm each hit is a real leak before you touch it, and confirm each non-hit is really absent rather than merely differently cased.

3. **Rate severity.** Critical = credential, secret, or PHI. High = internal infrastructure or customer name. Medium = repo or code detail, employee name.

4. **Locate precisely.** Quote the exact offending text and where it appears, so it is easy to excise. Give the line or section, not just the file.

5. **Recommend the scrub.** For each hit, give the safe replacement or "remove entirely." Secrets are never reworded, they are removed. If a real secret was exposed, flag that it needs **rotation**, not just deletion. Deleting the text from the doc does not un-publish the value.

6. **Hard gate.** Any Critical finding means do not publish until it is removed. Say so unambiguously. Do not soften this into a recommendation.

## Output Format

```
## Leak Scan: [target], [date]

### CRITICAL (do not publish):
- [exact text]: [secret/PHI], REMOVE + [rotate if real]

### HIGH / MEDIUM:
- [exact text]: [class], [scrub to: ...]

Verdict: [clear to publish / BLOCKED on N critical items]
```

## Notes
- Critical findings are a publish blocker, full stop.
- A real exposed secret needs rotation, not just deletion from the doc. Flag it.
- Especially important for anything drafted from an internal ticket or wiki source. That is the direction leaks travel: inward-facing text gets promoted outward, and the promotion step is where nobody re-reads it.
- **A clean scan of a saved copy is not a clean scan.** If you are working from an export or a cached fetch, the result is frozen at the moment of the fetch and will report the same count forever. Re-fetch the candidates live before you clear them.
- Reported severity is about exposure, not about effort to fix. A one-character leak of a live token outranks a paragraph of internal jargon.
