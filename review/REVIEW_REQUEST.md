# Independent Review Request

## Status

Automatic geography-first assignment/merge stage submitted for independent
review. Baseline approval at 062f4787aba835e3102df6a55493b302d17b2216 is preserved;
it does not approve this new algorithm or operational use.

### Commit(s) to review

- Implementation SHA: c1c56bf1fb8d7119aa4aed8c5d531d30b7e54c15
- Branch: implementation/baseline-diagnostics
- Parent/reviewer baseline SHA: 062f4787aba835e3102df6a55493b302d17b2216
- The subsequent handoff commit changes only this file; its parent is the exact
  implementation SHA above. Review code/tests/evidence at that immutable SHA.
- Prior baseline implementation/handoff: 6be8123672a4dcdfd1b629544a55ae7e0440cd4d /
  43ebc729c1739deee3ee58aa5aa83b2483a10a68.

### Goal and Reviewer requirement mapping

Implement generic assignment now, without waiting for real orders/matrices.

1. Route 0/missing/blank: raw audit distribution retained; informative Route
   counts/distant-Route findings corrected. Assignment never uses Route labels.
2. Traffic policy: all geographic thresholds use base_road_minutes; scheduling
   and detour costs use traffic-buffered minutes. Contradictory policy rejected.
3. Automatic engine: derives city/postcode road subareas, builds connected compact
   vehicles, preserves full-day geographic continuity and orders under constraints.
4. Compactness: complete-link seed splitting, all-cross-pair road graph links,
   whole-vehicle diameter and full-day driving-detour allowance; a close boundary
   pair alone cannot prove an acceptable territory.
5. Low use: actual adjacent merge/whole-location redistribution search and adjacent
   workload balancing; retained vehicles have observed blockers/search-scope status.

Item-by-item implementation response is appended to REVIEW_FEEDBACK.md without
altering reviewer history or inventing a new independent disposition.

### Files changed

- wdxdelivery/planner.py: automatic input normalization, derived subareas/graph,
  constrained bounded scheduling, packing/splits, balance, merge/redistribution,
  full-day territory evidence and CLI.
- wdxdelivery/baseline.py: informative Route semantics, explicit time policy and
  assignment decision rendering; still independently validates the generated plan.
- tests/test_planner.py: 26 assignment tests, adversarial territory/merge cases,
  CLI failures, small exhaustive oracle and 12 randomized five-task oracle cases.
- tests/test_baseline.py: original 21 tests retained plus 2 Reviewer correction tests.
- examples/make_assignment.py, generate_evidence.py, assignment-input.json:
  wholly invented automatic input and deterministic evidence regeneration.
- evidence/synthetic-baseline-v2.json/.md: corrected diagnostics, original v1 preserved.
- evidence/paired-baseline.json/.md, automatic-assignment.json/.md and
  assignment-comparison.json: human/machine-readable paired synthetic results.
- docs/ASSIGNMENT.md, BASELINE_INPUT.md, README.md: commands, schema and limitations.
- .github/workflows/tests.yml: definitions for unit checks, CLI evidence comparison
  and regeneration checks. Remote execution/pass is not claimed.
- business/WORK_STATUS.md, DECISIONS.md: stage, results, assumptions and next work.
- review/REVIEW_FEEDBACK.md: additive implementation response.
- review/REVIEW_REQUEST.md: this exact-SHA evidence handoff.

### Commands/tests actually run

From repository root on Python 3.12.14:

    python3 -m unittest discover -s tests -v
    python3 -m examples.generate_evidence
    python3 -m examples.generate_evidence --check
    python3 -m wdxdelivery examples/synthetic.json --json outputs/baseline-v2.json --markdown outputs/baseline-v2.md
    cmp outputs/baseline-v2.json evidence/synthetic-baseline-v2.json
    cmp outputs/baseline-v2.md evidence/synthetic-baseline-v2.md
    python3 -m wdxdelivery.planner examples/assignment-input.json --plan outputs/automatic-plan.json --json outputs/automatic-report.json --markdown outputs/automatic-report.md
    cmp outputs/automatic-report.json evidence/automatic-assignment.json
    cmp outputs/automatic-report.md evidence/automatic-assignment.md
    python3 -m wdxdelivery outputs/automatic-plan.json --json outputs/independent-validation.json --markdown outputs/independent-validation.md
    python3 -m compileall -q wdxdelivery examples tests
    git diff --check
    git diff --cached --check

