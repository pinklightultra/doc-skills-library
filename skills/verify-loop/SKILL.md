---
name: verify-loop
description: Retrofit a codebase's testing setup to the verify-then-discard methodology (disposable per-change scripts, fresh browser contexts, real-state assertions, build-time enforcement) instead of a persistent test suite that rots unwatched
user_invocable: true
---

# Verify Loop

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Apply this methodology to the target codebase. Don't just describe it, actually do the work: inspect the current test setup, diagnose where it's stale/rotting/decorative, and fix it in place.

## Diagnosis first

Before writing anything, check for rot:
- Run the existing suite (if any) and read the actual failures, don't assume green
- Check when it last ran for real (log timestamps, CI history, git blame on test files): a suite untouched for weeks/months is already rotting even if it "should" pass
- Look for session-scoped or shared fixtures (browser, server, DB connection): these are the single point that turns one crash into a cascade of unrelated failures
- Look for assertions on decorative state (page titles, element existence) vs real state (actual data values, row counts, application state objects): decorative assertions create the illusion of coverage without verifying anything
- Check whether verification is wired into the thing that produces the artifact (build script, deploy step) or is a separate suite someone has to remember to invoke: if it's separate, that gap is where staleness lives

## Core method

1. **Disposable scripts over persistent suites for one-off verification.** When checking "does this feature work," write a throwaway script named for what it checks, run it immediately, read the output, fix or move on, delete it. Don't accumulate a `tests/` folder of scripts that outlive the feature they verified unless they're genuinely regression-worthy.
2. **Fresh isolation per run/test, not shared/session-scoped.** Browser instances, server processes, DB connections: scope them to the smallest unit that makes sense (per-test, per-script-run). A shared session-scoped resource means one crash takes out everything downstream of it in the same session. This is almost always the actual cause when a suite "was fine, then wasn't". Trace it back to a stale dependency (browser channel, API version, cert) under a fixture nobody re-validated.
3. **Assert on real state, not surface text.** Pull actual data: application state objects, DOM node counts, real row values, response payloads. Don't assert a title or that an element "is visible" and call it coverage.
4. **Error/exception listeners always on.** Console errors, uncaught exceptions, page errors: wire these into every verification run regardless of what's being tested. Bugs get caught by an uncaught exception surfacing in a log far more often than by a targeted assertion.
5. **Verify in the same breath you build, not on a separate cadence.** Wire smoke verification into the build/deploy script itself so a broken build can't ship silently. If verification is a separate suite someone has to remember to run, it will go unrun, and staleness (dependency drift, environment drift) will accumulate invisibly until something breaks for an unrelated reason months later.
6. **Read the actual output before declaring success.** Never assume a suite passed because it exited without visibly erroring: read pass/fail counts, read the failure messages, re-run after any fix to confirm green.

## Retrofit steps for an existing codebase

1. Run whatever test setup currently exists. Capture the real pass/fail state, don't trust cached assumptions about it.
2. If anything fails, diagnose the root cause (usually: stale dependency/fixture, not a real regression) and fix it before touching methodology.
3. Find and eliminate session/module-scoped shared fixtures for anything that can crash (browsers, long-lived connections). Convert to function-scoped or per-run isolation. Accept the runtime cost: isolation beats speed for a suite that runs occasionally.
4. Audit existing assertions for decorative vs real-state checks. Strengthen the decorative ones or flag them if strengthening isn't practical.
5. Confirm console/page error listeners exist in every browser-based test file. Add them if missing.
6. Find the build/deploy/publish script for the project. Wire the test suite (or a fast smoke subset) to run automatically as part of it, hard-failing the build on test failure. This is the step that actually prevents future rot. Everything else just fixes today's instance of it.
7. Re-run everything end to end once more after the retrofit to confirm the new setup is itself green.

## When NOT to build a persistent suite

If the user is asking to verify a single change or feature (not requesting a retrofit of test infrastructure), don't build persistent test files: write a disposable script per the method above, run it, report results, delete it. Persistent suites are for regression protection on stable surfaces, not for one-off verification during active development.

## Output Format

```
## Verify Loop: [target], [date]

### Baseline (before)
Suite exists: [yes/no] | Last real run: [date or unknown]
Result on invocation: [N passed / N failed / would not run (reason)]
Root cause of failures: [stale dependency / real regression / environment drift]

### Findings
| Issue | Where | Class |
|---|---|---|
| [shared session-scoped fixture] | [file] | cascade risk |
| [asserts element visibility only] | [file:test] | decorative assertion |

### Changes made
- [what was converted, wired, or strengthened]

### Verification wiring
Build/deploy script: [path] | Smoke subset wired in: [yes/no] | Hard-fails build: [yes/no]

### Result (after)
[N passed / N failed], re-run end to end: [green / still failing, why]
```

## Notes
- Read the actual pass/fail counts before declaring success. A process that exited 0 without printing a count has not told you anything.
- Most "it was fine, then wasn't" failures are a stale shared fixture, not a code regression. Diagnose before you refactor, or you will rewrite working tests to chase a dependency bump.
- Step 6, wiring verification into the build, is the only step that prevents future rot. Everything before it fixes today's instance.
- A decorative assertion is worse than no assertion, because it reports coverage that does not exist.
