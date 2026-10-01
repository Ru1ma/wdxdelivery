# Acceptance and Verification Standard

Passing unit tests is necessary but not sufficient.

## Layer A — Data integrity

For every run report:
- total tasks,
- normal deliveries,
- Pickup,
- Redeliver,
- missing,
- duplicates,
- cross-station transfers.

Acceptance target:
- missing = 0,
- duplicates = 0,
- unauthorized cross-station transfers = 0.

## Layer B — Hard feasibility

Verify per vehicle/task:
- appointment/time-window feasibility,
- weight/capacity,
- maximum workday,
- required loading/service time,
- traffic-buffer policy,
- any verified order-count rule.

Do not assume historical parameter values until current config/source confirms them.

## Layer C — Geographic quality

For every station inspect:
- Route → city → postcode distribution,
- actual neighboring subareas,
- distant subareas inside one Route,
- per-vehicle continuous territory,
- multi-vehicle overlap/interleaving,
- obvious cross-region jumps,
- obvious backtracking.

A vehicle with only two Routes can still fail this layer.

## Layer D — Full-day continuity

Per vehicle show:
- AM territory,
- PM territory,
- transition between them,
- whether PM continues near AM,
- any large repositioning and why it is required.

## Layer E — Workload quality

Per vehicle show:
- AM normal deliveries,
- PM normal deliveries,
- total normal deliveries,
- Pickup,
- Redeliver,
- total tasks,
- km,
- driving time,
- service time where available,
- waiting time,
- total work time.

Per station show:
- number of vehicles,
- longest workday,
- shortest workday,
- workload spread,
- low-utilization vehicles and merge analysis.

Do not equalize workload at the cost of major geographic detours.

## Layer F — Fleet-efficiency check

For every low-utilization vehicle:
1. test whether its tasks can merge into an adjacent territory,
2. test a same/adjacent-area redistribution,
3. if impossible, identify the exact blocking constraint or state that the search did not find a feasible merge.

“Algorithm did not find one” is not proof that no feasible plan exists.

## Layer G — Regression comparison

For the historical 343-task workbook, compare new vs historical versions at global and station level.

At minimum report:
- vehicles,
- total km,
- total driving time,
- waiting time,
- total work time,
- longest/shortest vehicle workday,
- workload spread,
- hard-constraint failures,
- geographic-overlap/crossing observations.

If the new method uses more vehicles or distance, explain the source of the difference.

## Layer H — Required invariance/edge tests

Tests must include:
- Route 1 can be closer to Route 5 than Route 2.
- Route IDs can be renumbered without materially changing geographic vehicle territories.
- two geographically distant Routes are not merged just because the count is two.
- one large Route can split into continuous postcode subareas.
- Route 0/missing Route is handled geographically.
- Pickup/Redeliver stay outside normal-delivery quota but inside time/capacity/completeness.
- AM/PM continuity.
- low-utilization merge.
- strict appointment prevents merge with explicit explanation.
- full completeness and no unauthorized station transfer.

## Human-readable per-vehicle output

Every vehicle should be understandable without reading code:

- original Routes represented,
- cities,
- postcode subareas,
- AM/PM normal deliveries,
- Pickup,
- Redeliver,
- ordered area/stops summary,
- km,
- driving,
- waiting,
- total work time,
- exceptions/reasons.

## Release acceptance

Do not collapse these into one status:
1. local tests pass,
2. local artifact built,
3. executable independently rerun,
4. ZIP contents verified,
5. website updated,
6. published package downloaded,
7. published-package hash/behavior verified.
