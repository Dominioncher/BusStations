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

        self.graph = graph

    # Пересчет оптимального маршрута но основе остановок которые надо оптимизировать
    def optimize(self):
        for index, a in enumerate(self.modified_checkpoints):
            if self.graph.has_edge(a, self.neighbors[0]):
                self.graph.remove_edge(a, self.neighbors[0])
            if self.graph.has_edge(a, self.neighbors[1]):
                self.graph.remove_edge(a, self.neighbors[1])

        e = list()
        for index1, a in enumerate(self.modified_checkpoints):
            for index2, b in enumerate(self.modified_checkpoints):
                if index2 <= index1:
                    continue
                dist1 = get_dist((self.graph.nodes[a]['checkpoint'], self.graph.nodes[b]['checkpoint']))
                dist2 = get_dist((self.graph.nodes[b]['checkpoint'], self.graph.nodes[a]['checkpoint']))
                e.append((a, b, min(dist1, dist2)))

        for index, a in enumerate(self.modified_checkpoints):
            dist1 = get_dist((self.graph.nodes[a]['checkpoint'], self.graph.nodes[self.neighbors[0]]['checkpoint']))
            dist2 = get_dist((self.graph.nodes[self.neighbors[0]]['checkpoint'], self.graph.nodes[a]['checkpoint']))
            e.append((a, self.neighbors[0],
                      min(dist1, dist2)))
            dist1 = get_dist((self.graph.nodes[a]['checkpoint'], self.graph.nodes[self.neighbors[1]]['checkpoint']))
            dist2 = get_dist((self.graph.nodes[self.neighbors[1]]['checkpoint'], self.graph.nodes[a]['checkpoint']))
            e.append((a, self.neighbors[1],
                      min(dist1, dist2)))
        G = nx.Graph()
        G.add_weighted_edges_from(e)
        short = nx.dijkstra_path(G, self.neighbors[0], self.neighbors[1])
        length = len(short)
        for index1, edge in enumerate(short):
            for index2 in e:
                if index1 == length - 1:
                    break
                if index2[0] == short[index1] and index2[1] == short[index1 + 1] or index2[1] == short[index1] and \
                        index2[0] == short[index1 + 1]:
                    self.graph.add_edge(index2[0], index2[1], distance=index2[2])

        for node, edge in enumerate(short):
            if short[node] in self.modified_checkpoints: self.modified_checkpoints.remove(short[node])
        for x in self.modified_checkpoints:
            self.graph.remove_node(x)
        self.modified_checkpoints.clear()

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

        # for node in self.modified_checkpoints + self.neighbors:  # зачем просчитывать расстояния тут?
        #     distance = get_dist((checkpoint, self.graph.nodes[node]['checkpoint']))
        #     self.graph.add_edge(id, node, distance=distance)
        self.modified_checkpoints.append(id)
        return checkpoint

    def get_ordered_checkpoints(self):
        nodes = list(nx.dfs_preorder_nodes(self.graph, self.direct))
        checkpoints = []
        for node in nodes:
            checkpoints.append(self.graph.nodes[node]['checkpoint'])
        return checkpoints
