import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from examples.make_synthetic import fixture
from wdxdelivery.baseline import analyze


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()

    def test_six_station_metrics_against_manual_calculation(self):
        r = analyze(self.data)
        self.assertTrue(r["hard_constraints_pass"])
        self.assertEqual(r["integrity"], {"missing": [], "duplicates": {}, "unknown": [],
                                          "cross_station": 0})
        summary = r["summary"]
        for key, value in {"total_tasks": 30, "Delivery": 18, "Pickup": 6, "Redeliver": 6,
                           "vehicles": 12, "km": 1176, "driving_minutes": 1764,
                           "waiting_minutes": 1680, "service_minutes": 300,
                           "work_minutes": 3924, "longest_minutes": 358,
                           "shortest_minutes": 296, "spread_minutes": 62}.items():
            self.assertAlmostEqual(summary[key], value, msg=key)
        self.assertEqual(len(r["stations"]), 6)
        for s in r["stations"]:
            self.assertEqual(s["total_tasks"], 5)
            self.assertAlmostEqual(s["work_minutes"], 654)
        near = next(v for v in r["vehicles"] if v["id"] == "AMS-near")
        self.assertEqual(near["normal_deliveries_by_phase"], {"AM": 2, "PM": 0, "flexible": 0})
        self.assertEqual(near["peak_kg"], 300)
        self.assertEqual(near["area_reentries"], 2)
        self.assertEqual(near["am_pm_transitions"][0]["minutes"], 10)

    def test_route_one_neighbors_five_not_two(self):
        s = analyze(self.data)["stations"][0]
        self.assertEqual(s["neighbors"], [{"areas": ["alpha", "beta"], "minutes": 10}])
        self.assertIn({"areas": ["alpha", "gamma"], "minutes": 80}, s["separate_areas"])

    def test_route_renumbering_only_changes_labels(self):
        original = analyze(self.data)
        for t in self.data["tasks"]:
            if t["route"] is not None:
                t["route"] = {"1": "90", "5": "3", "2": "7", "0": "0"}[t["route"]]
        changed = analyze(self.data)
        for a, b in zip(original["stations"], changed["stations"]):
            for field in ("neighbors", "separate_areas", "overlapping_areas"):
                self.assertEqual(a[field], b[field])
        for a, b in zip(original["vehicles"], changed["vehicles"]):
            self.assertEqual(a["area_sequence"], b["area_sequence"])
        self.assertEqual(original["summary"], changed["summary"])

    def test_large_route_distant_subareas_are_reported(self):
        for t in self.data["tasks"]:
            t["route"] = "shared"
        s = analyze(self.data)["stations"][0]
        self.assertEqual(s["distant_routes"][0]["route"], "shared")
        self.assertEqual(len(s["distant_routes"][0]["distant_pairs"]), 2)

    def test_route_zero_and_missing_use_same_geography(self):
        before = analyze(self.data)
        for t in self.data["tasks"]:
            t["route"] = None if t["kind"] == "Pickup" else 0
        after = analyze(self.data)
        self.assertEqual(before["stations"][5]["neighbors"], after["stations"][5]["neighbors"])
        self.assertEqual(set(after["stations"][5]["routes"]), {"0", "(missing)"})

    def test_pickup_actual_location_required(self):
        self.data["tasks"][2]["pickup_location"] = "s0c"
        with self.assertRaisesRegex(ValueError, "actual pickup"):
            analyze(self.data)

    def test_pickup_load_increases_and_redelivery_unloads(self):
        self.data["tasks"][2]["weight_kg"] = 350
        r = analyze(self.data)
        v = next(v for v in r["vehicles"] if v["id"] == "AMS-near")
        self.assertEqual([s["load_kg"] for s in v["stops"]], [200, 100, 450, 350])
        self.assertEqual(v["Delivery"], 2)
        self.assertIn("capacity exceeded: s0t3", v["failures"])
        self.assertFalse(r["hard_constraints_pass"])

    def test_initial_load_includes_redelivery(self):
        self.data["config"]["capacity_kg"] = 250
        r = analyze(self.data)
        self.assertIn("initial capacity exceeded",
                      next(v for v in r["vehicles"] if v["id"] == "AMS-near")["failures"])

    def test_time_window_checks_service_completion(self):
        self.data["tasks"][0]["window"] = [0, 40]  # Arrival 33; service completion 43.
        r = analyze(self.data)
        self.assertIn("time window exceeded: s0t1",
                      next(v for v in r["vehicles"] if v["id"] == "AMS-near")["failures"])

    def test_return_to_depot_counts_in_workday(self):
        self.data["config"]["max_work_minutes"] = 300
        r = analyze(self.data)
        far = next(v for v in r["vehicles"] if v["id"] == "AMS-far")
        self.assertEqual(far["stops"][-1]["service_end"], 250)
        self.assertIn("maximum workday exceeded", far["failures"])

    def test_explicit_count_cap_scope(self):
        self.data["config"]["task_cap"] = {"scope": "normal_deliveries", "limit": 2}
        self.assertTrue(analyze(self.data)["hard_constraints_pass"])
        self.data["config"]["task_cap"]["scope"] = "all_tasks"
        self.assertFalse(analyze(self.data)["hard_constraints_pass"])

    def test_missing_duplicate_unknown_and_cross_station(self):
        self.data["vehicles"][0]["tasks"] = ["s0t1", "s0t1", "s1t1", "unknown"]
        r = analyze(self.data)
        self.assertFalse(r["hard_constraints_pass"])
        self.assertEqual(r["integrity"]["duplicates"], {"s0t1": 1, "s1t1": 1})
        self.assertEqual(r["integrity"]["cross_station"], 1)
        self.assertEqual(r["integrity"]["unknown"], ["unknown"])
        self.assertEqual(r["integrity"]["missing"], ["s0t2", "s0t3", "s0t4"])
        self.assertIsNone(r["summary"]["km"])

    def test_directed_adjacency_requires_both_directions(self):
        for arc in self.data["road"]["arcs"]:
            if arc["from"] == "s0b" and arc["to"] == "s0a":
                arc["minutes"] = 60
        s = analyze(self.data)["stations"][0]
        self.assertEqual(s["neighbors"], [])

    def test_unknown_arc_fails_closed(self):
        self.data["road"]["arcs"].pop()
        with self.assertRaisesRegex(ValueError, "missing directed road arc"):
            analyze(self.data)

    def test_approximation_label_preserved(self):
        self.data["road"]["basis"] = "approximation"
        self.assertEqual(analyze(self.data)["evidence"]["road_basis"], "approximation")

    def test_overlap_and_cross_region_jumps_are_observable(self):
        self.data["vehicles"][1]["tasks"] = ["s0t2", "s0t5"]
        self.data["vehicles"][0]["tasks"].remove("s0t2")
        r = analyze(self.data)
        self.assertEqual(r["stations"][0]["overlapping_areas"], {"beta": ["AMS-far", "AMS-near"]})
        v = next(v for v in r["vehicles"] if v["id"] == "AMS-far")
        self.assertEqual(v["cross_region_jumps"][0]["minutes"], 70)

    def test_absent_station_not_claimed_diagnostic_complete(self):
        self.data["tasks"] = self.data["tasks"][:5]
        self.data["vehicles"] = self.data["vehicles"][:2]
        self.assertFalse(analyze(self.data)["stations"][5]["data_available"])

    def test_schema_rejects_nonfinite_negative_and_duplicate_inputs(self):
        for field, value in (("capacity_kg", float("nan")), ("traffic_multiplier", 0.5),
                             ("loading_minutes", -1), ("capacity_kg", True)):
            data = copy.deepcopy(self.data)
            data["config"][field] = value
            with self.assertRaises(ValueError):
                analyze(data)
        self.data["tasks"].append(copy.deepcopy(self.data["tasks"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            analyze(self.data)

    def test_source_and_configuration_evidence_required(self):
        self.data["config"]["evidence"] = None
        with self.assertRaisesRegex(ValueError, "configuration evidence"):
            analyze(self.data)
        self.data = fixture()
        self.data["road"]["source"] = ""
        with self.assertRaisesRegex(ValueError, "road source"):
            analyze(self.data)

    def test_cli_prevents_overwriting_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "in.json"
            original = json.dumps(self.data)
            source.write_text(original)
            cmd = [sys.executable, "-m", "wdxdelivery", str(source), "--json", str(source),
                   "--markdown", str(Path(tmp) / "out.md")]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
            self.assertEqual(source.read_text(), original)

    def test_cli_exit_status_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, output, md = root / "in.json", root / "out.json", root / "out.md"
            cmd = [sys.executable, "-m", "wdxdelivery", str(source), "--json", str(output),
                   "--markdown", str(md)]
            source.write_text(json.dumps(self.data))
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertIn("BELGEM", md.read_text())
            self.data["vehicles"][0]["tasks"].pop()
            source.write_text(json.dumps(self.data))
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            self.assertFalse(json.loads(output.read_text())["hard_constraints_pass"])
            source.write_text("{}")
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
