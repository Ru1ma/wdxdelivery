# Work Status

Updated: 2026-10-01

## Current stage

**Automatic geography-first assignment, stop ordering, workload balancing and
adjacent merge/redistribution implemented; synthetic/adversarial review pending.**

Baseline scaffolding was approved READY_FOR_NEXT_STAGE at reviewer commit
062f4787aba835e3102df6a55493b302d17b2216. That approval is not algorithm or
operational acceptance. Missing real data no longer blocks generic development.

## Completed this stage

- Read latest implementation-branch Review feedback and all mandatory documents.
  Main still contains only the original specification; work extends the reviewed branch.
- Corrected Route 0/missing/blank semantics: raw audit labels retained, informative
  Route metrics separate, non-informative labels excluded from distant-Route conclusions.
- Fixed geographic policy to base road minutes, explicitly reported and tested;
  scheduling/drive costs apply the traffic multiplier.
- Added automatic city/postcode road subareas, complete-link splitting of dispersed
  seeds, a conservative all-cross-pair area graph and connected bounded-diameter vehicles.
  Supplied vehicles/subarea labels are ignored.
- Added bounded area-contiguous scheduling with dynamic load, real Pickup site,
  service completion windows, loading, traffic, cap scope and return-to-depot.
  Appointment-required reentry is explicitly explained; budget misses are not proof.
- Added whole-subarea workload balancing, low-use adjacent merge, whole-location
  redistribution across multiple recipients, and explicit retained-vehicle blockers.
- Added generated-plan independent baseline validation, 49 passing tests, small
  exhaustive/randomized scheduling oracles and a 90-task synthetic scale check.
- Preserved original historical synthetic fixture/reports; generated new v2
  diagnostics, paired baseline and automatic reports/comparison. Evidence regenerates exactly.
- Updated CI definitions; no remotely reproduced CI pass claimed.

## Current synthetic evidence

30 invented tasks = 18 Delivery + 6 Pickup + 6 Redeliver; missing/duplicates/
cross-station/unknown references = 0/0/0/0. All modeled hard checks pass.
18 initial subarea vehicles become 12 after six adjacent merges.
12 final vehicles; 1104 synthetic km; 1656 driving minutes; 1752 waiting minutes;
300 service + 180 loading minutes; 3888 work minutes.
Longest/shortest/spread = 358/290/68 minutes.

Each of AMS, ROT, DEN HAAG, UTRECHT, TILBURG, BELGEM:
5 tasks = 3/1/1, 2 final vehicles, 184 synthetic km, 276 driving minutes,
292 waiting minutes, 50 service minutes, 30 loading minutes, 648 work minutes;
longest/shortest/spread = 358/290/68.

Paired comparison uses identical tasks/windows/roads/config for both plans.
The original supplied plan remains feasible under the explicit invented AM end
at minute 180: 12 vehicles / 1176 km / 1764 driving / 1680 waiting / 3924 work.
Automatic deltas: vehicles 0, km -72, driving -108, waiting +72, work -36,
spread +6. More waiting and wider spread reflect earlier arrival and the unchanged
remote territories; geography is not sacrificed to equalize hours.

Area reentries decrease 12→6. Each remaining near-vehicle reentry has exhaustive
appointment evidence. Six low-use near vehicles (290 < synthetic 300 threshold)
remain because remote recipient territory is disconnected under geographic policy;
redistribution is also tested and rejected in that stated scope.
No overlaps or cross-region jumps flagged in this fixture; this is not proof
against actual road-path crossings. Full-day territory graph/diameter and AM/PM
span are reported for every vehicle.

Additional invented scale run: 90 tasks, 24 vehicles, all hard checks and complete
assignment pass; 246 ordering search nodes, 0 bounded queries (not the 343-task regression).

## Open limitations / real-data gates

- Real/private 343-task workbook, six-station road geography and operational
  configuration remain unavailable. Historical parameter values remain unverified.
- Greedy complete-link seeds/packing and bounded sequencing/redistribution can
  miss a feasible/better plan. Search-scope failure is not global impossibility.
- All-cross-pair adjacency and diameter thresholds are conservative provisional
  policy, not calibrated business territory boundaries.
- Weight-only homogeneous single-trip model and fixed common start; no real
  fleet availability, reloads, multi-day or multidimensional capacity.
- AM/PM annotations are descriptive; appointments govern scheduling. Soft normal
  AM volume targets are reported but not an optimization term. Route preference
  remains advisory; informative labels never determine grouping.
- Overlap/reentry/long-leg indicators cannot detect every physical road crossing.
  Capacity/appointments can require shared coarse subareas or location splits,
  with reasons reported.
- Algorithm/operational geographic quality and remote CI require independent review.
- No release/EXE/ZIP/website or production verification performed.

## Next recommended step

Independently review this algorithm/evidence handoff. Continue adversarial search
quality work and calibrate conservative territory limits; do not wait for real data
to improve generic logic. When authorized private inputs/config/matrix become
available, import them outside Git, validate a trusted baseline, run real six-station
diagnostics and the 343-task comparison before operational acceptance or release.

## Review state

All five reviewer correction/development requirements are addressed in code and
synthetic evidence, with item-by-item response appended to REVIEW_FEEDBACK.md.
New assignment stage awaits independent disposition; REVIEW_REQUEST.md identifies
its exact implementation commit and evidence.
