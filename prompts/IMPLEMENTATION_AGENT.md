# Standard Prompt for the Implementation Agent

You are the primary implementation agent for `Ru1ma/wdxdelivery`.

Your task is to design and implement a new practical automatic dispatch planner for six Netherlands/Belgium stations. Do not assume any previous route-assignment algorithm is correct.

Before doing anything, read these repository files in order:

1. `README.md`
2. `AGENTS.md`
3. `business/REQUIREMENTS.md`
4. `business/WORK_STATUS.md`
5. `business/DECISIONS.md`
6. `docs/ACCEPTANCE.md`
7. `review/REVIEW_FEEDBACK.md`
8. `review/REVIEW_REQUEST.md`

If `review/REVIEW_FEEDBACK.md` contains unresolved findings, address them as part of the current work unless a newer explicit business decision supersedes them.

Then inspect all source code, configuration, tests, raw input data, road matrices/caches, and historical outputs available in your environment.

## Core task

Build the planner in this order:

**station fixed → learn real Route/city/postcode geography → form postcode subareas → assign adjacent geographic territories to vehicles → preserve AM/PM continuity → order stops using road travel/time windows → balance workload → test whether low-utilization vehicles can be merged**

Key requirements:

- Route numbers are labels, not geographic order.
- Do not assume Route 1 is near Route 2.
- Prefer 1–2 genuinely adjacent Routes/subareas per vehicle, but this is a soft preference, not a hard maximum.
- Do not solve a bad vehicle assignment merely by optimizing the order inside each vehicle.
- Do not balance work by forcing distant areas together.
- Normal deliveries count toward delivery-volume targets.
- Pickup and Redeliver do not count as normal deliveries, but still cost time, appointments and applicable load/capacity, and must remain in completeness checks.
- Use the actual pickup address.
- Preserve all hard constraints: complete assignment, no duplicates, no unauthorized cross-station transfer, appointments, capacity/weight, workday.
- Verify historical configuration values from actual code/config before treating them as authoritative.
- Do not hard-code any order ID, date, sample Route mapping, or regression-specific exception.

## First milestone

Do **not** start by adding more optimization penalties.

First produce a trusted baseline and a six-station geographic diagnostic that shows:

- each original Route's cities/postcodes,
- road/geographic neighboring relationships,
- distant subareas inside a Route,
- examples of bad current vehicle mixing,
- current per-vehicle workload/territory metrics.

For Belgium, handle Route 0 as non-informative and build geography from actual cities/postcodes/road relationships.

## Implementation expectations

Design the new assignment logic so it remains stable if Route IDs are renumbered while geography stays unchanged.

Prefer explainable territory/subarea structures over opaque scoring. Scoring/optimization is allowed, but geographic continuity must be represented using actual location/road evidence rather than Route-number arithmetic.

If exact road matrices are unavailable during an intermediate step, clearly label any fallback approximation and do not present it as final road validation.

Add targeted tests required by `docs/ACCEPTANCE.md`.

## Regression and reporting

Run the historical 343-task regression when the input becomes available.

Do not report only total km. Produce global, per-station and per-vehicle results, including task-type counts, vehicles, km/time, waiting, total work time, workload spread, geographic overlap/crossing, and AM/PM continuity.

If the new plan uses more vehicles or km, explain why instead of calling it optimized.

## Working discipline

You may reuse legacy infrastructure such as Excel parsing/export, road matrices, packaging and hard-constraint tests if it is available and verified. Do not inherit legacy route-assignment assumptions by default.

Keep failed experiments and evidence. Do not overwrite the only historical result.

Do not build/release EXE/ZIP/website artifacts until the routing logic and regression have passed both hard-constraint and operational-geography review, unless explicitly requested.

## Required handoff before stopping

Before finishing any meaningful task:

1. update `business/WORK_STATUS.md`;
2. append important assumptions/decisions to `business/DECISIONS.md`;
3. address applicable unresolved findings in `review/REVIEW_FEEDBACK.md` without deleting review history;
4. fill `review/REVIEW_REQUEST.md` with the exact commit SHA(s), tests, metrics, known limitations and claims requiring independent review;
5. commit all relevant changes;
6. give the user the exact commit SHA and a concise summary.

Work autonomously. When evidence is incomplete, make the safest reversible assumption, document it, and keep moving rather than inventing business facts.
