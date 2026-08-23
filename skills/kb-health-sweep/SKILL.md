---
name: kb-health-sweep
description: "Run the recurring knowledge-base health sweep: orchestrate the corpus-scale analysis and client-safety skills into one periodic pass, and write a dated report to the configured reports directory. This is the scheduled umbrella that ties the individual analysis skills together and computes a run-to-run delta."
user_invocable: true
---

# KB Health Sweep

> **Guardrails:** this skill inherits the shared rules in [GUARDRAILS.md](../../GUARDRAILS.md).

Run the recurring knowledge-base health sweep: orchestrate the corpus-scale analysis and client-safety skills into one periodic pass, and write a dated report to `reports.output_dir`. This is the scheduled umbrella that ties the individual analysis skills together.

## When to use this

On a schedule, or on demand for a full checkup. Individual skills answer one question. This runs the standing battery and produces a single prioritized report plus a delta against the previous run.

## Inputs

Optional: `--quick` (safety and decay only) or `--full` (everything). Default: the standard battery below. Optional scope (version, category), passed through to each child skill.

## What To Do

Run these in sequence, collecting each result. **Skip any whose backend dependency is unavailable and note the skip in the report rather than failing the whole sweep.** A sweep that aborts on its first missing dependency produces nothing; one that degrades produces a partial report plus an honest gap list.

0. **Preflight: index freshness. Do this first.** If you maintain a local index over the corpus, run `index.status_command` before anything else:
   - Command fails or reports not-ok: the last sync FAILED. Surface as a **P1 operational item**: "Index sync failing since [timestamp]: [error]. Every finding below may be stale." Include the error text.
   - Reports ok, but the timestamp is older than `index.max_age_days`: the scheduled job is not firing. Surface as **P2**: "Index last synced [timestamp], [N] days ago. Run `index.sync_command`."
   - Fresh: note "Index fresh (synced [timestamp])" and continue.
   - The point of this step is to make a dead sync job **loud** instead of silently serving stale data as if it were current. A sweep over a stale index reports the same findings forever and looks like a stable corpus.
   - If `index.status_command` is unset, say "no index configured; reading corpus live" and continue.

1. **Client-safety gates. Highest priority.**
   - `/leak-scan` in batch mode: secrets, internal hostnames, customer names, repo paths
   - `/steelman-this-note` on recently published client-facing notes: availability and commitment overclaims
   - `/redline` on anything describing capability, timing, or a guarantee

2. **Corpus health and drift.**
   - `/doc-decay-model`: articles predicted to go stale next
   - `/audit-docs-coverage`: stub clusters, absent topics, coverage against support demand

3. **Forward-looking watch. Slower cadence only.**
   - `/institutional-amnesia-check`: are the defenses from past incidents still active

4. **Synthesize, do not concatenate.** Merge everything into ONE prioritized action list. Concatenating child reports produces a document nobody reads, which defeats the purpose of running them together.
   - **P1, act now:** confirmed client-safety issues. A live overclaim, a leaked secret, a live article contradicting its source.
   - **P2, schedule soon:** high decay risk, high-volume coverage gaps.
   - **P3, cleanup:** terminology drift, minor gaps.
   - Deduplicate where several children flagged the same article. An article that three children flagged is one item with three reasons, not three items.

5. **Write the report.** Save to `reports.output_dir/kb-health-YYYY-MM-DD.md`. Pass the date in the invoking prompt; the runtime cannot read the clock. Also update `reports.output_dir/latest.md` as a rolling current-state snapshot.

6. **Diff against the last run.** Compare to the previous report: what is new, what is resolved, what is still open. Regressions matter most, because a P1 that reappears means a fix did not hold. **Lead the report with the delta**, not with the full inventory.

7. **Surface, do not fix.** This reports and prioritizes. It never edits or unpublishes on its own. P1 items are flagged for human action, and a client-facing safety change may need product and legal sign-off rather than an author's edit ([references/incident-ga-overclaim.md](../../references/incident-ga-overclaim.md)).

## Output Format

```
## KB Health Sweep: [date]  ([quick/standard/full])

### Since last sweep: [new P1s / resolved / regressions]

### P1, act now:
- [issue] ([skill that found it]), [article], recommended: [action]

### P2, schedule soon: ...
### P3, cleanup: ...

### Skills run: [list] | Skipped (dependency down): [list]
### Index: [fresh (synced X) / stale / sync failing / none configured]
### Report: [path] | Prior: [path]
```

## Notes
- Report and prioritize only. Never auto-edit or auto-unpublish. P1 safety items are for human action.
- If a backend is down, run what is possible and name the gap. Do not fail the whole sweep, and do not report a skipped check as a passed check.
- **The value compounds through the run-to-run diff.** A single sweep is a snapshot; the second one is where the signal starts. A P1 that returns after being fixed is the loudest thing this skill can tell you.
- This is why every skill this sweep invokes has a fenced, literal `Output Format` with bracketed slots: identical structure run over run is what makes the delta computable. If a child's output shape drifts, the diff degrades into prose comparison and the umbrella loses its whole reason to exist. It is also the constraint on adding a step here. Skills whose output is deliberately prose or conversational, such as `/house-style` and `/rubber-duck`, cannot be diffed this way and are not run from the sweep.
- Pass the current date in the invoking prompt. The runtime cannot read the clock.
