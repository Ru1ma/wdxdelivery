# Work Status

Updated: 2026-10-01

## Current stage

**Initial reproducible baseline/diagnostic tooling complete on synthetic data.
Real operational baseline and assignment implementation remain pending.**

This is a baseline evidence milestone, not production routing acceptance.

## Completed

- Read all mandatory requirements, acceptance, privacy and Review files.
- Inspected every available repository file and local input directories: no legacy
  source/config, customer workbook, road matrices or historical outputs were supplied.
- Implemented standard-library JSON baseline runner and explicit input contract.
- Added six-station Route/city/coarse-postcode distribution, directed road-based
  candidate adjacency, distant/dispersed subarea and vehicle overlap/reentry diagnostics.
- Added task accounting, appointments, dynamic delivery/redelivery/pickup load,
  loading, traffic policy, return-to-depot, workday and explicitly scoped cap checks.
- Added per-vehicle, station/global metrics, supplied AM/PM geography/transitions,
  low-utilization and >2 Route flags; no hard Route-count limit.
- Added 21 passing tests, reproducible invented fixture/evidence, and CI configuration.
  Remote CI has not yet been run/verified.

## Current baseline

Invented six-station fixture only: 30 tasks = 18 Delivery + 6 Pickup + 6 Redeliver;
missing/duplicates/cross-station = 0/0/0; 12 supplied vehicles; 1176 synthetic km;
1764 driving minutes; 1680 waiting minutes; 300 service minutes; 180 loading minutes;
3924 total work minutes; longest/shortest/spread = 358/296/62 minutes.

Each station: 5 tasks (3/1/1), 2 vehicles, 196 synthetic km, 294 driving minutes,
280 waiting minutes, 50 service minutes, 654 work minutes. Hard checks pass
against invented parameters. Each near vehicle has two area reentries and work
296 < synthetic low-utilization threshold 300. These flaws are retained as evidence.
No overlap or cross-region jump is flagged in this fixture; this is not proof
against road-geometry crossing in real data.

## Open problems

- Real six-station operational input and trusted baseline are unavailable.
- The 343-task workbook, road matrix and legacy infrastructure are unavailable.
- Historical 900 kg / 12 hour / 30 minute / +25% / 25-order values remain unverified.
- Subareas and phases are explicitly supplied; geography learning/geocoding,
  automatic assignment, balancing and merge/redistribution search are not implemented.
- Full assignment acceptance tests (continuous splits, territory invariance,
  appointment split justification and merge feasibility) await that implementation.
- Nearest bidirectional road links are candidate adjacency, not proof of compactness.
  Reentry/overlap indicators do not detect every geometric crossing/backtrack.
- Conservative service-completion time-window semantics and single-trip
  homogeneous weight-only model need operational verification.
- Git HTTPS clone failed because the cloud environment proxy was unreachable.
  Source retrieval and authoritative commits use the GitHub connector; no bypass.

## Next recommended step

Keep real data private. Supply current station/depot/task/road/config evidence and
an ordered baseline in the documented contract; inspect the real six-station
diagnostics before implementing geographically continuous vehicle assignment.
Then add the remaining acceptance tests and run the historical regression when
available. Do not package/release until separate hard and operational review.

## Review state

Baseline tooling submitted for independent review with concrete evidence in
review/REVIEW_REQUEST.md. No independent approval or algorithm optimization claim.
