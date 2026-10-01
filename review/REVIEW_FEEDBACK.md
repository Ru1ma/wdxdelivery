# Independent Review Feedback

This file is reserved for reviewer findings after inspecting implementation commits, code, tests and regression outputs.

Implementation agents must **read this file before starting a new correction cycle** and must not erase unresolved reviewer findings.

## Current review status

Baseline/diagnostic milestone independently reviewed.

Current disposition: **READY_FOR_NEXT_STAGE**

This disposition approves only the baseline/diagnostic scaffolding as a foundation for further development. It does **not** approve routing quality, the 343-task regression, packaging, website publication, or production use.

## Review protocol

For each review cycle, the reviewer should record:

- reviewed commit SHA(s),
- evidence inspected,
- blocking correctness issues,
- geographic/operational issues,
- questionable assumptions,
- missing tests/evidence,
- non-blocking improvements,
- final disposition for that cycle: NEEDS_CHANGES / READY_FOR_NEXT_STAGE.

A disposition of READY_FOR_NEXT_STAGE means only that the reviewed scope may proceed. It does not automatically authorize packaging, website publication, or production deployment.

---

## Review history

### 2026-10-01 — Baseline/diagnostic milestone

Reviewed:

- implementation: `6be8123672a4dcdfd1b629544a55ae7e0440cd4d`
- evidence handoff: `43ebc729c1739deee3ee58aa5aa83b2483a10a68`
- parent baseline: `2a8130277f60a3384aa7b92412d6271a0dcd2ed3`

Evidence inspected:

- `wdxdelivery/baseline.py`
- `tests/test_baseline.py`
- `docs/BASELINE_INPUT.md`
- `.github/workflows/tests.yml`
- `business/WORK_STATUS.md`
- `business/DECISIONS.md`
- `review/REVIEW_REQUEST.md`
- synthetic evidence and commit diff

#### What is accepted in this milestone

The implementation correctly scopes itself as a **validator/diagnostic for a supplied plan**, not an optimizer. It does not falsely claim the synthetic fixture is real operational evidence.

The reviewed code has useful fail-closed behavior for missing road arcs, explicit task-type accounting, cross-station detection, appointment/service completion checking, return-to-depot workday accounting, Pickup load growth, separate normal-delivery cap scope, route-renumbering diagnostic invariance, area reentry/overlap indicators, and preservation of synthetic/approximate road provenance.

The 21 reported tests cover the intended baseline scope reasonably well. However, no GitHub Actions run/status was present for the reviewed implementation SHA, so the independent review confirms the code/test definitions and reported local result, **not a remotely reproduced CI pass**.

#### Required corrections before business-grade routing reports

1. **Route 0 / missing Route semantics**

   Raw Route distribution may continue to display `0` and missing labels, but `0` and missing Route must not be treated as meaningful geography for Route-count preference or Route-specific "distant route" conclusions.

   Current code counts Route `0` in `more_than_two_routes` and can include `0` / `(missing)` in `distant_routes`. This can produce misleading business diagnostics, especially for BELGEM where Route 0 is explicitly non-informative.

   Preserve the raw labels for audit, but separate **informative Route labels** from non-informative labels in operational quality metrics.

2. **Traffic-buffer semantics must be explicit and consistent**

   Scheduling/driving minutes apply `traffic_multiplier`, while adjacency, separation and cross-region-jump thresholds currently use raw matrix minutes.

   Before real-data routing, explicitly define whether adjacency thresholds operate on base road minutes or traffic-buffered minutes. Do not allow the same numeric threshold to mean two different travel-time concepts implicitly. Add tests for the chosen policy.

3. **Do not wait for real data before implementing the assignment engine**

   Missing real orders/matrices blocks calibration and final validation, but it does **not** block generic algorithm development.

   The next stage should immediately implement automatic geography-first assignment on synthetic/adversarial fixtures:
   - derive working subareas/territories from city/postcode + road relationships instead of requiring the final assignment to be predeclared,
   - create geographically continuous vehicle territories,
   - preserve AM/PM continuity,
   - order stops under appointments,
   - test low-utilization merge/redistribution,
   - explain unavoidable splits/reentries,
   - keep 1–2 Routes as a soft preference only.

