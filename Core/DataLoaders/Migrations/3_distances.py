from Core.DB.MongoController import db
from Core.DataLoaders.DataLoader import get_dist


def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield (a, b)
        a = b


# Добавили расстояния между остановками
checkpoints = list(db['checkpoints'].find())
routes = list(db['routes'].find())

distances = list()

for route in routes:
    direct = route['direct_ids']
    direct = [next(check for check in checkpoints if check['id'] == x) for x in direct]
    direct = [x for x in pairwise(direct)]
    reverse = route['reverse_ids']
    reverse = [next(check for check in checkpoints if check['id'] == x) for x in reverse]
    reverse = [x for x in pairwise(reverse)]
    checks = direct + reverse

    for check in checks:
        direct = next((x for x in distances
                       if (x['checkpoint_id_1'] == check[0]['id'] and x['checkpoint_id_2'] == check[1]['id'])
                       or (x['checkpoint_id_1'] == check[1]['id'] and x['checkpoint_id_2'] == check[0]['id'])), None)
        if direct:
            continue
        distances.append(get_dist(check))

db.drop_collection('checkpoints_distances')
db.create_collection('checkpoints_distances')
db['checkpoints_distances'].insert_many(distances)
