# Automatic geography-first assignment

    python3 -m unittest discover -s tests -v
    python3 -m wdxdelivery.planner examples/assignment-input.json --plan outputs/plan.json --json outputs/report.json --markdown outputs/report.md
    python3 -m wdxdelivery outputs/plan.json --json outputs/validated.json --markdown outputs/validated.md
    python3 -m examples.generate_evidence --check

The JSON plan is independently consumable by the existing baseline validator.
Exit codes are 0 for a complete hard-feasible modeled plan, 1 for an incomplete
assignment with explicit unassigned reasons, and 2 for invalid input. Input and
all output paths must be distinct. Invalid input leaves existing output files
unchanged; use fresh paths to avoid stale-result confusion.

## Input and explicit policy

Use the baseline contract for stations, depots, tasks, actual Pickup locations,
city/coarse postcode and directed road arcs. Automatic input does **not** require
vehicles or final subarea labels; supplied values are ignored and replaced.
Phases remain supplied annotations; actual time windows govern feasibility.
The sample AM appointments end at minute 180, not an inferred universal 13:00.

Add a planning object with explicit values:

| Field | Meaning |
| --- | --- |
| start_minute | Fixed common vehicle start; loading counts from here |
| subarea_max_minutes | Maximum base-road pairwise spread within a derived subarea |
| territory_max_minutes | Maximum base-road pairwise spread across a vehicle territory |
| max_extra_driving_minutes | Allowed extra traffic-buffered driving for merge/balance/redistribution |
| search_node_budget | Positive per-pass stop-order search node bound |
| redistribution_node_budget | Positive whole-location redistribution node bound |
| balance_passes | Positive workload-balancing iteration bound |

Require subarea_max_minutes <= config.adjacency_minutes <= territory_max_minutes.
Geographic distances use the maximum of the two directed base-road travel times,
never Route arithmetic or numeric postcode distance. All geographic thresholds
have the same fixed base_road_minutes policy; buffered driving is a separate
explicit scheduling/cost quantity. Thresholds and sample config are invented,
require calibration, and are not verified production parameters.

## Assignment and search

1. Keep station fixed. Seed city/postcode areas from current task locations.
   Split each seed by deterministic complete-link road clustering: every internal
   pair must satisfy the subarea spread bound. Labels alone cannot glue distant sites.
2. Build an area graph. An edge requires **every** cross-location pair to satisfy
   the bidirectional adjacency threshold, not merely one close boundary point.
   A vehicle's induced area graph must be connected and its whole-day pairwise
   road diameter must satisfy the territory bound. These conservative checks may
   retain more vehicles than a less restrictive calibrated rule.
3. Pack whole subareas when feasible. If capacity, appointments, workday or the
   bounded search blocks a whole area, pack location blocks and finally tasks at
   a shared site, recording blockers and whether the search was exhaustive.
   Avoid sharing locations across vehicles unless those finer splits are needed.
4. Sequence stops with loading, time windows, service, buffered road time,
   dynamic delivery/redelivery unload and Pickup load, and return to depot.
   First search area-contiguous orderings. If none is found, search allowing
   reentry. A merge may introduce reentry only when exhaustive contiguous search
   established that no contiguous ordering exists; recorded constraint blockers
   explain it. A budget-limited miss is never called unavoidable.
5. Balance by moving whole adjacent subareas while both remaining/receiving
   territories stay connected/compact and feasible. A move must reduce the
   station workday spread and stay within the explicit driving-detour allowance.
6. For every low-utilization vehicle, try feasible adjacent merges. If a single
   recipient cannot absorb it, search whole-location redistribution across
   same-station recipients. Report successful reductions and exact observed
   geography/capacity/appointment/workday/cap/detour blockers or search exhaustion.
   Recheck after balancing; merges strictly decrease vehicle count.

For feasible orders, prefer fewer area reentries, then less driving, shorter
work and waiting. Stable task/location keys break ties; no Route IDs participate.
Equivalent task permutations are collapsed by location/type/phase/window/load
and service attributes. The ordering search is bounded, not a globally optimal
solver. No feasible result found in its scope is not proof that none exists.
Redistribution completeness includes the status of its underlying ordering queries.

The 1–2 informative Route preference is advisory. It never blocks a compact
territory or influences renumbering behavior. More than two informative Routes
is allowed with a road-territory explanation. Route 0/missing/blank remain raw
audit metadata and cannot drive grouping.

## Evidence and remaining gates

Reports contain per-vehicle/station/global task types, km/time/wait/service/work,
workload spread, AM/PM areas, full-day connectedness and AM/PM maximum road span,
ordered stops/loads, working subareas, splits and bounded-search status, and
merge/redistribution decisions. Coarse overlap and reentry observations remain
visible. Actual road-path crossings cannot be proven absent from a pairwise matrix.

Invented paired comparison: the original supplied plan is still feasible with
the tighter explicit AM windows. Automatic grouping retains 12 vehicles, lowers
synthetic km 1176→1104 and driving minutes 1764→1656, raises waiting 1680→1752,
lowers total work 3924→3888, and widens spread 62→68. Reentries fall 12→6; each
remaining reentry has exhaustive appointment evidence. Six low-use near vehicles
remain separated from remote territories by geographic blockers. These are
tradeoffs on invented data, not historical fleet or business optimization claims.

The planner currently provisions an unrestricted count of homogeneous single-trip
weight-only vehicles; no real fleet availability, reloads, multi-day windows or
multidimensional cargo is modeled. Normal-delivery AM targets are reported but
not a scheduling quota or optimization term. Low utilization is an explicit
test/calibration threshold, not a universal business rule. Greedy clustering,
packing, conservative graph links and bounded searches can miss better plans.

No raw customer data or private address cache was supplied. The real 343-task
regression, six-station geography, road provenance, production configuration,
operational acceptance and remote CI pass remain unverified. No release built.
Keep private inputs/detailed outputs in ignored data/private/ and outputs/.