49/49 local tests passed. Original baseline tests remain intact. Twelve randomized
five-task cases plus an explicit dynamic-load case are compared against complete
permutation enumeration. Generated JSON plan passes the existing baseline CLI
independently. New evidence regenerates byte-for-byte; old historical fixture/
evidence and reviewer history are verified unchanged. CLI success/failure/invalid
input statuses, distinct-path protection, missing arcs and Pickup site validation pass.

Additional scale command actually run (invented copies, not historical input):

    python3 - <<'PY'
    from copy import deepcopy
    from examples.make_assignment import automatic_fixture
    from wdxdelivery.planner import plan
    from wdxdelivery.baseline import analyze
    data = automatic_fixture()
    original = deepcopy(data["tasks"])
    data["tasks"] = []
    for copy in range(3):
        for task in original:
            task = deepcopy(task)
            task["id"] += f"-synthetic-copy-{copy}"
            data["tasks"].append(task)
    generated, report = plan(data)
    assert report["hard_constraints_pass"]
    assert analyze(generated)["hard_constraints_pass"]
    print(report["summary"], report["planning"]["search_nodes"])
    PY

90 invented tasks, 24 vehicles, zero missing/duplicate/cross-station failures;
246 ordering nodes, zero bounded queries. This does not validate 343-task
performance or real operational quality.

Staged privacy checks: source/docs/tests and regenerated invented evidence only;
no private input, identifying address cache, credentials or release artifacts.
Code commit tree is verified identical between local Git and GitHub connector.

### Actual results — paired synthetic comparison only

The paired input uses the same roads/tasks/config/time windows for both plans.
AM task windows explicitly end at minute 180; the supplied baseline remains
feasible with exactly its historical synthetic metrics. Original v1 evidence is
preserved under its original filenames.

| Metric | Supplied baseline | Automatic | Delta |
| --- | ---: | ---: | ---: |
| Tasks | 30 | 30 | 0 |
| Delivery / Pickup / Redeliver | 18 / 6 / 6 | 18 / 6 / 6 | 0 |
| Missing / duplicate / cross-station / unknown | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 |
| Vehicles | 12 | 12 | 0 |
| Synthetic km | 1176 | 1104 | -72 |
| Buffered driving minutes | 1764 | 1656 | -108 |
| Waiting minutes | 1680 | 1752 | +72 |
| Service minutes | 300 | 300 | 0 |
| Loading minutes | 180 | 180 | 0 |
| Total work minutes incl. depot return | 3924 | 3888 | -36 |
| Longest minutes | 358 | 358 | 0 |
| Shortest minutes | 296 | 290 | -6 |
| Spread minutes | 62 | 68 | +6 |
| Area reentries | 12 | 6 | -6 |
| Modeled hard-constraint failures | 0 | 0 | 0 |

Each station has 5 tasks (3 Delivery, 1 Pickup, 1 Redeliver), 2 final vehicles,
50 service + 30 loading minutes; zero missing/duplicate/cross-station failures.

| Station | Synthetic km before→after | Driving | Waiting | Work | Longest / shortest / spread after |
| --- | --- | --- | --- | --- | --- |
| AMS | 196→184 | 294→276 | 280→292 | 654→648 | 358 / 290 / 68 |
| ROT | 196→184 | 294→276 | 280→292 | 654→648 | 358 / 290 / 68 |
| DEN HAAG | 196→184 | 294→276 | 280→292 | 654→648 | 358 / 290 / 68 |
| UTRECHT | 196→184 | 294→276 | 280→292 | 654→648 | 358 / 290 / 68 |
| TILBURG | 196→184 | 294→276 | 280→292 | 654→648 | 358 / 290 / 68 |
| BELGEM | 196→184 | 294→276 | 280→292 | 654→648 | 358 / 290 / 68 |

