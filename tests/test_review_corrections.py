from copy import deepcopy
import json
import random
import unittest

from tests.test_planner import scenario, territories
from wdxdelivery.baseline import analyze
from wdxdelivery.planner import AssignmentEngine, plan


def rename_locations(data, seed):
    data = deepcopy(data)
    ids = [loc["id"] for loc in data["locations"]]
    labels = [f"opaque-{i:03d}" for i in range(len(ids))]
    random.Random(seed).shuffle(labels)
    mapping = dict(zip(ids, labels))
    for loc in data["locations"]:
        loc["id"] = mapping[loc["id"]]
    for station, depot in data["depots"].items():
        data["depots"][station] = mapping[depot]
    for task in data["tasks"]:
        task["location"] = mapping[task["location"]]
        if "pickup_location" in task:
            task["pickup_location"] = mapping[task["pickup_location"]]
    for arc in data["road"]["arcs"]:
        arc["from"], arc["to"] = mapping[arc["from"]], mapping[arc["to"]]
    random.Random(seed + 1).shuffle(data["locations"])
    random.Random(seed + 2).shuffle(data["road"]["arcs"])
    return data, {value: key for key, value in mapping.items()}


class ReviewCorrectionTests(unittest.TestCase):
    def test_non_low_vehicles_merge_at_workday_boundary(self):
        data = scenario({"a": 10, "b": 20},
                        [{"location": "a", "service_minutes": 280},
                         {"location": "b", "service_minutes": 280}])
        data["config"]["low_utilization_minutes"] = 300
        engine = AssignmentEngine(data)
        self.assertEqual([engine.schedule([tid]).report["work_minutes"] for tid in ("t0", "t1")], [300, 320])
        self.assertFalse(any(engine.schedule([tid]).report["low_utilization"] for tid in ("t0", "t1")))
        generated, report = engine.run()
        self.assertEqual(len(generated["vehicles"]), 1)
        self.assertEqual(report["summary"]["work_minutes"], 600)
        self.assertTrue(analyze(generated)["hard_constraints_pass"])
        self.assertIn("adjacent_merge", [e["action"] for e in report["merge_analysis"]])

    def test_non_low_merge_blockers_are_recorded(self):
        cases = [
            (scenario({"a": 10, "b": 20},
                      [{"location": "a", "service_minutes": 280, "weight_kg": 100},
                       {"location": "b", "service_minutes": 280, "weight_kg": 100}], capacity=100), "capacity"),
            (scenario({"a": 10, "b": 20},
                      [{"location": "a", "window": [300, 301]},
                       {"location": "b", "window": [300, 301]}]), "appointment"),
            (scenario({"a": 10, "b": 20},
                      [{"location": "a", "service_minutes": 290},
                       {"location": "b", "service_minutes": 290}]), "workday"),
            (scenario({"a": 10, "b": 90},
                      [{"location": "a", "service_minutes": 280},
                       {"location": "b", "service_minutes": 280}]), "disconnected"),
        ]
        for data, reason in cases:
            data["config"]["low_utilization_minutes"] = 300
            generated, report = plan(data)
            self.assertEqual(len(generated["vehicles"]), 2, msg=reason)
            self.assertTrue(analyze(generated)["hard_constraints_pass"])
            self.assertIn(reason, json.dumps(report["merge_analysis"]))
            self.assertIn("fleet_merge_retained", [e["action"] for e in report["merge_analysis"]])

    def test_location_renaming_preserves_chain_partition_and_assignment(self):
        data = scenario({"a": 10, "b": 20, "c": 30},
                        [{"location": "a", "weight_kg": 70, "window": [0, 50]},
                         {"location": "b", "weight_kg": 30},
                         {"location": "c", "weight_kg": 70, "window": [200, 400]}],
                        capacity=100, adjacency=15)
        for loc in data["locations"]:
            loc.update(city="Invented shared", postcode_area="TEST-shared")
        original = AssignmentEngine(data)
        reference_areas = sorted(sorted(ids) for ids in original.areas.values())
        reference, r = original.run()
        for seed in range(16):
            renamed, undo = rename_locations(data, seed)
            engine = AssignmentEngine(renamed)
            areas = sorted(sorted(undo[lid] for lid in ids) for ids in engine.areas.values())
            self.assertEqual(reference_areas, areas)
            generated, report = engine.run()
            self.assertEqual(territories(reference), territories(generated))
            self.assertEqual(r["summary"], report["summary"])
            self.assertTrue(analyze(generated)["hard_constraints_pass"])

    def test_symmetric_road_ties_do_not_choose_membership_by_location_id(self):
        data = scenario({"a": 10, "b": 20, "c": 30, "e": 40},
                        [{"location": l} for l in "abce"], adjacency=15)
        for loc in data["locations"]:
            loc.update(city="Invented shared", postcode_area="TEST-shared")
        original, r = plan(data)
        for seed in range(8):
            renamed, _ = rename_locations(data, seed)
            generated, report = plan(renamed)
            self.assertEqual(territories(original), territories(generated))
            self.assertEqual(r["summary"], report["summary"])

    def test_soft_am_target_influences_equal_geography_merge_choice(self):
        data = scenario({"a": 10, "b": 20, "c": 30},
                        [{"location": "b", "phase": "AM", "weight_kg": 40},
                         {"location": "a", "phase": "AM", "weight_kg": 20, "window": [200, 500]},
                         {"location": "a", "phase": "AM", "weight_kg": 20, "window": [200, 500]},
                         {"location": "c", "phase": "AM", "weight_kg": 40, "window": [200, 500]}],
                        capacity=80)
        plain, _ = plan(data)
        data["planning"]["am_delivery_targets"] = {"stations": {"AMS": {"min": 2, "max": 2}}}
        preferred, report = plan(data)
        self.assertNotEqual(territories(plain), territories(preferred))
        self.assertIn(["t0", "t3"], territories(preferred))
        self.assertEqual(len(preferred["vehicles"]), len(plain["vehicles"]))
        self.assertTrue(analyze(preferred)["hard_constraints_pass"])
        self.assertTrue(all(v["am_target"]["penalty"] == 0
                            for v in report["planning"]["full_day_continuity"].values()))

    def test_soft_target_cannot_block_fleet_reduction_or_override_hard_constraints(self):
        data = scenario({"a": 10, "b": 15, "c": 20},
                        [{"location": l, "phase": "AM", "weight_kg": 30} for l in "abc"], capacity=100)
        data["planning"]["am_delivery_targets"] = {"stations": {"AMS": {"min": 1, "max": 2}}}
        generated, report = plan(data)
        self.assertEqual(len(generated["vehicles"]), 1)
        target = next(iter(report["planning"]["full_day_continuity"].values()))["am_target"]
        self.assertEqual(target["deviation"], 1)
        self.assertIn("Fleet reduction", target["reason"])
        self.assertTrue(analyze(generated)["hard_constraints_pass"])
        blocked = scenario({"a": 10, "b": 80}, [{"location": "a", "phase": "AM"},
                                               {"location": "b", "phase": "AM"}])
        blocked["planning"]["am_delivery_targets"] = {"stations": {"AMS": {"min": 2, "max": 2}}}
        self.assertEqual(len(plan(blocked)[0]["vehicles"]), 2)
        blocked = scenario({"a": 10, "b": 20}, [{"location": "a", "phase": "AM", "window": [20, 21]},
                                               {"location": "b", "phase": "AM", "window": [20, 21]}])
        blocked["planning"]["am_delivery_targets"] = {"stations": {"AMS": {"min": 2, "max": 2}}}
        self.assertEqual(len(plan(blocked)[0]["vehicles"]), 2)

    def test_area_target_override_and_pickup_redelivery_exclusion(self):
        data = scenario({"a": 10},
                        [{"location": "a", "phase": "AM"},
                         {"location": "a", "phase": "AM", "kind": "Pickup"},
                         {"location": "a", "phase": "AM", "kind": "Redeliver"}])
        data["planning"]["am_delivery_targets"] = {
            "stations": {"AMS": {"min": 5, "max": 6}},
            "areas": [{"station": "AMS", "city": "Invented a", "postcode_area": "TEST-a", "min": 1, "max": 1}]}
        generated, report = plan(data)
        target = next(iter(report["planning"]["full_day_continuity"].values()))["am_target"]
        self.assertEqual(target["normal_deliveries"], 1)
        self.assertEqual(target["penalty"], 0)
        self.assertEqual(target["source"], "area override")
        self.assertTrue(analyze(generated)["hard_constraints_pass"])

    def test_phase_soft_preference_avoids_equivalent_pm_before_am(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a", "phase": "PM"},
                                           {"location": "b", "phase": "AM"}])
        generated, report = plan(data)
        self.assertEqual(generated["vehicles"][0]["tasks"], ["t1", "t0"])
        phase = next(iter(report["planning"]["full_day_continuity"].values()))["phase_preference"]
        self.assertEqual(phase["pm_before_am_pairs"], 0)
        self.assertTrue(analyze(generated)["hard_constraints_pass"])

    def test_appointments_can_force_soft_phase_inversion(self):
        data = scenario({"a": 10, "b": 20}, [{"location": "a", "phase": "PM", "window": [10, 15]},
                                           {"location": "b", "phase": "AM", "window": [30, 50]}])
        generated, report = plan(data)
        self.assertEqual(generated["vehicles"][0]["tasks"], ["t0", "t1"])
        phase = next(iter(report["planning"]["full_day_continuity"].values()))["phase_preference"]
        self.assertEqual(phase["pm_before_am_pairs"], 1)
        self.assertTrue(analyze(generated)["hard_constraints_pass"])

    def test_phase_handoff_prefers_near_pm_first_at_equal_driving(self):
        data = scenario({"a": 10, "b": 20, "c": 30},
                        [{"location": "c", "phase": "PM"},
                         {"location": "b", "phase": "PM"},
                         {"location": "a", "phase": "AM"}], adjacency=25)
        generated, report = plan(data)
        self.assertEqual(generated["vehicles"][0]["tasks"], ["t2", "t1", "t0"])
        self.assertEqual(report["summary"]["driving_minutes"], 60)
        phase = next(iter(report["planning"]["full_day_continuity"].values()))["phase_preference"]
        self.assertEqual(phase["handoff_base_minutes"], 10)

    def test_invalid_soft_target_and_phase_policy_rejected(self):
        data = scenario({"a": 10}, [{"location": "a"}])
        data["planning"]["am_delivery_targets"] = {"stations": {"AMS": {"min": 7, "max": 5}}}
        with self.assertRaisesRegex(ValueError, "min must not exceed"):
            plan(data)
        data["planning"]["am_delivery_targets"] = {}
        data["planning"]["phase_driving_slack_minutes"] = -1
        with self.assertRaises(ValueError):
            plan(data)


