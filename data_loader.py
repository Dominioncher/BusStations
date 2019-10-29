import json

import requests


def get_routes():
    return requests.get('https://api.tgt72.ru/api/v5/route/').json()


def get_checkpoints():
    return requests.get('https://api.tgt72.ru/api/v5/checkpoint/').json()


def get_road_works():
    return requests.get('https://api.tgt72.ru/api/v5/roadworks/').json()


# Если запустить в консоли питона, можно поглядеть на данные
if __name__ == '__main__':
    works = get_road_works()
    checkpoints = get_checkpoints()
    routes = get_routes()
