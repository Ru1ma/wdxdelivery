"""Validate an ordered baseline and diagnose geography from supplied road evidence.

Inputs and detailed reports can be private. Never infer geography from Route IDs.
No defaults are supplied for unverified historical operational parameters.
"""
import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

STATIONS = ("AMS", "ROT", "DEN HAAG", "UTRECHT", "TILBURG", "BELGEM")
KINDS = ("Delivery", "Pickup", "Redeliver")


def number(value, label, minimum=0):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label}: expected a number")
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f"{label}: invalid finite value")
    return value


def nonempty_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: nonempty text required")


def unique(items, label):
    result = {}
    for item in items:
        key = item["id"]
        if not isinstance(key, str) or not key.strip() or key in result:
            raise ValueError(f"{label}: invalid or duplicate id {key!r}")
        result[key] = item
    return result


def validate(data):
    cfg = data["config"]
    for field in ("capacity_kg", "max_work_minutes", "loading_minutes",
                  "traffic_multiplier", "adjacency_minutes", "low_utilization_minutes"):
        number(cfg[field], field)
    if cfg["capacity_kg"] == 0 or cfg["max_work_minutes"] == 0:
        raise ValueError("capacity and workday must be positive")
    if cfg["traffic_multiplier"] < 1:
        raise ValueError("traffic_multiplier must be >= 1")
    nonempty_text(cfg["evidence"], "explicit configuration evidence")
    cap = cfg["task_cap"]
    if cap is not None:
        if cap["scope"] not in ("all_tasks", "normal_deliveries"):
            raise ValueError("task_cap.scope must be explicit")
        if isinstance(cap["limit"], bool) or not isinstance(cap["limit"], int) or cap["limit"] < 1:
            raise ValueError("task_cap.limit must be a positive integer")
    locations = unique(data["locations"], "locations")
    tasks = unique(data["tasks"], "tasks")
    vehicles = unique(data["vehicles"], "vehicles")
    depots = data["depots"]
    for station, location in depots.items():
        if station not in STATIONS or locations[location]["station"] != station:
            raise ValueError("invalid depot station")
    for loc in locations.values():
        if loc["station"] not in STATIONS:
            raise ValueError("unknown station")
        for field in ("city", "postcode_area", "subarea"):
            if not isinstance(loc[field], str) or not loc[field].strip():
                raise ValueError(f"location needs explicit {field}")
    for task in tasks.values():
        station = task["station"]
        if station not in STATIONS or station not in depots:
            raise ValueError("task needs a supported station and depot")
        if task["kind"] not in KINDS or task["phase"] not in ("AM", "PM", "flexible"):
            raise ValueError("unknown task kind or phase")
        loc = locations[task["location"]]
        if loc["station"] != station:
            raise ValueError("task location must belong to its station")
        if task["kind"] == "Pickup" and task["pickup_location"] != task["location"]:
            raise ValueError("Pickup must use actual pickup_location")
        if task["route"] is not None and not isinstance(task["route"], (str, int)):
            raise ValueError("Route must be a label or null")
        number(task["weight_kg"], "task weight")
        number(task["service_minutes"], "service time")
        start, end = task["window"]
        number(start, "window start")
        number(end, "window end")
        if end < start:
            raise ValueError("reversed window")
    for vehicle in vehicles.values():
        if vehicle["station"] not in depots:
            raise ValueError("vehicle needs a supported station depot")
        number(vehicle["start_minute"], "vehicle start")
        if not isinstance(vehicle["tasks"], list):
            raise ValueError("vehicle tasks must be an ordered list")
    road = data["road"]
    if road["basis"] not in ("road", "synthetic", "approximation"):
        raise ValueError("road basis must be explicit")
    nonempty_text(road["source"], "road source")
    arcs = {}
    for arc in road["arcs"]:
        a, b = arc["from"], arc["to"]
        if a not in locations or b not in locations or (a, b) in arcs:
            raise ValueError("invalid or duplicate road arc")
        if locations[a]["station"] != locations[b]["station"]:
            raise ValueError("cross-station road arc")
        number(arc["minutes"], "road minutes")
        number(arc["km"], "road km")
        if a == b and (arc["minutes"] or arc["km"]):
            raise ValueError("self arc must be zero")
        arcs[a, b] = arc
    # Fail closed: unknown relationships must not look like zero-distance neighbors.
    for a, la in locations.items():
        for b, lb in locations.items():
            if la["station"] == lb["station"]:
                if a == b:
                    arcs.setdefault((a, b), {"minutes": 0, "km": 0})
                elif (a, b) not in arcs:
                    raise ValueError(f"missing directed road arc {a} -> {b}")
    return cfg, locations, tasks, vehicles, arcs


