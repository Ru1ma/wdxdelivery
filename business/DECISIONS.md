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
