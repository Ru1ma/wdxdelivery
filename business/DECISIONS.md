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
