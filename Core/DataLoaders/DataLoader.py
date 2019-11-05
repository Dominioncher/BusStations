import json

import requests


def get_routes():
    routes = requests.get('https://api.tgt72.ru/api/v5/route/').json()
    routes = routes['objects']
    for route in routes:
        checkpoints = get_route_checkpoints(route['id'])
        del route['checkpoints_ids']
        route['direct_ids'] = checkpoints[0]
        route['reverse_ids'] = checkpoints[1]
    return routes


def get_checkpoints():
    return requests.get('https://api.tgt72.ru/api/v5/checkpoint/').json()['objects']


def get_road_works():
    return requests.get('https://api.tgt72.ru/api/v5/roadworks/').json()['objects']


def get_route_checkpoints(route_id):
    checkpoints = requests.get(f'https://api.tgt72.ru/api/v5/routecheckpoint/?route_id={route_id}').json()['objects']
    direct_ids = [x['checkpoint_id'] for x in checkpoints if x['forward']]
    reverse_ids = [x['checkpoint_id'] for x in checkpoints if not x['forward']]
    return direct_ids, reverse_ids

