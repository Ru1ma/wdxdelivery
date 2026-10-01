# Dispatch baseline diagnostic

Evidence basis: synthetic; Invented symmetric travel table, not real road travel..
Operational geography review: pending. No optimization/production acceptance claim.
Geographic thresholds: base road minutes; scheduling: traffic-buffered minutes.
Merge analysis: 18 decisions; see section below.

Integrity: {"cross_station": 0, "duplicates": {}, "missing": [], "unknown": []}
Hard constraints pass: True

All times below are minutes; driving applies the explicit traffic multiplier.
Time windows require completion of service by the end. Depot return is included.

Global: {"Delivery": 18, "Pickup": 6, "Redeliver": 6, "driving_minutes": 1656.0, "km": 1104.0, "longest_minutes": 358.0, "metrics_available": true, "service_minutes": 300, "shortest_minutes": 290.0, "spread_minutes": 68.0, "total_tasks": 30, "vehicles": 12, "waiting_minutes": 1752.0, "work_minutes": 3888.0}

| Station | Tasks / Delivery / Pickup / Redeliver | Vehicles | km | Driving | Waiting | Work | Longest / shortest / spread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AMS | [5, 3, 1, 1] | 2 | 184.0 | 276.0 | 292.0 | 648.0 | [358.0, 290.0, 68.0] |
| ROT | [5, 3, 1, 1] | 2 | 184.0 | 276.0 | 292.0 | 648.0 | [358.0, 290.0, 68.0] |
| DEN HAAG | [5, 3, 1, 1] | 2 | 184.0 | 276.0 | 292.0 | 648.0 | [358.0, 290.0, 68.0] |
| UTRECHT | [5, 3, 1, 1] | 2 | 184.0 | 276.0 | 292.0 | 648.0 | [358.0, 290.0, 68.0] |
| TILBURG | [5, 3, 1, 1] | 2 | 184.0 | 276.0 | 292.0 | 648.0 | [358.0, 290.0, 68.0] |
| BELGEM | [5, 3, 1, 1] | 2 | 184.0 | 276.0 | 292.0 | 648.0 | [358.0, 290.0, 68.0] |

## AMS

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"], "minutes": 10}]