def task_counts(tasks):
    counts = Counter(t["kind"] for t in tasks)
    return {"total_tasks": sum(counts.values()), **{k: counts[k] for k in KINDS}}


def geography(station, tasks, locations, arcs, threshold):
    route_map = defaultdict(lambda: defaultdict(set))
    areas = defaultdict(set)
    for task in tasks:
        loc = locations[task["location"]]
        route = "(missing)" if task["route"] is None else str(task["route"])
        route_map[route][loc["city"]].add(loc["postcode_area"])
        areas[loc["subarea"]].add(task["location"])
    neighbors, separate, dispersed = [], [], []
    keys = sorted(areas)
    for i, a in enumerate(keys):
        internal = max((arcs[x, y]["minutes"] for x in areas[a] for y in areas[a]), default=0)
        if internal > threshold:
            dispersed.append({"subarea": a, "max_minutes": internal})
        for b in keys[i + 1:]:
            # Both directions must be close; no Route arithmetic or postcode sorting.
            minutes = min(max(arcs[x, y]["minutes"], arcs[y, x]["minutes"])
                          for x in areas[a] for y in areas[b])
            item = {"areas": [a, b], "minutes": minutes}
            (neighbors if minutes <= threshold else separate).append(item)
    distant_routes = []
    for route in sorted(route_map):
        route_areas = sorted({locations[t["location"]]["subarea"] for t in tasks
                              if ("(missing)" if t["route"] is None else str(t["route"])) == route})
        pairs = [p for p in separate if set(p["areas"]).issubset(route_areas)]
        if pairs:
            distant_routes.append({"route": route, "distant_pairs": pairs})
    return {"station": station, "data_available": bool(tasks),
            "routes": {r: {c: sorted(ps) for c, ps in sorted(cs.items())}
                       for r, cs in sorted(route_map.items())},
            "neighbors": neighbors, "separate_areas": separate,
            "dispersed_subareas": dispersed, "distant_routes": distant_routes}