4. **Do not use current candidate adjacency as sufficient proof of territory quality**

   `geography()` defines two subareas as candidate neighbors if at least one cross-pair is sufficiently close in both directions. That is acceptable for diagnostics, but a future assignment engine must not equate one close boundary pair with overall compactness.

   Use additional evidence when forming territories (dispersion, internal road spread, inter-area travel distribution/graph structure, full-day route effect, etc.).

5. **Low utilization must become a merge decision, not merely a fixed threshold flag**

   The current global `low_utilization_minutes` flag is acceptable as a diagnostic. In the assignment engine, low utilization must trigger an actual adjacent-merge / redistribution search and report the blocking constraint when no feasible merge is found.

#### Tests required in the next stage

Add assignment-level tests, not just diagnostic invariance:

- Route IDs are arbitrarily renumbered and vehicle territories remain materially the same.
- A large Route splits into continuous postcode/road subareas without interleaving vehicles.
- Two distant Routes are rejected even when that would satisfy a "two Routes" preference.
- Route 0 / missing Route cannot drive grouping decisions.
- A low-utilization vehicle is merged when geography + appointments + capacity allow it.
- A low-utilization vehicle remains separate when a concrete constraint blocks the merge, and that reason is emitted.
- Strict appointments can justify an otherwise undesirable territory split/reentry.
- AM/PM continuity is evaluated across the full vehicle day.
- Pickup/Redeliver remain outside normal-delivery quota while still affecting time/load.
- >2 informative Routes are allowed when geographically justified and explicitly explained.

#### Real-data gate

The following remain unverified and must not be claimed until real/private evidence is supplied and run:

- 343-task historical regression,
- real six-station Route/city/postcode distribution,
- actual road travel quality,
- historical production configuration (900 kg / 12 h / 30 min / +25% / 25-order semantics),
- real vehicle-count/km improvement,
- operational geographic acceptance.

#### Disposition

**READY_FOR_NEXT_STAGE**

Proceed directly to the automatic geography-first assignment/merge engine using synthetic and adversarial tests. Do not package or release. When real private input becomes available, run the existing validator plus the new assignment engine against it and submit a new `REVIEW_REQUEST.md` with exact metrics and commit SHA.

## Implementation handoff note — 2026-10-01

No unresolved reviewer findings were present at intake. Baseline tooling and
synthetic evidence were submitted for independent review; see REVIEW_REQUEST.md.
This note is an implementation status update, not an independent disposition.

## Implementation response — automatic assignment stage, 2026-10-01

The above reviewer history and READY_FOR_NEXT_STAGE disposition are preserved.
This response describes implementation work awaiting new independent review.

1. Route semantics: baseline raw distributions retain 0/missing/blank, while
   informative_routes and distant-Route findings exclude them. The automatic
   engine never uses Route labels for grouping/ties. Diagnostic and assignment
   tests cover zero/missing/renumbering and raw audit preservation.
2. Traffic semantics: explicitly choose base_road_minutes for all geographic
   thresholds/diagnostics/graph/diameter and traffic-buffered scheduling/costs.
   Reports expose the policy; a contradictory config policy is rejected. Tests
   vary the multiplier and verify the geographic graph/thresholds remain fixed.
3. Automatic engine: wdxdelivery/planner.py derives city/postcode road subareas
   and connected compact vehicle territories, schedules the full day, balances
   adjacent subareas and reduces fleet through actual merge/redistribution.
   It ignores predeclared vehicle/subarea assignments. Acceptance-level tests now
   cover territory invariance, large-Route splits, distant Route rejection,
   strict appointment splits/reentries, AM/PM, task types and >2 informative Routes.
4. Territory compactness: all-cross-pair graph links, complete-link seed splitting,
   whole-vehicle road diameter and full-day driving-detour checks supplement
   candidate adjacency. Counterexamples cover misleading close boundaries,
   connected-but-dispersed chains and dispersed city/postcode seeds.
5. Low utilization: attempts adjacent merges and whole-location redistribution
   across recipients, emitting concrete geographic/capacity/appointment/workday/
   count/detour blockers or budget-limited search status. Tests verify successful
   merge, blocked merge, redistribution reduction and neighboring workload balance.

49 tests pass locally; small exhaustive/randomized scheduling oracles and a
90-task invented scale check pass. New reproducible paired evidence retains six
appointment-required reentries and six geography-blocked low-use vehicles.
Exact implementation SHA, commands, metrics/tradeoffs and limitations are in the
new REVIEW_REQUEST.md. No remote CI, real 343-task regression, operational or
release acceptance claim; those original real-data gates remain unresolved.
