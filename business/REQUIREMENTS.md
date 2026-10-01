# Canonical Business Requirements

Last baseline update: 2026-10-01.

This document is the canonical project-level business specification. It should not be casually rewritten by an implementation agent. Amend it only when the user explicitly changes a business rule or when verified evidence corrects a factual statement.

## 1. Objective

Build a practical automatic dispatch planner for Netherlands and Belgium warehouse operations.

The target is not a complex mathematical optimization demo. The planner should behave like an experienced dispatcher:

1. understand what real areas each Route currently represents,
2. identify adjacent geographic areas and postcode subareas,
3. assign geographically coherent areas to vehicles,
4. preserve natural AM/PM continuity,
5. then order stops using actual road travel and appointment constraints,
6. then balance workload and check whether vehicles can be merged.

A vehicle should normally own one continuous operating territory, often one Route or two genuinely adjacent Routes. This is a preference, not a mechanical hard limit.

## 2. Stations

The planner must support all six business stations:

- AMS — Amsterdam
- ROT — Rotterdam
- DEN HAAG — The Hague
- UTRECHT — Utrecht
- TILBURG — Tilburg
- BELGEM — Belgium

Orders must remain inside their station unless an explicit future business rule says otherwise.

## 3. Terminology

**Station**: warehouse/business station to which an order belongs.

**Original Route List**: source-data regional label such as Route 1 or Route 5.

**Vehicle / delivery-group number**: output grouping such as AMS-1 or AMS-2. It must not be confused with the source Route number.

The current planning model historically treated one delivery group as one vehicle. If source data later contains a true multi-vehicle fleet/team structure, verify it before changing this assumption.

## 4. Geographic assignment rules

### 4.1 Learn geography before assigning vehicles

For every station, derive from current data:
- Route → cities/areas/postcodes,
- where those areas sit geographically,
- which Routes/subareas are actually adjacent,
- whether a Route itself contains distant subareas.

Route identifiers do not encode distance.

### 4.2 Form vehicle territories before sequencing stops

Prefer:
- one Route with adjacent postcode areas, or
- two truly adjacent Routes/subareas.

Do not:
- merge areas just because Route count is ≤ 2,
- assume Route 1→2→3 numerical adjacency,
- use workload balancing as a reason to cross distant areas,
- allow multiple vehicles to repeatedly interleave through the same district.

A large Route may be split across multiple vehicles when the split follows continuous postcode/city subareas.

If a vehicle must cover >2 Routes, report the reason and cost explicitly rather than silently weakening the rule.

### 4.3 Stop sequencing

After vehicle assignment:
- organize by postcode/city subarea,
- use road travel time for ordering and transitions,
- satisfy appointments,
- avoid obvious backtracking,
- normally finish one area before moving to the next.

Necessary backtracking caused by strict appointments is acceptable if reported.

Postcode numeric order is not a substitute for road distance. Straight-line distance must not be presented as road distance.

## 5. AM/PM logic

AM and PM may be considered as planning phases, but the vehicle's full day must remain geographically coherent.

Historical code classified appointments ending by 13:00 as AM and other tasks as PM. Treat that as existing implementation behavior, not permanent truth for all cross-period or flexible windows.

Operational delivery-volume targets:
- ordinary areas: roughly 5–6 normal deliveries per vehicle in the morning,
- DEN HAAG may reach about 7 due to higher geographic concentration,
- AMS and other longer-distance territories often remain around 5–6 depending on actual road/service time.

These are targets, not hard constraints.

PM tasks should preferentially continue near the vehicle's AM territory.

## 6. Delivery vs Pickup vs Redeliver

Normal deliveries count toward delivery-volume targets.

Pickup and Redeliver do not count as normal-delivery volume, but they:
- consume driving time,
- consume service time,
- obey appointments,
- consume applicable weight/capacity,
- remain part of full task-completeness checks.

Output must separately show:
- normal deliveries,
- Pickup count,
- Redeliver count,
- total task count.

Pickup must use the real pickup address.

## 7. Workload balance

Avoid extreme imbalance, but do not balance by forcing geographic detours.

Evaluate:
- normal-delivery volume,
- driving time,
- service time,
- waiting time,
- total work time,
- geographic continuity.

A long-distance vehicle may have fewer deliveries. A dense urban vehicle may have more.

For a very low-utilization vehicle:
1. try merging into a genuinely adjacent vehicle,
2. try redistributing within the same/adjacent territory,
3. if still required, report the blocking constraint.

Belgium deserves special scrutiny so a clearly underused extra group is not retained while others are busy.

## 8. Hard constraints

The planner must preserve:
- all tasks assigned,
- no missing tasks,
- no duplicate tasks,
- no cross-station reassignment,
- customer appointment/time-window feasibility,
- vehicle weight/capacity feasibility,
- maximum workday feasibility.

Historically observed configuration values that must be verified from current code/config before being treated as authoritative:
- 900 kg vehicle weight limit,
- 12-hour maximum workday,
- 30-minute loading time,
- road time +25% traffic buffer,
- historical maximum 25 orders per vehicle.

