# Independent Review Request — NEEDS_CHANGES corrections

## Exact review scope

- Implementation SHA: fb6ac2cc2dbd92f8d2b50c4de94bede6ef0c9d41
- Branch: implementation/baseline-diagnostics
- Reviewer parent: 3fd6be15ee459749bed73e1eef4f6015150dbe23
- Subsequent handoff commit changes only this file and directly parents the exact
  implementation above. Independent disposition remains pending; prior Reviewer
  NEEDS_CHANGES and baseline approval are preserved, not overridden.

## Changes and Reviewer mapping

1. planner.py now checks feasible adjacent merge/whole-location redistribution
   for all vehicles, prioritizing low use without gating eligibility. Fleet
   reduction precedes soft workload tuning and is checked again after balancing.
   The 300/320-minute example merges to 600; hard blockers still retain vehicles.
2. Road-profile complete-link agglomeration replaces opaque location-ID seed
   ordering. Ambiguous competing tied edges remain separate when their union
   violates diameter. Bijective renaming tests inspect actual geographic membership,
   task assignment and metrics under asymmetric attributes and symmetric road ties.
3. Optional station/area AM normal Delivery targets influence soft choices,
   exclude Pickup/Redeliver and report deviation/reasons. Fleet count and hard
   geography, capacity, workday and appointments take priority.
4. Configurable driving slack allows soft phase coherence among similarly
   efficient minimum-reentry orders: PM-before-AM pairs, road handoff, then time
   costs. Actual appointments can force PM first. Full permutation oracle checks
   this objective; no hard universal phase rule introduced.
5. Diverse invented 104/208-task fixtures cover unequal six-station workloads,
   multiple cities/postcodes, separated territories, mixed task types, service/
   cargo variation, tight AM/delayed PM/flexible windows and large/zero/missing
   Route labels. Search caps and retained imbalance remain visible.

Changed files: wdxdelivery/planner.py; tests/test_review_corrections.py;
examples/make_stress.py, generate_evidence.py, correction-input.json;
evidence/automatic-correction.json/.md, correction-comparison.json,
diverse-scale.json; docs/ASSIGNMENT.md; README.md; CI workflow;
business/WORK_STATUS.md, DECISIONS.md; additive REVIEW_FEEDBACK response.
Original assignment/paired/baseline evidence is unchanged. No private inputs,
address cache, credentials or release artifacts are included.

## Verification actually completed

Python 3.12.14, repository root:

    python3 -m unittest discover -s tests -v
    python3 -m examples.generate_evidence
    python3 -m examples.generate_evidence --check
    python3 -m wdxdelivery examples/synthetic.json --json outputs/baseline-v2.json --markdown outputs/baseline-v2.md
    cmp outputs/baseline-v2.json evidence/synthetic-baseline-v2.json
    cmp outputs/baseline-v2.md evidence/synthetic-baseline-v2.md
    python3 -m wdxdelivery.planner examples/correction-input.json --plan outputs/correction-plan.json --json outputs/correction-report.json --markdown outputs/correction-report.md
    cmp outputs/correction-report.json evidence/automatic-correction.json
    cmp outputs/correction-report.md evidence/automatic-correction.md
    python3 -m wdxdelivery outputs/correction-plan.json --json outputs/correction-independent.json --markdown outputs/correction-independent.md
    python3 -m compileall -q wdxdelivery examples tests
    git diff --check
    git diff --cached --check

62/62 tests pass, including original independent baseline, completeness/load/
appointments, CLI failures, reentry proofs and bounded-search uncertainty tests.
New tests cover general fleet reduction and four blocker classes, 24 location-ID
renamings, target influence/overrides/exclusions/hard priorities, phase inversion/
handoff/appointments and exhaustive slack objective. Both scale outputs are
independently baseline-validated. Evidence reproduces byte-for-byte; historical
files have no staged changes. Staged privacy inspection completed. Implementation
Git tree verified identical locally and on GitHub: 3470e82d5a6b54c1394a3e3ea0cabd6e1e467ef8.
Remote CI execution/pass is not claimed.

Runtime measurement command actually run:

    python3 - <<'PY'
    from time import perf_counter
    from examples.make_stress import stress_fixture
    from wdxdelivery.planner import plan
    for scale in (1, 2):
        start = perf_counter()
        _, report = plan(stress_fixture(scale))
        print(104 * scale, round(perf_counter() - start, 4),
              report['planning']['search_nodes'],
              report['planning']['bounded_ordering_queries'])
    PY

## Actual invented-data results

| Tasks | Vehicles | km | Driving | Waiting | Service | Work | Longest / shortest / spread | Nodes | Bounded queries | Adjacent merges | Local seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 104 (64 Delivery, 22 Pickup, 18 Redeliver) | 23 | 1092 | 2620.8 | 2008 | 915 | 5658.8 | 429.6 / 42.2 / 387.4 | 4510 | 8 | 8 | 0.0424 |
| 208 (127 Delivery, 41 Pickup, 40 Redeliver) | 44 | 2157 | 5176.8 | 4911.8 | 1837 | 12145.6 | 393.6 / 69.2 / 324.4 | 9990 | 23 | 1 | 0.0870 |

Both: zero missing/duplicates/unknown/cross-station; modeled hard checks pass,
all final territories connected. Scale evidence is a growth check, not a paired
fleet improvement claim; task attributes vary with growth, not copied identical
six-station templates. Large workload imbalance remains; observed runtimes are
one local run, not calibrated performance guarantees.

Paired 30-task comparison remains: vehicles 12→12; km 1176→1104;
driving 1764→1656; waiting 1680→1752; service 300→300; work 3924→3888;
longest 358→358; shortest 296→290; spread 62→68; area reentries 12→6.
All integrity counts zero; Pickup/Redeliver remain fully scheduled. Six reentries
have exhaustive appointment evidence. Waiting/spread regressions are retained.
Full-day continuity, AM target deviations and phase costs appear in correction
JSON/Markdown. Road-path crossings cannot be inferred from pairwise matrices.

## Self-review and limitations

- Fixed evidence generator's initial wrong bounded-query field before generation.
- Location-ID invariance does not imply task-ID invariance for final symmetric
  ordering ties. Conservative ambiguous clustering can retain extra vehicles.
- Targets are optional heuristic penalties; multiple area overrides use the
  smallest upper target. Config semantics need real-business calibration.
- Phase handoff skips flexible annotations and uses bidirectional base-road cost;
  it is a proxy, not actual traversed geometry. Search cap limits objective quality.
- Greedy packing/conservative adjacency/bounded ordering and redistribution may
  miss feasible or better plans. Retained blockers are scoped observations;
  bounded misses never prove global infeasibility or minimum fleet.
- Homogeneous unlimited-count weight-only single-trip vehicles, common start;
  no reloads, multidimensional cargo, fleet availability or multiday operation.
- Private 343-task regression, real roads/six-station geography, production
  config, actual km/fleet improvement, operational acceptance and remote CI
  remain unverified. No packaging, release or production readiness claim.

Independent review requested: validate all NEEDS_CHANGES mappings, road-structural
invariance, soft-policy priority, general merge blockers, bounded-search honesty,
privacy/history preservation and reproducible evidence at the exact code SHA.