Automatic staging begins with 18 subarea vehicles and performs six adjacent
merges to reach 12. No whole-location redistribution is needed in the six-station
sample; the dedicated counterexample eliminates a donor across two neighboring
vehicles when neither direct merge satisfies initial delivery capacity.

### Geographic/full-day/workload observations

- Route renumbering, zero/missing labels, shuffled input order and deliberately
  misleading supplied subarea/vehicle labels do not alter automatic territories.
- Vehicle territories are connected and bounded by whole-day road diameter.
  AM/PM maximum road spans and the strong working-area graph are reported.
- Six remaining near-vehicle reentries are justified by exhaustive contiguous-area
  search blocked by strict AM/PM appointments. Coarse geographic overlap and
  cross-region-jump flags are zero in this fixture; physical road crossing is unverified.
- Six near vehicles remain low-use (290 minutes vs invented 300 threshold).
  Direct merge and redistribution attempts report disconnected remote territories.
  The stated scoped search did not find a feasible merge; no global impossibility claim.
- Waiting rises because the shorter road ordering reaches strict PM windows earlier.
  Near workdays shorten by 6 minutes while remote workdays remain 358, widening spread.
  No distant areas are forced together to equalize hours.
- No sample vehicle has >2 informative Route labels; the separate targeted test
  permits three adjacent informative Routes with an explicit territory explanation.
- Pickup/Redeliver retain time/load/completeness cost and stay outside normal quotas.

### Self-review and retained failures/tradeoffs

- Fixed subarea-ID delimiter collision using structured geographic identities.
- Propagated nested ordering completeness into redistribution status.
- Corrected the proposed Pickup redistribution test assumption: unloading the
  delivery made one direct merge feasible. The final pure-delivery counterexample
  proves the intended 140 kg combined vs 100 kg capacity blockage and tests actual
  redistribution reduction.
- Original baseline geographic failures remain in immutable prior commits and
  original evidence. New evidence retains appointment reentries, blocked low-use
  vehicles, extra waiting and wider spread, rather than calling every metric improved.

### Known limitations / unresolved real-data gates

- No private real orders/road matrix/current verified production config supplied.
  Historical 343-task regression, real six-station geography, production parameter
  semantics and real km/vehicle improvement are not claimed.
- Greedy complete-link seed splitting/packing, conservative all-cross-pair adjacency
  and bounded search can miss feasible/better plans. Feasible outputs are checked;
  no optimal fleet, calibration or global infeasibility proof.
- Fixed common start, homogeneous unlimited-count single-trip weight-only vehicles.
  No fleet availability, reloads, multidimensional cargo or multi-day scheduling.
- Actual windows govern hard feasibility; supplied phase labels are descriptive.
  Soft AM normal-volume targets are reported, not optimized/hard-enforced.
- Soft 1–2 Route preference is advisory; labels do not participate in decisions.
- Coarse reentry/overlap/long-leg metrics cannot inspect actual traversed road geometry.
  Capacity/appointments/search limits may require shared coarse subareas or finer
  location/task splits; evidence marks the reason and completeness.
- Remote CI, independent algorithm/operational acceptance and production use
  remain unverified. No EXE/ZIP/website release or production artifact built.

### Claims requiring independent verification

1. All five Reviewer development/correction requirements are covered by final
   code and genuinely adversarial assignment-level tests, not only diagnostics.
2. Connectivity/diameter/full-day checks reject close-boundary and dispersed-chain
   counterexamples; Route IDs/0/missing labels cannot affect grouping.
3. Merge, redistribution and balance preserve completeness/station/appointments/
   dynamic load/workday and do not silently exceed the driving allowance.
4. Exact-vs-bounded ordering and redistribution status is honest; unavoidable
   reentries are supported by exhaustive contiguous-order evidence.
5. Reported paired metrics/tradeoffs reproduce on invented data only and privacy/
   historical review evidence is preserved. Real-data gates remain explicit.
