import networkx as nx
from Core.DB.MongoController import db
from Core.DataLoaders.DataLoader import get_dist
import pandas as pd

class BusGraph:

    def __init__(self):
        self.graph = nx.Graph()
        self.neighbors = list()
        self.modified_checkpoints = list()

    # Загрузка данных из базы в граф
    def load_data(self):
        query = {}
        query["routes_ids"] = 959  # 30ый маршрут
        checkpoints = list(db['checkpoints'].find(query))
        distanses = list(db['checkpoints_distances'].find())

        db_routes = db["routes"]
        db_checkpoints = db["checkpoints"]
        db_checkpoints_distances = db["checkpoints_distances"]
        routes = pd.DataFrame(list(db_routes.find()))
        # checkpoints = pd.DataFrame(list(db_checkpoints.find()))
        checkpoints_distances = pd.DataFrame(list(db_checkpoints_distances.find()))
        stops_1_30 = list(routes.loc[routes['name'] == '30']['direct_ids'])
        stops_1_30 = [item for sublists in stops_1_30 for item in sublists]
        stops_2_30 = list(routes.loc[routes['name'] == '30']['reverse_ids'])
        stops_2_30 = [item for sublists in stops_2_30 for item in sublists]

        # Достаем все остановки по 30ому маршруту
        query = {}
        query["routes_ids"] = 959  # id 30ого маршрута 959
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
                    if row.checkpoint_id_1 == stops_1_30[x] and row.checkpoint_id_2 == stops_1_30[x + 1]:
                        distances_1_30.append(row.distance)  # лист с растояниями между маршрутами в одну сторону
                        x = x + 1

        distances_2_30 = list()
        x = 0
        for index in stops_2_30:
            for y, row in checkpoints_distances.iterrows():
                if x != len(stops_2_30) - 1:
                    if row.checkpoint_id_1 == stops_2_30[x] and row.checkpoint_id_2 == stops_2_30[x + 1]:
                        distances_2_30.append(row.distance)  # лист с растояниями между маршрутами в обратную сторону
                        x = x + 1

        graph = nx.Graph()

        for node in checkpoints:
            graph.add_node(node['id'], checkpoint=node)
        # for edge in distanses:
        #     graph.add_edge(edge['checkpoint_id_1'], edge['checkpoint_id_2'], distance=edge)
        x = 0
        for dist in distances_1_30:
            graph.add_edge(stops_1_30[x], stops_1_30[x+1], distance=dist)
            x = x + 1
        x = 0
        for dist in distances_2_30:
            graph.add_edge(stops_2_30[x], stops_2_30[x+1], distance=dist)
            x = x + 1
        self.graph = graph

    # TODO Пересчет оптимального маршрута но основе остановок которые надо оптимизировать
    def optimize(self):
        gg = self.neighbors

    # Модификация остановок
    def modify_checkpoints(self, nodes: list):
        self.modified_checkpoints = nodes
        neighbors = list()
        for node in nodes:
            neighbors += list(self.graph.neighbors(node))
        self.neighbors = list(set(neighbors))

    # Удалить остановку
    def remove_checkpoint(self, node: int):
        if node not in self.modified_checkpoints:
            return False
        self.graph.remove_node(node)
        return True

    # Добавить остановку
    def add_checkpoint(self, name, lat, lng):
        checkpoint = dict()
        id = max(self.graph.nodes.keys()) + 1
        checkpoint['id'] = id
        checkpoint['name'] = name
        checkpoint['lat'] = lat
        checkpoint['lon'] = lng
        self.graph.add_node(id, checkpoint=checkpoint)

        for node in self.modified_checkpoints + self.neighbors:
            distance = get_dist((checkpoint, self.graph.nodes[node]['checkpoint']))
            self.graph.add_edge(id, node, distance=distance)
        self.modified_checkpoints.append(id)
        return id
