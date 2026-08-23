# Guardrails

Every skill in this library inherits these five rules. In the source library 55 of
61 skills carried their own copy of them, and the copies had drifted: only one pair
was identical. They live here once instead, and each `SKILL.md` points at this file.

- **Default audits and reviews to read-only.** Do not edit, publish, reorganize,
  or change any knowledge-base article or issue-tracker record unless the user
  explicitly requests that action.
- **Gate every write behind a shown diff and a confirmation.** Before any edit,
  publish, or reorganization, show the proposed change and obtain clear
  confirmation. Verify the audience scope of the target location, and verify the
  live reader result after an approved write.
- **Parse structurally, never by regex.** Use a real JSON or HTML parser over
  API payloads and article bodies. A regex over a raw payload silently matches
  the wrong thing and reports it as fact.
- **Never expose credentials, tokens, customer names, PII, or PHI.** Keep
  client-facing drafts generic. Stop when source evidence is missing rather than
  filling the gap with a plausible value.
- **Treat fixed paths and dated examples as historical context.** Resolve the
  current paths and connected services from `config.yml` before acting, rather
  than trusting a path baked into a skill body.

## Three error-handling idioms

These are the failure conventions the skills share. They matter more than any
individual step list.

1. **Degrade rather than fail.** If one dependency of a multi-step sweep is
   unavailable, run the rest and record the skipped step in the report. An
   umbrella skill that aborts on its first missing backend produces nothing; one
   that degrades produces a partial report plus an honest gap list.
2. **Absence of evidence is not evidence of absence.** A 404, an auth failure, or
   an empty search result means *unverifiable*, not *no problem found*. These
   states get distinct labels (`NOT VERIFIED (NO ACCESS)` versus `NO KB SOURCE`)
   precisely so a broken connection can never be read as a clean bill of health.
3. **Hard stop over confident guess.** If a lookup for a config value, field
   name, or navigation path finds nothing, stop and hand the question to the
   human. Do not emit a `[CONFIRM]` placeholder and continue; placeholders get
   published.

## Write ritual

Any skill that writes follows the same four beats, in order: **dry run, show the
diff, confirm, verify the live result.** Skipping the fourth beat is the common
failure. A write that returned HTTP 200 is not a write you have seen.