if __name__ == "__main__":
    unittest.main()

class DiverseScaleTests(unittest.TestCase):
    def test_uneven_six_station_growth_preserves_integrity(self):
        from examples.make_stress import stress_fixture
        for scale in (1, 2):
            with self.subTest(scale=scale):
                source = stress_fixture(scale)
                generated, report = plan(source)
                self.assertTrue(report['hard_constraints_pass'])
                self.assertTrue(analyze(generated)['hard_constraints_pass'])
                self.assertEqual(report['summary']['total_tasks'], 104 * scale)
                self.assertEqual(report['integrity'], {'missing': [], 'duplicates': {},
                                                     'unknown': [], 'cross_station': 0})
                self.assertGreater(report['planning']['search_nodes'], 0)
                self.assertTrue(all(v['connected'] for v in report['planning']['full_day_continuity'].values()))

class PhaseOracleTests(unittest.TestCase):
    def test_phase_slack_matches_complete_feasible_order_oracle(self):
        from itertools import permutations
        data = scenario({'a': 10, 'b': 20, 'c': 30, 'e': 25}, [
            {'location': 'a', 'phase': 'PM'}, {'location': 'b', 'phase': 'AM'},
            {'location': 'c', 'phase': 'PM'}, {'location': 'e', 'phase': 'AM'}],
            adjacency=30, diameter=30)
        data['planning']['phase_driving_slack_minutes'] = 15
        engine = AssignmentEngine(data)
        ids = list(engine.tasks)
        candidates = [(order, engine.report(order)) for order in permutations(ids)]
        candidates = [(o,r) for o,r in candidates if not r['failures']]
        reentries = min(r['area_reentries'] for _,r in candidates)
        candidates = [(o,r) for o,r in candidates if r['area_reentries'] == reentries]
        driving = min(r['driving_minutes'] for _,r in candidates)
        candidates = [(o,r) for o,r in candidates if r['driving_minutes'] <= driving + 15]
        expected = min(candidates, key=lambda item: (*engine.phase_cost(item[0]),
            item[1]['driving_minutes'], item[1]['work_minutes'], item[1]['waiting_minutes'], item[0]))[0]
        result = engine.schedule(ids)
        self.assertTrue(result.search_complete)
        self.assertEqual(tuple(result.order), expected)
