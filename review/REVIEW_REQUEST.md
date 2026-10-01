# Independent Review Request

## Status

Baseline tooling ready for independent review. No reviewer approval yet.

### Commit(s) to review

- Implementation SHA: 6be8123672a4dcdfd1b629544a55ae7e0440cd4d
- Branch: implementation/baseline-diagnostics
- Parent/baseline SHA: 2a8130277f60a3384aa7b92412d6271a0dcd2ed3
- This handoff is a subsequent documentation-only commit. Its parent is the
  exact implementation SHA above; review code/evidence at that immutable SHA.

### Goal of this change

Establish an explicit baseline validator and six-station geographic diagnostic
runner before designing assignment logic. No real input/config/matrix/source
was supplied after repository and local-directory inspection. This submission
therefore demonstrates reproducibility on invented data only.

### Files changed

- wdxdelivery/baseline.py, __init__.py, __main__.py: explicit JSON input validation,
  supplied-plan feasibility, task accounting, geographic and workload reports.
- tests/test_baseline.py: 21 targeted baseline tests including CLI exit behavior.
- examples/make_synthetic.py and synthetic.json: wholly invented six-station fixture.
- evidence/synthetic-baseline.json and .md: retained machine/human-readable results.
- docs/BASELINE_INPUT.md and README.md: schema, commands and model limitations.
- .github/workflows/tests.yml: tests and byte-for-byte evidence comparison.
- business/WORK_STATUS.md and DECISIONS.md: evidence state and interim assumptions.
- review/REVIEW_FEEDBACK.md: implementation handoff note, no reviewer history erased.
- review/REVIEW_REQUEST.md: this exact-SHA evidence handoff.

### Commands/tests actually run

From repository root:

    python3 examples/make_synthetic.py
    python3 -m unittest discover -s tests -v
    python3 -m wdxdelivery examples/synthetic.json --json evidence/synthetic-baseline.json --markdown evidence/synthetic-baseline.md
    python3 -m wdxdelivery examples/synthetic.json --json outputs/baseline.json --markdown outputs/baseline.md
    cmp outputs/baseline.json evidence/synthetic-baseline.json
    cmp outputs/baseline.md evidence/synthetic-baseline.md
    python3 -m compileall -q wdxdelivery examples tests
    git diff --check
    git diff --cached --check

21/21 tests passed on Python 3.12.14. Regenerated JSON/Markdown matched committed
evidence byte-for-byte. Invalid input/failing baseline/success CLI statuses
2/1/0 are tested. Staged privacy inspection confirmed only code/docs and
regenerated invented fixtures/reports, no private input, address cache or artifacts.
Cloud Git HTTPS access failed (proxy unavailable); connector reads and commits
were used. Remote CI execution is not claimed.

### Results — synthetic only

| Metric | Global |
| --- | ---: |
| Total tasks | 30 |
| Delivery | 18 |
| Pickup | 6 |
| Redeliver | 6 |
| Missing / duplicate / cross-station / unknown references | 0 / 0 / 0 / 0 |
| Supplied vehicles | 12 |
| Synthetic km | 1176 |
| Driving minutes (explicit test traffic multiplier) | 1764 |
| Waiting minutes | 1680 |
| Service / loading minutes | 300 / 180 |
| Total work minutes (including depot return) | 3924 |
| Longest / shortest / spread minutes | 358 / 296 / 62 |
| Modeled hard-constraint failures | 0 |

Every one of AMS, ROT, DEN HAAG, UTRECHT, TILBURG, BELGEM has identical invented
station totals: 5 tasks = 3 Delivery + 1 Pickup + 1 Redeliver; 2 vehicles; 196
synthetic km; 294 driving minutes; 280 waiting minutes; 50 service minutes;
30 loading minutes; 654 work minutes; longest/shortest/spread 358/296/62.
See retained reports for all original Route labels, city/postcode areas, stops,
phase counts, changing loads and per-vehicle evidence.

### Geographic-quality findings

- Route 1 alpha neighbors Route 5 beta (10 minutes), not Route 2 gamma
  (80 minutes). Missing and 0 Route labels remain descriptive.
- Six near vehicles deliberately retain alpha→beta→alpha→beta, two reentries each.
  These are reported flaws, not optimized results.
- No cross-region jumps or overlapping subarea ownership flagged in supplied fixture.
  Actual road-path crossings are not computed; absence of a flag is not acceptance.
- Six direct AM→PM transitions have 10-minute travel within adjacent areas.
  Far vehicles have PM only; no AM territory is fabricated.
- Six near vehicles flagged low-utilization: 296 minutes vs invented 300 threshold.
  Merge/redistribution search is not implemented; feasibility/impossibility not claimed.
- No vehicle has >2 known Route labels in supplied fixture. This is not a cap.
- Waiting is intentionally retained (280 minutes/station); no efficiency claim.

### Comparison to baseline

The parent had requirements only, no runnable plan or metrics. This adds a
reproducible diagnostic/validation capability; it makes no historical vehicle/km
improvement claim. The historical 343-task regression was not run because its
private workbook and road matrix are unavailable. No historical failures removed.

### Known limitations / unresolved questions

- No real operational baseline, road matrix or verified production config.
- Declared subareas/phases and nearest bidirectional road adjacency require
  inspection; the runner does not learn territories or geocode input.
- No automatic vehicle assignment, balancing, merge or redistribution.
- Acceptance tests for continuous splits, algorithm territory invariance,
  appointment-induced split/merge explanations and low-utilization merge remain
  pending a subsequent assignment implementation. Current renumbering tests
  establish diagnostic invariance only, not an assignment algorithm claim.
- Single-trip homogeneous weight-only load model; Redeliver unloads initial goods,
  Pickup increases load; service-completion windows are conservative assumptions.
- Coarse overlap/reentry/long-leg indicators do not detect all spatial crossings.
  Flexible tasks may interrupt direct AM→PM transition reporting.
- Every directed within-station location pair is required; incomplete matrices
  fail closed. Source provenance is explicit but not authenticated.
- Detailed real reports contain task IDs and must remain in ignored private paths.
- No EXE/ZIP/build/website release or production verification performed.

### Claims requiring reviewer verification

1. Route identifiers/postcode arithmetic never determine road adjacency.
2. Task completeness/cross-station failures cannot silently pass; missing matrix
   arcs fail closed; invalid station metrics are null rather than invented travel.
3. Pickup actual site, dynamic weight, waiting, service completion, traffic/loading
   and depot-return workday accounting match the documented interim model.
4. All committed data/evidence is invented and regenerates exactly.
5. Reporting clearly separates hard checks, synthetic geography and pending
   operational/assignment acceptance; retained geography flaws remain visible.
