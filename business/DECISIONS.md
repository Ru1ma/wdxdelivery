# Decision Log

Append new decisions chronologically. Do not rewrite history unless correcting a factual error, in which case record the correction.

## 2026-10-01 — Clean repository strategy

A new repository is being used so the replacement route planner can be designed without assuming the old assignment logic is correct.

Historical infrastructure may be reused when available, especially input parsing, Excel export, road-matrix/time calculation, packaging, and hard-constraint tests.

## 2026-10-01 — Geography-first architecture

Vehicle assignment quality is evaluated primarily by real geographic continuity subject to hard feasibility constraints. Route-number order is not a geographic signal.

## 2026-10-01 — “1–2 Routes” is soft

Prefer one or two genuinely adjacent Routes/subareas per vehicle, but do not impose an absolute two-Route cap that creates unnecessary vehicles or detours.

## 2026-10-01 — Separate normal-delivery quota from total tasks

Pickup and Redeliver must be scheduled and cost time/capacity, but do not count toward normal-delivery volume targets.

## 2026-10-01 — Review handshake

Implementation agents must update `review/REVIEW_REQUEST.md` after meaningful implementation/regression work. Independent review should inspect the stated commit SHA rather than relying on prose claims alone.

## 2026-10-01 — Baseline milestone with unavailable operational evidence

All available files were inspected. No source/config/workbook/matrix/private input
was present. Implement baseline validation and six-station diagnostics first;
do not invent real territories, parameters or historical regression results.
Invented six-station evidence is committed for reproducibility only. Automatic
assignment and merge search remain pending actual baseline evidence.

## 2026-10-01 — Explicit road/config evidence and conservative load/time model

Require explicit matrix provenance, operational parameters, task phases and
geographic subareas. Never derive geography from Route identifiers or postcode
arithmetic. Use directed road relationships in both directions for candidate
adjacency, report dispersed areas, and fail closed on missing arcs. Synthetic
and approximate inputs remain labeled even when modeled constraints pass.

Interim validator assumes one trip, a homogeneous weight-only fleet, all Delivery
and Redeliver goods loaded initially, Pickup loaded at its actual location,
service completed by appointment end, and return to the fixed depot included.
These are documented assumptions requiring operational verification, not new
canonical business rules. Explicit cap scope separates normal volume from tasks.

## 2026-10-01 — Preserve failed geography and scope acceptance claims

Synthetic baseline intentionally retains two area reentries per near vehicle
and six low-utilization flags. Hard checks passing does not erase those failures.
No merge search, impossibility, real road, historical improvement or operational
acceptance claim is made. Detailed real outputs remain private/ignored.

## 2026-10-01 — Reviewer supersedes waiting for real operational data

Reviewer commit 062f4787aba835e3102df6a55493b302d17b2216 approves baseline
scaffolding and explicitly requires immediate generic assignment development.
This supersedes the prior stage decision to defer assignment until actual data.
Real data still gates calibration, historical regression and business acceptance.

## 2026-10-01 — Informative Route audit and base-road geography policy

Route 0/missing/blank are non-informative, retained in raw distribution but
excluded from operational Route counts/distant-Route conclusions. The assignment
engine uses no Route labels in grouping or ties, making arbitrary renumbering
and zero/missing labels immaterial. More than two informative Routes remains
allowed and explained; the 1–2 Route preference is advisory.

Choose one explicit policy: geography thresholds/graph/diameter/reentry legs
use bidirectional base road minutes; scheduling and driving-detour costs use
traffic-buffered minutes. Config may explicitly confirm this policy, never
silently substitute buffered geography with the same threshold value.

## 2026-10-01 — Conservative derived territories and bounded search evidence

Derive city/postcode seeds and split by complete-link road spread. Area edges
require all cross-pairs close, and every vehicle has a connected induced area
graph and bounded whole-day road diameter. One close boundary pair is insufficient.
These provisional thresholds are explicit calibration inputs, not business truth.

Sequence within territories, try area-contiguous order first, and allow a merge
to introduce reentry only with exhaustive contiguous-order failure evidence.
Capacity/time windows still govern every task. Node-budget exhaustion is reported
without impossibility/optimality claims; nested ordering status propagates into
redistribution completeness. Balance whole adjacent subareas within a driving
allowance; low-use vehicles trigger actual merge/whole-location redistribution.

## 2026-10-01 — Paired synthetic evidence and retained tradeoffs

Preserve the first milestone files unchanged. New paired evidence explicitly
tightens invented AM windows to minute 180 for both supplied/automatic plans.
The supplied baseline remains feasible with identical prior metrics. Automatic
results reduce driving but increase waiting and spread; report both. Remaining
appointment-driven reentries and geographically blocked low-use cars are retained.
No historical/business improvement or release claim.

Self-review caught ambiguous delimiter-based subarea IDs; structured identities
remove collisions. A proposed Pickup redistribution counterexample did not block
all direct merges after delivery unload; it was replaced with a verified 140 kg
combined delivery vs 100 kg-capacity case. Final tests verify redistribution can
eliminate that vehicle by splitting its location blocks across neighbors.
