# Independent Review Feedback

This file is reserved for reviewer findings after inspecting implementation commits, code, tests and regression outputs.

Implementation agents must **read this file before starting a new correction cycle** and must not erase unresolved reviewer findings.

## Current review status

NEEDS_CHANGES correction cycle independently re-reviewed.

Current disposition: **NEEDS_CHANGES**

The previous fleet-reduction and location-ID blockers are fixed. One new soft-objective/workload-balance blocker remains before the assignment stage can proceed to real-data acceptance work.

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

Disposition: **READY_FOR_NEXT_STAGE**

The baseline validator/diagnostic scaffolding is accepted as a development foundation only. Historical real-data, operational and release gates remain unresolved.

### 2026-10-01 — Automatic geography-first assignment milestone

Reviewed:

- implementation: `c1c56bf1fb8d7119aa4aed8c5d531d30b7e54c15`
- evidence handoff: `657e38297a80a831506f3d5e6e8969ed1ec82c94`
- reviewer baseline: `062f4787aba835e3102df6a55493b302d17b2216`

Evidence inspected:

- `wdxdelivery/planner.py`
- updated `wdxdelivery/baseline.py`
- `tests/test_planner.py`
- updated `tests/test_baseline.py`
- `docs/ASSIGNMENT.md`
- `.github/workflows/tests.yml`
- `business/WORK_STATUS.md`
- `business/DECISIONS.md`
- `review/REVIEW_REQUEST.md`
- paired synthetic evidence and implementation diff

No GitHub Actions run/status was present for the reviewed implementation SHA. The independent review therefore verifies the submitted code/test design and evidence claims, not a remotely reproduced CI pass.

#### What is accepted in this milestone

The implementation materially addresses the previous review:

- Route `0`, blank and missing labels are separated from informative Route metrics.
- Geographic thresholds are explicitly base-road minutes while scheduling/driving uses traffic-buffered minutes.
- Automatic station-fixed assignment now exists and ignores predeclared vehicle/subarea assignments.
- Working subareas are derived from city/postcode plus road relationships.
- Vehicle territories require connected area graphs and bounded whole-territory road diameter.
- Stop ordering checks appointments, service completion, dynamic Pickup load, capacity, workday and depot return.
- Contiguous-area ordering is tried before allowing reentry, and budget-limited search is not presented as an infeasibility proof.
- Low-utilization vehicles trigger real merge/redistribution attempts with blocker evidence.
- Workload balancing moves whole adjacent subareas only when spread improves and detour limits remain satisfied.
- The generated plan is revalidated by the independent baseline validator.
- Synthetic comparison reports tradeoffs honestly: km/driving/work improve while waiting and workday spread worsen.

These are meaningful improvements over the prior diagnostic-only stage.

#### Blocking issue 1 — fleet reduction is incorrectly gated by the low-utilization threshold

`reduce_fleet()` only considers donors where:

`self.schedule(g).report["low_utilization"] == True`

This means the planner can retain an unnecessary vehicle even when two adjacent vehicles can be merged with:

- valid geography,
- valid appointments,
- valid capacity,
- valid workday,
- acceptable driving detour,

simply because neither current vehicle falls below the configured low-utilization threshold.

That conflicts with the project objective to use fewer vehicles when a practical feasible merge exists. The low-utilization threshold may prioritize which vehicle to inspect first, but it must **not be the gate that decides whether fleet reduction is attempted at all**.

Concrete counterexample to add as a test:

- max workday = 600 min
- low-utilization threshold = 300 min
- two adjacent single-task vehicles
- individual workdays are approximately 300 and 320 min, therefore neither is "low utilization" under the current strict `< 300` rule
- a combined adjacent route is still feasible at or below 600 min

The current algorithm will not attempt the merge.

Required correction:

- run a general adjacent feasible-merge pass for all same-station groups, not only low-utilization donors;
- low-utilization may be used as a search priority / tie-breaker;
- fleet count reduction should be lexicographically preferred before workload fine-tuning, subject to geography and all hard constraints;
- retain the current explicit blocker evidence when a merge is rejected.

#### Blocking issue 2 — derived subareas can materially depend on opaque location ID ordering

`derive_subareas()` iterates:

`for loc_id in sorted(ids)`

and performs greedy complete-link packing into the first/best existing cluster.

The same geography can therefore produce different subarea membership when location IDs are renamed, even though road distances, city/postcode, tasks and appointments are unchanged.

Example shape:

- three locations in one city/postcode seed,
- A↔B and B↔C are within the subarea threshold,
- A↔C exceeds it.

