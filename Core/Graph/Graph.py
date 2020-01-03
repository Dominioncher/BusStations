import networkx as nx
from Core.DB.MongoController import db
from Core.DataLoaders.DataLoader import get_dist


class BusGraph:

    def __init__(self):
        self.graph = nx.Graph()
        self.neighbors = list()
        self.modified_checkpoints = list()
        self.direct = None

    # Загрузка данных из базы в граф
    def load_data(self):
        query = {"name": '14'}  # 30ый маршрут
        routes = list(db['routes'].find(query))  # 30ый маршрут
        stops_1_30 = routes[0]['direct_ids']  # все остановки по 30ому маршруту в одну сторону
        stops_2_30 = routes[0]['reverse_ids']  # все остановки по 30ому маршруту в обратную сторону
        query = {"routes_ids": routes[0]['id']}
        checkpoints = list(db['checkpoints'].find(query))  # все остановки по 30ому маршруту
        distanses = list(db['checkpoints_distances'].find())  # все дистанции
        self.direct = stops_1_30[0]
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
        # for dist in distances_2_30:
        #     graph.add_edge(stops_2_30[x], stops_2_30[x + 1], distance=dist)
        #     x = x + 1

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
        self.modified_checkpoints += nodes
        self.modified_checkpoints = list(set(self.modified_checkpoints))
        neighbors = list()
        for node in self.modified_checkpoints:
            neighbors += list(self.graph.neighbors(node))
        self.neighbors = list(set(neighbors))
        self.neighbors = list([x for x in self.neighbors if x not in self.modified_checkpoints])

    # Удалить остановку по id
    def remove_checkpoint(self, node: int):
        if node not in self.modified_checkpoints:
            return False
        self.graph.remove_node(node)
        self.modified_checkpoints.remove(node)
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
        return checkpoint

    def get_optimised_route(self, node_a: list, node_b: list, nodes: list):
        all_nodes = list()
        all_nodes.append(node_a)
        all_nodes = all_nodes + nodes
        all_nodes.append(node_b)
        e = list()
        for id1, a in enumerate(all_nodes):
            for id2, b in enumerate(all_nodes):
                if id2 <= id1:
                    continue
                e.append((a['id'], b['id'], get_dist((a, b))))
        G = nx.Graph()
        G.add_weighted_edges_from(e)
        short = nx.dijkstra_path(G, node_a['id'], node_b['id'])
        bad_nodes = list()
        for x in all_nodes:
            b = False
            for y in short:
                if x['id'] == y:
                    b = True
                    continue
            if not b:
                bad_nodes.append(x)
        return bad_nodes

    def get_ordered_checkpoints(self):
        nodes = list(nx.dfs_preorder_nodes(self.graph, self.direct))
        checkpoints = []
        for node in nodes:
            checkpoints.append(self.graph.nodes[node]['checkpoint'])
        return checkpoints
