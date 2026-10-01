"""Uneven, wholly invented six-station road/appointment workloads."""
from examples.make_assignment import automatic_fixture


def stress_fixture(scale=1):
    data = automatic_fixture()
    data['tasks'], data['locations'], data['road']['arcs'] = [], [], []
    data['depots'] = {}
    data['config'].update(capacity_kg=100, traffic_multiplier=1.2,
                          loading_minutes=5, max_work_minutes=600,
                          low_utilization_minutes=180, adjacency_minutes=18)
    data['planning'].update(subarea_max_minutes=12, territory_max_minutes=32,
                            search_node_budget=300, redistribution_node_budget=150,
                            max_extra_driving_minutes=10, balance_passes=2,
                            am_delivery_targets={'stations': {'AMS': {'min': 3, 'max': 5}}},
                            phase_driving_slack_minutes=3)
    stations = ['AMS', 'ROT', 'DEN HAAG', 'UTRECHT', 'TILBURG', 'BELGEM']
    for s, count in enumerate([28, 23, 19, 15, 11, 8]):
        station = stations[s]
        depot = f's{s}-depot'
        data['depots'][station] = depot
        positions = {depot: (0, 0)}
        for j in range(8):
            positions[f's{s}-site{j}'] = (8 + (j // 4) * 55 + (j % 4) * 6, (j % 3) * 2)
        for lid, position in positions.items():
            j = list(positions).index(lid) - 1
            data['locations'].append({'id': lid, 'station': station,
                'city': f'Invented city {s}-{max(j, 0) // 4}',
                'postcode_area': f'TEST-{s}-{max(j, 0) // 2}'})
            for other, dest in positions.items():
                if lid != other:
                    distance = abs(position[0] - dest[0]) + abs(position[1] - dest[1])
                    data['road']['arcs'].append({'from': lid, 'to': other,
                                                 'minutes': distance, 'km': distance / 2})
        for i in range(count * scale):
            j = (i * 3 + i // 8 + s) % 8
            kind = ['Delivery', 'Delivery', 'Pickup', 'Delivery', 'Redeliver'][i % 5]
            phase = ['AM', 'flexible', 'PM', 'AM', 'PM'][i % 5]
            window = [0, 600]
            if phase == 'AM':
                window = [0, 150 + (i % 3) * 20]
            elif phase == 'PM':
                window = [220 + (i % 3) * 30, 380 + (i % 4) * 20]
            task = {'id': f's{s}-task{i:03d}', 'station': station,
                'location': f's{s}-site{j}', 'kind': kind, 'phase': phase,
                'weight_kg': 8 + (i * 7 + s) % 24,
                'service_minutes': 3 + (i * 5 + s) % 13, 'window': window,
                'route': None if i % 11 == 0 else (0 if i % 7 == 0 else 'large-route')}
            if kind == 'Pickup':
                task['pickup_location'] = task['location']
            data['tasks'].append(task)
    return data
