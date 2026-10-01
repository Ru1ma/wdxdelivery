"""Generate invented six-station evidence, never historical/customer data."""
import json
from pathlib import Path

STATIONS = ("AMS", "ROT", "DEN HAAG", "UTRECHT", "TILBURG", "BELGEM")


def fixture():
    data = {
        "config": {"capacity_kg": 400, "max_work_minutes": 600, "loading_minutes": 15,
                   "traffic_multiplier": 1.2, "adjacency_minutes": 15,
                   "low_utilization_minutes": 300, "task_cap": None,
                   "evidence": "Invented test parameters; no verified operational configuration."},
        "road": {"basis": "synthetic", "source": "Invented symmetric travel table, not real road travel.",
                 "arcs": []},
        "locations": [], "tasks": [], "vehicles": [], "depots": {},
    }
    minutes = {("d", "a"): 15, ("d", "b"): 20, ("d", "c"): 90,
               ("a", "b"): 10, ("a", "c"): 80, ("b", "c"): 70}
    for i, station in enumerate(STATIONS):
        prefix = f"s{i}"
        data["depots"][station] = prefix + "d"
        for key, area in (("d", "depot"), ("a", "alpha"), ("b", "beta"), ("c", "gamma")):
            data["locations"].append({"id": prefix + key, "station": station,
                                     "city": "Invented " + area, "postcode_area": "TEST-" + area,
                                     "subarea": area})
        for a in "dabc":
            for b in "dabc":
                if a == b:
                    continue
                value = minutes.get((a, b), minutes.get((b, a)))
                data["road"]["arcs"].append({"from": prefix + a, "to": prefix + b,
                                            "minutes": value, "km": value * 0.8})
        definitions = [
            ("t1", "a", "Delivery", "AM", "1", 100),
            ("t2", "b", "Delivery", "AM", "5", 100),
            ("t3", "a", "Pickup", "PM", None, 50),
            ("t4", "b", "Redeliver", "PM", "0", 100),
            ("t5", "c", "Delivery", "PM", "2", 100),
        ]
        for key, loc, kind, phase, route, weight in definitions:
            task = {"id": prefix + key, "station": station, "location": prefix + loc,
                    "kind": kind, "phase": phase, "route": route, "weight_kg": weight,
                    "service_minutes": 10, "window": [0 if phase == "AM" else 240, 600]}
            if kind == "Pickup":
                task["pickup_location"] = prefix + loc
            data["tasks"].append(task)
        data["vehicles"] += [
            {"id": station + "-near", "station": station, "start_minute": 0,
             "tasks": [prefix + f"t{n}" for n in (1, 2, 3, 4)],
             "explanation": "Synthetic supplied baseline; alpha/beta reentry deliberately retained."},
            {"id": station + "-far", "station": station, "start_minute": 0,
             "tasks": [prefix + "t5"], "explanation": "Synthetic remote territory; merge not tested."},
        ]
    return data


if __name__ == "__main__":
    Path(__file__).with_name("synthetic.json").write_text(
        json.dumps(fixture(), indent=2, sort_keys=True) + "\n")
