"""Automatic station-fixed road territories with bounded, explainable fleet search."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path

from .baseline import (GEOGRAPHY_TIME_BASIS, analyze, informative_route,
                       markdown, number, validate, vehicle_report)


@dataclass
class Schedule:
    order: tuple
    report: dict | None
    reasons: tuple
    search_complete: bool
    nodes: int
    continuity_exception: str = ""


class AssignmentEngine:
    def __init__(self, source):
        self.data = deepcopy(source)
        # Supplied assignments and subarea labels are not inputs to automatic grouping.
        self.data["vehicles"] = []
        for loc in self.data["locations"]:
            loc["subarea"] = f"{loc['city']} / {loc['postcode_area']}"
        self.cfg, self.locations, self.tasks, _, self.arcs = validate(self.data)
        self.settings = self.data["planning"]
        for field in ("start_minute", "subarea_max_minutes", "territory_max_minutes",
                      "max_extra_driving_minutes"):
            number(self.settings[field], field)
        if not (self.settings["subarea_max_minutes"] <= self.cfg["adjacency_minutes"]
                <= self.settings["territory_max_minutes"]):
            raise ValueError("require subarea_max <= adjacency <= territory_max (base road minutes)")
        for field in ("search_node_budget", "redistribution_node_budget", "balance_passes"):
            value = self.settings[field]
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{field} must be a positive integer")
        self.cache = {}
        self.events = []
        self.unassigned = []
        self.split_reasons = {}
        self.search_nodes = 0
        self.areas = self.derive_subareas()
        self.edges = self.area_edges()

    def minutes(self, a, b):
        return max(self.arcs[a, b]["minutes"], self.arcs[b, a]["minutes"])

    def derive_subareas(self):
        """City/postcode seeds, then complete-link road splitting; never Route labels."""
        seeds = defaultdict(set)
        for task in self.tasks.values():
            loc = self.locations[task["location"]]
            seeds[loc["station"], loc["city"], loc["postcode_area"]].add(loc["id"])
        areas = {}
        for (station, city, postcode), ids in sorted(seeds.items()):
            clusters = []
            for loc_id in sorted(ids):
                candidates = [(max(self.minutes(loc_id, x) for x in cluster), i)
                              for i, cluster in enumerate(clusters)]
                candidates = [c for c in candidates if c[0] <= self.settings["subarea_max_minutes"]]
                if candidates:
                    clusters[min(candidates)[1]].append(loc_id)
                else:
                    clusters.append([loc_id])
            for i, cluster in enumerate(clusters, 1):
                # Structured identity avoids collisions when city/postcode text contains delimiters.
                area = json.dumps([station, city, postcode, i], ensure_ascii=False, separators=(",", ":"))
                areas[area] = tuple(cluster)
                for loc_id in cluster:
                    self.locations[loc_id]["subarea"] = area
        return areas

    def area_edges(self):
        edges = defaultdict(set)
        keys = sorted(self.areas)
        for i, a in enumerate(keys):
            edges[a]  # Retain isolated working areas.
            for b in keys[i + 1:]:
                if self.locations[self.areas[a][0]]["station"] != self.locations[self.areas[b][0]]["station"]:
                    continue
                # A close boundary pair alone is insufficient: every cross-pair must be close.
                spread = max(self.minutes(x, y) for x in self.areas[a] for y in self.areas[b])
                if spread <= self.cfg["adjacency_minutes"]:
                    edges[a].add(b)
                    edges[b].add(a)
        return edges

    def territory(self, ids):
        locs = sorted({self.tasks[t]["location"] for t in ids})
        stations = {self.tasks[t]["station"] for t in ids}
        if len(stations) != 1:
            return False, {"reason": "station boundary"}
        areas = {self.locations[x]["subarea"] for x in locs}
        visited = set()
        pending = [min(areas)]
        while pending:
            area = pending.pop()
            if area in visited:
                continue
            visited.add(area)
            pending.extend(sorted((self.edges[area] & areas) - visited))
        diameter = max(self.minutes(a, b) for a in locs for b in locs)
        info = {"areas": sorted(areas), "diameter_base_minutes": diameter,
                "connected": visited == areas, "time_basis": GEOGRAPHY_TIME_BASIS}
        if visited != areas:
            return False, {**info, "reason": "disconnected road subareas"}
        if diameter > self.settings["territory_max_minutes"]:
            return False, {**info, "reason": "territory road diameter exceeded"}
        return True, info

    def raw_vehicle(self, ids, name="candidate", explanation=""):
        return {"id": name, "station": self.tasks[ids[0]]["station"],
                "start_minute": self.settings["start_minute"], "tasks": list(ids),
                "explanation": explanation}

    def report(self, ids):
        return vehicle_report(self.raw_vehicle(ids), self.tasks, self.locations,
                              self.data["depots"], self.arcs, self.cfg)

    def schedule(self, ids):
        key = tuple(sorted(ids))
        if key in self.cache:
            return self.cache[key]
        result = self._schedule(key)
        self.search_nodes += result.nodes
        self.cache[key] = result
        return result

    def _schedule(self, ids):
        ts = [self.tasks[t] for t in ids]
        initial_load = sum(t["weight_kg"] for t in ts if t["kind"] != "Pickup")
        reasons = set()
        if initial_load > self.cfg["capacity_kg"]:
            reasons.add("initial delivery/redelivery capacity")
        if sum(t["weight_kg"] for t in ts if t["kind"] == "Pickup") > self.cfg["capacity_kg"]:
            reasons.add("final pickup capacity")
        cap = self.cfg["task_cap"]
        if cap and (len(ts) if cap["scope"] == "all_tasks" else
                    sum(t["kind"] == "Delivery" for t in ts)) > cap["limit"]:
            reasons.add("explicit task cap")
        if self.cfg["loading_minutes"] + sum(t["service_minutes"] for t in ts) > self.cfg["max_work_minutes"]:
            reasons.add("loading/service workday lower bound")
        if reasons:
            return Schedule((), None, tuple(sorted(reasons)), True, 0)
        start = self.settings["start_minute"]
        clock = start + self.cfg["loading_minutes"]
        depot = self.data["depots"][ts[0]["station"]]
        total_nodes = 0
        continuous_complete = False
        continuous_reasons = ()

        def advance(task, current, now, load):
            arrive = now + self.arcs[current, task["location"]]["minutes"] * self.cfg["traffic_multiplier"]
            finish = max(arrive, task["window"][0]) + task["service_minutes"]
            newload = load + (task["weight_kg"] if task["kind"] == "Pickup" else -task["weight_kg"])
            if finish > task["window"][1]:
                return None, "appointment/service completion"
            if newload > self.cfg["capacity_kg"]:
                return None, "dynamic pickup capacity"
            if finish - start > self.cfg["max_work_minutes"]:
                return None, "maximum workday"
            return (finish, newload), None

        for continuous in (True, False):
            best = None
            best_score = None
            nodes = 0
            exhausted = False
            blocked = set()

            def visit(path, remaining, current, now, load, closed, area):
                nonlocal nodes, exhausted, best, best_score
                if nodes >= self.settings["search_node_budget"]:
                    exhausted = True
                    return
                nodes += 1
                if not remaining:
                    r = self.report(path)
                    if r["failures"]:
                        blocked.add("return-to-depot maximum workday")
                        return
                    score = (r["area_reentries"], r["driving_minutes"],
                             r["work_minutes"], r["waiting_minutes"], tuple(path))
                    if best_score is None or score < best_score:
                        best, best_score = (tuple(path), r), score
                    return
                candidates = sorted(remaining, key=lambda t: (
                    self.tasks[t]["window"][1],
                    self.arcs[current, self.tasks[t]["location"]]["minutes"],
                    self.tasks[t]["window"][0], t))
                equivalent = set()
                for tid in candidates:
                    t = self.tasks[tid]
                    signature = (t["location"], t["kind"], t["phase"], t["weight_kg"],
                                 t["service_minutes"], tuple(t["window"]))
                    if signature in equivalent:
                        continue  # Interchangeable task permutations cannot change feasibility/cost.
                    equivalent.add(signature)
                    newarea = self.locations[t["location"]]["subarea"]
                    if continuous and newarea in closed:
                        continue
                    next_state, failure = advance(t, current, now, load)
                    if failure:
                        blocked.add(failure)
                        continue
                    newclosed = closed | ({area} if area is not None and area != newarea else set())
                    visit(path + [tid], remaining - {tid}, t["location"],
                          *next_state, newclosed, newarea)
                    if exhausted:
                        break

            visit([], set(ids), depot, clock, initial_load, set(), None)
            total_nodes += nodes
            if best is not None:
                exception = ""
                if not continuous:
                    exception = (
                        "Contiguous-area sequencing has no feasible ordering; exhaustive search "
                        if continuous_complete else
                        "No contiguous-area ordering found within the search budget; ") + (
                        "observed blockers: " + ", ".join(continuous_reasons))
                return Schedule(best[0], best[1], (), not exhausted, total_nodes, exception)
            reasons.update(blocked)
            if continuous:
                continuous_complete = not exhausted
                continuous_reasons = tuple(sorted(blocked))
        if exhausted or not continuous_complete:
            reasons.add("bounded ordering search exhausted; no infeasibility proof")
        return Schedule((), None, tuple(sorted(reasons)), not exhausted and continuous_complete, total_nodes)

    def pack_subareas(self):
        groups = []
        byarea = defaultdict(list)
        for tid in sorted(self.tasks):
            byarea[self.locations[self.tasks[tid]["location"]]["subarea"]].append(tid)
        for area, ids in sorted(byarea.items()):
            whole = self.schedule(ids)
            if whole.report:
                groups.append(whole.order)
                continue
            self.split_reasons[area] = {"reasons": list(whole.reasons),
                                       "search_complete": whole.search_complete}
            bylocation = defaultdict(list)
            for tid in ids:
                bylocation[self.tasks[tid]["location"]].append(tid)
            blocks = []
            for _, block in sorted(bylocation.items()):
                if self.schedule(block).report:
                    blocks.append(block)
                else:
                    blocks.extend([[t] for t in sorted(block, key=lambda t: (self.tasks[t]["window"][1], t))])
            packs = []
            for block in blocks:
                options = []
                for i, pack in enumerate(packs):
                    result = self.schedule(tuple(pack) + tuple(block))
                    if result.report:
                        options.append((result.report["driving_minutes"], i, result.order))
                if options:
                    _, i, order = min(options)
                    packs[i] = order
                else:
                    result = self.schedule(block)
                    if result.report:
                        packs.append(result.order)
                    else:
                        self.unassigned.extend({"task": t, "reasons": list(result.reasons),
                                                "search_complete": result.search_complete} for t in block)
            groups.extend(packs)
        return groups

    def acceptable_order(self, result, previous):
        if not result.report:
            return False
        old_reentries = sum(self.schedule(g).report["area_reentries"] for g in previous)
        if result.report["area_reentries"] > old_reentries:
            # Never call a budget-limited failure proof of an unavoidable reentry.
            if not result.continuity_exception.startswith("Contiguous-area sequencing has no feasible"):
                return False
        return True

    def pair_merge(self, a, b):
        ok, geo = self.territory(tuple(a) + tuple(b))
        if not ok:
            return None, [geo["reason"]], geo
        result = self.schedule(tuple(a) + tuple(b))
        if not result.report:
            return None, list(result.reasons), {**geo, "search_complete": result.search_complete}
        if not self.acceptable_order(result, [a, b]):
            return None, ["unjustified area reentry after bounded search"], geo
        old_driving = sum(self.schedule(g).report["driving_minutes"] for g in (a, b))
        if result.report["driving_minutes"] > old_driving + self.settings["max_extra_driving_minutes"]:
            return None, ["full-day driving detour allowance exceeded"], geo
        return result, [], geo

    def redistribute(self, donor, recipients):
        """Try eliminating a low-use vehicle across neighbors using whole location blocks."""
        blocks = defaultdict(list)
        for tid in donor:
            blocks[self.tasks[tid]["location"]].append(tid)
        blocks = [tuple(v) for _, v in sorted(blocks.items())]
        nodes = 0
        exhausted = False
        ordering_complete = True
        reasons = set()
        old_driving = sum(self.schedule(g).report["driving_minutes"] for g in [donor] + recipients)

        def search(index, current):
            nonlocal nodes, exhausted, ordering_complete
            if nodes >= self.settings["redistribution_node_budget"]:
                exhausted = True
                return None
            nodes += 1
            if index == len(blocks):
                drive = sum(self.schedule(g).report["driving_minutes"] for g in current)
                if drive <= old_driving + self.settings["max_extra_driving_minutes"]:
                    return current
                reasons.add("full-day driving detour allowance exceeded")
                return None
            block = blocks[index]
            for i, group in enumerate(current):
                ids = tuple(group) + block
                ok, geo = self.territory(ids)
                if not ok:
                    reasons.add(geo["reason"])
                    continue
                result = self.schedule(ids)
                ordering_complete = ordering_complete and result.search_complete
                if not result.report:
                    reasons.update(result.reasons)
                    continue
                if not self.acceptable_order(result, [group]):
                    reasons.add("unjustified area reentry after bounded search")
                    continue
                changed = current[:i] + [result.order] + current[i + 1:]
                found = search(index + 1, changed)
                if found is not None:
                    return found
                if exhausted:
                    return None
            return None

        found = search(0, list(recipients)) if recipients else None
        if not recipients:
            reasons.add("no same-station recipient")
        if exhausted:
            reasons.add("redistribution node budget exhausted")
        return found, {"nodes": nodes, "search_complete": not exhausted and ordering_complete,
                       "ordering_queries_complete": ordering_complete,
                       "reasons": sorted(reasons),
                       "scope": "whole-location redistribution; no global infeasibility proof"}

    def reduce_fleet(self, groups):
        groups = list(groups)
        while True:
            changed = False
            low = sorted([g for g in groups if self.schedule(g).report["low_utilization"]],
                         key=lambda g: (self.schedule(g).report["work_minutes"], tuple(sorted(g))))
            for donor in low:
                station = self.tasks[donor[0]]["station"]
                recipients = sorted([g for g in groups if g != donor and self.tasks[g[0]]["station"] == station],
                                    key=lambda g: tuple(sorted(g)))
                options, attempts = [], []
                for recipient in recipients:
                    result, reasons, geo = self.pair_merge(donor, recipient)
                    attempts.append({"recipient": sorted(recipient), "reasons": reasons, "geography": geo})
                    if result:
                        score = (result.report["area_reentries"], geo["diameter_base_minutes"],
                                 result.report["driving_minutes"], result.report["work_minutes"],
                                 tuple(sorted(recipient)))
                        options.append((score, recipient, result.order))
                if options:
                    _, recipient, order = min(options)
                    groups.remove(donor)
                    groups.remove(recipient)
                    groups.append(order)
                    self.events.append({"action": "adjacent_merge", "station": station,
                                        "source": sorted(donor), "recipient": sorted(recipient),
                                        "result": list(order), "attempts": attempts})
                    changed = True
                    break
                found, search = self.redistribute(donor, recipients)
                if found is not None:
                    groups = [g for g in groups if g != donor and g not in recipients] + found
                    self.events.append({"action": "adjacent_redistribution", "station": station,
                                        "source": sorted(donor), "recipients_after": [list(g) for g in found],
                                        "attempts": attempts, "search": search})
                    changed = True
                    break
                self.events.append({"action": "low_utilization_retained", "station": station,
                                    "source": sorted(donor), "attempts": attempts,
                                    "redistribution": search,
                                    "conclusion": "No feasible merge/redistribution found in the stated search scope."})
            if not changed:
                return groups

    def balance(self, groups):
        groups = list(groups)
        for _ in range(self.settings["balance_passes"]):
            options = []
            for i, donor in enumerate(groups):
                blocks = defaultdict(list)
                for tid in donor:
                    blocks[self.locations[self.tasks[tid]["location"]]["subarea"]].append(tid)
                for block in blocks.values():
                    remaining = tuple(t for t in donor if t not in block)
                    if not remaining or not self.territory(remaining)[0]:
                        continue
                    for j, recipient in enumerate(groups):
                        if i == j or self.tasks[donor[0]]["station"] != self.tasks[recipient[0]]["station"]:
                            continue
                        joined = tuple(recipient) + tuple(block)
                        if not self.territory(joined)[0]:
                            continue
                        a, b = self.schedule(remaining), self.schedule(joined)
                        if (not a.report or not b.report or not self.acceptable_order(a, [donor])
                                or not self.acceptable_order(b, [recipient])):
                            continue
                        old = [self.schedule(g).report for g in (donor, recipient)]
                        old_drive = sum(r["driving_minutes"] for r in old)
                        new_drive = a.report["driving_minutes"] + b.report["driving_minutes"]
                        station_groups = [g for g in groups if self.tasks[g[0]]["station"] == self.tasks[donor[0]]["station"]]
                        old_work = [self.schedule(g).report["work_minutes"] for g in station_groups]
                        new_work = [self.schedule(g).report["work_minutes"] for g in station_groups if g not in (donor, recipient)]
                        new_work += [a.report["work_minutes"], b.report["work_minutes"]]
                        improvement = (max(old_work) - min(old_work)) - (max(new_work) - min(new_work))
                        if improvement > 0 and new_drive <= old_drive + self.settings["max_extra_driving_minutes"]:
                            options.append((-improvement, new_drive, i, j, a.order, b.order, tuple(block)))
            if not options:
                break
            _, _, i, j, a, b, block = min(options)
            groups[i], groups[j] = a, b
            self.events.append({"action": "adjacent_workload_balance", "moved": sorted(block),
                                "donor_after": list(a), "recipient_after": list(b)})
        return groups

    def run(self):
        groups = self.pack_subareas()
        groups = self.reduce_fleet(self.balance(groups))
        balanced = self.balance(groups)
        if balanced != groups:
            groups = self.reduce_fleet(balanced)
        groups.sort(key=lambda g: (self.tasks[g[0]]["station"], tuple(sorted(g))))
        vehicles = []
        numbers = Counter()
        continuity = {}
        for group in groups:
            station = self.tasks[group[0]]["station"]
            numbers[station] += 1
            vid = f"{station}-{numbers[station]}"
            ok, geo = self.territory(group)
            if not ok:
                raise RuntimeError("Internal error: noncontinuous territory")
            result = self.schedule(group)
            explanations = []
            for area in geo["areas"]:
                if area in self.split_reasons:
                    explanations.append("Subarea split: " + json.dumps(self.split_reasons[area], sort_keys=True))
            if result.continuity_exception:
                explanations.append(result.continuity_exception)
            routes = {str(self.tasks[t]["route"]) for t in group if informative_route(self.tasks[t]["route"])}
            if len(routes) > 2:
                explanations.append("More than two informative Routes permitted: connected compact road territory; labels did not determine grouping.")
            vehicles.append(self.raw_vehicle(result.order, vid, "; ".join(explanations)))
            am = [self.tasks[t]["location"] for t in group if self.tasks[t]["phase"] == "AM"]
            pm = [self.tasks[t]["location"] for t in group if self.tasks[t]["phase"] == "PM"]
            continuity[vid] = {**geo, "max_am_pm_base_minutes":
                               max((self.minutes(a, b) for a in am for b in pm), default=None),
                               "ordering_search_complete": result.search_complete}
        self.data["vehicles"] = vehicles
        report = analyze(self.data)
        report["merge_analysis"] = self.events
        report["planning"] = {
            "method": "city/postcode road subareas; connected bounded-diameter territories",
            "settings": self.settings, "subareas": self.areas,
            "area_graph_edges": [
                {"areas": [a, b], "max_cross_base_minutes":
                 max(self.minutes(x, y) for x in self.areas[a] for y in self.areas[b])}
                for a in sorted(self.edges) for b in sorted(self.edges[a]) if a < b],
            "subarea_splits": self.split_reasons, "unassigned": self.unassigned,
            "full_day_continuity": continuity, "search_nodes": self.search_nodes,
            "bounded_ordering_queries": sum(not r.search_complete for r in self.cache.values()),
            "route_preference": "advisory only; no Route labels used in grouping or tie-breaking",
            "geography_time_basis": GEOGRAPHY_TIME_BASIS}
        if not self.unassigned and not report["hard_constraints_pass"]:
            raise RuntimeError("Internal error: assignment failed independent baseline validator")
        return self.data, report


def plan(data):
    return AssignmentEngine(data).run()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    paths = (args.input, args.plan, args.json, args.markdown)
    if len({p.resolve() for p in paths}) != len(paths):
        parser.exit(2, "Input and output paths must be distinct.\n")
    try:
        generated, report = plan(json.loads(args.input.read_text(encoding="utf-8")))
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Invalid planner input: {error}\n")
    for path in paths[1:]:
        path.parent.mkdir(parents=True, exist_ok=True)
    args.plan.write_text(json.dumps(generated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown.write_text(markdown(report) + "\n", encoding="utf-8")
    if not report["hard_constraints_pass"]:
        parser.exit(1, "Incomplete assignment; inspect unassigned task reasons.\n")


if __name__ == "__main__":
    main()
