"""Reproduce safe evidence using only invented fixtures; --check never overwrites."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from examples.make_assignment import automatic_fixture
from examples.make_synthetic import fixture
from examples.make_stress import stress_fixture
from wdxdelivery.baseline import analyze, markdown
from wdxdelivery.planner import plan


def evidence_files():
    old = fixture()
    baseline_v2 = analyze(old)
    automatic_input = automatic_fixture()
    automatic_input['planning']['am_delivery_targets'] = {'stations': {
        station: {'min': 5, 'max': 6} for station in automatic_input['depots']}}
    automatic_input['planning']['phase_driving_slack_minutes'] = 3
    paired = deepcopy(old)
    paired["tasks"] = deepcopy(automatic_input["tasks"])
    paired_report = analyze(paired)
    generated, automatic = plan(automatic_input)
    assert paired_report["hard_constraints_pass"] and automatic["hard_constraints_pass"]
    compare_keys = ("vehicles", "km", "driving_minutes", "waiting_minutes", "service_minutes",
                    "work_minutes", "longest_minutes", "shortest_minutes", "spread_minutes")
    comparison = {
        "basis": "synthetic only; identical task windows, locations and configuration for both plans",
        "fixture_note": "AM windows explicitly end at minute 180 in the paired input; historical reports are retained.",
        "before": paired_report["summary"], "after": automatic["summary"],
        "delta": {k: automatic["summary"][k] - paired_report["summary"][k] for k in compare_keys},
        "before_reentries": sum(v["area_reentries"] for v in paired_report["vehicles"]),
        "after_reentries": sum(v["area_reentries"] for v in automatic["vehicles"]),
        "geographic_review": "pending real/private input; no historical/production optimization claim",
    }
    reports = {"synthetic-baseline-v2": baseline_v2, "paired-baseline": paired_report,
               "automatic-correction": automatic}
    files = {}
    for name, report in reports.items():
        files["evidence/" + name + ".json"] = json.dumps(report, indent=2, sort_keys=True) + "\n"
        files["evidence/" + name + ".md"] = markdown(report) + "\n"
    files["evidence/correction-comparison.json"] = json.dumps(comparison, indent=2, sort_keys=True) + "\n"
    files["examples/correction-input.json"] = json.dumps(automatic_input, indent=2, sort_keys=True) + "\n"
    scale_results = []
    for scale in (1, 2):
        source = stress_fixture(scale)
        generated, report = plan(source)
        assert report['hard_constraints_pass'] and analyze(generated)['hard_constraints_pass']
        scale_results.append({'tasks': len(source['tasks']), 'summary': report['summary'],
                              'integrity': report['integrity'],
                              'search_nodes': report['planning']['search_nodes'],
                              'bounded_queries': report['planning']['bounded_ordering_queries'],
                              'adjacent_merges': sum(e['action'] == 'adjacent_merge' for e in report['merge_analysis'])})
    files['evidence/diverse-scale.json'] = json.dumps(scale_results, indent=2, sort_keys=True) + '\n'
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    mismatches = []
    for name, contents in evidence_files().items():
        path = root / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != contents:
                mismatches.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
    if mismatches:
        parser.exit(1, "Evidence differs: " + ", ".join(mismatches) + "\n")
    print("Invented assignment evidence " + ("matches." if args.check else "generated."))


if __name__ == "__main__":
    main()
