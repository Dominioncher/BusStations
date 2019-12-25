import networkx as nx
from Core.DB.MongoController import db
from Core.DataLoaders.DataLoader import get_dist


class BusGraph:

    def __init__(self):
        self.graph = nx.Graph()
        self.neighbors = list()
        self.modified_checkpoints = list()

    # Загрузка данных из базы в граф
    def load_data(self):
        query = {"routes_ids": 959}  # 30ый маршрут
        checkpoints = list(db['checkpoints'].find(query))  # все остановки по 30ому маршруту
        distanses = list(db['checkpoints_distances'].find())  # все дистанции
        query = {"name": '30'}  # 30ый маршрут
        routes = list(db['routes'].find(query))  # 30ый маршрут
        stops_1_30 = routes[0]['direct_ids']  # все остановки по 30ому маршруту в одну сторону
        stops_2_30 = routes[0]['reverse_ids']  # все остановки по 30ому маршруту в обратную сторону
        stops_all_30 = list(set(stops_1_30) | set(stops_2_30))  # все остановки по 30ому маршруту

        distances_1_30 = list()
        x = 0
        for index in stops_1_30:
            for row in distanses:
                if x != len(stops_1_30) - 1:
                    if row['checkpoint_id_1'] == stops_1_30[x] and row['checkpoint_id_2'] == stops_1_30[x + 1]:
                        distances_1_30.append(row['distance'])  # лист с растояниями между маршрутами в одну сторону
                        x = x + 1

        distances_2_30 = list()
        x = 0
        for index in stops_2_30:
            for row in distanses:
                if x != len(stops_2_30) - 1:
                    if row['checkpoint_id_1'] == stops_2_30[x] and row['checkpoint_id_2'] == stops_2_30[x + 1]:
                        distances_2_30.append(row['distance'])  # лист с растояниями между маршрутами в обратную сторону
                        x = x + 1

        graph = nx.Graph()
        for node in checkpoints:
            graph.add_node(node['id'], checkpoint=node)
        x = 0
        for dist in distances_1_30:
            graph.add_edge(stops_1_30[x], stops_1_30[x + 1], distance=dist)
            x = x + 1
        x = 0
        for dist in distances_2_30:
            graph.add_edge(stops_2_30[x], stops_2_30[x + 1], distance=dist)
            x = x + 1

        self.graph = graph

        # import matplotlib.pyplot as plt
        # nx.draw(graph)
        # plt.show() # проверял граф

        x = 1  # остановочка

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

    def get_optimised_route(self, node_a: list, node_b: list, nodes: list):
        distances = list()
        for n in nodes:
            d = dict()
            d['a_x'] = get_dist((node_a, n))
            d['x_b'] = get_dist((n, node_b))
            d['dist'] = d['a_x'] + d['x_b']
            d['x'] = n
            distances.append(d)
        best_node = min(distances, key=lambda x: x['dist'])
        bad_nodes = [i for i in nodes if not (i['id'] == best_node['x']['id'])]  # ноды которые надо удалить
        x = 0
