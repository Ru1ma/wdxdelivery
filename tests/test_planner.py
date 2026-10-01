from copy import deepcopy
from itertools import permutations
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

from examples.make_assignment import automatic_fixture
from examples.make_synthetic import fixture
from wdxdelivery.baseline import analyze
from wdxdelivery.planner import AssignmentEngine, plan


def scenario(positions, specs, capacity=400, adjacency=15, diameter=45):
    """Wholly invented one-dimensional metric road fixture for small counterexamples."""
    data = automatic_fixture()
    data["tasks"], data["locations"], data["road"]["arcs"] = [], [], []
    data["depots"] = {"AMS": "d"}
    data["config"].update(capacity_kg=capacity, traffic_multiplier=1,
                          loading_minutes=0, adjacency_minutes=adjacency,
                          max_work_minutes=600, low_utilization_minutes=600)
    data["planning"].update(territory_max_minutes=diameter, subarea_max_minutes=adjacency)
    locs = {"d": 0, **positions}
    for lid, pos in locs.items():
        data["locations"].append({"id": lid, "station": "AMS",
                                 "city": "Invented " + lid, "postcode_area": "TEST-" + lid})
        for other, dest in locs.items():
            if lid != other:
                data["road"]["arcs"].append({"from": lid, "to": other,
                                            "minutes": abs(pos - dest), "km": abs(pos - dest)})
    for i, spec in enumerate(specs):
        task = {"id": f"t{i}", "station": "AMS", "location": spec["location"],
                "kind": "Delivery", "phase": "flexible", "route": str(i + 1),
                "weight_kg": 10, "service_minutes": 1, "window": [0, 600]}
        task.update(spec)
        if task["kind"] == "Pickup":
            task["pickup_location"] = task["location"]
        data["tasks"].append(task)
    return data


def territories(generated):
    return sorted(sorted(v["tasks"]) for v in generated["vehicles"])


