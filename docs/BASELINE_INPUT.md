# Baseline diagnostic runner

This first-stage tool checks a **supplied ordered plan**, not an automatically
optimized assignment. Python 3.10+ and the standard library are sufficient.

Run from the repository root:

    python3 examples/make_synthetic.py
    python3 -m unittest discover -s tests -v
    python3 -m wdxdelivery examples/synthetic.json --json outputs/baseline.json --markdown outputs/baseline.md

Exit codes: 0 means the supplied baseline satisfies modeled hard constraints;
1 means a report was generated with constraint/integrity failures; 2 means invalid
input, including missing matrix relationships. A failed input does not overwrite
existing reports; use fresh output paths to avoid mistaking stale reports for a
new successful run.

examples/synthetic.json is wholly invented. Its distances, station territories,
times and parameters are **not** historical observations or business defaults.
Committed evidence is a reproducible smoke baseline, not real six-station
operational acceptance. A road basis of approximation or synthetic never
establishes real road feasibility, even when modeled checks pass.

## Input contract

The generated example is the executable schema reference. All quantities must
be finite nonnegative numbers. No operational parameters have implicit defaults.

- config: explicit uniform-fleet capacity_kg, max_work_minutes, loading_minutes,
  traffic_multiplier (at least 1), adjacency_minutes, low_utilization_minutes and
  nonempty evidence. task_cap must be null or an explicit positive integer limit
  and scope of all_tasks or normal_deliveries. Thresholds and test settings require
  verification before operational use. There is no assumed 900 kg / 12 hour / 25 task rule.
- locations: unique string id, supported station, city, coarse postcode_area and
  declared geographically meaningful subarea. Subareas are supplied evidence;
  this version does not geocode or discover them. Depot locations use this format.
- depots: supported station name to depot location ID.
- tasks: unique string id, station, location, kind (Delivery, Pickup or Redeliver),
  phase (AM, PM or flexible), route label or null, weight_kg, service_minutes, and
  [start, end] window. Pickup also requires pickup_location, equal to the actual
  task location. Use the pickup site, not an unrelated delivery site. Phase is
  supplied, never inferred from 13:00.
- vehicles: unique string id, station, start_minute, ordered task ID list, and
  optional explanation for unusual grouping. IDs have no geographic meaning.
- road: nonempty source, explicit basis (road, synthetic, approximation), and
  arcs containing from, to, minutes, km. Supply every directed pair of distinct
  locations within each represented station. Self travel is zero. Traffic
  multiplier applies to travel time, not distance. Provenance is reported, not
  independently authenticated by the program.

Times are minutes from one common planning-day origin. Service must finish by
the time-window end (a conservative interim interpretation). Every vehicle loads
all Delivery and Redeliver goods at its depot, unloads them when served, collects
Pickup goods, and returns to the depot. No mid-day replenishment, pickup unload
at other depots, multidimensional capacity, heterogeneous fleet or multi-day
scheduling is modeled.

## Diagnostic interpretation and limits

Station is fixed. Route labels (including 0 and missing) only describe source
distribution. Two subareas are candidates for adjacency if the closest location
pair has travel within the configured threshold **in both directions**. This
reports possible road connections, not proof of a compact territory; dispersed
subareas are separately reported. Numeric postcode order is never a distance.

All geography thresholds, separation/dispersion metrics, cross-region-jump
flags and AM/PM leg diagnostics use **base road minutes**. Scheduling and driving
totals use traffic-buffered minutes. The fixed policy is exposed as
geography_time_basis=base_road_minutes in every report; an explicit conflicting
config policy is rejected. Changing the traffic multiplier can change scheduling
feasibility and vehicle assignment, but never the underlying geographic graph.

Raw Route 0/missing/blank labels are retained for audit, excluded from informative
Route counts and distant-Route conclusions. Vehicles expose informative_routes
separately; more_than_two_routes uses only those informative labels.

Reports include counts by task type, missing/duplicate/unknown/cross-station
references, per-vehicle scheduling and changing loads, station/global workload,
Route/city/postcode distributions, distant subareas, area reentries, overlap,
large direct transitions, supplied AM/PM territories and direct AM-to-PM legs.
These are transparent indicators for human inspection, not a geometric crossing
detector. Flexible windows may obscure a direct AM/PM transition; inspect the
whole stop sequence. More than two Routes is flagged without imposing a cap.

This runner itself checks a supplied baseline. Use the automatic planner in
[ASSIGNMENT.md](ASSIGNMENT.md) for actual low-utilization merge/redistribution
and automatic assignment. Assignment-level synthetic/adversarial tests now
cover Route invariance, continuous splits, appointment splits/reentries and
merge decisions. Actual road quality and operational acceptance remain pending.

Original synthetic-baseline.json/.md are historical first-stage evidence.
Corrected diagnostic output is synthetic-baseline-v2.json/.md; the original
files have not been overwritten.

Private inputs and detailed reports may contain task IDs and fine location
information. Keep them in ignored data/private/ and outputs/, never commit them.
Only invented fixtures and non-identifying aggregate evidence belong in this
public repository. No EXE/ZIP or production artifact is generated here.
