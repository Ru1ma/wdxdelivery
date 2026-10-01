"""Synthetic automatic-assignment input, with actual invented AM deadlines."""
import json
from pathlib import Path

try:
    from examples.make_synthetic import fixture
except ModuleNotFoundError:
    from make_synthetic import fixture


def automatic_fixture():
    data = fixture()
    data["planning"] = {
        "start_minute": 0, "subarea_max_minutes": 15, "territory_max_minutes": 45,
        "max_extra_driving_minutes": 0, "search_node_budget": 20000,
        "redistribution_node_budget": 2000, "balance_passes": 5}
    data.pop("vehicles")
    for loc in data["locations"]:
        loc.pop("subarea")
    for task in data["tasks"]:
        if task["phase"] == "AM":
            task["window"][1] = 180
    return data


if __name__ == "__main__":
    Path(__file__).with_name("assignment-input.json").write_text(
        json.dumps(automatic_fixture(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