class PlannerTests(unittest.TestCase):
    def test_six_station_automatic_assignment_and_baseline_validation(self):
        data = automatic_fixture()
        original = deepcopy(data)
        generated, report = plan(data)
        self.assertEqual(data, original)
        self.assertTrue(report["hard_constraints_pass"])
        self.assertTrue(analyze(generated)["hard_constraints_pass"])
        self.assertEqual(report["summary"]["total_tasks"], 30)
        self.assertEqual(report["summary"]["vehicles"], 12)
        self.assertEqual(report["integrity"], {"missing": [], "duplicates": {},
                                              "unknown": [], "cross_station": 0})
        self.assertEqual(sum(e["action"] == "adjacent_merge" for e in report["merge_analysis"]), 6)
        self.assertTrue(all(v["connected"] for v in report["planning"]["full_day_continuity"].values()))

    def test_assignment_renumbering_and_input_order_invariance(self):
        data = automatic_fixture()
        before, _ = plan(data)
        for task in data["tasks"]:
            task["route"] = {"1": "900", "2": "47", "5": "1", "0": "unknown", None: "74"}[task["route"]]
        for loc in data["locations"]:
            loc["subarea"] = "intentionally misleading supplied territory"
        data["vehicles"] = fixture()["vehicles"]
        random.Random(7).shuffle(data["tasks"])
        random.Random(8).shuffle(data["locations"])
        random.Random(9).shuffle(data["road"]["arcs"])
        after, _ = plan(data)
        self.assertEqual(territories(before), territories(after))
        self.assertEqual([v["tasks"] for v in before["vehicles"]], [v["tasks"] for v in after["vehicles"]])

    def test_route_zero_and_missing_do_not_drive_assignment(self):
        data = automatic_fixture()
        a, _ = plan(data)
        for task in data["tasks"]:
            task["route"] = 0 if task["kind"] == "Delivery" else None
        b, report = plan(data)
        self.assertEqual(territories(a), territories(b))
        self.assertTrue(all(not s["distant_routes"] for s in report["stations"]))
        self.assertTrue(all(not v["more_than_two_routes"] for v in report["vehicles"]))
        self.assertTrue(all(not v["informative_routes"] for v in report["vehicles"]))

    def test_large_route_splits_into_continuous_postcode_territories(self):
        data = scenario({"a": 10, "b": 20, "c": 80, "e": 90},
                        [{"location": l, "route": "large", "weight_kg": 100} for l in "abce"],
                        capacity=200)
        generated, r = plan(data)
        self.assertEqual(territories(generated), [["t0", "t1"], ["t2", "t3"]])
        self.assertFalse(r["stations"][0]["overlapping_areas"])
        self.assertTrue(all(c["connected"] for c in r["planning"]["full_day_continuity"].values()))
        self.assertTrue(all(v["area_reentries"] == 0 for v in r["vehicles"]))

    def test_distant_two_routes_do_not_merge(self):
        data = scenario({"a": 10, "b": 80}, [{"location": "a", "route": "1"},
                                            {"location": "b", "route": "2"}])
        generated, r = plan(data)
        self.assertEqual(len(generated["vehicles"]), 2)
        reasons = json.dumps(r["merge_analysis"])
        self.assertIn("disconnected road subareas", reasons)

    def test_close_boundary_pair_does_not_imply_compact_territory(self):
        data = scenario({"a": 10, "b": 20, "c": 30, "e": 40},
                        [{"location": l} for l in "abce"], adjacency=15, diameter=20)
        # Alpha and beta each internally close, boundary b-c close; a-e are far.
        for loc in data["locations"]:
            if loc["id"] in "ab":
                loc.update(city="Invented alpha", postcode_area="TEST-alpha")
            elif loc["id"] in "ce":
                loc.update(city="Invented beta", postcode_area="TEST-beta")
        engine = AssignmentEngine(data)
        self.assertEqual(len(engine.areas), 2)
        self.assertFalse(engine.territory(["t0", "t1", "t2", "t3"])[0])
        generated, _ = engine.run()
        self.assertEqual(len(generated["vehicles"]), 2)

    def test_chain_connected_but_excessive_diameter_is_rejected(self):
        data = scenario({"a": 10, "b": 20, "c": 30, "e": 40},
                        [{"location": l} for l in "abce"], adjacency=15, diameter=20)
        engine = AssignmentEngine(data)
        ok, geo = engine.territory(["t0", "t1", "t2", "t3"])
        self.assertFalse(ok)
        self.assertTrue(geo["connected"])
        self.assertEqual(geo["reason"], "territory road diameter exceeded")
        self.assertGreater(len(engine.run()[0]["vehicles"]), 1)

    def test_dispersed_city_postcode_is_road_split(self):
        data = scenario({"a": 10, "b": 80}, [{"location": "a"}, {"location": "b"}])
        for loc in data["locations"]:
            loc.update(city="Invented same", postcode_area="TEST-same")
        generated, r = plan(data)
        self.assertEqual(len(r["planning"]["subareas"]), 2)
        self.assertEqual(len(generated["vehicles"]), 2)

    def test_city_postcode_delimiter_cannot_collide_subarea_identity(self):
        data = scenario({"a": 10, "b": 80}, [{"location": "a"}, {"location": "b"}])
        data["locations"][1].update(city="Invented a / b", postcode_area="TEST-c")
        data["locations"][2].update(city="Invented a", postcode_area="b / TEST-c")
        engine = AssignmentEngine(data)
        self.assertEqual(len(engine.areas), 2)
        self.assertFalse(engine.territory(["t0", "t1"])[0])

    def test_low_vehicle_merged_when_feasible(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a"}, {"location": "b"}])
        generated, report = plan(data)
        self.assertEqual(len(generated["vehicles"]), 1)
        self.assertIn("adjacent_merge", [e["action"] for e in report["merge_analysis"]])
        self.assertTrue(report["hard_constraints_pass"])

    def test_capacity_block_prevents_low_merge_with_concrete_reason(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a", "weight_kg": 100},
                                            {"location": "b", "weight_kg": 100}], capacity=100)
        generated, report = plan(data)
        self.assertEqual(len(generated["vehicles"]), 2)
        self.assertIn("initial delivery/redelivery capacity", json.dumps(report["merge_analysis"]))

    def test_appointments_prevent_merge_with_concrete_reason(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a", "window": [20, 21]},
                                            {"location": "b", "window": [20, 21]}])
        generated, report = plan(data)
        self.assertEqual(len(generated["vehicles"]), 2)
        text = json.dumps(report["merge_analysis"])
        self.assertIn("appointment/service completion", text)
        self.assertIn('"search_complete": true', text)

    def test_strict_appointments_can_justify_reentry(self):
        data = scenario({"a": 10, "b": 20},
                        [{"location": "a", "window": [10, 15], "phase": "AM"},
                         {"location": "b", "window": [25, 30], "phase": "AM"},
                         {"location": "a", "window": [45, 50], "phase": "PM"}])
        generated, report = plan(data)
        self.assertEqual(len(generated["vehicles"]), 1)
        self.assertEqual(report["vehicles"][0]["area_reentries"], 1)
        self.assertIn("Contiguous-area sequencing has no feasible ordering",
                      report["vehicles"][0]["exceptions"])
        self.assertIn("appointment/service completion", report["vehicles"][0]["exceptions"])

    def test_full_day_am_pm_keeps_nearby_territory(self):
        data = scenario({"a": 10, "b": 20, "c": 80},
                        [{"location": "a", "phase": "AM", "window": [0, 100]},
                         {"location": "b", "phase": "PM", "window": [150, 300]},
                         {"location": "c", "phase": "PM", "window": [150, 300]}])
        generated, report = plan(data)
        self.assertIn(["t0", "t1"], territories(generated))
        together = next(v for v in report["vehicles"] if v["Delivery"] == 2)
        continuity = report["planning"]["full_day_continuity"][together["id"]]
        self.assertEqual(continuity["max_am_pm_base_minutes"], 10)
        self.assertEqual(together["normal_deliveries_by_phase"]["AM"], 1)

    def test_pickup_redelivery_quota_and_load_while_planning(self):
        data = scenario({"a": 10, "b": 20},
                        [{"location": "a", "weight_kg": 90},
                         {"location": "b", "kind": "Redeliver", "weight_kg": 90},
                         {"location": "a", "kind": "Pickup", "weight_kg": 100, "window": [80, 100]}],
                        capacity=200)
        data["config"]["task_cap"] = {"scope": "normal_deliveries", "limit": 1}
        generated, report = plan(data)
        self.assertEqual(len(generated["vehicles"]), 1)
        v = report["vehicles"][0]
        self.assertEqual((v["Delivery"], v["Pickup"], v["Redeliver"]), (1, 1, 1))
        self.assertLessEqual(v["peak_kg"], 200)
        self.assertEqual(v["stops"][-1]["load_kg"], 100)
        self.assertTrue(report["hard_constraints_pass"])

    def test_more_than_two_informative_routes_permitted_with_explanation(self):
        data = scenario({"a": 10, "b": 15, "c": 20},
                        [{"location": "a", "route": "1"}, {"location": "b", "route": "5"},
                         {"location": "c", "route": "9"}])
        generated, r = plan(data)
        self.assertEqual(len(generated["vehicles"]), 1)
        self.assertTrue(r["vehicles"][0]["more_than_two_routes"])
        self.assertIn("connected compact road territory", r["vehicles"][0]["exceptions"])

    def test_redistribution_eliminates_vehicle_when_no_single_merge_fits(self):
        data = scenario({"a": 10, "b": 20, "c": 30},
                        [{"location": "a", "weight_kg": 60},
                         {"location": "b", "weight_kg": 60},
                         {"location": "a", "weight_kg": 40},
                         {"location": "c", "weight_kg": 40}], capacity=100, adjacency=25)
        engine = AssignmentEngine(data)
        donor, left, right = ("t2", "t3"), ("t0",), ("t1",)
        self.assertIsNone(engine.pair_merge(donor, left)[0])
        self.assertIsNone(engine.pair_merge(donor, right)[0])
        found, evidence = engine.redistribute(donor, [left, right])
        self.assertIsNotNone(found)
        self.assertEqual(sorted(t for group in found for t in group), ["t0", "t1", "t2", "t3"])
        self.assertTrue(all(engine.schedule(g).report for g in found))
        reduced = engine.reduce_fleet([donor, left, right])
        self.assertEqual(len(reduced), 2)
        self.assertIn("adjacent_redistribution", [e["action"] for e in engine.events])

    def test_workload_balance_moves_whole_adjacent_subarea(self):
        data = scenario({"a": 10, "b": 20, "c": 30},
                        [{"location": "a", "service_minutes": 90},
                         {"location": "b", "service_minutes": 40},
                         {"location": "c", "service_minutes": 5}], adjacency=25)
        engine = AssignmentEngine(data)
        groups = [engine.schedule(["t0", "t1"]).order, engine.schedule(["t2"]).order]
        before = sorted(engine.schedule(g).report["work_minutes"] for g in groups)
        after = engine.balance(groups)
        work = sorted(engine.schedule(g).report["work_minutes"] for g in after)
        self.assertLess(work[-1] - work[0], before[-1] - before[0])
        self.assertTrue(all(engine.territory(g)[0] for g in after))
        self.assertTrue(any(e["action"] == "adjacent_workload_balance" for e in engine.events))

    def test_impossible_singleton_reported_not_silently_assigned(self):
        data = scenario({"a": 10}, [{"location": "a", "weight_kg": 500}], capacity=100)
        generated, r = plan(data)
        self.assertEqual(generated["vehicles"], [])
        self.assertFalse(r["hard_constraints_pass"])
        self.assertEqual(r["integrity"]["missing"], ["t0"])
        self.assertIn("capacity", json.dumps(r["planning"]["unassigned"]))

    def test_bounded_search_never_claims_infeasibility_proof(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a"}, {"location": "b"}])
        data["planning"]["search_node_budget"] = 2
        engine = AssignmentEngine(data)
        result = engine.schedule(["t0", "t1"])
        self.assertFalse(result.search_complete)
        self.assertIn("bounded ordering search exhausted; no infeasibility proof", result.reasons)
        generated, r = engine.run()
        self.assertTrue(r["hard_constraints_pass"])
        self.assertGreater(r["planning"]["bounded_ordering_queries"], 0)
        self.assertEqual(len(generated["vehicles"]), 2)

    def test_exhaustive_scheduler_matches_bruteforce_small_oracle(self):
        data = scenario({"a": 10, "b": 20, "c": 30},
                        [{"location": "a", "window": [0, 30]},
                         {"location": "b", "kind": "Pickup", "weight_kg": 90, "window": [30, 60]},
                         {"location": "c", "weight_kg": 80}], capacity=100)
        engine = AssignmentEngine(data)
        ids = list(engine.tasks)
        valid = [engine.report(p) for p in permutations(ids) if not engine.report(p)["failures"]]
        self.assertTrue(valid)
        best = min((r["area_reentries"], r["driving_minutes"], r["work_minutes"], r["waiting_minutes"])
                   for r in valid)
        result = engine.schedule(ids)
        self.assertTrue(result.search_complete)
        self.assertEqual(tuple(result.report[k] for k in
                               ("area_reentries", "driving_minutes", "work_minutes", "waiting_minutes")), best)

    def test_scheduler_small_randomized_oracle_and_assignment_integrity(self):
        for seed in range(12):
            rng = random.Random(seed)
            specs = []
            for _ in range(5):
                low = rng.randint(0, 80)
                specs.append({"location": rng.choice("abc"), "window": [low, low + rng.randint(30, 120)],
                              "weight_kg": rng.randint(10, 40), "kind": rng.choice(("Delivery", "Pickup", "Redeliver"))})
            data = scenario({"a": 10, "b": 20, "c": 30}, specs, capacity=100, adjacency=25)
            engine = AssignmentEngine(data)
            valid = [r for order in permutations(engine.tasks)
                     if not (r := engine.report(order))["failures"]]
            result = engine.schedule(tuple(engine.tasks))
            self.assertTrue(result.search_complete)
            self.assertEqual(bool(valid), result.report is not None, msg=f"seed={seed}")
            if valid:
                fields = ("area_reentries", "driving_minutes", "work_minutes", "waiting_minutes")
                self.assertEqual(tuple(result.report[k] for k in fields),
                                 min(tuple(r[k] for k in fields) for r in valid))
            generated, report = engine.run()
            self.assertTrue(analyze(generated)["hard_constraints_pass"], msg=f"seed={seed}")
            self.assertFalse(report["integrity"]["missing"])
            self.assertFalse(report["integrity"]["duplicates"])
            self.assertEqual(report["integrity"]["cross_station"], 0)

    def test_same_postcode_capacity_split_is_explained(self):
        data = scenario({"a": 10, "b": 15}, [{"location": "a", "weight_kg": 100},
                                            {"location": "b", "weight_kg": 100}], capacity=100)
        for loc in data["locations"]:
            loc.update(city="Invented shared", postcode_area="TEST-shared")
        generated, r = plan(data)
        self.assertEqual(len(generated["vehicles"]), 2)
        self.assertTrue(r["hard_constraints_pass"])
        self.assertIn("initial delivery/redelivery capacity", json.dumps(r["planning"]["subarea_splits"]))
        self.assertTrue(all("Subarea split" in v["exceptions"] for v in r["vehicles"]))

    def test_missing_matrix_invalid_pickup_and_invalid_policy_fail_closed(self):
        data = automatic_fixture()
        data["road"]["arcs"].pop()
        with self.assertRaisesRegex(ValueError, "missing directed road arc"):
            plan(data)
        data = automatic_fixture()
        next(t for t in data["tasks"] if t["kind"] == "Pickup")["pickup_location"] = "s0c"
        with self.assertRaisesRegex(ValueError, "actual pickup"):
            plan(data)
        data = automatic_fixture()
        data["config"]["geography_time_basis"] = "traffic_buffered"
        with self.assertRaisesRegex(ValueError, "base_road_minutes"):
            plan(data)

    def test_traffic_only_changes_scheduling_not_geographic_thresholds(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a"}, {"location": "b"}])
        a = AssignmentEngine(data)
        data["config"]["traffic_multiplier"] = 2
        b = AssignmentEngine(data)
        self.assertEqual(a.areas, b.areas)
        self.assertEqual(a.edges, b.edges)
        self.assertEqual(a.territory(["t0", "t1"]), b.territory(["t0", "t1"]))
        ga, ra = a.run()
        gb, rb = b.run()
        self.assertEqual(territories(ga), territories(gb))
        self.assertEqual(rb["summary"]["driving_minutes"], ra["summary"]["driving_minutes"] * 2)

    def test_cli_success_failure_and_path_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, generated, output, md = [root / p for p in ("in.json", "plan.json", "report.json", "report.md")]
            data = scenario({"a": 10}, [{"location": "a"}])
            source.write_text(json.dumps(data))
            cmd = [sys.executable, "-m", "wdxdelivery.planner", str(source), "--plan", str(generated),
                   "--json", str(output), "--markdown", str(md)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertTrue(analyze(json.loads(generated.read_text()))["hard_constraints_pass"])
            self.assertIn("Merge / redistribution", md.read_text())
            data["tasks"][0]["weight_kg"] = 500
            source.write_text(json.dumps(data))
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            self.assertEqual(json.loads(output.read_text())["integrity"]["missing"], ["t0"])
            cmd[cmd.index("--plan") + 1] = str(source)
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
            self.assertEqual(json.loads(source.read_text())["tasks"][0]["weight_kg"], 500)


if __name__ == "__main__":
    unittest.main()