Depending on which opaque ID sorts first, the greedy split can become {A,B}+{C} or {A}+{B,C}. With asymmetric task windows/loads that can materially change vehicle territories.

Route-number invariance is already tested; the same principle should apply to non-geographic opaque location IDs.

Required correction:

- make subarea derivation depend on road/geographic structure, not lexical location IDs;
- add an assignment-level test that arbitrarily renames location IDs and rewrites all references/arcs while preserving geography, then verifies materially equivalent territories/results.

A deterministic tie-break is still allowed for genuinely symmetric geography, but arbitrary database/order identifiers must not decide a materially different geographic partition.

#### Business acceptance gap 3 — normal-delivery AM targets are currently only reported

The business baseline specifies soft operational targets around:

- ordinary areas: about 5–6 normal morning deliveries,
- DEN HAAG dense areas: up to about 7,
- long-distance areas: often fewer according to travel/service time.

The current planner reports phase counts but does not use them as a soft assignment/order objective.

This is not a hard-constraint bug, but before real 343-task acceptance the planner needs a configurable soft mechanism so vehicle reduction does not create operationally undesirable morning concentration.

Required next-stage behavior:

- keep these targets soft, never override hard feasibility/geography;
- make them configurable by station/area rather than hard-coded magic values;
- report deviations and why a target was intentionally exceeded/underrun;
- test that geography/appointments can legitimately override the target.

#### Business acceptance gap 4 — AM/PM phase continuity is measured but not explicitly preferred

Actual appointment windows correctly remain the hard truth. However, where multiple schedules are equally feasible, the current scheduler objective prioritizes:

1. area reentries,
2. driving,
3. work,
4. waiting,

without a soft penalty for unnecessary PM-before-AM phase inversion or a large AM→PM handoff when another similarly efficient sequence avoids it.

Because the requirements explicitly ask to consider morning and afternoon separately while maintaining a coherent full day, add a soft phase-continuity preference where it does not conflict with appointments.

Do **not** turn phase labels into a hard universal rule; use them as an operational preference only.

#### Non-blocking observation — current 90-task scale check is useful but weak

The 90-task check is made by copying the same invented task pattern three times. It is useful as a smoke test for integrity, but it is not a meaningful stress test of geographic diversity or search behavior.

Before the 343-task regression, add at least one larger adversarial synthetic case with:

- multiple cities/postcode seeds,
- uneven station volumes,
- mixed Pickup/Redeliver,
- tight and flexible windows,
- one or more large Routes spanning subareas,
- Route 0/missing labels,
- several plausible merge choices,
- workload imbalance.

Track search nodes, bounded-query count, runtime class/order-of-growth evidence, vehicle count and integrity.

#### Required regression tests for the correction cycle

At minimum add:

1. two non-low-utilization adjacent vehicles merge when all hard/geographic constraints allow it;
2. fleet reduction still rejects that merge when appointment/capacity/workday/geography blocks it, with the blocker recorded;
3. arbitrary location-ID renaming does not materially change derived territories;
4. soft AM delivery targets influence tie-breaking but never violate geography/appointments;
5. avoid unnecessary PM-before-AM ordering when an otherwise equivalent coherent order exists;
6. the independent baseline validator still passes every generated feasible plan;
7. bounded-search uncertainty remains explicitly labeled and never becomes a false impossibility claim.

#### Real-data gates still unresolved

Do not claim any of the following yet:

- 343-task historical regression,
- real six-station Route/city/postcode behavior,
- actual road-quality validation,
- verified production parameter semantics,
- real vehicle-count/km improvement,
- operational route acceptance,
- production readiness.

#### Disposition

**NEEDS_CHANGES**

The assignment engine is now structurally promising, but the fleet-reduction gate is a core business-logic defect and location-ID-dependent subarea partitioning is an avoidable source of unstable geography.

Fix those before the next independent review. Continue using synthetic/adversarial tests while real private data remains unavailable. Do not package or release.

## Implementation handoff note — 2026-10-01

The implementation response for the automatic-assignment stage remains part of repository history. Its claims are superseded only where this independent review identifies gaps above.


## Implementation response — NEEDS_CHANGES corrections, 2026-10-01

Reviewer disposition above is preserved; independent approval is still pending.

1. General fleet reduction: all donors now checked; low-use sorting only. The
   300/320-minute counterexample merges to 600; separate capacity, appointment,
   workday and geography counterexamples retain vehicles with explicit blockers.
2. Road-structural subareas: complete-link agglomeration uses road profiles;
   ambiguous dispersed ties remain separate. Sixteen asymmetric and eight tied
   bijective location renamings preserve derived geographic membership and final
   task territories/metrics, including shuffled locations/arcs.
