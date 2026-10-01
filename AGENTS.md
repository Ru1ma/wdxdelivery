# AGENTS.md — Mandatory Operating Protocol

This file governs every autonomous coding/analysis agent working in this repository.

## 1. Required reading order

Before changing code, read:

1. `README.md`
2. `business/REQUIREMENTS.md`
3. `business/WORK_STATUS.md`
4. `business/DECISIONS.md`
5. `docs/ACCEPTANCE.md`
6. `review/REVIEW_FEEDBACK.md`
7. `review/REVIEW_REQUEST.md`

If code, tests, data samples, historical outputs, or configuration are later added, inspect those before proposing a new algorithm.

If `review/REVIEW_FEEDBACK.md` contains unresolved findings, treat them as required work unless they conflict with a newer explicit business decision.

## 2. Source-of-truth hierarchy

When information conflicts, use this order:

1. Explicit business requirements in `business/REQUIREMENTS.md`
2. Verified raw input data and configuration
3. Verified current implementation behavior
4. Historical outputs and regression notes
5. Agent assumptions

Never silently promote an assumption to a business rule.

## 3. Non-negotiable reasoning order

The planner must reason in this order:

**station fixed → real geographic area recognition → postcode subareas → adjacent-area vehicle assignment → AM/PM continuity → within-vehicle road ordering → workload balancing → vehicle-reduction check**

Do not reverse this by optimizing stop order inside an already-bad vehicle assignment.

## 4. Geography rules

- Route numbers are labels, not geographic coordinates.
- Route 1 is not assumed near Route 2.
- “Prefer 1–2 Routes per vehicle” is a soft operational preference, not a hard cap.
- Two Routes may still be too far apart to share a vehicle.
- One large Route may be split across vehicles only by geographically continuous postcode/city subareas.
- Avoid multiple vehicles interleaving through the same area.
- Evaluate the full day, not AM and PM independently.
- Use road travel time/distance when available. Do not present postcode numeric order or straight-line distance as road distance.

## 5. Task-type rules

Normal deliveries count toward delivery-volume targets.

`Pickup` and `Redeliver`:
- must be scheduled,
- do not count as normal-delivery volume,
- still consume driving time and service time,
- still obey time-window constraints,
- still consume applicable weight/capacity,
- still count in completeness checks.

Pickup location must use the actual pickup address.

## 6. Hard constraints

Do not trade away:
- complete assignment of every task,
- zero duplicates,
- zero cross-station transfers unless a future explicit rule authorizes them,
- appointment/time-window feasibility,
- vehicle weight/capacity feasibility,
- workday-duration feasibility.

Parameters such as 900 kg vehicle weight, 12-hour workday, 30-minute loading, +25% road-time traffic buffer, and any 25-order cap are **provisional until verified from code/config/business evidence**.

## 7. No hard-coded regression tricks

Never hard-code:
- a specific order ID,
- a specific date,
- this sample's Route-to-city mapping as permanent truth,
- exceptions designed only to improve one historical workbook.

The algorithm must remain useful when Route numbers change while geography remains the same.

## 8. Evidence discipline

When reporting an improvement, show at minimum:
- task counts by type,
- missing/duplicate/cross-station counts,
- vehicle count,
- driving km/time,
- waiting time,
- total work time,
- longest/shortest vehicle workday,
- workload spread,
- geographic overlap/crossing observations,
- AM/PM continuity observations.

If a new result uses more vehicles or distance, explain why. Never label it “optimized” solely because tests pass.

## 9. Required update protocol after meaningful work

Before ending a task:

1. Update `business/WORK_STATUS.md` with:
   - completed work,
   - current baseline,
   - open problems,
   - next recommended step.
2. Append material decisions/assumptions to `business/DECISIONS.md`.
3. Address every applicable unresolved item in `review/REVIEW_FEEDBACK.md`, but do not delete reviewer history.
4. Update `review/REVIEW_REQUEST.md` with:
   - exact commit SHA(s),
   - files changed,
   - commands/tests run,
   - actual metrics/results,
   - known failures/limitations,
   - claims that still require independent review.
5. Do not erase historical failures merely because a newer version improves them.

## 10. Stop conditions

Do not package/release an EXE, ZIP, website build, or production artifact until:
- hard constraints pass,
- geographic/operational acceptance has been inspected,
- regression output is human-readable,
- release has been explicitly requested.

Local generation, website publication, and downloaded-production verification are separate stages and must be reported separately.