def vehicle_report(vehicle, tasks, locations, depots, arcs, cfg):
    station = vehicle["station"]
    ordered = [tasks[x] for x in vehicle["tasks"] if x in tasks]
    failures = []
    if any(x not in tasks for x in vehicle["tasks"]):
        failures.append("unknown task reference")
    if any(t["station"] != station for t in ordered):
        # Do not compute made-up travel for an invalid station assignment.
        return {"id": vehicle["id"], "station": station, "metrics_available": False,
                "failures": failures + ["cross-station assignment"], **task_counts(ordered)}
    cap = cfg["task_cap"]
    if cap and (len(ordered) if cap["scope"] == "all_tasks" else
                sum(t["kind"] == "Delivery" for t in ordered)) > cap["limit"]:
        failures.append("task cap exceeded")
    clock = vehicle["start_minute"] + cfg["loading_minutes"]
    load = sum(t["weight_kg"] for t in ordered if t["kind"] != "Pickup")
    peak = load
    if load > cfg["capacity_kg"]:
        failures.append("initial capacity exceeded")
    current = depots[station]
    driving = km = waiting = service = 0
    stops, area_sequence, jumps = [], [], []
    for task in ordered:
        arc = arcs[current, task["location"]]
        travel = arc["minutes"] * cfg["traffic_multiplier"]
        driving += travel
        km += arc["km"]
        clock += travel
        wait = max(0, task["window"][0] - clock)
        waiting += wait
        clock += wait
        begin = clock
        clock += task["service_minutes"]
        service += task["service_minutes"]
        if clock > task["window"][1]:
            failures.append(f"time window exceeded: {task['id']}")
        load += task["weight_kg"] if task["kind"] == "Pickup" else -task["weight_kg"]
        peak = max(peak, load)
        if load > cfg["capacity_kg"]:
            failures.append(f"capacity exceeded: {task['id']}")
        area = locations[task["location"]]["subarea"]
        if not area_sequence or area_sequence[-1] != area:
            if area_sequence and arc["minutes"] > cfg["adjacency_minutes"]:
                jumps.append({"from": area_sequence[-1], "to": area,
                              "minutes": arc["minutes"]})
            area_sequence.append(area)
        stops.append({"task": task["id"], "subarea": area, "phase": task["phase"],
                      "service_start": begin, "service_end": clock, "load_kg": load})
        current = task["location"]
    back = arcs[current, depots[station]]
    km += back["km"]
    driving += back["minutes"] * cfg["traffic_multiplier"]
    clock += back["minutes"] * cfg["traffic_multiplier"]
    work = clock - vehicle["start_minute"]
    if work > cfg["max_work_minutes"]:
        failures.append("maximum workday exceeded")
    phase_areas = {p: sorted({locations[t["location"]]["subarea"] for t in ordered
                              if t["phase"] == p}) for p in ("AM", "PM", "flexible")}
    transitions = []
    for a, b in zip(ordered, ordered[1:]):
        if a["phase"] == "AM" and b["phase"] == "PM":
            transitions.append({"from": locations[a["location"]]["subarea"],
                                "to": locations[b["location"]]["subarea"],
                                "minutes": arcs[a["location"], b["location"]]["minutes"]})
    routes = sorted({str(t["route"]) for t in ordered if t["route"] is not None})
    return {"id": vehicle["id"], "station": station, "metrics_available": True,
            **task_counts(ordered), "normal_deliveries_by_phase": {
                p: sum(t["kind"] == "Delivery" and t["phase"] == p for t in ordered)
                for p in ("AM", "PM", "flexible")},
            "routes": routes, "cities": sorted({locations[t["location"]]["city"] for t in ordered}),
            "postcode_areas": sorted({locations[t["location"]]["postcode_area"] for t in ordered}),
            "phase_areas": phase_areas, "am_pm_transitions": transitions,
            "area_sequence": area_sequence, "area_reentries": len(area_sequence) - len(set(area_sequence)),
            "cross_region_jumps": jumps, "stops": stops, "km": km,
            "driving_minutes": driving, "service_minutes": service, "waiting_minutes": waiting,
            "loading_minutes": cfg["loading_minutes"], "work_minutes": work, "peak_kg": peak,
            "low_utilization": work < cfg["low_utilization_minutes"],
            "more_than_two_routes": len(routes) > 2,
            "exceptions": vehicle.get("explanation", ""), "failures": failures}


def totals(reports):
    available = all(v["metrics_available"] for v in reports)
    work = [v["work_minutes"] for v in reports if v["metrics_available"]]
    return {"vehicles": len(reports), "metrics_available": available,
            **{key: sum(v[key] for v in reports) if available else None
               for key in ("km", "driving_minutes", "service_minutes", "waiting_minutes", "work_minutes")},
            "longest_minutes": max(work, default=0) if available else None,
            "shortest_minutes": min(work, default=0) if available else None,
            "spread_minutes": max(work, default=0) - min(work, default=0) if available else None}