separate_areas: [{"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 80}, {"areas": ["[\"AMS\",\"Invented beta\",\"TEST-beta\",1]", "[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## ROT

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"], "minutes": 10}]

separate_areas: [{"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 80}, {"areas": ["[\"ROT\",\"Invented beta\",\"TEST-beta\",1]", "[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## DEN HAAG

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"], "minutes": 10}]

separate_areas: [{"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 80}, {"areas": ["[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]", "[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## UTRECHT

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"], "minutes": 10}]

separate_areas: [{"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 80}, {"areas": ["[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]", "[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## TILBURG

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"], "minutes": 10}]

separate_areas: [{"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 80}, {"areas": ["[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]", "[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## BELGEM

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"], "minutes": 10}]

separate_areas: [{"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 80}, {"areas": ["[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]", "[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## Vehicle AMS-1

| Metric | Value |
| --- | --- |
| id | AMS-1 |
| station | AMS |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| informative_routes | ["1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"], "PM": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"], "flexible": []} |
| am_pm_transitions | [{"from": "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]", "minutes": 0, "to": "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"}] |
| area_sequence | ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]", "[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]"] |
| area_reentries | 1 |
| cross_region_jumps | [] |
| km | 40.0 |
| driving_minutes | 60.0 |
| service_minutes | 40 |
| waiting_minutes | 175.0 |
| loading_minutes | 15 |
| work_minutes | 290.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | False |
| exceptions | Contiguous-area sequencing has no feasible ordering; exhaustive search observed blockers: appointment/service completion |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s0t1 | ["AMS","Invented alpha","TEST-alpha",1] | AM | 33.0 | 43.0 | 200 |
| s0t2 | ["AMS","Invented beta","TEST-beta",1] | AM | 55.0 | 65.0 | 100 |
| s0t4 | ["AMS","Invented beta","TEST-beta",1] | PM | 240.0 | 250.0 | 0 |
| s0t3 | ["AMS","Invented alpha","TEST-alpha",1] | PM | 262.0 | 272.0 | 50 |

## Vehicle AMS-2

| Metric | Value |
| --- | --- |
| id | AMS-2 |
| station | AMS |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| informative_routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"] |
| area_reentries | 0 |
| cross_region_jumps | [] |
| km | 144.0 |
| driving_minutes | 216.0 |
| service_minutes | 10 |
| waiting_minutes | 117.0 |
| loading_minutes | 15 |
| work_minutes | 358.0 |
| peak_kg | 100 |
| low_utilization | False |
| more_than_two_routes | False |
| exceptions |  |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s0t5 | ["AMS","Invented gamma","TEST-gamma",1] | PM | 240.0 | 250.0 | 0 |

## Vehicle BELGEM-1

| Metric | Value |
| --- | --- |
| id | BELGEM-1 |
| station | BELGEM |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| informative_routes | ["1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"], "PM": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"], "flexible": []} |
| am_pm_transitions | [{"from": "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]", "minutes": 0, "to": "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"}] |
| area_sequence | ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]", "[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]"] |
| area_reentries | 1 |
| cross_region_jumps | [] |
| km | 40.0 |
| driving_minutes | 60.0 |
| service_minutes | 40 |
| waiting_minutes | 175.0 |
| loading_minutes | 15 |
| work_minutes | 290.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | False |
| exceptions | Contiguous-area sequencing has no feasible ordering; exhaustive search observed blockers: appointment/service completion |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s5t1 | ["BELGEM","Invented alpha","TEST-alpha",1] | AM | 33.0 | 43.0 | 200 |
| s5t2 | ["BELGEM","Invented beta","TEST-beta",1] | AM | 55.0 | 65.0 | 100 |
| s5t4 | ["BELGEM","Invented beta","TEST-beta",1] | PM | 240.0 | 250.0 | 0 |
| s5t3 | ["BELGEM","Invented alpha","TEST-alpha",1] | PM | 262.0 | 272.0 | 50 |

## Vehicle BELGEM-2

| Metric | Value |
| --- | --- |
| id | BELGEM-2 |
| station | BELGEM |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| informative_routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"] |
| area_reentries | 0 |
| cross_region_jumps | [] |
| km | 144.0 |
| driving_minutes | 216.0 |
| service_minutes | 10 |
| waiting_minutes | 117.0 |
| loading_minutes | 15 |
| work_minutes | 358.0 |
| peak_kg | 100 |
| low_utilization | False |
| more_than_two_routes | False |
| exceptions |  |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s5t5 | ["BELGEM","Invented gamma","TEST-gamma",1] | PM | 240.0 | 250.0 | 0 |

## Vehicle DEN HAAG-1

| Metric | Value |
| --- | --- |
| id | DEN HAAG-1 |
| station | DEN HAAG |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| informative_routes | ["1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"], "PM": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"], "flexible": []} |
| am_pm_transitions | [{"from": "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]", "minutes": 0, "to": "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"}] |
| area_sequence | ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]", "[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]"] |
| area_reentries | 1 |
| cross_region_jumps | [] |
| km | 40.0 |
| driving_minutes | 60.0 |
| service_minutes | 40 |
| waiting_minutes | 175.0 |
| loading_minutes | 15 |
| work_minutes | 290.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | False |
| exceptions | Contiguous-area sequencing has no feasible ordering; exhaustive search observed blockers: appointment/service completion |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s2t1 | ["DEN HAAG","Invented alpha","TEST-alpha",1] | AM | 33.0 | 43.0 | 200 |
| s2t2 | ["DEN HAAG","Invented beta","TEST-beta",1] | AM | 55.0 | 65.0 | 100 |
| s2t4 | ["DEN HAAG","Invented beta","TEST-beta",1] | PM | 240.0 | 250.0 | 0 |
| s2t3 | ["DEN HAAG","Invented alpha","TEST-alpha",1] | PM | 262.0 | 272.0 | 50 |

## Vehicle DEN HAAG-2

| Metric | Value |
| --- | --- |
| id | DEN HAAG-2 |
| station | DEN HAAG |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| informative_routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"] |
| area_reentries | 0 |
| cross_region_jumps | [] |
| km | 144.0 |
| driving_minutes | 216.0 |
| service_minutes | 10 |
| waiting_minutes | 117.0 |
| loading_minutes | 15 |
| work_minutes | 358.0 |
| peak_kg | 100 |
| low_utilization | False |
| more_than_two_routes | False |
| exceptions |  |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s2t5 | ["DEN HAAG","Invented gamma","TEST-gamma",1] | PM | 240.0 | 250.0 | 0 |

## Vehicle ROT-1

| Metric | Value |
| --- | --- |
| id | ROT-1 |
| station | ROT |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| informative_routes | ["1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"], "PM": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"], "flexible": []} |
| am_pm_transitions | [{"from": "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]", "minutes": 0, "to": "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"}] |
| area_sequence | ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]", "[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]"] |
| area_reentries | 1 |
| cross_region_jumps | [] |
| km | 40.0 |
| driving_minutes | 60.0 |
| service_minutes | 40 |
| waiting_minutes | 175.0 |
| loading_minutes | 15 |
| work_minutes | 290.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | False |
| exceptions | Contiguous-area sequencing has no feasible ordering; exhaustive search observed blockers: appointment/service completion |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s1t1 | ["ROT","Invented alpha","TEST-alpha",1] | AM | 33.0 | 43.0 | 200 |
| s1t2 | ["ROT","Invented beta","TEST-beta",1] | AM | 55.0 | 65.0 | 100 |
| s1t4 | ["ROT","Invented beta","TEST-beta",1] | PM | 240.0 | 250.0 | 0 |
| s1t3 | ["ROT","Invented alpha","TEST-alpha",1] | PM | 262.0 | 272.0 | 50 |

## Vehicle ROT-2

| Metric | Value |
| --- | --- |
| id | ROT-2 |
| station | ROT |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| informative_routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"] |
| area_reentries | 0 |
| cross_region_jumps | [] |
| km | 144.0 |
| driving_minutes | 216.0 |
| service_minutes | 10 |
| waiting_minutes | 117.0 |
| loading_minutes | 15 |
| work_minutes | 358.0 |
| peak_kg | 100 |
| low_utilization | False |
| more_than_two_routes | False |
| exceptions |  |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s1t5 | ["ROT","Invented gamma","TEST-gamma",1] | PM | 240.0 | 250.0 | 0 |

## Vehicle TILBURG-1

| Metric | Value |
| --- | --- |
| id | TILBURG-1 |
| station | TILBURG |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| informative_routes | ["1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"], "PM": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"], "flexible": []} |
| am_pm_transitions | [{"from": "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]", "minutes": 0, "to": "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"}] |
| area_sequence | ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]", "[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]"] |
| area_reentries | 1 |
| cross_region_jumps | [] |
| km | 40.0 |
| driving_minutes | 60.0 |
| service_minutes | 40 |
| waiting_minutes | 175.0 |
| loading_minutes | 15 |
| work_minutes | 290.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | False |
| exceptions | Contiguous-area sequencing has no feasible ordering; exhaustive search observed blockers: appointment/service completion |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s4t1 | ["TILBURG","Invented alpha","TEST-alpha",1] | AM | 33.0 | 43.0 | 200 |
| s4t2 | ["TILBURG","Invented beta","TEST-beta",1] | AM | 55.0 | 65.0 | 100 |
| s4t4 | ["TILBURG","Invented beta","TEST-beta",1] | PM | 240.0 | 250.0 | 0 |
| s4t3 | ["TILBURG","Invented alpha","TEST-alpha",1] | PM | 262.0 | 272.0 | 50 |

## Vehicle TILBURG-2

| Metric | Value |
| --- | --- |
| id | TILBURG-2 |
| station | TILBURG |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| informative_routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"] |
| area_reentries | 0 |
| cross_region_jumps | [] |
| km | 144.0 |
| driving_minutes | 216.0 |
| service_minutes | 10 |
| waiting_minutes | 117.0 |
| loading_minutes | 15 |
| work_minutes | 358.0 |
| peak_kg | 100 |
| low_utilization | False |
| more_than_two_routes | False |
| exceptions |  |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s4t5 | ["TILBURG","Invented gamma","TEST-gamma",1] | PM | 240.0 | 250.0 | 0 |

## Vehicle UTRECHT-1

| Metric | Value |
| --- | --- |
| id | UTRECHT-1 |
| station | UTRECHT |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| informative_routes | ["1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"], "PM": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"], "flexible": []} |
| am_pm_transitions | [{"from": "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]", "minutes": 0, "to": "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"}] |
| area_sequence | ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]", "[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]"] |
| area_reentries | 1 |
| cross_region_jumps | [] |
| km | 40.0 |
| driving_minutes | 60.0 |
| service_minutes | 40 |
| waiting_minutes | 175.0 |
| loading_minutes | 15 |
| work_minutes | 290.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | False |
| exceptions | Contiguous-area sequencing has no feasible ordering; exhaustive search observed blockers: appointment/service completion |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s3t1 | ["UTRECHT","Invented alpha","TEST-alpha",1] | AM | 33.0 | 43.0 | 200 |
| s3t2 | ["UTRECHT","Invented beta","TEST-beta",1] | AM | 55.0 | 65.0 | 100 |
| s3t4 | ["UTRECHT","Invented beta","TEST-beta",1] | PM | 240.0 | 250.0 | 0 |
| s3t3 | ["UTRECHT","Invented alpha","TEST-alpha",1] | PM | 262.0 | 272.0 | 50 |

## Vehicle UTRECHT-2

| Metric | Value |
| --- | --- |
| id | UTRECHT-2 |
| station | UTRECHT |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| informative_routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"] |
| area_reentries | 0 |
| cross_region_jumps | [] |
| km | 144.0 |
| driving_minutes | 216.0 |
| service_minutes | 10 |
| waiting_minutes | 117.0 |
| loading_minutes | 15 |
| work_minutes | 358.0 |
| peak_kg | 100 |
| low_utilization | False |
| more_than_two_routes | False |
| exceptions |  |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s3t5 | ["UTRECHT","Invented gamma","TEST-gamma",1] | PM | 240.0 | 250.0 | 0 |

## Assignment and feasibility evidence

| Metric | Value |
| --- | --- |
| method | city/postcode road subareas; connected bounded-diameter territories |
| settings | {"am_delivery_targets": {"stations": {"AMS": {"max": 6, "min": 5}, "BELGEM": {"max": 6, "min": 5}, "DEN HAAG": {"max": 6, "min": 5}, "ROT": {"max": 6, "min": 5}, "TILBURG": {"max": 6, "min": 5}, "UTRECHT": {"max": 6, "min": 5}}}, "balance_passes": 5, "max_extra_driving_minutes": 0, "phase_driving_slack_minutes": 3, "redistribution_node_budget": 2000, "search_node_budget": 20000, "start_minute": 0, "subarea_max_minutes": 15, "territory_max_minutes": 45} |
| area_graph_edges | [{"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"], "max_cross_base_minutes": 10}, {"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"], "max_cross_base_minutes": 10}, {"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"], "max_cross_base_minutes": 10}, {"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"], "max_cross_base_minutes": 10}, {"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"], "max_cross_base_minutes": 10}, {"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"], "max_cross_base_minutes": 10}] |
| search_nodes | 312 |
| bounded_ordering_queries | 0 |
| route_preference | advisory only; no Route labels used in grouping or tie-breaking |
| geography_time_basis | base_road_minutes |

| Derived working subarea | Locations |
| --- | --- |
| ["AMS","Invented alpha","TEST-alpha",1] | ('s0a',) |
| ["AMS","Invented beta","TEST-beta",1] | ('s0b',) |
| ["AMS","Invented gamma","TEST-gamma",1] | ('s0c',) |
| ["BELGEM","Invented alpha","TEST-alpha",1] | ('s5a',) |
| ["BELGEM","Invented beta","TEST-beta",1] | ('s5b',) |
| ["BELGEM","Invented gamma","TEST-gamma",1] | ('s5c',) |
| ["DEN HAAG","Invented alpha","TEST-alpha",1] | ('s2a',) |
| ["DEN HAAG","Invented beta","TEST-beta",1] | ('s2b',) |
| ["DEN HAAG","Invented gamma","TEST-gamma",1] | ('s2c',) |
| ["ROT","Invented alpha","TEST-alpha",1] | ('s1a',) |
| ["ROT","Invented beta","TEST-beta",1] | ('s1b',) |
| ["ROT","Invented gamma","TEST-gamma",1] | ('s1c',) |
| ["TILBURG","Invented alpha","TEST-alpha",1] | ('s4a',) |
| ["TILBURG","Invented beta","TEST-beta",1] | ('s4b',) |
| ["TILBURG","Invented gamma","TEST-gamma",1] | ('s4c',) |
| ["UTRECHT","Invented alpha","TEST-alpha",1] | ('s3a',) |
| ["UTRECHT","Invented beta","TEST-beta",1] | ('s3b',) |
| ["UTRECHT","Invented gamma","TEST-gamma",1] | ('s3c',) |

| Vehicle | Full-day continuity |
| --- | --- |
| AMS-1 | {"am_target": {"configured": true, "deviation": -3, "normal_deliveries": 2, "penalty": 3, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "max_am_pm_base_minutes": 10, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| AMS-2 | {"am_target": {"configured": true, "deviation": -5, "normal_deliveries": 0, "penalty": 5, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": true, "diameter_base_minutes": 0, "max_am_pm_base_minutes": null, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| BELGEM-1 | {"am_target": {"configured": true, "deviation": -3, "normal_deliveries": 2, "penalty": 3, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "max_am_pm_base_minutes": 10, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| BELGEM-2 | {"am_target": {"configured": true, "deviation": -5, "normal_deliveries": 0, "penalty": 5, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": true, "diameter_base_minutes": 0, "max_am_pm_base_minutes": null, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| DEN HAAG-1 | {"am_target": {"configured": true, "deviation": -3, "normal_deliveries": 2, "penalty": 3, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "max_am_pm_base_minutes": 10, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| DEN HAAG-2 | {"am_target": {"configured": true, "deviation": -5, "normal_deliveries": 0, "penalty": 5, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": true, "diameter_base_minutes": 0, "max_am_pm_base_minutes": null, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| ROT-1 | {"am_target": {"configured": true, "deviation": -3, "normal_deliveries": 2, "penalty": 3, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "max_am_pm_base_minutes": 10, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| ROT-2 | {"am_target": {"configured": true, "deviation": -5, "normal_deliveries": 0, "penalty": 5, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": true, "diameter_base_minutes": 0, "max_am_pm_base_minutes": null, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| TILBURG-1 | {"am_target": {"configured": true, "deviation": -3, "normal_deliveries": 2, "penalty": 3, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "max_am_pm_base_minutes": 10, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| TILBURG-2 | {"am_target": {"configured": true, "deviation": -5, "normal_deliveries": 0, "penalty": 5, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": true, "diameter_base_minutes": 0, "max_am_pm_base_minutes": null, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| UTRECHT-1 | {"am_target": {"configured": true, "deviation": -3, "normal_deliveries": 2, "penalty": 3, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "max_am_pm_base_minutes": 10, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |
| UTRECHT-2 | {"am_target": {"configured": true, "deviation": -5, "normal_deliveries": 0, "penalty": 5, "range": [5, 6], "reason": "Insufficient normal AM tasks in this vehicle's territory; inspect geographic/constraint merge blockers", "source": "station"}, "areas": ["[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": true, "diameter_base_minutes": 0, "max_am_pm_base_minutes": null, "ordering_search_complete": true, "phase_preference": {"handoff_base_minutes": 0, "pm_before_am_pairs": 0, "reason": "Selected among lowest-reentry feasible orders within configured driving slack; appointments are hard, phases are soft", "search_complete": true}, "time_basis": "base_road_minutes"} |

Subarea splits: {}

Unassigned tasks: []

## Merge / redistribution decisions

{"action": "adjacent_merge", "attempts": [{"geography": {"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "time_basis": "base_road_minutes"}, "reasons": [], "recipient": ["s0t2", "s0t4"]}, {"geography": {"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s0t5"]}], "recipient": ["s0t2", "s0t4"], "result": ["s0t1", "s0t2", "s0t4", "s0t3"], "source": ["s0t1", "s0t3"], "station": "AMS"}

{"action": "adjacent_merge", "attempts": [{"geography": {"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "time_basis": "base_road_minutes"}, "reasons": [], "recipient": ["s1t2", "s1t4"]}, {"geography": {"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s1t5"]}], "recipient": ["s1t2", "s1t4"], "result": ["s1t1", "s1t2", "s1t4", "s1t3"], "source": ["s1t1", "s1t3"], "station": "ROT"}

{"action": "adjacent_merge", "attempts": [{"geography": {"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "time_basis": "base_road_minutes"}, "reasons": [], "recipient": ["s2t2", "s2t4"]}, {"geography": {"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s2t5"]}], "recipient": ["s2t2", "s2t4"], "result": ["s2t1", "s2t2", "s2t4", "s2t3"], "source": ["s2t1", "s2t3"], "station": "DEN HAAG"}

{"action": "adjacent_merge", "attempts": [{"geography": {"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "time_basis": "base_road_minutes"}, "reasons": [], "recipient": ["s3t2", "s3t4"]}, {"geography": {"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s3t5"]}], "recipient": ["s3t2", "s3t4"], "result": ["s3t1", "s3t2", "s3t4", "s3t3"], "source": ["s3t1", "s3t3"], "station": "UTRECHT"}

{"action": "adjacent_merge", "attempts": [{"geography": {"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "time_basis": "base_road_minutes"}, "reasons": [], "recipient": ["s4t2", "s4t4"]}, {"geography": {"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s4t5"]}], "recipient": ["s4t2", "s4t4"], "result": ["s4t1", "s4t2", "s4t4", "s4t3"], "source": ["s4t1", "s4t3"], "station": "TILBURG"}

{"action": "adjacent_merge", "attempts": [{"geography": {"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]"], "connected": true, "diameter_base_minutes": 10, "time_basis": "base_road_minutes"}, "reasons": [], "recipient": ["s5t2", "s5t4"]}, {"geography": {"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s5t5"]}], "recipient": ["s5t2", "s5t4"], "result": ["s5t1", "s5t2", "s5t4", "s5t3"], "source": ["s5t1", "s5t3"], "station": "BELGEM"}

{"action": "low_utilization_retained", "attempts": [{"geography": {"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]", "[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s0t5"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s0t1", "s0t2", "s0t3", "s0t4"], "station": "AMS"}

{"action": "low_utilization_retained", "attempts": [{"geography": {"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]", "[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s1t5"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s1t1", "s1t2", "s1t3", "s1t4"], "station": "ROT"}

{"action": "low_utilization_retained", "attempts": [{"geography": {"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]", "[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s2t5"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s2t1", "s2t2", "s2t3", "s2t4"], "station": "DEN HAAG"}

{"action": "low_utilization_retained", "attempts": [{"geography": {"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]", "[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s3t5"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s3t1", "s3t2", "s3t3", "s3t4"], "station": "UTRECHT"}

{"action": "low_utilization_retained", "attempts": [{"geography": {"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]", "[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s4t5"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s4t1", "s4t2", "s4t3", "s4t4"], "station": "TILBURG"}

{"action": "low_utilization_retained", "attempts": [{"geography": {"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]", "[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s5t5"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s5t1", "s5t2", "s5t3", "s5t4"], "station": "BELGEM"}

{"action": "fleet_merge_retained", "attempts": [{"geography": {"areas": ["[\"AMS\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"AMS\",\"Invented beta\",\"TEST-beta\",1]", "[\"AMS\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s0t1", "s0t2", "s0t3", "s0t4"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s0t5"], "station": "AMS"}

{"action": "fleet_merge_retained", "attempts": [{"geography": {"areas": ["[\"ROT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"ROT\",\"Invented beta\",\"TEST-beta\",1]", "[\"ROT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s1t1", "s1t2", "s1t3", "s1t4"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s1t5"], "station": "ROT"}

{"action": "fleet_merge_retained", "attempts": [{"geography": {"areas": ["[\"DEN HAAG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"DEN HAAG\",\"Invented beta\",\"TEST-beta\",1]", "[\"DEN HAAG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s2t1", "s2t2", "s2t3", "s2t4"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s2t5"], "station": "DEN HAAG"}

{"action": "fleet_merge_retained", "attempts": [{"geography": {"areas": ["[\"UTRECHT\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"UTRECHT\",\"Invented beta\",\"TEST-beta\",1]", "[\"UTRECHT\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s3t1", "s3t2", "s3t3", "s3t4"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s3t5"], "station": "UTRECHT"}

{"action": "fleet_merge_retained", "attempts": [{"geography": {"areas": ["[\"TILBURG\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"TILBURG\",\"Invented beta\",\"TEST-beta\",1]", "[\"TILBURG\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s4t1", "s4t2", "s4t3", "s4t4"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s4t5"], "station": "TILBURG"}

{"action": "fleet_merge_retained", "attempts": [{"geography": {"areas": ["[\"BELGEM\",\"Invented alpha\",\"TEST-alpha\",1]", "[\"BELGEM\",\"Invented beta\",\"TEST-beta\",1]", "[\"BELGEM\",\"Invented gamma\",\"TEST-gamma\",1]"], "connected": false, "diameter_base_minutes": 80, "reason": "disconnected road subareas", "time_basis": "base_road_minutes"}, "reasons": ["disconnected road subareas"], "recipient": ["s5t1", "s5t2", "s5t3", "s5t4"]}], "conclusion": "No feasible merge/redistribution found in the stated search scope.", "redistribution": {"nodes": 1, "ordering_queries_complete": true, "reasons": ["disconnected road subareas"], "scope": "whole-location redistribution; no global infeasibility proof", "search_complete": true}, "source": ["s5t5"], "station": "BELGEM"}