If a 25-order cap exists, verify whether it is defined on normal deliveries only or all tasks. Do not silently count Pickup/Redeliver against normal-delivery quotas.

## 9. Historical 343-task regression

These are historical regression facts, not permanent daily business volumes:

| Version | Main change | Vehicles | Total km |
|---|---|---:|---:|
| Original problem solution | crossing territories/backtracking/imbalance | 27 | 6633.1 |
| v17 | road clustering, cross-vehicle adjustment, quality checks | 26 | 6364.6 |
| v18 | simplified Route/postcode/AM-PM allocation | 24 | 6135.0 |
| v19 | inter-Route road ordering; separate delivery count | 24 | 6031.9 |
| v20 | strict max two Routes/vehicle | 31 | 6543.5 |
| v21 | workload adjustment on top of v20 | 30 | 6646.2 |

v21 passed extensive hard-constraint/testing work, but that does **not** prove operational geographic quality.

Known v21 facts from the historical sample:
- Belgium: 3 groups with 15 / 14 / 17 normal deliveries.
- Belgium work times about 11:09 / 11:51 / 11:40.
- Utrecht reduced from 5 groups to 4.
- Total 30 vehicles.
- All 343 tasks were accounted for.
- AMS and ROT still had unsatisfactory geographic partitioning/workload cases.

## 10. Known failure modes to prevent

1. Treating Route number order as geography.
2. Treating “≤2 Routes” as proof of geographic coherence.
3. Turning a soft 1–2 Route preference into a strict fleet-expanding cap.
4. Optimizing stop order before fixing wrong vehicle assignment.
5. Balancing hours/counts by destroying geographic continuity.
6. Treating test pass = business acceptance.

A documented AMS failure combined Route 9 Dronten with Route 2 Haarlem/Hoofddorp/Noordwijkerhout in one vehicle: only two Routes numerically, but geographically poor.

## 11. AMS sample geography — validation data only

For the historical 343-task sample, the observed AMS mapping was:

| Original Route | Main observed areas |
|---|---|
| 1 | Alkmaar, Heerhugowaard, Winkel, Kreileroord, Medemblik, Hoorn / Zwaag |
| 2 | Haarlem, Hoofddorp, Abbenes, Noordwijkerhout, Zandvoort, Vijfhuizen |
| 3 | Amsterdam Noord, Zaandam, Wormer, Krommenie, Purmerend |
| 4 | Heemskerk, Limmen |
| 5 | Amsterdam Nieuw-West and part of 1013 |
| 6 | Amsterdam centre, west, south |
| 7 | Amsterdam Zuid, Amstelveen, Uithoorn |
| 8 | Amsterdam Oost, IJburg, Zuidoost, Diemen |
| 9 | Weesp, Almere, Lelystad, Dronten |

Historical AMS sample totals:
- 94 tasks,
- 84 normal deliveries,
- 10 other tasks,
- 5 additional SheetRE tasks outside Route 1–9 classification.

Verified historical AMS station code for this sample: `20000136`.

Do **not** hard-code this mapping or station code as a universal permanent rule without current source-data/config evidence.

A diagnostic fixed-pool experiment used:
- Route 1 + 4
- Route 2
- Route 3
- Route 5 + 6
- Route 7 + 8
- Route 9

On the same road matrix it increased AMS from 8 vehicles / 1757.5 km to 10 vehicles / 1962.9 km. It was diagnostic only and was not a solved algorithm.

## 12. Other stations

ROT, DEN HAAG, UTRECHT, TILBURG, and BELGEM require the same Route/city/postcode/road-neighbor analysis as AMS.

For the historical Belgium sample, original Route values were all 0. Therefore Route 0 has no useful geographic meaning. Build territories from actual city/postcode/road geography, including relevant directions such as Zeeland, Antwerp, East Flanders, Brussels, etc., as supported by the actual data.

## 13. Required implementation sequence

1. Establish a trusted baseline from current source/config/tests/input.
2. Produce six-station Route → city → postcode and adjacency diagnostics.
3. Redesign vehicle assignment using geography-first logic.
4. Add targeted tests for geography invariance and task-type accounting.
5. Run the historical regression and produce human-readable per-station/per-vehicle checks.
6. Only after acceptance, package/release artifacts if requested.

## 14. Targeted tests required

At minimum test that:
- Route numbering does not determine adjacency.
- Renumbering Routes while keeping geography fixed does not materially alter vehicle territories.
- Two distant Routes are not merged merely because the count is two.
- Large Routes can split into adjacent postcode subareas.
- Pickup/Redeliver do not count as normal deliveries but still consume applicable time/capacity.
- missing/0 Route values are handled.
- AM/PM continuity is preserved.
- low-utilization vehicles are considered for geographic merge.
- strict appointments can justify otherwise undesirable splits and produce an explanation.
- task completeness, no duplicates, and no cross-station transfer always hold.

## 15. Release discipline

Testing, local packaging, website publication, and downloading/verifying the published package are separate stages.

Never claim a website/release is verified until the published artifact itself has been downloaded and checked.