def analyze(data):
    cfg, locations, tasks, vehicles, arcs = validate(data)
    assigned = Counter(t for v in vehicles.values() for t in v["tasks"])
    missing = sorted(set(tasks) - set(assigned))
    duplicates = {t: n - 1 for t, n in assigned.items() if n > 1}
    unknown = sorted(set(assigned) - set(tasks))
    cross = sum(tasks[t]["station"] != v["station"] for v in vehicles.values()
                for t in v["tasks"] if t in tasks)
    reports = [vehicle_report(v, tasks, locations, data["depots"], arcs, cfg)
               for v in sorted(vehicles.values(), key=lambda v: v["id"])]
    stations = []
    for station in STATIONS:
        ts = [t for t in tasks.values() if t["station"] == station]
        vs = [v for v in reports if v["station"] == station]
        geo = geography(station, ts, locations, arcs, cfg["adjacency_minutes"])
        owners = defaultdict(list)
        for v in vs:
            for area in set(v.get("area_sequence", [])):
                owners[area].append(v["id"])
        geo["overlapping_areas"] = {a: ids for a, ids in sorted(owners.items()) if len(ids) > 1}
        stations.append({**geo, **task_counts(ts), **totals(vs)})
    return {"evidence": {"road_basis": data["road"]["basis"], "road_source": data["road"]["source"],
                         "config": cfg, "operational_geography_review": "pending",
                         "historical_343_regression": "not run; input unavailable"},
            "integrity": {"missing": missing, "duplicates": duplicates, "unknown": unknown,
                          "cross_station": cross},
            "hard_constraints_pass": not (missing or duplicates or unknown or cross or
                                          any(v["failures"] for v in reports)),
            "summary": {**task_counts(tasks.values()), **totals(reports)},
            "stations": stations, "vehicles": reports,
            "merge_analysis": "not implemented in baseline stage; no impossibility claim"}


def markdown(report):
    def cell(value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, sort_keys=True)
        return str(value).replace("|", "\\|").replace("\n", " ")

    def table(headers, rows):
        return ["| " + " | ".join(headers) + " |",
                "| " + " | ".join("---" for _ in headers) + " |",
                *["| " + " | ".join(cell(v) for v in row) + " |" for row in rows], ""]

    lines = ["# Dispatch baseline diagnostic", "",
             f"Evidence basis: {report['evidence']['road_basis']}; {report['evidence']['road_source']}.",
             "Operational geography review: pending. No optimization/production acceptance claim.",
             "Merge/redistribution search: not implemented in this baseline stage.", "",
             "Integrity: " + json.dumps(report["integrity"], sort_keys=True),
             f"Hard constraints pass: {report['hard_constraints_pass']}", "",
             "All times below are minutes; driving applies the explicit traffic multiplier.",
             "Time windows require completion of service by the end. Depot return is included.", "",
             "Global: " + json.dumps(report["summary"], sort_keys=True), ""]
    lines += table(
        ["Station", "Tasks / Delivery / Pickup / Redeliver", "Vehicles", "km", "Driving",
         "Waiting", "Work", "Longest / shortest / spread"],
        [[s["station"], [s[k] for k in ("total_tasks", "Delivery", "Pickup", "Redeliver")],
          s["vehicles"], s["km"], s["driving_minutes"], s["waiting_minutes"], s["work_minutes"],
          [s[k] for k in ("longest_minutes", "shortest_minutes", "spread_minutes")]]
         for s in report["stations"]])
    for station in report["stations"]:
        lines += [f"## {station['station']}", "",
                  f"Task data available: {station['data_available']}", ""]
        lines += table(["Original Route label", "City", "Postcode areas"],
                       [[route, city, postcodes] for route, cities in station["routes"].items()
                        for city, postcodes in cities.items()])
        for key in ("neighbors", "separate_areas", "distant_routes", "dispersed_subareas",
                    "overlapping_areas"):
            lines += [f"{key}: " + cell(station[key]), ""]
    for vehicle in report["vehicles"]:
        lines += [f"## Vehicle {vehicle['id']}", ""]
        lines += table(["Metric", "Value"], [[k, v] for k, v in vehicle.items() if k != "stops"])
        lines += table(["Task", "Subarea", "Phase", "Service start", "Service end", "Load kg"],
                       [[s[k] for k in ("task", "subarea", "phase", "service_start",
                                       "service_end", "load_kg")] for s in vehicle.get("stops", [])])
    return "\n".join(lines).rstrip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    if len({p.resolve() for p in (args.input, args.json, args.markdown)}) != 3:
        parser.exit(2, "Input and report paths must be distinct.\n")
    try:
        report = analyze(json.loads(args.input.read_text(encoding="utf-8")))
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Invalid baseline input: {error}\n")
    for path in (args.json, args.markdown):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown.write_text(markdown(report) + "\n", encoding="utf-8")
    if not report["hard_constraints_pass"]:
        parser.exit(1, "Baseline fails hard constraints; inspect generated reports.\n")
