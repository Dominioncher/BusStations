import requests
from Core.DataLoaders.Maps import distance_finder


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


def get_dist(pair):
    dist = dict()
    first = pair[0]
    second = pair[1]
    dist['checkpoint_id_1'] = first['id']
    dist['checkpoint_id_2'] = second['id']
    distance = distance_finder(first['lat'], first['lon'], second['lat'], second['lon'])
    dist['distance'] = distance['dist']
    dist['time'] = distance['time']
    return distance['dist']
