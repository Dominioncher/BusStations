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
        query = {}
        query["routes_ids"] = 959
        checkpoints = list(db['checkpoints'].find(query))
        distanses = list(db['checkpoints_distances'].find())

        graph = nx.Graph()

        for node in checkpoints:
            graph.add_node(node['id'], checkpoint=node)
        for edge in distanses:
            graph.add_edge(edge['checkpoint_id_1'], edge['checkpoint_id_2'], distance=edge)
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
