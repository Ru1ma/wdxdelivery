# Dispatch baseline diagnostic

Evidence basis: synthetic; Invented symmetric travel table, not real road travel..
Operational geography review: pending. No optimization/production acceptance claim.
Merge/redistribution search: not implemented in this baseline stage.

Integrity: {"cross_station": 0, "duplicates": {}, "missing": [], "unknown": []}
Hard constraints pass: True

All times below are minutes; driving applies the explicit traffic multiplier.
Time windows require completion of service by the end. Depot return is included.

Global: {"Delivery": 18, "Pickup": 6, "Redeliver": 6, "driving_minutes": 1764.0, "km": 1176.0, "longest_minutes": 358.0, "metrics_available": true, "service_minutes": 300, "shortest_minutes": 296.0, "spread_minutes": 62.0, "total_tasks": 30, "vehicles": 12, "waiting_minutes": 1680.0, "work_minutes": 3924.0}

| Station | Tasks / Delivery / Pickup / Redeliver | Vehicles | km | Driving | Waiting | Work | Longest / shortest / spread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AMS | [5, 3, 1, 1] | 2 | 196.0 | 294.0 | 280.0 | 654.0 | [358.0, 296.0, 62.0] |
| ROT | [5, 3, 1, 1] | 2 | 196.0 | 294.0 | 280.0 | 654.0 | [358.0, 296.0, 62.0] |
| DEN HAAG | [5, 3, 1, 1] | 2 | 196.0 | 294.0 | 280.0 | 654.0 | [358.0, 296.0, 62.0] |
| UTRECHT | [5, 3, 1, 1] | 2 | 196.0 | 294.0 | 280.0 | 654.0 | [358.0, 296.0, 62.0] |
| TILBURG | [5, 3, 1, 1] | 2 | 196.0 | 294.0 | 280.0 | 654.0 | [358.0, 296.0, 62.0] |
| BELGEM | [5, 3, 1, 1] | 2 | 196.0 | 294.0 | 280.0 | 654.0 | [358.0, 296.0, 62.0] |

## AMS

Task data available: True

| Original Route label | City | Postcode areas |
| --- | --- | --- |
| (missing) | Invented alpha | ["TEST-alpha"] |
| 0 | Invented beta | ["TEST-beta"] |
| 1 | Invented alpha | ["TEST-alpha"] |
| 2 | Invented gamma | ["TEST-gamma"] |
| 5 | Invented beta | ["TEST-beta"] |

neighbors: [{"areas": ["alpha", "beta"], "minutes": 10}]

separate_areas: [{"areas": ["alpha", "gamma"], "minutes": 80}, {"areas": ["beta", "gamma"], "minutes": 70}]

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

neighbors: [{"areas": ["alpha", "beta"], "minutes": 10}]

separate_areas: [{"areas": ["alpha", "gamma"], "minutes": 80}, {"areas": ["beta", "gamma"], "minutes": 70}]

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

neighbors: [{"areas": ["alpha", "beta"], "minutes": 10}]

separate_areas: [{"areas": ["alpha", "gamma"], "minutes": 80}, {"areas": ["beta", "gamma"], "minutes": 70}]

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

neighbors: [{"areas": ["alpha", "beta"], "minutes": 10}]

separate_areas: [{"areas": ["alpha", "gamma"], "minutes": 80}, {"areas": ["beta", "gamma"], "minutes": 70}]

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

neighbors: [{"areas": ["alpha", "beta"], "minutes": 10}]

separate_areas: [{"areas": ["alpha", "gamma"], "minutes": 80}, {"areas": ["beta", "gamma"], "minutes": 70}]

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

neighbors: [{"areas": ["alpha", "beta"], "minutes": 10}]

separate_areas: [{"areas": ["alpha", "gamma"], "minutes": 80}, {"areas": ["beta", "gamma"], "minutes": 70}]

distant_routes: []

dispersed_subareas: []

overlapping_areas: {}

## Vehicle AMS-far