3. Soft AM targets: configurable station defaults and city/postcode overrides
   affect feasible merge/balance choices, exclude Pickup/Redeliver, and report
   deviation/reasons. Tests demonstrate assignment influence and hard geography/
   appointment priority; fleet reduction may exceed a target.
4. Soft AM/PM coherence: equivalent/similarly efficient feasible orders prefer
   fewer PM-before-AM pairs and smaller handoff. Tests cover equivalent driving,
   hard PM-first appointments, handoff ties and exhaustive driving-slack oracle.
5. Larger adverse fixtures: 104/208 uneven six-station tasks, multiple invented
   cities/postcodes, large/zero/missing Routes, varied weights/services, mixed
   tasks and tight/flexible windows. Fleet 23/44; nodes 4510/9990; bounded queries
   8/23; successful adjacent merges 8/1. Runtime one local run 0.0424/0.0870s.
   All modeled hard constraints and integrity pass; substantial imbalance remains.
6. Independent baseline, original tests, CLI failures and bounded-search honesty
   remain covered. 62 tests pass and correction evidence reproduces exactly.

Self-review: evidence generator initially referenced the wrong bounded-query
field; corrected to bounded_ordering_queries before generation. Historical
reports are preserved. AM handoff is an annotated road-matrix proxy; phase
preference and targets are scoped soft heuristics, not global optimality proofs.
Real-data/calibration/road/operational/CI gates from the Reviewer remain open.
Exact code SHA and verification commands are in the new REVIEW_REQUEST.


### 2026-10-02 — NEEDS_CHANGES correction re-review

Reviewed:

- implementation: `fb6ac2cc2dbd92f8d2b50c4de94bede6ef0c9d41`
- evidence handoff: `31a1a75c3bfdc5f5e87d2a0ee5c7af84864d1cee`
- reviewer baseline: `3fd6be15ee459749bed73e1eef4f6015150dbe23`

Disposition: **NEEDS_CHANGES**

The two previous blocking defects are materially corrected:

- fleet reduction now checks all same-station donors; low-utilization only prioritizes search order;
- subarea derivation no longer directly uses opaque location IDs to choose a greedy geographic partition, and location-renaming regression coverage is substantially improved.

The configurable AM Delivery target and soft AM/PM sequencing preference are also directionally correct: hard geography/appointments/capacity still dominate, Pickup/Redeliver remain outside the normal-Delivery target, and phase preference is bounded by explicit driving slack.

The 104/208-task diverse synthetic runs are useful development evidence. They remain synthetic, and no remote GitHub Actions run/status exists for the reviewed implementation SHA, so this review does not independently reproduce the reported 62/62 local pass.

#### Blocking issue — AM soft target can worsen workload balance without any bound

In `balance()`, a candidate move is accepted when:

`(target_delta, -improvement) < (0, 0)`

where `target_delta < 0` means the AM target improves and `improvement` is the reduction in station workday spread.

Because tuple comparison prioritizes `target_delta`, **any** target improvement is accepted even when `improvement` is strongly negative. Therefore a soft AM target can make station workload spread arbitrarily worse, provided geography/hard constraints and the driving-detour allowance still pass.

That conflicts with two project rules simultaneously:

- AM delivery counts are a **soft target**, not a dominant objective;
- workload should not become highly uneven merely to hit counts.

The large spread visible in the 104/208 synthetic evidence makes this important to constrain before real-data regression, even though the evidence does not prove that this exact condition caused those spreads.

Required correction:

1. Keep fleet-count reduction first and hard feasibility/geography non-negotiable.
2. For pure workload-balancing moves, do not allow AM-target improvement to cause unbounded spread worsening.
3. Add an explicit policy, for example either:
   - target improvement only among moves that do not worsen spread beyond a configurable tolerance; or
   - lexicographically minimize a documented combined soft cost with an explicit maximum spread-worsening bound.
4. Report when an AM target remains unmet because satisfying it would create unacceptable workload imbalance.
5. Add a regression test where a target-improving move would create a very large workday spread and verify that it is rejected; also test a small/tolerated tradeoff if such tradeoffs are allowed.

#### Additional cleanup before next review

`business/WORK_STATUS.md` still contains an older statement saying soft AM volume targets are “reported but not an optimization term,” while the current implementation does optimize against them. Update stale lower-stage text so repository status is internally consistent.

The remaining limitations are still correctly scoped: bounded search can miss better plans; real 343-task regression, road calibration, production configuration, operational geography review, remote CI and release acceptance remain unresolved.

Do not package/release yet.
