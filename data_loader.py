import requests


def get_routes():
    return requests.get('https://api.tgt72.ru/api/v5/route/')


def get_checkpoints():
    return requests.get('https://api.tgt72.ru/api/v5/checkpoint/')


def get_road_works():
    return requests.get('https://api.tgt72.ru/api/v5/roadworks/')


if __name__ == '__main__':
    get_road_works()
    get_checkpoints()
    get_routes()