| Metric | Value |
| --- | --- |
| id | AMS-far |
| station | AMS |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["gamma"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["gamma"] |
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
| exceptions | Synthetic remote territory; merge not tested. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s0t5 | gamma | PM | 240.0 | 250.0 | 0 |

## Vehicle AMS-near

| Metric | Value |
| --- | --- |
| id | AMS-near |
| station | AMS |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["alpha", "beta"], "PM": ["alpha", "beta"], "flexible": []} |
| am_pm_transitions | [{"from": "beta", "minutes": 10, "to": "alpha"}] |
| area_sequence | ["alpha", "beta", "alpha", "beta"] |
| area_reentries | 2 |
| cross_region_jumps | [] |
| km | 52.0 |
| driving_minutes | 78.0 |
| service_minutes | 40 |
| waiting_minutes | 163.0 |
| loading_minutes | 15 |
| work_minutes | 296.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | True |
| exceptions | Synthetic supplied baseline; alpha/beta reentry deliberately retained. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s0t1 | alpha | AM | 33.0 | 43.0 | 200 |
| s0t2 | beta | AM | 55.0 | 65.0 | 100 |
| s0t3 | alpha | PM | 240.0 | 250.0 | 150 |
| s0t4 | beta | PM | 262.0 | 272.0 | 50 |

## Vehicle BELGEM-far

| Metric | Value |
| --- | --- |
| id | BELGEM-far |
| station | BELGEM |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["gamma"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["gamma"] |
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
| exceptions | Synthetic remote territory; merge not tested. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s5t5 | gamma | PM | 240.0 | 250.0 | 0 |

## Vehicle BELGEM-near

| Metric | Value |
| --- | --- |
| id | BELGEM-near |
| station | BELGEM |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["alpha", "beta"], "PM": ["alpha", "beta"], "flexible": []} |
| am_pm_transitions | [{"from": "beta", "minutes": 10, "to": "alpha"}] |
| area_sequence | ["alpha", "beta", "alpha", "beta"] |
| area_reentries | 2 |
| cross_region_jumps | [] |
| km | 52.0 |
| driving_minutes | 78.0 |
| service_minutes | 40 |
| waiting_minutes | 163.0 |
| loading_minutes | 15 |
| work_minutes | 296.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | True |
| exceptions | Synthetic supplied baseline; alpha/beta reentry deliberately retained. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s5t1 | alpha | AM | 33.0 | 43.0 | 200 |
| s5t2 | beta | AM | 55.0 | 65.0 | 100 |
| s5t3 | alpha | PM | 240.0 | 250.0 | 150 |
| s5t4 | beta | PM | 262.0 | 272.0 | 50 |

## Vehicle DEN HAAG-far

| Metric | Value |
| --- | --- |
| id | DEN HAAG-far |
| station | DEN HAAG |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["gamma"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["gamma"] |
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
| exceptions | Synthetic remote territory; merge not tested. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s2t5 | gamma | PM | 240.0 | 250.0 | 0 |

## Vehicle DEN HAAG-near

| Metric | Value |
| --- | --- |
| id | DEN HAAG-near |
| station | DEN HAAG |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["alpha", "beta"], "PM": ["alpha", "beta"], "flexible": []} |
| am_pm_transitions | [{"from": "beta", "minutes": 10, "to": "alpha"}] |
| area_sequence | ["alpha", "beta", "alpha", "beta"] |
| area_reentries | 2 |
| cross_region_jumps | [] |
| km | 52.0 |
| driving_minutes | 78.0 |
| service_minutes | 40 |
| waiting_minutes | 163.0 |
| loading_minutes | 15 |
| work_minutes | 296.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | True |
| exceptions | Synthetic supplied baseline; alpha/beta reentry deliberately retained. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s2t1 | alpha | AM | 33.0 | 43.0 | 200 |
| s2t2 | beta | AM | 55.0 | 65.0 | 100 |
| s2t3 | alpha | PM | 240.0 | 250.0 | 150 |
| s2t4 | beta | PM | 262.0 | 272.0 | 50 |

## Vehicle ROT-far

| Metric | Value |
| --- | --- |
| id | ROT-far |
| station | ROT |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["gamma"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["gamma"] |
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
| exceptions | Synthetic remote territory; merge not tested. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s1t5 | gamma | PM | 240.0 | 250.0 | 0 |

## Vehicle ROT-near

| Metric | Value |
| --- | --- |
| id | ROT-near |
| station | ROT |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["alpha", "beta"], "PM": ["alpha", "beta"], "flexible": []} |
| am_pm_transitions | [{"from": "beta", "minutes": 10, "to": "alpha"}] |
| area_sequence | ["alpha", "beta", "alpha", "beta"] |
| area_reentries | 2 |
| cross_region_jumps | [] |
| km | 52.0 |
| driving_minutes | 78.0 |
| service_minutes | 40 |
| waiting_minutes | 163.0 |
| loading_minutes | 15 |
| work_minutes | 296.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | True |
| exceptions | Synthetic supplied baseline; alpha/beta reentry deliberately retained. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s1t1 | alpha | AM | 33.0 | 43.0 | 200 |
| s1t2 | beta | AM | 55.0 | 65.0 | 100 |
| s1t3 | alpha | PM | 240.0 | 250.0 | 150 |
| s1t4 | beta | PM | 262.0 | 272.0 | 50 |

