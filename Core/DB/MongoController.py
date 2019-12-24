from pymongo import MongoClient
import pandas as pd

connection = MongoClient("mongodb+srv://BusStation:BusStation@busstations-fcpis.mongodb.net/test?retryWrites=true&w=majority")
db = connection['BusStation']
db_routes = db["routes"]
db_checkpoints = db["checkpoints"]
db_checkpoints_distances = db["checkpoints_distances"]

if __name__ == '__main__':
    routes = pd.DataFrame(list(db_routes.find()))
    checkpoints = pd.DataFrame(list(db_checkpoints.find()))
    checkpoints_distances = pd.DataFrame(list(db_checkpoints_distances.find()))
    stops_1_30 = list(routes.loc[routes['name'] == '30']['direct_ids'])
    stops_1_30 = [item for sublists in stops_1_30 for item in sublists]
    stops_2_30 = list(routes.loc[routes['name'] == '30']['reverse_ids'])
    stops_2_30 = [item for sublists in stops_2_30 for item in sublists]

    # Достаем все остановки по 30ому маршруту
    query = {}
    query["routes_ids"] = 959 # id 30ого маршрута 959
    c_1_30 = list()
    cursor = db_checkpoints.find(query)
    for doc in cursor:
        c_1_30.append(doc)
    checkpoints_1_30 = pd.DataFrame(c_1_30)

    distances_1_30 = list()
    x = 0
    for index in stops_1_30:
        for y, row in checkpoints_distances.iterrows():
            if x != len(stops_1_30) - 1:
                if row.checkpoint_id_1 == stops_1_30[x] and row.checkpoint_id_2 == stops_1_30[x+1]:
                    distances_1_30.append(row.distance) # лист с растояниями между маршрутами в одну сторону
                    print(x)
                    x = x + 1

    distances_2_30 = list()
    x = 0
    for index in stops_2_30:
        for y, row in checkpoints_distances.iterrows():
            if x != len(stops_2_30) - 1:
                if row.checkpoint_id_1 == stops_2_30[x] and row.checkpoint_id_2 == stops_2_30[x+1]:
                    distances_2_30.append(row.distance) # лист с растояниями между маршрутами в обратную сторону
                    print(x)
                    x = x + 1