## Vehicle TILBURG-far

| Metric | Value |
| --- | --- |
| id | TILBURG-far |
| station | TILBURG |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["gamma"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["gamma"] |
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
| exceptions | Synthetic remote territory; merge not tested. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s4t5 | gamma | PM | 240.0 | 250.0 | 0 |

## Vehicle TILBURG-near

| Metric | Value |
| --- | --- |
| id | TILBURG-near |
| station | TILBURG |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["alpha", "beta"], "PM": ["alpha", "beta"], "flexible": []} |
| am_pm_transitions | [{"from": "beta", "minutes": 10, "to": "alpha"}] |
| area_sequence | ["alpha", "beta", "alpha", "beta"] |
| area_reentries | 2 |
| cross_region_jumps | [] |
| km | 52.0 |
| driving_minutes | 78.0 |
| service_minutes | 40 |
| waiting_minutes | 163.0 |
| loading_minutes | 15 |
| work_minutes | 296.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | True |
| exceptions | Synthetic supplied baseline; alpha/beta reentry deliberately retained. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s4t1 | alpha | AM | 33.0 | 43.0 | 200 |
| s4t2 | beta | AM | 55.0 | 65.0 | 100 |
| s4t3 | alpha | PM | 240.0 | 250.0 | 150 |
| s4t4 | beta | PM | 262.0 | 272.0 | 50 |

## Vehicle UTRECHT-far

| Metric | Value |
| --- | --- |
| id | UTRECHT-far |
| station | UTRECHT |
| metrics_available | True |
| total_tasks | 1 |
| Delivery | 1 |
| Pickup | 0 |
| Redeliver | 0 |
| normal_deliveries_by_phase | {"AM": 0, "PM": 1, "flexible": 0} |
| routes | ["2"] |
| cities | ["Invented gamma"] |
| postcode_areas | ["TEST-gamma"] |
| phase_areas | {"AM": [], "PM": ["gamma"], "flexible": []} |
| am_pm_transitions | [] |
| area_sequence | ["gamma"] |
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
| exceptions | Synthetic remote territory; merge not tested. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s3t5 | gamma | PM | 240.0 | 250.0 | 0 |

## Vehicle UTRECHT-near

| Metric | Value |
| --- | --- |
| id | UTRECHT-near |
| station | UTRECHT |
| metrics_available | True |
| total_tasks | 4 |
| Delivery | 2 |
| Pickup | 1 |
| Redeliver | 1 |
| normal_deliveries_by_phase | {"AM": 2, "PM": 0, "flexible": 0} |
| routes | ["0", "1", "5"] |
| cities | ["Invented alpha", "Invented beta"] |
| postcode_areas | ["TEST-alpha", "TEST-beta"] |
| phase_areas | {"AM": ["alpha", "beta"], "PM": ["alpha", "beta"], "flexible": []} |
| am_pm_transitions | [{"from": "beta", "minutes": 10, "to": "alpha"}] |
| area_sequence | ["alpha", "beta", "alpha", "beta"] |
| area_reentries | 2 |
| cross_region_jumps | [] |
| km | 52.0 |
| driving_minutes | 78.0 |
| service_minutes | 40 |
| waiting_minutes | 163.0 |
| loading_minutes | 15 |
| work_minutes | 296.0 |
| peak_kg | 300 |
| low_utilization | True |
| more_than_two_routes | True |
| exceptions | Synthetic supplied baseline; alpha/beta reentry deliberately retained. |
| failures | [] |

| Task | Subarea | Phase | Service start | Service end | Load kg |
| --- | --- | --- | --- | --- | --- |
| s3t1 | alpha | AM | 33.0 | 43.0 | 200 |
| s3t2 | beta | AM | 55.0 | 65.0 | 100 |
| s3t3 | alpha | PM | 240.0 | 250.0 | 150 |
| s3t4 | beta | PM | 262.0 | 272.0 | 50 |
